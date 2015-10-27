# -*- coding: utf-8; Mode: Python; indent-tabs-mode: nil; tab-width: 4 -*-
#
#  zfs.py
#
#  Copyright © 2013-2015 Antergos
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import subprocess
import os
import logging

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

try:
    from gtkbasebox import GtkBaseBox
except ImportError:
    import sys
    sys.path.append('/usr/share/cnchi/cnchi')
    from gtkbasebox import GtkBaseBox

import parted

import misc.misc as misc

COL_USE_ACTIVE = 0
COL_USE_VISIBLE = 1
COL_USE_SENSITIVE = 2
COL_DISK = 3
COL_SIZE = 4
COL_DEVICE_NAME = 5


class ZFS(GtkBaseBox):
    def __init__(self, params, prev_page="", next_page=""):
        super().__init__(self, params, "zfs", prev_page, next_page)

        self.page = self.ui.get_object('zfs')

        self.force_4k = False
        self.pool_name = ""
        self.encrypt_swap = False

        self.disks = None
        self.diskdic = {}

        self.device_list = self.ui.get_object('treeview')
        self.device_list_store = self.ui.get_object('liststore')
        self.prepare_device_list()
        self.device_list.set_hexpand(True)

        '''
        liststore
        pool_type_label
        pool_type_combo
        partition_scheme_label
        partition_scheme_combo
        scrolledwindow
        treeview
        password_check_lbl
        password_check_entry
        encrypt_swap_btn
        password_entry
        password_lbl
        encrypt_disk_btn
        swap_size_lbl
        swap_size_entry
        pool_name_btn
        pool_name_entry
        force_4k_btn
        '''

    def on_use_device_toggled(self, widget, path):
        self.device_list_store[path][COL_USE_ACTIVE] = not self.device_list_store[path][COL_USE_ACTIVE]

    def prepare_device_list(self):
        """ Create columns for our treeview """

        # Use check | Disk (sda) | Size(GB) | Name (device name)

        use_toggle = Gtk.CellRendererToggle()
        use_toggle.connect("toggled", self.on_use_device_toggled)

        col = Gtk.TreeViewColumn(
            _("Use"),
            use_toggle,
            active=COL_USE_ACTIVE,
            visible=COL_USE_VISIBLE,
            sensitive=COL_USE_SENSITIVE)

        self.device_list.append_column(col)

        render_text = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn(_("Disk"), render_text, text=COL_DISK)
        self.device_list.append_column(col)

        render_text_right = Gtk.CellRendererText()
        render_text_right.set_property("xalign", 1)
        col = Gtk.TreeViewColumn(_("Size (GB)"), render_text_right, text=COL_SIZE)
        self.device_list.append_column(col)

        col = Gtk.TreeViewColumn(_("Device"), render_text, text=COL_DEVICE_NAME)
        self.device_list.append_column(col)

    def fill_device_list(self):
        """ Fill the partition list with all the data. """

        # We will store our data model in 'device_list_store'
        if self.device_list_store is not None:
            self.device_list_store.clear()

        self.device_list_store = Gtk.TreeStore(bool, bool, bool, str, int, str)

        with misc.raised_privileges():
            devices = parted.getAllDevices()

        for dev in devices:
            # avoid cdrom and any raid, lvm volumes or encryptfs
            if not dev.path.startswith("/dev/sr") and not dev.path.startswith("/dev/mapper"):
                size_in_gigabytes = int((dev.length * dev.sectorSize) / 1000000000)
                # Use check | Disk (sda) | Size(GB) | Name (device name)
                if dev.path.startswith("/dev/"):
                    path = dev.path[len("/dev/"):]
                else:
                    path = dev.path
                row = [False, True, True, path, size_in_gigabytes, dev.model]
                self.device_list_store.append(None, row)

        self.device_list.set_model(self.device_list_store)

    def translate_ui(self):
        #lbl = self.ui.get_object('wireless_section_label')
        #lbl.set_markup(_("Connecting this computer to a wi-fi network"))

        # Disable objects

        entries = [
            'pool_name_entry', 'password_entry', 'password_check_entry',
            'password_lbl', 'password_check_lbl']
        for name in entries:
            entry = self.ui.get_object(name)
            entry.set_sensitive(False)

        '''
        liststore
        scrolledwindow
        treeview
        '''

        lbl = self.ui.get_object('pool_type_label')
        lbl.set_markup(_("Pool type"))

        combo = self.ui.get_object('pool_type_combo')
        combo.remove_all()
        combo.append_text(_("None"))
        combo.append_text(_("Stripe"))
        combo.append_text(_("Mirror"))
        combo.append_text(_("RAID-Z"))
        combo.append_text(_("RAID-Z2"))

        lbl = self.ui.get_object('partition_scheme_label')
        lbl.set_markup(_("Partition scheme"))

        combo = self.ui.get_object('partition_scheme_combo')
        combo.remove_all()
        combo.append_text(_("GPT"))
        combo.append_text(_("MBR"))

        lbl = self.ui.get_object('password_check_lbl')
        lbl.set_markup(_("Validate password"))

        lbl = self.ui.get_object('password_lbl')
        lbl.set_markup(_("Password"))

        lbl = self.ui.get_object('swap_size_lbl')
        lbl.set_markup(_("Swap size"))

        btn = self.ui.get_object('encrypt_swap_btn')
        btn.set_label(_("Encrypt swap"))

        btn = self.ui.get_object('encrypt_disk_btn')
        btn.set_label(_("Encrypt disk"))

        btn = self.ui.get_object('pool_name_btn')
        btn.set_label(_("Pool name"))

        btn = self.ui.get_object('force_4k_btn')
        btn.set_label(_("Force ZFS 4k block size"))

    def on_encrypt_swap_btn_toggled(self, widget):
        self.encrypt_swap = not self.encrypt_swap

    def on_encrypt_disk_btn_toggled(self, widget):
        names = [
            'password_entry', 'password_check_entry',
            'password_lbl', 'password_check_lbl']

        for name in names:
            obj = self.ui.get_object(name)
            obj.set_sensitive(not obj.get_sensitive())

    def on_pool_name_btn_toggled(self, widget):
        obj = self.ui.get_object('pool_name_entry')
        obj.set_sensitive(not obj.get_sensitive())

    def on_force_4k_btn_toggled(self, widget):
        self.force_4k = not self.force_4k

    def prepare(self, direction):
        self.translate_ui()
        self.fill_device_list()
        self.show_all()

    def store_values():
        return True

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

if __name__ == '__main__':
    from test_screen import _, run
    run('zfs')
