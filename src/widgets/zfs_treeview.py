# -*- coding: utf-8; Mode: Python; indent-tabs-mode: nil; tab-width: 4 -*-
#
#  zfs_treeview.py
#
# Copyright © 2013-2018 Antergos
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

""" ZFS Treeview """

import os
import parted
import misc.extra as misc

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

DEST_DIR = "/install"

# Partition sizes are in MiB
MAX_ROOT_SIZE = 30000
MAX_ROOT_SIZE_GB = MAX_ROOT_SIZE // 1024

# KDE (with all features) needs 8 GB for its files
# (including pacman cache xz files).
MIN_ROOT_SIZE = 8000
MIN_ROOT_SIZE_GB = MIN_ROOT_SIZE // 1024


def is_int(num):
    """ Checks if num is an integer """
    return isinstance(num, int)


class ZFSTreeview(Gtk.TreeView):
    """ ZFS installation screen class """

    __gtype_name__ = 'ZFSTreeview'

    COL_USE_ACTIVE = 0
    COL_USE_VISIBLE = 1
    COL_USE_SENSITIVE = 2
    COL_DISK = 3
    COL_SIZE = 4
    COL_DEVICE_NAME = 5
    COL_DISK_ID = 6

    def __init__(self, zfs_ui):
        Gtk.TreeView.__init__(self)

        self.change_list = []
        self.ids = {}

        self.use_toggle = None

        self.device_list = zfs_ui.get_object('treeview')
        self.device_list_store = zfs_ui.get_object('liststore')
        self.prepare_device_list()
        self.device_list.set_hexpand(True)

    def use_device_toggled(self, _widget, path):
        """ Use device clicked """
        status = self.device_list_store[path][ZFSTreeview.COL_USE_ACTIVE]
        self.device_list_store[path][ZFSTreeview.COL_USE_ACTIVE] = not status

    def connect_use_device(self, callback):
        """ Connect 'toggle' callback of use device cell """
        if self.use_toggle:
            self.use_toggle.connect('toggled', callback)

    def prepare_device_list(self):
        """ Create columns for our treeview """

        # Use check | Disk (sda) | Size(GB) | Name (device name) | Device ID

        self.use_toggle = Gtk.CellRendererToggle()
        self.use_toggle.connect("toggled", self.use_device_toggled)

        col = Gtk.TreeViewColumn(
            _("Use"),
            self.use_toggle,
            active=ZFSTreeview.COL_USE_ACTIVE,
            visible=ZFSTreeview.COL_USE_VISIBLE,
            sensitive=ZFSTreeview.COL_USE_SENSITIVE)

        self.device_list.append_column(col)

        render_text = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn(_("Disk"), render_text, text=ZFSTreeview.COL_DISK)
        self.device_list.append_column(col)

        render_text_right = Gtk.CellRendererText()
        render_text_right.set_property("xalign", 1)
        col = Gtk.TreeViewColumn(
            _("Size (GB)"),
            render_text_right,
            text=ZFSTreeview.COL_SIZE)
        self.device_list.append_column(col)

        col = Gtk.TreeViewColumn(
            _("Device"),
            render_text,
            text=ZFSTreeview.COL_DEVICE_NAME)
        self.device_list.append_column(col)

        col = Gtk.TreeViewColumn(
            _("Disk ID"),
            render_text,
            text=ZFSTreeview.COL_DISK_ID)
        self.device_list.append_column(col)

    def fill_device_list(self):
        """ Fill the partition list with all the data. """

        # We will store our data model in 'device_list_store'
        if self.device_list_store is not None:
            self.device_list_store.clear()

        self.device_list_store = Gtk.TreeStore(
            bool, bool, bool, str, int, str, str)

        with misc.raised_privileges():
            devices = parted.getAllDevices()

        self.get_ids()

        for dev in devices:
            # Skip cdrom, raid, lvm volumes or encryptfs
            if dev.path.startswith("/dev/sr") or dev.path.startswith("/dev/mapper"):
                continue
            size = dev.length * dev.sectorSize
            size_gbytes = int(parted.formatBytes(size, 'GB'))
            # Use check | Disk (sda) | Size(GB) | Name (device name)
            if dev.path.startswith("/dev/"):
                path = dev.path[len("/dev/"):]
            else:
                path = dev.path
            disk_id = self.ids.get(path, "")
            row = [False, True, True, path, size_gbytes, dev.model, disk_id]
            self.device_list_store.append(None, row)

        self.device_list.set_model(self.device_list_store)

    def get_ids(self):
        """ Get disk and partitions IDs """
        path = "/dev/disk/by-id"
        for entry in os.scandir(path):
            if (not entry.name.startswith('.') and
                    entry.is_symlink() and
                    entry.name.startswith("ata")):
                dest_path = os.readlink(entry.path)
                device = dest_path.split("/")[-1]
                self.ids[device] = entry.name

    def get_num_drives(self):
        """ Returns number of active drives that will conform the zfs pool """
        num_drives = 0
        for row in self.device_list_store:
            if row[ZFSTreeview.COL_USE_ACTIVE]:
                num_drives += 1
        return num_drives

    def get_device_paths(self):
        """ Get device paths """
        device_paths = []
        for row in self.device_list_store:
            if row[ZFSTreeview.COL_USE_ACTIVE]:
                device_paths.append(
                    "/dev/{0}".format(row[ZFSTreeview.COL_DISK]))
        return device_paths

GObject.type_register(ZFSTreeview)
