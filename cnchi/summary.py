#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  summary.py
#
#  Copyright © 2013-2015 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

""" Check screen (detects if Antergos prerequisites are meet) """


from gi.repository import Gtk, GLib
import subprocess
import os
import logging

import misc.misc as misc
import misc.gtkwidgets as gtkwidgets
import desktop_info
import features_info
from gtkbasebox import GtkBaseBox

from installation.process import Process

# Constants
NM = 'org.freedesktop.NetworkManager'
NM_STATE_CONNECTED_GLOBAL = 70
UPOWER = 'org.freedesktop.UPower'
UPOWER_PATH = '/org/freedesktop/UPower'
MIN_ROOT_SIZE = 6000000000


class Summary(GtkBaseBox):
    """ Summary Screen """

    def __init__(self, params, prev_page="", next_page="user_info"):
        """ Init class ui """
        super().__init__(self, params, "summary", prev_page, next_page)

        self.main_window = params['main_window']

        scrolled_window = self.ui.get_object("scrolled_window")
        if scrolled_window:
            scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)

        self.process = None

    def translate_ui(self):
        """ Translates all ui elements """
        txt = _("Installation Summary")
        self.header.set_subtitle(txt)

        items = {
            "location": _("Location"),
            "timezone": _("Timezone"),
            "keyboard": _("Keyboard"),
            "de": _("Desktop Environment"),
            "features": _("Features"),
            "partitions": _("Partitions")}

        for item_id in items:
            label = self.ui.get_object(item_id + "_label")
            txt = "<b>{0}</b>".format(items[item_id])
            label.set_markup(txt)

        # Fill stateboxes

        # Location
        statebox = self.ui.get_object("location_statebox")
        statebox.set_property("label", self.settings.get('location'))

        # Timezone
        statebox = self.ui.get_object("timezone_statebox")
        txt = "{0}/{1}".format(
            self.settings.get("timezone_human_country"),
            self.settings.get("timezone_human_zone"))
        statebox.set_property("label", txt)

        # Keyboard
        statebox = self.ui.get_object("keyboard_statebox")
        layout = self.settings.get("keyboard_layout")
        variant = self.settings.get("keyboard_variant")
        txt = _("Layout: {0}").format(layout)
        if variant:
            txt += "\n" + _("Variant: {0}").format(variant)
        statebox.set_property("label", txt)

        # Desktop Environment
        statebox = self.ui.get_object("de_statebox")
        desktop = self.settings.get('desktop')
        desktop_name = desktop_info.NAMES[desktop]
        statebox.set_property("label", desktop_name)

        # Features
        statebox = self.ui.get_object("features_statebox")
        txt = ""
        for feature in features_info.TITLES:
            if self.settings.get("feature_" + feature):
                txt += "{0} ".format(features_info.TITLES[feature])
        statebox.set_property("label", txt)

        # Partitions
        install_screen = self.get_install_screen()
        if install_screen:
            changes = install_screen.get_changes()
            statebox = self.ui.get_object("partitions_statebox")
            txt = ""
            for action in changes:
                txt += "{0}\n".format(str(action))
            statebox.set_property("label", txt)

    def get_install_screen(self):
        method = self.settings.get('partition_mode')
        try:
            install_screen = self.main_window.pages[method]
        except AttributeError:
            install_screen = None
        return install_screen

    def store_values(self):
        install_screen = self.get_install_screen()
        self.process = Process(install_screen, self.callback_queue)
        self.process.start()
        return True

    def prepare(self, direction):
        """ Load screen """
        self.translate_ui()
        self.show_all()

    def get_prev_page(self):
        method = self.settings.get('partition_mode')
        return method


# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

if __name__ == '__main__':
    from test_screen import _, run

    run('Summary')
