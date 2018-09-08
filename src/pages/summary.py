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
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import desktop_info
import features_info
from pages.gtkbasebox import GtkBaseBox
from installation.process import Process

import misc.extra as misc
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
            raise misc.InstallError("Can't get main window")

        scrolled_window = self.gui.get_object("scrolled_window")
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
            label = self.gui.get_object(item_id + "_label")
            txt = "<b>{0}</b>".format(items[item_id])
            label.set_markup(txt)

        # Fill stateboxes

        # Location
        statebox = self.gui.get_object("location_statebox")
        statebox.set_property("label", self.settings.get('location'))

        # Timezone
        statebox = self.gui.get_object("timezone_statebox")
        txt = "{0}/{1}".format(
            self.settings.get("timezone_human_country"),
            self.settings.get("timezone_human_zone"))
        statebox.set_property("label", txt)

        # Keyboard
        statebox = self.gui.get_object("keyboard_statebox")
        layout = self.settings.get("keyboard_layout")
        variant = self.settings.get("keyboard_variant")
        txt = _("Layout: {0}").format(layout)
        if variant:
            txt += ", " + _("Variant: {0}").format(variant)
        statebox.set_property("label", txt)

        # Desktop Environment
        statebox = self.gui.get_object("de_statebox")
        desktop = self.settings.get('desktop')
        desktop_name = desktop_info.NAMES[desktop]
        statebox.set_property("label", desktop_name)

        # Features
        statebox = self.gui.get_object("features_statebox")
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
            statebox = self.gui.get_object("partitions_statebox")
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
            raise misc.InstallError(msg)
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
                widget = self.gui.get_object(name)
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

        # Check if there are still processes running...
        self.wait()

        install_screen = self.get_install_screen()
        self.process = Process(
            install_screen, self.settings, self.callback_queue)
        self.process.start()
        return True

    def create_wait_window(self):
        """ Creates a wait dialog so the user knows that cnchi is updating
        the mirror lists. Returns the wait window and its progress bar """

        action_txt = _("Ranking mirrors")
        action_txt = "<big>{}</big>".format(action_txt)

        description_txt = _(
            "Cnchi is still updating and optimizing your mirror lists.")
        description_txt += "\n\n"
        description_txt += _("Please be patient...")
        description_txt = "<i>{}</i>".format(description_txt)

        wait_ui = Gtk.Builder()
        ui_file = os.path.join(self.gui_dir, "wait.ui")
        wait_ui.add_from_file(ui_file)

        action_lbl = wait_ui.get_object("action_label")
        action_lbl.set_markup(action_txt)

        description_lbl = wait_ui.get_object("description_label")
        description_lbl.set_markup(description_txt)

        progress_bar = wait_ui.get_object("progressbar")
        progress_bar.set_fraction(0.0)

        wait_window = wait_ui.get_object("wait_window")
        wait_window.set_modal(True)
        wait_window.set_transient_for(self.get_main_window())
        wait_window.set_default_size(360, 180)
        wait_window.set_position(Gtk.WindowPosition.CENTER)

        return (wait_window, progress_bar)

    def wait(self):
        """ Check if there are still processes running and
            waits for them to finish """

        # Check if there are still processes to finish
        must_wait = False
        processes = self.settings.get('processes')
        for proc in processes:
            if misc.check_pid(proc['pid']):
                must_wait = True
                break
        if not must_wait:
            return

        wait_window, progress_bar = self.create_wait_window()
        wait_window.show_all()

        # Disable this page (so the user can't click on it)
        summary_box = self.gui.get_object("summary")
        if summary_box:
            summary_box.set_sensitive(False)

        logging.debug("Waiting for all external processes to finish...")
        while must_wait:
            must_wait = False
            for proc in processes:
                if misc.check_pid(proc['pid']):
                    if proc['name'] != 'rankmirrors':
                        must_wait = True
                    else:
                        if proc['pipe'] and proc['pipe'].poll():
                            # Update wait window progress bar
                            try:
                                fraction = proc['pipe'].recv()
                                progress_bar.set_fraction(fraction)
                            except EOFError as _err:
                                fraction = -1
                            if fraction < 1.0:
                                must_wait = True
                        else:
                            must_wait = True
            while Gtk.events_pending():
                Gtk.main_iteration()
        logging.debug(
            "All external processes are finished. Installation can go on")
        wait_window.hide()
        wait_window.destroy()

        # Enable ask page so the user can continue the installation process
        if summary_box:
            summary_box.set_sensitive(True)
