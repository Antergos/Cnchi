#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  installation_alongside.py
#
#  Copyright 2013 Antergos
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

import xml.etree.ElementTree as etree

from gi.repository import Gtk, Gdk

import sys
import os
import logging
import subprocess

if __name__ == '__main__':
    # Insert the parent directory at the front of the path.
    # This is used only when we want to test this screen
    base_dir = os.path.dirname(__file__) or '.'
    parent_dir = os.path.join(base_dir, '..')
    sys.path.insert(0, parent_dir)

import canonical.misc as misc
import show_message as show
import bootinfo

try:
    import parted
except:
    pass

# Insert the src/parted directory at the front of the path.
base_dir = os.path.dirname(__file__) or '.'
parted_dir = os.path.join(base_dir, 'parted3')
sys.path.insert(0, parted_dir)

import parted3.partition_module as pm
import parted3.fs_module as fs

from installation import process as installation_process

#_next_page = "timezone"
_next_page = "user_info"
_prev_page = "installation_ask"

# leave at least 3.5GB for Antergos when shrinking
_minimum_space_for_antergos = 3500

class InstallationAlongside(Gtk.Box):
    def __init__(self, params):
        self.header = params['header']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        self.callback_queue = params['callback_queue']
        self.settings = params['settings']
        self.alternate_package_list = params['alternate_package_list']
        self.testing = params['testing']

        super().__init__()
        self.ui = Gtk.Builder()
        self.ui.add_from_file(os.path.join(self.ui_dir, "alongside.ui"))

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
        path = os.path.join(self.settings.get("data"), "css", "scale.css")

        self.available_slider_range = [0, 0]

        if os.path.exists(path):
            with open(path, "rb") as css:
                css_data = css.read()

            provider = Gtk.CssProvider()

            try:
                provider.load_from_data(css_data)

                Gtk.StyleContext.add_provider_for_screen(
                    Gdk.Screen.get_default(), provider,
                    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
                )
            except:
                logging.exception(_("Can't load %s css") % path)


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
        txt = _("Select the OS you would like Antergos installed next to.")
        txt = '<span size="large">%s</span>' % txt
        self.label.set_markup(txt)

        #self.header.set_title("Cnchi")
        self.header.set_subtitle(_("Antergos Alongside Installation"))

        #txt = _("Antergos Alongside Installation")
        #txt = "<span weight='bold' size='large'>%s</span>" % txt
        #self.title.set_markup(txt)

        txt = _("Install Now!")
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

        try:
            device_list = parted.getAllDevices()
        except:
            logging.error(_("Can't import parted module! This installer won't work."))
            device_list = []

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
                    logging.warning(_("Unable to create list of partitions for alongside installation."))

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
            subprocess.call(["mount", partition_path, "/mnt"], stderr=subprocess.DEVNULL)
            x = subprocess.check_output(['df', partition_path]).decode()
            subprocess.call(["umount", "/mnt"], stderr=subprocess.DEVNULL)
            x = x.split('\n')
            x = x[1].split()
            self.max_size = int(x[1]) / 1000
            self.min_size = int(x[2]) / 1000
        except subprocess.CalledProcessError as e:
            logging.exception("CalledProcessError.output = %s" % e.output)

        if self.min_size + _minimum_space_for_antergos < self.max_size:
            self.new_size = self.ask_shrink_size(other_os_name)
        else:
            show.error(_("Can't shrink the partition (maybe it's nearly full)"))
            return

        if self.new_size > 0 and self.is_room_available():
            self.forward_button.set_sensitive(True)
        else:
            self.forward_button.set_sensitive(False)


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

    def is_room_available(self):
        partition_path = self.row[0]
        otherOS = self.row[1]
        fs_type = self.row[2]

        # what if path is sda10 (two digits) ? this is wrong
        device_path = self.row[0][:-1]

        new_size = self.new_size

        logging.debug("partition_path: %s" % partition_path)
        logging.debug("device_path: %s" % device_path)
        logging.debug("new_size: %s" % new_size)

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

        logging.debug("extended partition: %s" % extended_path)
        logging.debug("primary partitions: %s" % primary_partitions)

        if len(primary_partitions) >= 4:
            logging.error("There're too many primary partitions, can't create a new one")
            return False

        self.extended_path = extended_path

        return True

    def start_installation(self):
        # Alongside method shrinks selected partition
        # and creates root and swap partition in the available space

        if self.is_room_available() == False:
            return

        partition_path = self.row[0]
        otherOS = self.row[1]
        fs_type = self.row[2]

        # what if path is sda10 (two digits) ? this is wrong
        device_path = self.row[0][:-1]

        #re.search(r'\d+$', self.row[0])

        new_size = self.new_size

        # first, shrink file system
        res = fs.resize(partition_path, fs_type, new_size)
        if res:
            # destroy original partition and create a new resized one
            pm.split_partition(device_path, partition_path, new_size)
        else:
            logging.error("Can't shrink %s(%s) filesystem" % (otherOS, fs_type))
            return



        '''
        # Prepare info for installer_process
        mount_devices = {}
        mount_devices["/"] =
        mount_devices["swap"] =

        root = mount_devices["/"]
        swap = mount_devices["swap"]

        fs_devices = {}
        fs_devices[root] = "ext4"
        fs_devices[swap] = "swap"
        fs_devices[partition_path] = self.row[2]


        # TODO: Ask where to install the bootloader (if the user wants to install it)


        if os.path.exists("/sys/firmware/efi/systab"):
            self.settings.set('bootloader_type', "UEFI_x86_64")
        else:
            self.settings.set('bootloader_type', "GRUB2")

        if self.settings.get('install_bootloader'):
            self.settings.set('bootloader_device', mount_devices["/"])
            logging.info(_("Antergos will install the bootloader of type %s in %s") % \
                (self.settings.get('bootloader_type'), self.settings.get('bootloader_device'))
        else:
            logging.warning("Cnchi will not install any boot loader")

        if not self.testing:
            self.process = installation_process.InstallationProcess( \
                            self.settings, \
                            self.callback_queue, \
                            mount_devices, \
                            fs_devices, \
                            None, \
                            self.alternate_package_list)

            self.process.start()
        '''

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message): return message

if __name__ == '__main__':
    from test_screen import _,run
    run('InstallationAlongside')
