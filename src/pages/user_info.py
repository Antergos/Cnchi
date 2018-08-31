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

    def __init__(self, params, prev_page=None, next_page="summary"):
        super().__init__(self, params, "user_info", prev_page, next_page)

        self.load_widgets()

        self.require_password = True
        self.encrypt_home = False

        self.data_path = self.settings.get('data')
        self.avatars_path = os.path.join(self.data_path, 'images/avatars')
        self.avatars = ['bob', 'jarry', 'jonathan', 'mike', 'suzanne', 'tom']

        if self.overlay:
            self.overlay.show()

        self.avatar_image = None
        self.selected_avatar_path = None

        # Camera
        # TODO: Store avatar from the video when user clicks on it
        # We disable webcam widget until this is done
        self.webcam = None
        #self.webcam = webcam.WebcamWidget(
        #    UserInfo.CAMERA_WIDTH,
        #    UserInfo.CAMERA_HEIGHT)
        if self.webcam and not self.webcam.error:
            self.overlay.set_size_request(
                UserInfo.CAMERA_WIDTH,
                UserInfo.CAMERA_HEIGHT)

            event_box = Gtk.EventBox.new()
            event_box.connect(
                'button-press-event',
                self.webcam.clicked)

            self.overlay.add_overlay(event_box)
            event_box.add(self.webcam)

            self.webcam.set_halign(Gtk.Align.START)
            self.webcam.set_valign(Gtk.Align.START)
        else:
            # Can't find a camera, use an avatar icon
            random.seed()
            avatar = random.choice(self.avatars)
            self.set_avatar(avatar)

    def load_widgets(self):
        """ Get widgets """
        self.widgets = dict()

        self.widgets['fullname'] = dict()
        self.widgets['fullname']['entry'] = self.gui.get_object('fullname')
        self.widgets['fullname']['image'] = self.gui.get_object('fullname_ok')

        self.widgets['hostname'] = dict()
        self.widgets['hostname']['entry'] = self.gui.get_object('hostname')
        self.widgets['hostname']['image'] = self.gui.get_object('hostname_ok')
        self.widgets['hostname']['label'] = self.gui.get_object(
            'hostname_error_label')

        self.widgets['username'] = dict()
        self.widgets['username']['entry'] = self.gui.get_object('username')
        self.widgets['username']['image'] = self.gui.get_object('username_ok')
        self.widgets['username']['label'] = self.gui.get_object(
            'username_error_label')

        self.widgets['password'] = dict()
        self.widgets['password']['entry'] = self.gui.get_object('password')
        self.widgets['password']['image'] = self.gui.get_object('password_ok')
        self.widgets['password']['label'] = self.gui.get_object(
            'password_error_label')
        self.widgets['password']['strength'] = self.gui.get_object('password_strength')

        self.widgets['verified_password'] = dict()
        self.widgets['verified_password']['entry'] = self.gui.get_object(
            'verified_password')

        self.login = dict()
        self.login['auto'] = self.gui.get_object('login_auto')
        self.login['pass'] = self.gui.get_object('login_pass')
        self.login['encrypt'] = self.gui.get_object('login_encrypt')

        self.overlay = self.gui.get_object('user_info_overlay')

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
            label = self.gui.get_object(name)
            label.set_markup(txt)

        label = self.gui.get_object('hostname_extra_label')
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
            label = self.gui.get_object(name)
            label.set_placeholder_text(txt)

        labels = {
            'hostname': _("You must enter a name"),
            'username': _("You must enter a username"),
            'password': _("You must enter a password")}

        small_dark_red = '<small><span color="darkred">{0}</span></small>'

        for name, txt in labels.items():
            txt = small_dark_red.format(txt)
            self.widgets[name]['label'].set_markup(txt)

        self.login['auto'].set_label(_("Log in automatically"))
        self.login['pass'].set_label(_("Require my password to log in"))
        self.login['encrypt'].set_label(_("Encrypt my home folder"))

        btn = self.gui.get_object('checkbutton_show_password')
        btn.set_label(_("show password"))

        self.header.set_subtitle(_("Create Your User Account"))

    def hide_widgets(self):
        """ Hide unused and message widgets """

        for element in self.widgets:
            if isinstance(element, dict):
                if 'image' in element.keys():
                    element['image'].hide()
                if 'label' in element.keys():
                    element['label'].hide()
            else:
                print(element)
        try:
            self.widgets['password']['strength'].hide()
        except KeyError:
            pass

        # Hide cryfs encryption if using LUKS encryption
        # (user must use one or the other but not both)
        if self.settings.get('use_luks'):
            self.login['encrypt'].hide()

        # TODO: Setup installed system so it mounts encrypted home folder on boot
        # FIXME: We need to deactivate the encrypt widget as it is not finished
        self.login['encrypt'].hide()

    def store_values(self):
        """ Store all user values in self.settings """
        self.settings.set(
            'user_fullname', self.widgets['fullname']['entry'].get_text())
        self.settings.set(
            'hostname', self.widgets['hostname']['entry'].get_text())
        self.settings.set('user_name', self.widgets['username']['entry'].get_text())
        self.settings.set('user_password', self.widgets['password']['entry'].get_text())
        self.settings.set('require_password', self.require_password)

        # FIXME: Allow home encryption
        self.settings.set('encrypt_home', False)
        if self.encrypt_home:
            message = _(
                "Are you sure you want to encrypt your home directory?")
            res = show.question(self.get_main_window(), message)
            if res == Gtk.ResponseType.YES:
                self.settings.set('encrypt_home', True)

        # Store user's avatar
        self.settings.set('user_avatar', self.selected_avatar_path)

        return True

    def prepare(self, direction):
        """ Prepare screen """
        self.translate_ui()
        self.show_all()
        self.hide_widgets()

        if self.webcam and not self.webcam.error:
            self.webcam.show_all()
        elif self.avatar_image:
            self.avatar_image.show_all()

        # Disable autologin if using 'base' desktop
        if self.settings.get('desktop') == "base":
            self.login['auto'].set_sensitive(False)

        # Disable forward button until user data is filled correctly
        self.forward_button.set_sensitive(False)

    def show_password_toggled(self, _widget):
        """ show/hide user password """
        btn = self.gui.get_object('checkbutton_show_password')
        shown = btn.get_active()
        self.widgets['password']['entry'].set_visibility(shown)
        self.widgets['verified_password']['entry'].set_visibility(shown)

    def authentication_toggled(self, widget):
        """ User has changed autologin or home encrypting """
        if widget == self.login['auto']:
            self.require_password = not bool(self.login['auto'].get_active())

        if widget == self.login['encrypt']:
            self.encrypt_home = bool(self.login['encrypt'].get_active())

    def validate(self, element, value):
        """ Check that what the user is typing is ok """
        val_error = validation.check(element, value)
        if not val_error:
            # Value validated
            self.set_icon(element, UserInfo.ICON_OK)
            self.widgets[element]['label'].hide()
        else:
            # Not validated. Show warning icon and error
            self.set_icon(element, UserInfo.ICON_WARNING)
            txt = self.format_validation_error(val_error)
            self.widgets[element]['label'].set_markup(txt)
            self.widgets[element]['label'].show()

    def set_icon(self, element, icon_type):
        """ Sets icon image """
        self.widgets[element]['image'].set_from_icon_name(
            icon_type,
            Gtk.IconSize.LARGE_TOOLBAR)
        self.widgets[element]['image'].show()

    @staticmethod
    def format_validation_error(validation_error):
        """ Format validation error message """
        if validation.NAME_BADCHAR in validation_error:
            txt = _("Invalid characters entered")
        elif validation.NAME_BADDOTS in validation_error:
            txt = _("Username can't contain dots")
        elif validation.NAME_LENGTH in validation_error:
            txt = _("Too few or too many characters")
        else:
            txt = _("Unknown error")
        txt = "<small><span color='darkred'>{0}</span></small>"
        return txt.format(txt)

    def info_loop(self, widget):
        """ User has introduced new information. Check it here. """

        for key, element in self.widgets.items():
            if widget != element['entry']:
                continue
            if key in ('fullname', 'hostname', 'username'):
                value = element['entry'].get_text()
                self.validate(key, value)
            elif key in ('password', 'verified_password'):
                self.validate_password()

        # Check if all fields are filled and ok by checking image icons
        all_ok = True
        if not self.settings.get('hidden'):
            for element in self.widgets:
                if 'image' in element.keys():
                    icon_name = element['image'].get_property('icon-name')
                    visible = element['image'].is_visible()
                    if not visible or icon_name == UserInfo.ICON_WARNING:
                        all_ok = False
        self.forward_button.set_sensitive(all_ok)

    def validate_password(self):
        """ Validates changed password entry """
        validation.check_password(
            self.widgets['password'],
            self.widgets['verified_password'])

    def get_prev_page(self):
        """ Returns previous screen """
        pages = {
            'advanced':  'installation_advanced',
            'alongside': 'installation_alongside',
            'automatic': 'installation_automatic',
            'zfs': 'installation_zfs'}

        partition_mode = self.settings.get('partition_mode')
        self.prev_page = pages.get(partition_mode, None)
        return self.prev_page
