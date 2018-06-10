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

import logging
import os
import re

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import parted3.fs_module as fs

from dialogs.luks_settings import LuksSettingsDialog

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

class EditPartitionDialog(Gtk.Dialog):
    """ Shows edit partition dialog """

    UI_FILE = "edit_partition.ui"

    def __init__(self, ui_dir, transient_for=None):
        Gtk.Dialog.__init__(self)
        self.transient_for = transient_for
        self.set_transient_for(transient_for)

        self.ui = Gtk.Builder()
        self.ui_dir = ui_dir
        ui_file = os.path.join(
            ui_dir, 'dialogs', EditPartitionDialog.UI_FILE)
        self.ui.add_from_file(ui_file)

        # Connect UI signals
        self.ui.connect_signals(self)

        self.luks_dialog = None
        # luks options in a tuple (use_luks, vol_name, password) """
        self.luks_options = (False, "", "")

        area = self.get_content_area()
        area.add(self.ui.get_object('edit_partition_vbox'))

        self.buttons = {}
        self.buttons['apply'] = self.add_button(
            Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY)
        self.buttons['cancel'] = self.add_button(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)

    def get_label(self):
        """ Returns partition label """
        label = self.ui.get_object('label_entry')
        if label:
            label = label.get_text()
            if not label.isalpha():
                logging.debug("'%s' is not a valid label.", label)
                label = ""
            elif len(label) > 16:
                label = label[:16]
                pattern = re.compile(r"\w+")
                if not pattern.fullmatch(label):
                    logging.debug("'%s' is not a valid label.", label)
                    label = ""
            return label.replace(" ", "_")
        return ""

    def get_mount_point(self):
        """ Returns mount point for the new partition """
        mount_combo = self.ui.get_object('mount_combo_entry')
        if mount_combo:
            return mount_combo.get_text().strip()
        return ""

    def get_filesystem(self):
        """ Returns desired filesystem """
        fs_combo = self.ui.get_object('use_combo')
        if fs_combo:
            filesystem = fs_combo.get_active_text()
            if filesystem is None:
                filesystem = ""
            return filesystem
        return ""

    def get_beginning_point(self):
        """ Returns where the new partition should start """
        beg = self.ui.get_object('create_place_beginning')
        return beg.get_active()

    def is_format_active(self):
        """ Returns if format checkbox is active """
        format_check = self.ui.get_object('format_check')
        return format_check.get_active()

    def prepare(self):
        """ Prepare elements for showing (before run) """

        # Initialize filesystems combobox
        combo = self.ui.get_object('use_combo')
        combo.remove_all()
        for fs_name in sorted(fs.NAMES):
            combo.append_text(fs_name)
        combo.set_wrap_width(2)

        # Initialize edit partition dialog mount point combobox.
        combo = self.ui.get_object('mount_combo')
        combo.remove_all()
        for mount_point in fs.COMMON_MOUNT_POINTS:
            combo.append_text(mount_point)

        # label
        label_entry = self.ui.get_object('label_entry')
        label_entry.set_text("")

        # use as (fs)
        fs_combo = self.ui.get_object('use_combo')
        fs_combo.set_active(3)

        # mount combo entry
        mount_combo = self.ui.get_object('mount_combo_entry')
        mount_combo.set_text("")

        # Get encryption (LUKS) options dialog
        if not self.luks_dialog:
            self.luks_dialog = LuksSettingsDialog(
                self.ui_dir, self.transient_for)

        # Assign labels and images to buttons

        btns = [
            ('cancel', 'dialog-cancel', _('_Cancel')),
            ('apply', 'dialog-apply', _('_Apply'))]

        for grp in btns:
            (btn_id, icon, lbl) = grp
            image = Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.BUTTON)
            btn = self.buttons[btn_id]
            btn.set_always_show_image(True)
            btn.set_image(image)
            btn.set_label(lbl)

        self.translate_ui()

    def use_combo_changed(self, selection):
        """ If user selects a swap fs, it can't be mounted the usual way """
        fs_selected = selection.get_active_text()

        mount_combo = self.ui.get_object('mount_combo')
        mount_label = self.ui.get_object('mount_label')

        if fs_selected == 'swap':
            mount_combo.hide()
            mount_label.hide()
        else:
            mount_combo.show()
            mount_label.show()

    def create_type_extended_toggled(self, widget):
        """ If user selects to create an extended partition,
            some widgets must be disabled """
        wdgts = {
            'use_label':   self.ui.get_object('use_label'),
            'use_combo':   self.ui.get_object('use_combo'),
            'mount_label': self.ui.get_object('mount_label'),
            'mount_combo': self.ui.get_object('mount_combo'),
            'label_label': self.ui.get_object('label_label'),
            'label_entry': self.ui.get_object('label_entry')}

        sensitive = True

        if widget.get_active():
            sensitive = False

        for i in wdgts:
            wdgts[i].set_sensitive(sensitive)

    def luks_settings_clicked(self, _widget):
        """ Show luks settings dialog """
        if not self.luks_dialog:
            self.luks_dialog = LuksSettingsDialog(
                self.ui_dir, self.transient_for)

        self.luks_dialog.prepare(self.luks_options)

        self.luks_dialog.show_all()

        response = self.luks_dialog.run()
        if response == Gtk.ResponseType.OK:
            self.luks_options = self.luks_dialog.get_options()

        self.luks_dialog.hide()

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
        combo = self.ui.get_object('use_combo')
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
        mount_combo_entry = self.ui.get_object('mount_combo_entry')
        mount_combo_entry.set_text(mount_point)

    def set_label(self, label):
        """ Sets current partition label """
        label_entry = self.ui.get_object('label_entry')
        label_entry.set_text(label)

    def set_format(self, format_active, format_sensitive):
        """ Sets format checkbox """
        format_check = self.ui.get_object('format_check')
        format_check.set_active(format_active)
        format_check.set_sensitive(format_sensitive)

    def translate_ui(self):
        """ Translates dialog interface """

        self.set_title(_("Edit partition"))

        labels = [
            ('use_label', _("Use As:")),
            ('mount_label', _("Mount Point:")),
            ('label_label', _("Label (optional):")),
            ('format_label', _("Format:"))]

        for grp in labels:
            label_id, text = grp
            label = self.ui.get_object(label_id)
            label.set_label(text)
