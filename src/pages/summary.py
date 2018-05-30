#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# summary.py
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


""" Summary screen (last chance for the user) """


import logging

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import desktop_info
import features_info
from pages.gtkbasebox import GtkBaseBox
from installation.process import Process

from misc.extra import InstallError

import show_message as show

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

# Constants
NM = 'org.freedesktop.NetworkManager'
NM_STATE_CONNECTED_GLOBAL = 70
UPOWER = 'org.freedesktop.UPower'
UPOWER_PATH = '/org/freedesktop/UPower'
MIN_ROOT_SIZE = 6000000000


class Summary(GtkBaseBox):
    """ Summary Screen """

    def __init__(self, params, prev_page="user_info", next_page="slides"):
        """ Init class ui """
        super().__init__(self, params, "summary", prev_page, next_page)

        self.main_window = params['main_window']

        if not self.main_window:
            raise InstallError("Can't get main window")

        scrolled_window = self.ui.get_object("scrolled_window")
        if scrolled_window:
            scrolled_window.set_policy(
                Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)

        self.num_features = 0
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
            txt += ", " + _("Variant: {0}").format(variant)
        statebox.set_property("label", txt)

        # Desktop Environment
        statebox = self.ui.get_object("de_statebox")
        desktop = self.settings.get('desktop')
        desktop_name = desktop_info.NAMES[desktop]
        statebox.set_property("label", desktop_name)

        # Features
        statebox = self.ui.get_object("features_statebox")
        txt = ""
        self.num_features = 0
        for feature in features_info.TITLES:
            if self.settings.get("feature_" + feature):
                feature_title = _(features_info.TITLES[feature])
                txt += "{0}\n".format(feature_title)
                self.num_features += 1
        txt = txt[:-1]
        statebox.set_property("label", txt)

        # Partitions
        install_screen = self.get_install_screen()
        if install_screen:
            txt = ""
            statebox = self.ui.get_object("partitions_statebox")
            changes = install_screen.get_changes()
            if changes is None or not changes:
                txt = _("Error getting changes from install screen")
                logging.error("Error getting changes from install screen")
            else:
                for action in changes:
                    txt += "{0}\n".format(_(str(action)))
                txt = txt[:-1]
        else:
            txt = _("Error getting changes from install screen")
            logging.error("Error getting changes from install screen")

        statebox.set_property("label", txt)

    def get_install_screen(self):
        """ Returns installation screen page """
        page = "installation_" + self.settings.get('partition_mode')
        install_screen = None
        try:
            install_screen = self.main_window.pages[page]
        except (AttributeError, KeyError) as page_error:
            msg = "Can't find installation page called {0}: {1}"
            msg = msg.format(page, page_error)
            logging.error(msg)
            raise InstallError(msg)
        return install_screen

    def prepare(self, direction):
        """ Load screen """
        self.translate_ui()

        # self.forward_button.set_label(_("Install now!"))
        # self.forward_button.set_name('fwd_btn_install_now')

        self.show_all()

        # Hide features statebox if no features are selected
        if self.num_features == 0:
            names = ["features_statebox", "features_label"]
            for name in names:
                widget = self.ui.get_object(name)
                widget.hide()

    def store_values(self):
        """ User wants to continue """
        parent = self.get_toplevel()
        msg = _("Are you REALLY sure you want to continue?")

        try:
            response = show.question(parent, msg)
        except TypeError as _ex:
            response = show.question(None, msg)

        if response != Gtk.ResponseType.YES:
            return False

        install_screen = self.get_install_screen()
        self.process = Process(
            install_screen, self.settings, self.callback_queue)
        self.process.start()
        return True

    def get_prev_page(self):
        """ Gets previous page """
        page = "installation_" + self.settings.get('partition_mode')
        return page


if __name__ == '__main__':
    from test_screen import _, run

    run('Summary')
