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

from gi.repository import Gtk

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

import installation_thread

_next_page = "timezone"
_prev_page = "installation_ask"

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

        super().add(self.ui.get_object("installation_alongside"))

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
        
        print("partition_path: ", partition_path)
        
        min_size = 0
        max_size = 0

        try:
            x = subprocess.check_output(['df', partition_path]).decode()
            x = x.split('\n')
            x = x[1].split()
            max_size = int(x[1])
            min_size = int(x[2])
        except subprocess.CalledProcessError as e:
            print("CalledProcessError.output = %s" % e.output)

        print("Final min_size: %d" % min_size)
        print("Final max_size: %d" % max_size)
        
        if min_size < max_size:
            self.new_size = self.ask_shrink_size(min_size, max_size)
            print("new_size: %d" % self.new_size)

            if self.new_size > 0:
                self.forward_button.set_sensitive(True)
        else:
            # Can't shrink the partition (maybe it's nearly full)
            # TODO: Show error message but let the user choose
            # another install method
            pass
        
        return False
        
    def ask_shrink_size(self, min_size, max_size):
        dialog = self.ui.get_object("shrink-dialog")
        
        # Set scale GtkScale
        # value, lower, upper, step_incr, page_incr, page_size
        adj = Gtk.Adjustment(min_size, min_size, max_size, 1, 10, 0)
        
        scale = self.ui.get_object("scale")
        scale.set_adjustment(adj)
        scale.set_value(min_size)
        
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            pass
        
        dialog.hide()

        return 0

    def start_installation(self):
        # Alongside method shrinks selected partition
        # and creates root and swap partition in the available space
                
            
        mount_devices = {}
        mount_devices["alongside"] = device
        mount_devices["new_size"] = self.new_size
        
        fs_devices = {}
        
        '''
        #self.install_progress.set_sensitive(True)

        mount_devices = {}
        mount_devices["/"] = self.combobox["root"].get_active_text()
        mount_devices["swap"] = self.combobox["swap"].get_active_text()

        # Easy method formats root and swap by default
        # should we ask the user or directly use ext4 ?

        root = mount_devices["/"]
        swap = mount_devices["swap"]
        
        fs_devices = {}
        fs_devices[root] = "ext4"
        fs_devices[swap] = "swap"
        
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
