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

import logging
import os
import re

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import parted3.fs_module as fs

from dialogs.luks_settings import LuksSettingsDialog

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

class CreatePartitionDialog(Gtk.Dialog):
    """ Shows creation partition dialog """

    UI_FILE = "create_partition.ui"

    def __init__(self, ui_dir, transient_for=None):
        Gtk.Dialog.__init__(self)
        self.transient_for = transient_for
        self.set_transient_for(transient_for)

        self.ui = Gtk.Builder()
        self.ui_dir = ui_dir
        ui_file = os.path.join(
            ui_dir, 'dialogs', CreatePartitionDialog.UI_FILE)
        self.ui.add_from_file(ui_file)

        # Connect UI signals
        self.ui.connect_signals(self)

        self.luks_dialog = None
        # luks options in a tuple (use_luks, vol_name, password) """
        self.luks_options = (False, "", "")

        area = self.get_content_area()
        area.add(self.ui.get_object('create_partition_vbox'))

        self.add_button(Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)

        self.add_luks_button()

        #self.show_all()

    def add_luks_button(self):
        pass
        """
        <object class="GtkButton" id="luks_settings">
                        <property name="label" translatable="yes">Encryption options...</property>
                        <property name="use_action_appearance">False</property>
                        <property name="visible">True</property>
                        <property name="can_focus">True</property>
                        <property name="receives_default">True</property>
                        <signal name="clicked" handler="luks_settings_clicked" swapped="no"/>
                    </object>
        """

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

    def get_partition_size(self):
        """ Returns desired partition size """
        size_spin = self.ui.get_object('size_spinbutton')
        size = int(size_spin.get_value())
        return size

    def get_beginning_point(self):
        """ Returns where the new partition should start """
        beg = self.ui.get_object('create_place_beginning')
        return beg.get_active()

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

    def prepare(self, params):
        """ Prepare elements for showing (before run)
            params: 'supports_extended,
                    'extended_partition',
                    'is_primary_or_extended',
                    'max_size_mb' """

        # Initialize filesystem combobox
        combo = self.ui.get_object('use_combo')
        combo.remove_all()
        for fs_name in sorted(fs.NAMES):
            combo.append_text(fs_name)
        combo.set_wrap_width(2)

        # Initialize mount points combobox
        combo = self.ui.get_object('mount_combo')
        combo.remove_all()
        for mount_point in fs.COMMON_MOUNT_POINTS:
            combo.append_text(mount_point)

        self.prepare_radiobuttons(params)

        # Prepare size spin
        size_spin = self.ui.get_object('size_spinbutton')
        size_spin.set_digits(0)
        adjustment = Gtk.Adjustment(
            value=params['max_size_mb'],
            lower=1,
            upper=params['max_size_mb'],
            step_increment=1,
            page_increment=10,
            page_size=0)
        size_spin.set_adjustment(adjustment)
        size_spin.set_value(params['max_size_mb'])

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
            ('ok', 'dialog-apply', _('_Apply'))]

        for grp in btns:
            (btn_id, icon, lbl) = grp
            image = Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.BUTTON)
            btn = self.ui.get_object(btn_id)
            btn.set_always_show_image(True)
            btn.set_image(image)
            btn.set_label(lbl)

        self.translate_ui()

    def translate_ui(self):
        """ Translate user interface """
        # Translate dialog "Create partition"

        self.set_title(_("Create partition"))

        btns = [
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
            ('luks_settings', _("Encryption Options..."))]

        for grp in btns:
            btn_id, lbl = grp
            btn = self.ui.get_object(btn_id)
            btn.set_label(lbl)

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

        self.luks_dialog.prepare(self.luks_options)

        response = self.luks_dialog.run()
        if response == Gtk.ResponseType.OK:
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
