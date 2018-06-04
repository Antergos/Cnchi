#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# partition_treeview.py
#
# Copyright © 2013-2018 Antergos
#
# This file is part of Cnchi.
#
# Cnchi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Cnchi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# The following additional terms are in effect as per Section 7 of the license:
#
# The preservation of all legal notices and author attributions in
# the material or in the Appropriate Legal Notices displayed
# by works containing it is required.
#
# You should have received a copy of the GNU General Public License
# along with Cnchi; If not, see <http://www.gnu.org/licenses/>.

""" Partition Treeview Widget """

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message


class PartitionTreeview(Gtk.TreeView):
    """ Partition Treeview Class """
    COL_PATH = 0
    COL_FS = 1
    COL_MOUNT_POINT = 2
    COL_LABEL = 3
    COL_FORMAT_ACTIVE = 4
    COL_FORMAT_VISIBLE = 5
    COL_SIZE = 6
    COL_USED = 7
    COL_PARTITION_PATH = 8
    COL_FLAGS = 9
    COL_PARTITION_TYPE = 10
    COL_FORMAT_SENSITIVE = 11
    COL_SSD_ACTIVE = 12
    COL_SSD_VISIBLE = 13
    COL_SSD_SENSITIVE = 14
    COL_ENCRYPTED = 15

    def __init__(self):
        Gtk.TreeView.__init__(self)
        # Treeview model
        self.store = None
        # Checkbox cells
        self.format_toggle = None
        self.ssd_toggle = None

    def prepare(self):
        """ Create columns for our treeview """
        render_text = Gtk.CellRendererText()

        col = Gtk.TreeViewColumn(
            _("Device"), render_text, text=PartitionTreeview.COL_PATH)
        self.append_column(col)

        col = Gtk.TreeViewColumn(
            _("Type"), render_text, text=PartitionTreeview.COL_FS)
        self.append_column(col)

        col = Gtk.TreeViewColumn(
            _("Mount point"), render_text, text=PartitionTreeview.COL_MOUNT_POINT)
        self.append_column(col)

        col = Gtk.TreeViewColumn(
            _("Label"), render_text, text=PartitionTreeview.COL_LABEL)
        self.append_column(col)

        self.format_toggle = Gtk.CellRendererToggle()
        self.connect_format_cell(self.format_cell_toggled)

        col = Gtk.TreeViewColumn(
            _("Format"),
            self.format_toggle,
            active=PartitionTreeview.COL_FORMAT_ACTIVE,
            visible=PartitionTreeview.COL_FORMAT_VISIBLE,
            sensitive=PartitionTreeview.COL_FORMAT_SENSITIVE)
        self.append_column(col)

        col = Gtk.TreeViewColumn(
            _("Size"), render_text, text=PartitionTreeview.COL_SIZE)
        self.append_column(col)

        col = Gtk.TreeViewColumn(
            _("Used"), render_text, text=PartitionTreeview.COL_USED)
        self.append_column(col)

        col = Gtk.TreeViewColumn(
            _("Flags"), render_text, text=PartitionTreeview.COL_FLAGS)
        self.append_column(col)

        self.ssd_toggle = Gtk.CellRendererToggle()
        self.connect_ssd_cell(self.ssd_cell_toggled)

        col = Gtk.TreeViewColumn(
            _("SSD"),
            self.ssd_toggle,
            active=PartitionTreeview.COL_SSD_ACTIVE,
            visible=PartitionTreeview.COL_SSD_VISIBLE,
            sensitive=PartitionTreeview.COL_SSD_SENSITIVE)
        self.append_column(col)

    def connect_format_cell(self, callback):
        """ Helper to connect a callback function with the format checkbox cell """
        self.format_toggle.connect("toggled", callback)

    def connect_ssd_cell(self, callback):
        """ Helper to connect a callback function with the sdd checkbox cell """
        self.ssd_toggle.connect("toggled", callback)

    def format_cell_toggled(self, _widget, path):
        """ Toggle format checkbox """
        status = self.store[path][PartitionTreeview.COL_FORMAT_ACTIVE]
        self.store[path][PartitionTreeview.COL_FORMAT_ACTIVE] = not status

    def ssd_cell_toggled(self, _widget, path):
        """ Mark disk as ssd """
        status = self.store[path][PartitionTreeview.COL_SSD_ACTIVE]
        self.store[path][PartitionTreeview.COL_SSD_ACTIVE] = not status

    def append(self, parent, row):
        """ Appends a new row into the model (store) """
        return self.store.append(parent, row)

    def create_store(self):
        """ Create store for our data model """

        if self.store is not None:
            self.store.clear()

        self.store = Gtk.TreeStore(
            str, str, str, str, bool, bool, str, str,
            str, str, int, bool, bool, bool, bool, bool)

    def load_model(self):
        """ Sets our self.store model
        (this needs to be called after modifying our model) """
        self.set_model(self.store)


GObject.type_register(PartitionTreeview)
