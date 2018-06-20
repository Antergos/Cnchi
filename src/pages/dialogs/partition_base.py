#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# partition_base.py
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

""" Base class for Create/Edit partition dialogs """

import logging
import os
import re

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import parted3.fs_module as fs

try:
    from dialogs.luks_settings import LuksSettingsDialog
except ImportError:
    from luks_settings import LuksSettingsDialog

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

class PartitionBaseDialog(Gtk.Dialog):
    """ Create/Edit partition base dialog """

    def __init__(self, child, ui_info, transient_for):
        """ Init base class """
        Gtk.Dialog.__init__(self)
        self.transient_for = transient_for
        self.set_transient_for(transient_for)

        # ui_info is a dict with these fields:
        # ui_dir, ui_file, ui_object
        self.ui = Gtk.Builder()
        self.ui_dir = ui_info['ui_dir']
        self.ui_path = os.path.join(
            self.ui_dir, 'dialogs', ui_info['ui_file'])
        self.ui.add_from_file(self.ui_path)

        # Connect UI signals
        self.ui.connect_signals(self)
        self.ui.connect_signals(child)

        self.luks_dialog = None
        # luks options is a tuple (use_luks, vol_name, password)
        self.luks_options = (False, "", "")

        area = self.get_content_area()
        area.add(self.ui.get_object(ui_info['ui_object']))

        self.add_stock_buttons()

    def add_stock_buttons(self):
        """ Adds apply and cancel buttons to the dialog """
        self.buttons = {}
        self.buttons['apply'] = self.add_button(
            Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY)
        self.buttons['cancel'] = self.add_button(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)

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

    def get_beginning_point(self):
        """ Returns where the new partition should start """
        beg = self.ui.get_object('create_place_beginning')
        return beg.get_active()

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

    def create_type_extended_toggled(self, widget):
        """ If user selects to create an extended partition,
            some widgets must be disabled """
        wdgts = {
            'use_label': self.ui.get_object('use_label'),
            'use_combo': self.ui.get_object('use_combo'),
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

        # Do not show warning message when creating
        # a new partition. It's obvious all data will be
        # erased.
        self.luks_dialog.warning_message_shown = True

        self.luks_dialog.show_all()
        self.luks_dialog.prepare(self.luks_options)

        response = self.luks_dialog.run()
        if response == Gtk.ResponseType.APPLY:
            self.luks_options = self.luks_dialog.get_options()

        self.luks_dialog.hide()

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

        self.translate_ui()

    def translate_ui(self):
        """ Translate user interface """

        labels = [
            ('create_place_label', _("Location:")),
            ('size_label', _("Size:")),
            ('create_type_label', _("Type:")),
            ('create_type_primary', _("Primary")),
            ('create_type_logical', _("Logical")),
            ('create_type_extended', _("Extended")),
            ('create_place_beginning', _("Beginning of this space")),
            ('create_place_end', _("End of this space")),
            ('use_label', _("Use As:")),
            ('mount_label', _("Mount Point:")),
            ('label_label', _("Label (optional):")),
            ('format_label', _("Format:"))]

        for grp in labels:
            label_id, text = grp
            label = self.ui.get_object(label_id)
            if label:
                label.set_label(text)
