#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# user_info.py
#
# Copyright © 2013-2016 Antergos
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

""" User info screen """

from gi.repository import Gtk

import misc.validation as validation
import show_message as show

from gtkbasebox import GtkBaseBox

ICON_OK = "emblem-default"
ICON_WARNING = "dialog-warning"


# import misc.camera as camera
# camera.cheese_init()


class UserInfo(GtkBaseBox):
    """ Asks for user information """

    def __init__(self, params, prev_page="disk_group", next_page="summary", **kwargs):
        super().__init__(self, params, name="user_info", prev_page=prev_page,
                         next_page=next_page, **kwargs)
        self.title = _('User Account')

        self.image_is_ok = {
            'fullname': self.ui.get_object('fullname_ok'),
            'hostname': self.ui.get_object('hostname_ok'),
            'username': self.ui.get_object('username_ok'),
            'password': self.ui.get_object('password_ok')
        }

        self.error_label = {
            'hostname': self.ui.get_object('hostname_error_label'),
            'username': self.ui.get_object('username_error_label'),
            'password': self.ui.get_object('password_error_label')
        }

        self.password_strength = self.ui.get_object('password_strength')

        self.entry = {
            'fullname': self.ui.get_object('fullname'),
            'hostname': self.ui.get_object('hostname'),
            'username': self.ui.get_object('username'),
            'password': self.ui.get_object('password'),
            'verified_password': self.ui.get_object('verified_password')
        }

        self.login = {
            'auto': self.ui.get_object('login_auto'),
            'pass': self.ui.get_object('login_pass'),
            'encrypt': self.ui.get_object('login_encrypt')
        }

        self.require_password = True
        self.encrypt_home = False

        # self.camera_window = self.ui.get_object('cheese_box')
        # self.camera = camera.CameraBox()

        self.camera_window = None
        self.camera = None

        if self.camera and self.camera.found():
            self.camera_window.add(self.camera)
            self.camera.show()
        else:
            pass
            # We don't have a camera.
            # Move all fields to the right (to center them).
            # user_info_grid = self.ui.get_object('user_info_grid')
            # user_info_grid.set_property('margin_start', 140)

    def translate_ui(self):
        """ Translates all ui elements """
        pass

    def hide_widgets(self):
        """ Hide unused and message widgets """
        ok_widgets = self.image_is_ok.values()
        for ok_widget in ok_widgets:
            ok_widget.hide()

        error_label_widgets = self.error_label.values()
        for error_label in error_label_widgets:
            error_label.hide()

        self.password_strength.hide()

        # Hide encryption if using LUKS encryption (user must use one or
        # the other but not both)
        if self.settings.get('use_luks'):
            self.login['encrypt'].hide()

        # TODO: Fix home encryption and stop hiding its widget
        if not self.settings.get('z_hidden'):
            self.login['encrypt'].hide()

    def store_values(self):
        """ Store all user values in self.settings """
        # For developer testing
        # Do not use this, is confusing for others when testing dev version
        self.settings.set('fullname', self.entry['fullname'].get_text())
        self.settings.set('hostname', self.entry['hostname'].get_text())
        self.settings.set('username', self.entry['username'].get_text())
        self.settings.set('password', self.entry['password'].get_text())
        self.settings.set('require_password', self.require_password)

        self.settings.set('encrypt_home', False)
        if self.encrypt_home:
            message = _("Are you sure you want to encrypt your home directory?")
            res = show.question(self.get_main_window(), message)
            if res == Gtk.ResponseType.YES:
                self.settings.set('encrypt_home', True)

        # Let installer_process know that all info has been entered
        self.settings.set('user_info_done', True)

        return True

    def prepare(self, direction):
        """ Prepare screen """
        self.translate_ui()
        self.show_all()
        self.hide_widgets()

        # Disable autologin if using 'base' desktop
        if self.settings.get('desktop') == "base":
            self.login['auto'].set_sensitive(False)

        # self.forward_button.set_label(_('Save'))
        # self.forward_button.set_name('fwd_btn_save')
        self.forward_button.set_sensitive(False)

    def on_checkbutton_show_password_toggled(self, widget):
        """ show/hide user password """
        btn = self.ui.get_object('checkbutton_show_password')
        shown = btn.get_active()
        self.entry['password'].set_visibility(shown)
        self.entry['verified_password'].set_visibility(shown)

    def on_authentication_toggled(self, widget):
        """ User has changed autologin or home encrypting """

        if widget == self.login['auto']:
            if self.login['auto'].get_active():
                self.require_password = False
            else:
                self.require_password = True

        if widget == self.login['encrypt']:
            if self.login['encrypt'].get_active():
                self.encrypt_home = True
            else:
                self.encrypt_home = False

    def validate(self, element, value):
        """ Check that what the user is typing is ok """
        if len(value) == 0:
            self.image_is_ok[element].set_from_icon_name(
                    ICON_WARNING,
                    Gtk.IconSize.LARGE_TOOLBAR)
            self.image_is_ok[element].show()
            self.error_label[element].show()
        else:
            result = validation.check(element, value)
            if not result:
                self.image_is_ok[element].set_from_icon_name(
                        ICON_OK,
                        Gtk.IconSize.LARGE_TOOLBAR)
                self.image_is_ok[element].show()
                self.error_label[element].hide()
            else:
                self.image_is_ok[element].set_from_icon_name(
                        ICON_WARNING,
                        Gtk.IconSize.LARGE_TOOLBAR)
                self.image_is_ok[element].show()

                if validation.NAME_BADCHAR in result:
                    txt = _("Invalid characters entered")
                elif validation.NAME_BADDOTS in result:
                    txt = _("Username can't contain dots")
                elif validation.NAME_LENGTH in result:
                    txt = _("Too many characters")
                else:
                    txt = _("Unknown error")

                my_format = "<small><span color='darkred'>{0}</span></small>"
                txt = my_format.format(txt)
                self.error_label[element].set_markup(txt)
                self.error_label[element].show()

    def info_loop(self, widget):
        """ User has introduced new information. Check it here. """

        if widget == self.entry['fullname']:
            fullname = self.entry['fullname'].get_text()
            if fullname:
                self.image_is_ok['fullname'].set_from_icon_name(
                        ICON_OK,
                        Gtk.IconSize.LARGE_TOOLBAR)
            else:
                self.image_is_ok['fullname'].set_from_icon_name(
                        ICON_WARNING,
                        Gtk.IconSize.LARGE_TOOLBAR)
            self.image_is_ok['fullname'].show()

        elif widget == self.entry['hostname']:
            hostname = self.entry['hostname'].get_text()
            self.validate('hostname', hostname)

        elif widget == self.entry['username']:
            username = self.entry['username'].get_text()
            self.validate('username', username)

        elif (widget == self.entry['password'] or
                      widget == self.entry['verified_password']):
            validation.check_password(
                    self.entry['password'],
                    self.entry['verified_password'],
                    self.image_is_ok['password'],
                    self.error_label['password'],
                    self.password_strength)

        # Check if all fields are filled and ok
        all_ok = True
        ok_widgets = self.image_is_ok.values()
        if not self.settings.get('z_hidden'):
            for ok_widget in ok_widgets:
                icon_name = ok_widget.get_property('icon-name')
                visible = ok_widget.is_visible()
                if not visible or icon_name == ICON_WARNING:
                    all_ok = False

        self.forward_button.set_sensitive(all_ok)


if __name__ == '__main__':
    from test_screen import _, run

    run('UserInfo')
