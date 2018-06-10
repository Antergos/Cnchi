#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# luks_settings.py
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


""" Luks settings dialog (advanced mode) """

import os

import show_message as show

import misc.validation as validation

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

class LuksSettingsDialog(Gtk.Dialog):
    """ Shows LUKS settings dialog """

    UI_FILE = "luks_settings.ui"

    def __init__(self, ui_dir, transient_for=None):
        Gtk.Dialog.__init__(self)
        self.transient_for = transient_for
        self.set_transient_for(transient_for)

        self.ui = Gtk.Builder()
        ui_file = os.path.join(
            ui_dir, 'dialogs', LuksSettingsDialog.UI_FILE)
        self.ui.add_from_file(ui_file)

        # Connect UI signals
        self.ui.connect_signals(self)

        # Show an warning message just once
        self.warning_message_shown = False

        area = self.get_content_area()
        area.add(self.ui.get_object('luks_settings_vbox'))

        self.buttons = {}
        self.buttons['apply'] = self.add_button(
            Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY)
        self.buttons['cancel'] = self.add_button(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)

    def maybe_show_warning_message(self):
        """ Show warning message """
        if not self.warning_message_shown:
            show.warning(
                self.transient_for,
                _("Using LUKS encryption will DELETE all partition contents!"))
            self.warning_message_shown = True

    def prepare(self, options):
        """ Show LUKS encryption options dialog """

        entry_vol_name = self.ui.get_object('vol_name_entry')
        entry_password = self.ui.get_object('password_entry')
        entry_password_confirm = self.ui.get_object('password_confirm_entry')

        use_luks, vol_name, password = options

        entry_vol_name.set_text(vol_name)
        entry_password.set_text(password)
        entry_password_confirm.set_text(password)

        switch_use_luks = self.ui.get_object('use_luks_switch')
        switch_use_luks.set_active(use_luks)
        self.enable_widgets(use_luks)

        self.maybe_show_warning_message()

        # Assign images to buttons
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

    def translate_ui(self):
        """ Translate dialog widgets """
        self.set_title(_("Encryption properties"))

        labels = [
            ('use_luks_label', _("Use LUKS encryption:")),
            ('vol_name_label', _("LUKS volume name:")),
            ('password_label', _("Password:")),
            ('password_confirm_label', _("Confirm password:"))
        ]

        for grp in labels:
            name, txt = grp
            label = self.ui.get_object(name)
            label.set_markup(txt)

    def get_use_luks(self):
        """ Returns if luks switch is activated or not """
        switch = self.ui.get_object('use_luks_switch')
        return switch.get_active()

    def get_vol_name(self):
        """ Returns volume name """
        entry = self.ui.get_object('vol_name_entry')
        return entry.get_text()

    def get_password(self):
        """ Returns luks password """
        entry = self.ui.get_object('password_entry')
        return entry.get_text()

    def get_password_confirm(self):
        """ Returns luks password confirmation """
        entry = self.ui.get_object('password_confirm_entry')
        return entry.get_text()

    def use_luks_switch_activate(self, widget, _data):
        """ User enables / disables luks encription """
        self.enable_widgets(widget.get_active())

    def enable_widgets(self, status):
        """ Enables or disables the LUKS encryption dialog widgets """
        w_sensitive = ['vol_name_label', 'password_label',
                       'password_confirm_label', 'vol_name_entry',
                       'password_entry', 'password_confirm_entry']
        w_hide = ['password_confirm_image', 'password_status_label']

        for w_name in w_sensitive:
            widget = self.ui.get_object(w_name)
            widget.set_sensitive(status)

        if status is False:
            for w_name in w_hide:
                widget = self.ui.get_object(w_name)
                widget.hide()

        widget = self.ui.get_object('use_luks_switch')
        widget.set_active(status)

    def get_options(self):
        """ Returns luks options in a 
            tuple (use_luks, vol_name, password) """
        
        options = (False, "", "")

        use_luks = self.get_use_luks()
        vol_name = self.get_vol_name()
        password = self.get_password()
        password_check = self.get_password_confirm()

        if use_luks:
            if vol_name and password:
                if password == password_check:
                    # Save new choices
                    options = (use_luks, vol_name, password)
                else:
                    msg = _(
                        "LUKS passwords do not match! Encryption NOT enabled.")
                    show.warning(self.transient_for, msg)
            else:
                msg = _(
                    "Volume name and password are mandatory! Encryption NOT enabled.")
                show.warning(self.transient_for, msg)
        
        return options

    def password_changed(self, widget):
        """ User has introduced new information. Check it here. """
        password = {}
        password['entry'] = self.ui.get_object('password_entry')
        password['confirm'] = self.ui.get_object('password_confirm_entry')
        password['image'] = self.ui.get_object('password_confirm_image')
        password['status'] = self.ui.get_object('password_status_label')
        password['strength'] = self.ui.get_object('password_strength')

        if widget in [password['entry'], password['confirm']]:
            validation.check_password(
                password['entry'], password['confirm'],
                password['image'], password['status'],
                password['strength'])
