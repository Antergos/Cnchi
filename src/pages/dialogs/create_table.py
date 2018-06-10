#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# create_table.py
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


""" Create disk table dialog (advanced mode) """

import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import misc.extra as misc

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

class CreateTableDialog(Gtk.Dialog):
    """ Shows creation table disk dialog """

    __gtype_name__ = "CreateTableDialog"

    UI_FILE = "create_table.ui"

    def __init__(self, ui_dir, transient_for=None):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(transient_for)

        self.ui = Gtk.Builder()
        self.ui_dir = ui_dir
        ui_file = os.path.join(
            ui_dir, 'dialogs', CreateTableDialog.UI_FILE)
        self.ui.add_from_file(ui_file)

        # Connect UI signals
        self.ui.connect_signals(self)
        
        area = self.get_content_area()
        area.add(self.ui.get_object('create_table_vbox'))

        self.add_button(Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)

        self.set_title(_("Create Partition Table"))
        self.prepare()

    def get_table_type(self):
        """ Returns selected table type (msdos or gpt) """
        line = None
        combo = self.ui.get_object('partition_types_combo')
        if combo:
            line = combo.get_active_text()
            if line:
                line = line.lower()
        return line

    def prepare(self):
        """ Prepare partition types combobox """
        combo = self.ui.get_object('partition_types_combo')
        combo.remove_all()
        combo.append_text("msdos (MBR)")
        combo.append_text("GUID Partition Table (GPT)")
        # Automatically select first entry
        misc.select_first_combobox_item(combo)
