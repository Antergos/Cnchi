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

from gi.repository import Gtk

import os
import canonical.validation as validation
import config
import show_message as show

_next_page = "slides"
#_prev_page = "keymap"
_prev_page = None

class UserInfo(Gtk.Box):
    """ Asks for user information """
    def __init__(self, params):
        self.header = params['header']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        self.settings = params['settings']

        Gtk.Box.__init__(self)

        self.ui = Gtk.Builder()

        self.ui.add_from_file(os.path.join(self.ui_dir, "user_info.ui"))

        self.is_ok = dict()
        self.is_ok['fullname'] = self.ui.get_object('fullname_ok')
        self.is_ok['hostname'] = self.ui.get_object('hostname_ok')
        self.is_ok['username'] = self.ui.get_object('username_ok')
        self.is_ok['password'] = self.ui.get_object('password_ok')

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

        self.add(self.ui.get_object("user_info"))

    def translate_ui(self):
        """ Translate all widgets """
        label = self.ui.get_object('fullname_label')
        txt = _("Your name:")
        label.set_markup(txt)

        label = self.ui.get_object('fullname')
        txt = _("Your name")
        label.set_placeholder_text(txt)

        label = self.ui.get_object('hostname_label')
        txt = _("Your computer's name:")
        label.set_markup(txt)

        label = self.ui.get_object('username_label')
        txt = _("Pick a username:")
        label.set_markup(txt)

        label = self.ui.get_object('username')
        txt = _("Username")
        label.set_placeholder_text(txt)

        label = self.ui.get_object('password_label')
        txt = _("Choose a password:")
        label.set_markup(txt)

        label = self.ui.get_object('password')
        txt = _("Password")
        label.set_placeholder_text(txt)

        label = self.ui.get_object('verified_password_label')
        txt = _("Confirm your password:")
        label.set_markup(txt)

        label = self.ui.get_object('verified_password')
        txt = _("Confirm password")
        label.set_placeholder_text(txt)

        label = self.ui.get_object('hostname_extra_label')
        txt = _("Identifies your system to other computers and devices.")
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

        btn = self.ui.get_object('checkbutton_show_password')
        btn.set_label(_("show password"))

        #self.header.set_title("Cnchi")
        self.header.set_subtitle(_("Create Your User Account"))

        #txt = _("Create Your User Account")
        #txt = "<span weight='bold' size='large'>%s</span>" % txt
        #self.title.set_markup(txt)

        # Restore forward button text (from install now! to next)
        self.forward_button.set_label("gtk-go-forward")

    def hide_widgets(self):
        """ Hide unused and message widgets """
        ok_widgets = self.is_ok.values()
        for ok_widget in ok_widgets:
            ok_widget.hide()

        error_label_widgets = self.error_label.values()
        for error_label in error_label_widgets:
            error_label.hide()

        self.password_strength.hide()

        # Hide encryption if using LUKS encryption (user must use one or the other but not both)
        if self.settings.get('use_luks'):
            self.login['encrypt'].hide()

        # TODO: Fix home encryption and stop hidding its widget
        self.login['encrypt'].hide()

    def store_values(self):
        """ Store all user values in self.settings """
        # For developer testing
        if self.settings.get('z_hidden'):
            self.settings.set('fullname', 'Antergos Testing')
            self.settings.set('hostname', 'Testing Machine')
            self.settings.set('username', 'antergos')
            self.settings.set('password', 'testing')
            self.settings.set('require_password', True)
        else:
            self.settings.set('fullname', self.entry['fullname'].get_text())
            self.settings.set('hostname', self.entry['hostname'].get_text())
            self.settings.set('username', self.entry['username'].get_text())
            self.settings.set('password', self.entry['password'].get_text())
            self.settings.set('require_password', self.require_password)



        self.settings.set('encrypt_home', False)
        if self.encrypt_home:
            '''
            # This is not true anymore, we use encFS now.
            message = _("Antergos will use eCryptfs to encrypt your home directory.\n"
                "Unfortunately, eCryptfs does not handle sparse files very well.\n\n"
                "Don't worry though, for most intents and purposes this deficiency does not pose a problem.\n\n"
                "One popular but inadvisable application of eCryptfs is to encrypt a BitTorrent download "
                "locationw as this often requires eCryptfs to handle sparse files of 10 GB or more and can "
                "lead to intense disk starvation.\n\n"
                "A simple workaround is to place sparse files in an unencrypted Public directory.\n\n"
                "Review https://wiki.archlinux.org/index.php/ECryptfs for more detailed information.\n\n"
                "Are you sure you want to encrypt your home directory?")
            '''
            message = _("Are you sure you want to encrypt your home directory?")
            res = show.question(message)
            if res == Gtk.ResponseType.YES:
                self.settings.set('encrypt_home', True)

        # this way installer_process will know all info has been entered
        self.settings.set('user_info_done', True)

    def prepare(self, direction):
        """ Prepare screen """
        self.translate_ui()
        self.show_all()
        self.hide_widgets()

        desktop = self.settings.get('desktop')
        if desktop != "nox" and self.login['auto']:
            self.login['auto'].set_sensitive(True)
        else:
            self.login['auto'].set_sensitive(False)
        if not self.settings.get('z_hidden'):
            self.forward_button.set_sensitive(False)

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page

    def on_checkbutton_show_password_toggled(self, widget):
        """ show/hide user password """
        btn = self.ui.get_object('checkbutton_show_password')
        show = btn.get_active()
        self.entry['password'].set_visibility(show)
        self.entry['verified_password'].set_visibility(show)

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
            self.is_ok[element].set_from_stock("gtk-no", Gtk.IconSize.BUTTON)
            self.is_ok[element].show()
            self.error_label[element].show()
        else:
            result = validation.check(element, value)
            if len(result) == 0:
                self.is_ok[element].set_from_stock("gtk-yes", Gtk.IconSize.BUTTON)
                self.is_ok[element].show()
                self.error_label[element].hide()
            else:
                self.is_ok[element].set_from_stock("gtk-no", Gtk.IconSize.BUTTON)
                self.is_ok[element].show()

                if validation.NAME_BADCHAR in result:
                    txt = _("Invalid characters entered")
                    txt = "<small><span color='darkred'>%s</span></small>" % txt
                    self.error_label[element].set_markup(txt)
                elif validation.NAME_BADDOTS in result:
                    txt = _("Username can't contain dots")
                    txt = "<small><span color='darkred'>%s</span></small>" % txt
                    self.error_label[element].set_markup(txt)
                elif validation.NAME_LENGTH in result:
                    txt = _("Too many characters")
                    txt = "<small><span color='darkred'>%s</span></small>" % txt
                    self.error_label[element].set_markup(txt)

                self.error_label[element].show()


    def info_loop(self, widget):
        """ User has introduced new information. Check it here. """

        if widget == self.entry['fullname']:
            fullname = self.entry['fullname'].get_text()
            if len(fullname) > 0:
                self.is_ok['fullname'].show()
            else:
                self.is_ok['fullname'].hide()

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
                    self.is_ok['password'], \
                    self.error_label['password'], \
                    self.password_strength)

        # Check if all fields are filled and ok
        all_ok = True
        ok_widgets = self.is_ok.values()
        if not self.settings.get('z_hidden'):
            for ok_widget in ok_widgets:
                (icon_name, icon_size) = ok_widget.get_stock()
                visible = ok_widget.get_visible()
                if visible == False or icon_name != "gtk-yes":
                    all_ok = False

        self.forward_button.set_sensitive(all_ok)

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message): return message

if __name__ == '__main__':
    from test_screen import _,run
    run('UserInfo')
