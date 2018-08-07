#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# create_partition.py
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

""" Create partition dialog (advanced mode) """

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from pages.dialogs.partition_base import PartitionBaseDialog

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

class CreatePartitionDialog(PartitionBaseDialog):
    """ Shows creation partition dialog """

    UI_FILE = 'create_partition.ui'
    UI_OBJECT = 'create_partition_vbox'

    def __init__(self, ui_dir, transient_for=None):
        ui_info = {
            'ui_dir': ui_dir,
            'ui_file': CreatePartitionDialog.UI_FILE,
            'ui_object': CreatePartitionDialog.UI_OBJECT}
        PartitionBaseDialog.__init__(self, self, ui_info, transient_for)

    def get_partition_size(self):
        """ Returns desired partition size """
        size_spin = self.ui.get_object('size_spinbutton')
        size = int(size_spin.get_value())
        return size

    def wants_primary(self):
        """ Returns True if the user wants to create a primary partition """
        return self.ui.get_object('create_type_primary').get_active()

    def wants_logical(self):
        """ Returns True if the user wants to create a primary partition """
        return self.ui.get_object('create_type_logical').get_active()

    def wants_extended(self):
        """ Returns True if the user wants to create a primary partition """
        return self.ui.get_object('create_type_extended').get_active()

    def prepare_radiobuttons(self, params):
        """ Prepare radio buttons for showing (before run)
            params: 'supports_extended,
                    'extended_partition',
                    'is_primary_or_extended',
                    'max_size_mb' """
        radio = {
            "primary": self.ui.get_object('create_type_primary'),
            "logical": self.ui.get_object('create_type_logical'),
            "extended": self.ui.get_object('create_type_extended')}

        radio['primary'].set_active(True)
        radio['logical'].set_active(False)
        radio['extended'].set_active(False)

        radio['primary'].set_visible(True)
        radio['logical'].set_visible(True)
        radio['extended'].set_visible(True)

        if not params['supports_extended']:
            radio['extended'].set_visible(False)

        if params['is_primary_or_extended'] and params['extended_partition']:
            radio['logical'].set_visible(False)
            radio['extended'].set_visible(False)
        elif params['is_primary_or_extended'] and not params['extended_partition']:
            radio['logical'].set_visible(False)
        elif not params['is_primary_or_extended']:
            radio['primary'].set_visible(False)
            radio['logical'].set_active(True)
            radio['extended'].set_visible(False)

        radio['begin'] = self.ui.get_object('create_place_beginning')
        radio['end'] = self.ui.get_object('create_place_end')

        radio['begin'].set_active(True)
        radio['end'].set_active(False)

    def prepare_size_spin(self, max_size_mb):
        """ Prepare size spin """
        size_spin = self.ui.get_object('size_spinbutton')
        size_spin.set_digits(0)
        adjustment = Gtk.Adjustment(
            value=max_size_mb, lower=1, upper=max_size_mb,
            step_increment=1, page_increment=10, page_size=0)
        size_spin.set_adjustment(adjustment)
        size_spin.set_value(max_size_mb)

    def prepare(self, params):
        """ Prepare elements for showing (before run)
            params: 'supports_extended,
                    'extended_partition',
                    'is_primary_or_extended',
                    'max_size_mb' """

        super().prepare()

        self.prepare_radiobuttons(params)
        self.prepare_size_spin(params['max_size_mb'])

        self.set_title(_("Create partition"))
