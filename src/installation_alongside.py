#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  installation_alongside.py
#  
#  Copyright 2013 Cinnarch
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  Cinnarch Team:
#   Alex Filgueira (faidoc) <alexfilgueira.cinnarch.com>
#   Raúl Granados (pollitux) <raulgranados.cinnarch.com>
#   Gustau Castells (karasu) <karasu.cinnarch.com>
#   Kirill Omelchenko (omelcheck) <omelchek.cinnarch.com>
#   Marc Miralles (arcnexus) <arcnexus.cinnarch.com>
#   Alex Skinner (skinner) <skinner.cinnarch.com>

import xml.etree.ElementTree as etree

from gi.repository import Gtk, Gdk

import sys
import os
import misc
import parted
import log
import show_message as show
import bootinfo
import subprocess

# Insert the src/parted directory at the front of the path.
base_dir = os.path.dirname(__file__) or '.'
parted_dir = os.path.join(base_dir, 'parted')
sys.path.insert(0, parted_dir)

import partition_module as pm
import fs_module as fs

import installation_thread

_next_page = "timezone"
_prev_page = "installation_ask"

# leave at least 3GB for Antergos when shrinking
_minimum_space_for_antergos = 3000

class InstallationAlongside(Gtk.Box):

    def __init__(self, params):
        self.title = params['title']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        self.callback_queue = params['callback_queue']
        self.settings = params['settings']

        super().__init__()
        self.ui = Gtk.Builder()
        self.ui.add_from_file(os.path.join(self.ui_dir, "installation_alongside.ui"))

        self.ui.connect_signals(self)
        
        self.label = self.ui.get_object('label_info')
        
        self.treeview = self.ui.get_object("treeview1")
        self.treeview_store = None
        self.prepare_treeview()
        self.populate_treeview()
        
        # Init dialog slider
        self.init_slider()

        super().add(self.ui.get_object("installation_alongside"))

    def init_slider(self):
        dialog = self.ui.get_object("shrink-dialog")
        slider = self.ui.get_object("scale")
        
        slider.set_name("myslider")
        path = os.path.join(self.settings.get("DATA_DIR"), "css", "scale.css")
        
        self.available_slider_range = [0, 0]
        
        if os.path.exists(path):
            with open(path, "rb") as css:
                css_data = css.read()
            
            provider = Gtk.CssProvider()
            
            provider.load_from_data(css_data)

            Gtk.StyleContext.add_provider_for_screen(
                Gdk.Screen.get_default(), provider,     
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
        

        #slider.add_events(Gdk.EventMask.SCROLL_MASK)

        slider.connect("change-value", self.slider_change_value)
        '''
        slider.connect("value_changed",
                self.main.on_volume_changed)
        slider.connect("button_press_event",
                self.on_scale_button_press_event)
        slider.connect("button_release_event",
                self.on_scale_button_release_event)
        slider.connect("scroll_event",
                self.on_scale_scroll_event)
        '''
    
    def slider_change_value(self, slider, scroll, value):
        if value <= self.available_slider_range[0] or \
           value >= self.available_slider_range[1]:
            return True
        else:
            slider.set_fill_level(value)
            self.update_ask_shrink_size_labels(value)
            return False
    
    def translate_ui(self):
        txt = _("Choose next to which OS you want to install Cinnarch")
        txt = '<span size="large">%s</span>' % txt
        self.label.set_markup(txt)

        txt = _("Cinnarch alongside another OS")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.title.set_markup(txt)

        txt = _("Install now!")
        self.forward_button.set_label(txt)

    def prepare(self, direction):
        self.translate_ui()
        self.show_all()
        self.forward_button.set_sensitive(False)

    def store_values(self):
        self.start_installation()
        return True

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page
        
    def prepare_treeview(self):
        ## Create columns for our treeview
        render_text = Gtk.CellRendererText()
                
        col = Gtk.TreeViewColumn(_("Device"), render_text, text=0)
        self.treeview.append_column(col)
        
        col = Gtk.TreeViewColumn(_("Detected OS"), render_text, text=1)
        self.treeview.append_column(col)

        col = Gtk.TreeViewColumn(_("Filesystem"), render_text, text=2)
        self.treeview.append_column(col)
    
    @misc.raise_privileges
    def populate_treeview(self):
        if self.treeview_store != None:
            self.treeview_store.clear()

        self.treeview_store = Gtk.TreeStore(str, str, str)

        oses = {}
        oses = bootinfo.get_os_dict()
        
        self.partitions = {}

        device_list = parted.getAllDevices()
        
        for dev in device_list:
            ## avoid cdrom and any raid, lvm volumes or encryptfs
            if not dev.path.startswith("/dev/sr") and \
               not dev.path.startswith("/dev/mapper"):
                try:           
                    disk = parted.Disk(dev)
                    # create list of partitions for this device (p.e. /dev/sda)
                    partition_list = disk.partitions
                    
                    for p in partition_list:
                        if p.type != pm.PARTITION_EXTENDED:
                            ## Get file system
                            fs_type = ""
                            if p.fileSystem and p.fileSystem.type:
                                fs_type = p.fileSystem.type
                            if "swap" not in fs_type:
                                if p.path in oses:
                                    row = [ p.path, oses[p.path], fs_type ]
                                else:
                                    row = [ p.path, _("unknown"), fs_type ]
                                self.treeview_store.append(None, row)
                        self.partitions[p.path] = p
                except Exception as e:
                    log.debug(_("In alongside install, can't create list of partitions"))

        # assign our new model to our treeview
        self.treeview.set_model(self.treeview_store)
        self.treeview.expand_all()

    def on_treeview_cursor_changed(self, widget):
        selection = self.treeview.get_selection()
        
        if not selection:
            return
            
        model, tree_iter = selection.get_selected()

        if tree_iter == None:
            return
        
        self.row = model[tree_iter]
        
        partition_path = self.row[0]
        other_os_name = self.row[1]
        
        self.min_size = 0
        self.max_size = 0
        self.new_size = 0

        try:
            x = subprocess.check_output(['df', partition_path]).decode()
            x = x.split('\n')
            x = x[1].split()
            self.max_size = int(x[1]) / 1000
            self.min_size = int(x[2]) / 1000
        except subprocess.CalledProcessError as e:
            print("CalledProcessError.output = %s" % e.output)

        if self.min_size + _minimum_space_for_antergos < self.max_size:
            self.new_size = self.ask_shrink_size(other_os_name)
        else:
            # Can't shrink the partition (maybe it's nearly full)
            # TODO: Show error message but let the user choose
            # another install method
            pass

        if self.new_size > 0:
            self.forward_button.set_sensitive(True)
        else:
            self.forward_button.set_sensitive(False)
        
        return False

    def update_ask_shrink_size_labels(self, new_value):
        label_other_os_size = self.ui.get_object("label_other_os_size")
        label_other_os_size.set_markup(str(int(new_value)) + " MB")

        label_antergos_size = self.ui.get_object("label_antergos_size")
        label_antergos_size.set_markup(str(int(self.max_size - new_value)) + " MB")
        
    def ask_shrink_size(self, other_os_name):
        dialog = self.ui.get_object("shrink-dialog")
                
        slider = self.ui.get_object("scale")

        # leave space for Antergos
        self.available_slider_range = [ self.min_size, self.max_size - _minimum_space_for_antergos ]

        slider.set_fill_level(self.min_size)
        slider.set_show_fill_level(True)
        slider.set_restrict_to_fill_level(False)
        slider.set_range(0, self.max_size)
        slider.set_value(self.min_size)
        slider.set_draw_value(False)
        
        label_other_os = self.ui.get_object("label_other_os")
        txt = "<span weight='bold' size='large'>%s</span>" % other_os_name
        label_other_os.set_markup(txt)

        label_antergos = self.ui.get_object("label_antergos")
        txt = "<span weight='bold' size='large'>Antergos</span>"
        label_antergos.set_markup(txt)
        
        self.update_ask_shrink_size_labels(self.min_size)
       
        response = dialog.run()

        value = 0
        
        if response == Gtk.ResponseType.OK:
            value = int(slider.get_value()) + 1
        
        dialog.hide()

        return value
        

    def start_installation(self):
        # Alongside method shrinks selected partition
        # and creates root and swap partition in the available space
        
        partition_path = self.row[0]
        otherOS = self.row[1]
        fs_type = self.row[2]

        # what if path is sda10 (two digits) ? this is wrong
        device_path = self.row[0][:-1]

        new_size = self.new_size
        
        print("partition_path: ", partition_path)
        print("device_path: ", device_path)
        print("new_size: ", new_size)
        
        # Find out how many primary partitions device has, and also
        # if there's already an extended partition

        extended_path = ""
        primary_partitions = []
        
        for path in self.partitions:
            if device_path in path:
                p = self.partitions[path]
                if p.type == pm.PARTITION_EXTENDED:
                    extended_path = path
                elif p.type == pm.PARTITION_PRIMARY:
                    primary_partitions.append(path)
        
        primary_partitions.sort()
        
        print("extended partition: ", extended_path)
        print("primary partitions: ", primary_partitions)
        
        # If we don't have 3 or 4 primary partitions,
        # we will be able to create a new one
        if len(primary_partitions) < 3:
            # first, shrink file system
            res = fs.resize(partition_path, fs_type, new_size)
            if res:
                # destroy original partition and create two new ones
                pm.split_partition(device_path, partition_path, new_size)
            else:
                print("Can't shrink %s(%s) filesystem" % (otherOS, fs_type))
        else:
            print("There're too many primary partitions, can't create a new one")
            

        '''
        # Prepare info for installer_thread
        mount_devices = {}
        mount_devices["/"] =
        mount_devices["swap"] = 
        
        root = mount_devices["/"]
        swap = mount_devices["swap"]
        
        fs_devices = {}
        fs_devices[root] = "ext4"
        fs_devices[swap] = "swap"
        fs_devices[partition_path] = self.row[2]
        '''




        '''        
        # TODO: Ask where to install GRUB
        grub_device = mount_devices["/"]

        self.thread = installation_thread.InstallationThread( \
                        self.settings, \
                        self.callback_queue, \
                        mount_devices, \
                        grub_device, \
                        fs_devices)
        
        self.thread.start()
        '''
