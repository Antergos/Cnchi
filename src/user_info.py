#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  user_info.py
#  
#  Copyright 2013 Antergos
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  Antergos Team:
#   Alex Filgueira (faidoc) <alexfilgueira.antergos.com>
#   Raúl Granados (pollitux) <raulgranados.antergos.com>
#   Gustau Castells (karasu) <karasu.antergos.com>
#   Kirill Omelchenko (omelcheck) <omelchek.antergos.com>
#   Marc Miralles (arcnexus) <arcnexus.antergos.com>
#   Alex Skinner (skinner) <skinner.antergos.com>

from gi.repository import Gtk

import os
import validation
import config

_next_page = "slides"
_prev_page = "keymap"

class UserInfo(Gtk.Box):

    def __init__(self, params):

        self.title = params['title']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        self.settings = params['settings']

        super().__init__()

        self.ui = Gtk.Builder()

        self.ui.add_from_file(os.path.join(self.ui_dir, "user_info.ui"))

        self.ok = dict()
        self.ok['fullname'] = self.ui.get_object('fullname_ok')
        self.ok['hostname'] = self.ui.get_object('hostname_ok')
        self.ok['username'] = self.ui.get_object('username_ok')
        self.ok['password'] = self.ui.get_object('password_ok')

        self.error_label = dict()
        self.error_label['hostname'] = self.ui.get_object('hostname_error_label')
        self.error_label['username'] = self.ui.get_object('username_error_label')
        self.error_label['password'] = self.ui.get_object('password_error_label')

        self.password_strength = self.ui.get_object('password_strength')

        self.entry = dict()
        self.entry['fullname'] = self.ui.get_object('fullname')
        self.entry['hostname'] = self.ui.get_object('hostname')
        self.entry['username'] = self.ui.get_object('username')
        self.entry['password'] = self.ui.get_object('password')
        self.entry['verified_password'] = self.ui.get_object('verified_password')

        self.login = dict()
        self.login['auto'] = self.ui.get_object('login_auto')
        self.login['pass'] = self.ui.get_object('login_pass')
        self.login['encrypt'] = self.ui.get_object('login_encrypt')

        self.ui.connect_signals(self)

        self.require_password = True
        self.encrypt_home = False

        super().add(self.ui.get_object("user_info"))

    def translate_ui(self):
        label = self.ui.get_object('fullname_label')
        txt = _("Your name:")
        label.set_markup(txt)

        label = self.ui.get_object('hostname_label')
        txt = _("Your computer's name:")
        label.set_markup(txt)

        label = self.ui.get_object('username_label')
        txt = _("Pick a username:")
        label.set_markup(txt)

        label = self.ui.get_object('password_label')
        txt = _("Choose a password:")
        label.set_markup(txt)

        label = self.ui.get_object('verified_password_label')
        txt = _("Confirm your password:")
        label.set_markup(txt)

        label = self.ui.get_object('hostname_extra_label')
        txt = _("The name it uses when it talks to other computers.")
        txt = '<span size="small">%s</span>' % txt
        label.set_markup(txt)

        txt = _("You must enter a name")
        txt = '<small><span color="darkred">%s</span></small>' % txt
        self.error_label['hostname'].set_markup(txt)

        txt = _("You must enter a username")
        txt = '<small><span color="darkred">%s</span></small>' % txt
        self.error_label['username'].set_markup(txt)

        txt = _("You must enter a password")
        txt = '<small><span color="darkred">%s</span></small>' % txt
        self.error_label['password'].set_markup(txt)

        self.login['auto'].set_label(_("Log in automatically"))
        self.login['pass'].set_label(_("Require my password to log in"))
        self.login['encrypt'].set_label(_("Encrypt my home folder"))

        txt = _("Who are you?")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.title.set_markup(txt)

    def hide_widgets(self):
        ok_widgets = self.ok.values()
        for ok in ok_widgets:
            ok.hide()

        error_label_widgets = self.error_label.values()
        for error_label in error_label_widgets:
            error_label.hide()

        self.password_strength.hide()
        
        self.login['encrypt'].hide()

    def store_values(self):
        self.settings.set('fullname', self.entry['fullname'].get_text())
        self.settings.set('hostname', self.entry['hostname'].get_text())
        self.settings.set('username', self.entry['username'].get_text())
        self.settings.set('password', self.entry['password'].get_text())
        self.settings.set('require_password', self.require_password)
        
        # TODO: Allow to encrypt home directory
        self.settings.set('encrypt_home', False)
        
        # this way installer_thread will know all info has been entered
        self.settings.set('user_info_done', True)

    def prepare(self, direction):
        self.translate_ui()
        self.show_all()
        self.hide_widgets()
        self.forward_button.set_sensitive(False)

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page

    def on_authentication_toggled(self, widget):
        # user has changed autologin or home encrypting

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
        if len(value) == 0:
            self.ok[element].set_from_stock("gtk-no", Gtk.IconSize.BUTTON)
            self.ok[element].show()
            self.error_label[element].show()
        else:
            result = validation.check(element, value)
            #print(result)
            if len(result) == 0:
                self.ok[element].set_from_stock("gtk-yes", Gtk.IconSize.BUTTON)
                self.ok[element].show()
                self.error_label[element].hide()
            else:
                self.ok[element].set_from_stock("gtk-no", Gtk.IconSize.BUTTON)
                self.ok[element].show()

                if validation.NAME_BADCHAR in result:
                    txt = _("Invalid characters entered")
                    txt = "<small><span color='darkred'>%s</span></small>" % txt
                    self.error_label[element].set_markup(txt)
                elif validation.NAME_BADDOTS in result:
                    txt = _("Contains consecutive, initial and/or final dots")
                    txt = "<small><span color='darkred'>%s</span></small>" % txt
                    self.error_label[element].set_markup(txt)
                elif validation.NAME_LENGTH in result:
                    txt = _("Too many characters")
                    txt = "<small><span color='darkred'>%s</span></small>" % txt
                    self.error_label[element].set_markup(txt)

                self.error_label[element].show()


    def info_loop(self, widget):
        # user has introduced new information. Check it here.

        if widget == self.entry['fullname']:
            fullname = self.entry['fullname'].get_text()
            if len(fullname) > 0:
                self.ok['fullname'].show()
            else:
                self.ok['fullname'].hide()

        if widget == self.entry['hostname']:
            hostname = self.entry['hostname'].get_text()
            self.validate('hostname', hostname)

        if widget == self.entry['username']:
            username = self.entry['username'].get_text()
            self.validate('username', username)

        if widget == self.entry['password'] or \
                widget == self.entry['verified_password']:
            validation.check_password(self.entry['password'], \
                    self.entry['verified_password'], \
                    self.ok['password'], \
                    self.error_label['password'], \
                    self.password_strength)

        # check if all fields are filled and ok
        all_ok = True
        ok_widgets = self.ok.values()
        for ok in ok_widgets:
            (icon_name, icon_size) = ok.get_stock()
            visible = ok.get_visible()
            if visible == False or icon_name != "gtk-yes":
                all_ok = False

        self.forward_button.set_sensitive(all_ok)
