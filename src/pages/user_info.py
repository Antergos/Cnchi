#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# user_info.py
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

""" User info screen """

import logging
import os
import random

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

import show_message as show

from pages.gtkbasebox import GtkBaseBox

import widgets.webcam_widget as webcam

import misc.validation as validation
import misc.avatars as avatars_chooser

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message


class UserInfo(GtkBaseBox):
    """ Asks for user information """

    ICON_OK = "emblem-default"
    ICON_WARNING = "dialog-warning"
    AVATAR_WIDTH = 160
    AVATAR_HEIGHT = 160
    # These cannot be any values, must conform to camera capabilities
    CAMERA_WIDTH = 160
    CAMERA_HEIGHT = 90

    def __init__(self, params, prev_page=None, next_page="slides"):
        super().__init__(self, params, "user_info", prev_page, next_page)

        self.image_is_ok = dict()
        self.image_is_ok['fullname'] = self.ui.get_object('fullname_ok')
        self.image_is_ok['hostname'] = self.ui.get_object('hostname_ok')
        self.image_is_ok['username'] = self.ui.get_object('username_ok')
        self.image_is_ok['password'] = self.ui.get_object('password_ok')

        self.error_label = dict()
        self.error_label['hostname'] = self.ui.get_object(
            'hostname_error_label')
        self.error_label['username'] = self.ui.get_object(
            'username_error_label')
        self.error_label['password'] = self.ui.get_object(
            'password_error_label')

        self.password_strength = self.ui.get_object('password_strength')

        self.entry = dict()
        self.entry['fullname'] = self.ui.get_object('fullname')
        self.entry['hostname'] = self.ui.get_object('hostname')
        self.entry['username'] = self.ui.get_object('username')
        self.entry['password'] = self.ui.get_object('password')
        self.entry['verified_password'] = self.ui.get_object(
            'verified_password')

        self.login = dict()
        self.login['auto'] = self.ui.get_object('login_auto')
        self.login['pass'] = self.ui.get_object('login_pass')
        self.login['encrypt'] = self.ui.get_object('login_encrypt')

        self.require_password = True
        self.encrypt_home = False

        self.data_path = self.settings.get('data')
        self.avatars_path = os.path.join(self.data_path, 'images/avatars')
        self.avatars = ['bob', 'jarry', 'jonathan', 'mike', 'suzanne', 'tom']

        self.overlay = self.ui.get_object('user_info_overlay')
        self.overlay.show()

        self.avatar_image = None
        self.selected_avatar_path = None

        # Camera
        self.webcam = webcam.WebcamWidget(
            UserInfo.CAMERA_WIDTH,
            UserInfo.CAMERA_HEIGHT)
        if not self.webcam.error:
            self.overlay.set_size_request(
                UserInfo.CAMERA_WIDTH,
                UserInfo.CAMERA_HEIGHT)
            self.overlay.add_overlay(self.webcam)
            self.webcam.set_halign(Gtk.Align.START)
            self.webcam.set_valign(Gtk.Align.START)
        else:
            # Can't find a camera, use an avatar icon
            random.seed()
            avatar = random.choice(self.avatars)
            self.set_avatar(avatar)

    def set_avatar(self, avatar):
        """ Sets avatar image """
        icon_path = os.path.join(self.avatars_path, avatar + '.png')
        if os.path.exists(icon_path):
            if not self.avatar_image:
                self.avatar_image = Gtk.Image.new_from_file(icon_path)
                event_box = Gtk.EventBox.new()
                event_box.connect(
                    'button-press-event',
                    self.avatar_clicked)
                self.overlay.set_size_request(
                    UserInfo.AVATAR_WIDTH,
                    UserInfo.AVATAR_HEIGHT)
                self.overlay.add_overlay(event_box)
                event_box.add(self.avatar_image)
            else:
                self.avatar_image.set_from_file(icon_path)
            self.selected_avatar_path = icon_path
            # Resize it
            pixbuf = self.avatar_image.get_pixbuf()
            new_pixbuf = pixbuf.scale_simple(
                UserInfo.AVATAR_WIDTH,
                UserInfo.AVATAR_HEIGHT,
                GdkPixbuf.InterpType.BILINEAR)
            self.avatar_image.set_from_pixbuf(new_pixbuf)
        else:
            self.avatar_image = None
            logging.warning("Cannot load '%s' avatar", avatar)

    def avatar_clicked(self, _widget, _button):
        """ Avatar image has been clicked """
        main_window = self.settings.get("main_window")
        avatars = avatars_chooser.Avatars(
            self.data_path, main_window)
        avatars.run()
        avatar = avatars.selected_avatar
        if avatar:
            self.set_avatar(avatar)
        avatars.destroy()

    def translate_ui(self):
        """ Translates all ui elements """

        labels = {
            'fullname_label': _("Your name:"),
            'hostname_label': _("Your computer's name:"),
            'username_label': _("Pick a username:"),
            'password_label': _("Choose a password:"),
            'verified_password_label': _("Confirm your password:")}

        for name, txt in labels.items():
            label = self.ui.get_object(name)
            label.set_markup(txt)

        label = self.ui.get_object('hostname_extra_label')
        txt = _("Identifies your system to other computers and devices.")
        txt = '<span size="small">{0}</span>'.format(txt)
        label.set_markup(txt)

        labels = {
            'fullname': _("Your name"),
            'hostname': _("Hostname"),
            'username': _("Username"),
            'password': _("Password"),
            'verified_password': _("Confirm password")}

        for name, txt in labels.items():
            label = self.ui.get_object(name)
            label.set_placeholder_text(txt)

        labels = {
            'hostname': _("You must enter a name"),
            'username': _("You must enter a username"),
            'password': _("You must enter a password")}

        small_dark_red = '<small><span color="darkred">{0}</span></small>'

        for name, txt in labels.items():
            txt = small_dark_red.format(txt)
            self.error_label[name].set_markup(txt)

        self.login['auto'].set_label(_("Log in automatically"))
        self.login['pass'].set_label(_("Require my password to log in"))
        self.login['encrypt'].set_label(_("Encrypt my home folder"))

        btn = self.ui.get_object('checkbutton_show_password')
        btn.set_label(_("show password"))

        self.header.set_subtitle(_("Create Your User Account"))


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
        self.settings.set('user_fullname', self.entry['fullname'].get_text())
        self.settings.set('hostname', self.entry['hostname'].get_text())
        self.settings.set('user_name', self.entry['username'].get_text())
        self.settings.set('user_password', self.entry['password'].get_text())
        self.settings.set('require_password', self.require_password)

        self.settings.set('encrypt_home', False)
        if self.encrypt_home:
            message = _(
                "Are you sure you want to encrypt your home directory?")
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

        if not self.webcam.error:
            self.webcam.show_all()
        elif self.avatar_image:
            self.avatar_image.show_all()

        # Disable autologin if using 'base' desktop
        if self.settings.get('desktop') == "base":
            self.login['auto'].set_sensitive(False)

        self.forward_button.set_label(_('Save'))
        self.forward_button.set_name('fwd_btn_save')
        self.forward_button.set_sensitive(False)

    def on_checkbutton_show_password_toggled(self, _widget):
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
        if not value:
            self.image_is_ok[element].set_from_icon_name(
                UserInfo.ICON_WARNING,
                Gtk.IconSize.LARGE_TOOLBAR)
            self.image_is_ok[element].show()
            self.error_label[element].show()
        else:
            result = validation.check(element, value)
            if not result:
                self.image_is_ok[element].set_from_icon_name(
                    UserInfo.ICON_OK,
                    Gtk.IconSize.LARGE_TOOLBAR)
                self.image_is_ok[element].show()
                self.error_label[element].hide()
            else:
                self.image_is_ok[element].set_from_icon_name(
                    UserInfo.ICON_WARNING,
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
                    UserInfo.ICON_OK,
                    Gtk.IconSize.LARGE_TOOLBAR)
            else:
                self.image_is_ok['fullname'].set_from_icon_name(
                    UserInfo.ICON_WARNING,
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
                if not visible or icon_name == UserInfo.ICON_WARNING:
                    all_ok = False

        self.forward_button.set_sensitive(all_ok)
