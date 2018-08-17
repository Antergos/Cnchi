#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# edit_partition.py
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

from pages.dialogs.partition_base import PartitionBaseDialog

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

class EditPartitionDialog(PartitionBaseDialog):
    """ Shows edit partition dialog """

    GUI_FILE = 'edit_partition.ui'
    GUI_OBJECT = 'edit_partition_vbox'

    def __init__(self, gui_dir, transient_for=None):

        ui_info = {
            'gui_dir': gui_dir,
            'gui_file': EditPartitionDialog.GUI_FILE,
            'gui_object': EditPartitionDialog.GUI_OBJECT}
        PartitionBaseDialog.__init__(self, self, gui_info, transient_for)

    def wants_format(self):
        """ Returns if format checkbox is active """
        format_check = self.gui.get_object('format_check')
        return format_check.get_active()

    def prepare(self):
        """ Prepare elements for showing (before run) """

        super().prepare()

        self.set_title(_("Edit partition"))

    def set_partition_info(self, partition_info):
        """ Sets partition info to widgets """
        self.set_filesystem(partition_info['filesystem'])
        self.set_mount_point(partition_info['mount_point'])
        self.set_label(partition_info['label'])
        self.set_format(
            partition_info['format_active'],
            partition_info['format_sensitive'])

    def set_filesystem(self, filesystem):
        """ Selects the fs in the combobox """
        combo = self.gui.get_object('use_combo')
        combo_model = combo.get_model()

        combo_iter = combo_model.get_iter_first()
        while combo_iter:
            combo_row = combo_model[combo_iter]
            if combo_row[0] and combo_row[0] in filesystem:
                combo.set_active_iter(combo_iter)
                combo_iter = None
            else:
                combo_iter = combo_model.iter_next(combo_iter)

    def set_mount_point(self, mount_point):
        """ Sets current mount point """
        mount_combo_entry = self.gui.get_object('mount_combo_entry')
        mount_combo_entry.set_text(mount_point)

    def set_label(self, label):
        """ Sets current partition label """
        label_entry = self.gui.get_object('label_entry')
        label_entry.set_text(label)

    def set_format(self, format_active, format_sensitive):
        """ Sets format checkbox """
        format_check = self.gui.get_object('format_check')
        format_check.set_active(format_active)
        format_check.set_sensitive(format_sensitive)
