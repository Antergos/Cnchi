#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  check.py
#
#  Copyright © 2013-2016 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  The following additional terms are in effect as per Section 7 of the license:
#
#  The preservation of all legal notices and author attributions in
#  the material or in the Appropriate Legal Notices displayed
#  by works containing it is required.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; If not, see <http://www.gnu.org/licenses/>.


""" Check screen (detects if Antergos prerequisites are meet) """

import logging
import os
import shutil

from gi.repository import Gtk, GLib

import info
import misc.extra as misc
import show_message as show
import updater
from misc.run_cmd import call
from ui.page import Page

# Constants
NM = 'org.freedesktop.NetworkManager'
NM_STATE_CONNECTED_GLOBAL = 70
UPOWER = 'org.freedesktop.UPower'
UPOWER_PATH = '/org/freedesktop/UPower'
MIN_ROOT_SIZE = 8000000000


class Check(Page):
    """ System requirements check page """

    def __init__(self, params, prev_page="welcome", next_page="location_grp", cnchi_main=None):
        """ Init class ui """
        super().__init__(self, params, "check", prev_page, next_page)

        self.remove_timer = False
        self.title = _("System Check")

        self.updater = None
        self.prepare_power_source = None
        self.prepare_network_connection = None
        self.prepare_enough_space = None
        self.timeout_id = None
        self.prepare_best_results = None
        self.updated = None
        self.latest_iso = None
        self.cnchi_main = cnchi_main
        self.cnchi_notified = False
        self.has_space = False
        self.has_internet = False
        self.has_iso = False
        self.is_updated = False
        self.header = params['header']

        self.header.set_title('')

        if 'checks_are_optional' in params:
            self.checks_are_optional = params['checks_are_optional']
        else:
            self.checks_are_optional = False

    def translate_ui(self):
        """ Translates all ui elements """
        # self.header.set_subtitle(self.title)

        self.updated = self.ui.get_object("updated")

        self.latest_iso = self.ui.get_object("latest_iso")

        self.prepare_enough_space = self.ui.get_object("prepare_enough_space")

        self.prepare_power_source = self.ui.get_object("prepare_power_source")

        self.prepare_network_connection = self.ui.get_object("prepare_network_connection")

    def check_all(self):
        """ Check that all requirements are meet """
        if os.path.exists("/tmp/.cnchi_partitioning_completed"):
            msg = "You must reboot before retrying again."
            logging.error(msg)
            msg = _("You must reboot before retrying again.")
            show.fatal_error(self.main_window, msg)
            return False

        has_internet = misc.has_connection()
        self.prepare_network_connection.set_state(has_internet)

        #if has_internet and not self.cnchi_notified:
        #    self.cnchi_main.on_has_internet_connection()
        #    logging.debug('on_has_internet_connection() is running')
        #    self.cnchi_notified = True

        on_power = not self.on_battery()
        self.prepare_power_source.set_state(on_power)

        space = self.has_enough_space() if not self.has_space else True
        self.prepare_enough_space.set_state(space)

        if self.has_internet or 'development' == info.CNCHI_RELEASE_STAGE:
            updated = self.is_updated_check() if not self.is_updated else True
        else:
            updated = False

        self.updated.set_state(updated)

        iso_check = self.check_iso_version() if not self.has_iso else True
        self.latest_iso.set_state(iso_check)

        if self.checks_are_optional:
            return True

        if has_internet and space:
            return True

        return False

    def on_battery(self):
        """ Checks if we are on battery power """
        import dbus

        if self.has_battery():
            bus = dbus.SystemBus()
            upower = bus.get_object(UPOWER, UPOWER_PATH)
            if misc.get_prop(upower, UPOWER_PATH, 'OnBattery'):
                return True

        return False

    def has_battery(self):
        """ Checks if we have a battery (thus we are a laptop) """
        # UPower doesn't seem to have an interface for this.
        path = '/sys/class/power_supply'
        if not os.path.exists(path):
            self.settings.set('laptop', False)
            return False

        for folder in os.listdir(path):
            type_path = os.path.join(path, folder, 'type')
            if os.path.exists(type_path):
                with open(type_path) as power_file:
                    if power_file.read().startswith('Battery'):
                        self.settings.set('laptop', True)
                        return True

        self.settings.set('laptop', False)
        return False

    def has_enough_space(self):
        """ Check that we have a disk or partition with enough space """

        output = call(cmd=["lsblk", "-lnb"], debug=False).split("\n")

        max_size = 0

        for item in output:
            col = item.split()
            if len(col) >= 5:
                if col[5] == "disk" or col[5] == "part":
                    size = int(col[3])
                    if size > max_size:
                        max_size = size

        if max_size >= MIN_ROOT_SIZE:
            self.has_space = True
            return True

        return False

    def is_updated_check(self):
        """ Checks that cnchi version is, at least, latest stable """
        if 'development' == info.CNCHI_RELEASE_STAGE:
            return True
        if self.updater is None:
            # Only call updater once
            self.updater = updater.Updater(local_cnchi_version=info.CNCHI_VERSION)
        return not self.updater.is_remote_version_newer()

    def check_iso_version(self):
        """ Hostname contains the ISO version """
        # TODO: Make this actually check if iso version is recent
        from socket import gethostname

        hostname = gethostname()
        # ant-year.month[-min]
        prefix = "ant-"
        if hostname.startswith(prefix):
            # We're running form the ISO, register which version.
            suffix = "-min" if hostname.endswith("-min") else ''
            version = hostname[len(prefix):-len(suffix)]
            logging.debug("Running from ISO version %s", version)
            self.settings.set('is_iso', True)
            cache_dir = "/home/antergos/.cache/chromium"
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
        else:
            logging.debug("Not running from ISO")
        return True

    def on_timer(self):
        """ If all requirements are met, enable forward button """
        if not self.remove_timer:
            self.forward_button.set_sensitive(self.check_all())
        return not self.remove_timer

    def store_values(self):
        """ Continue """
        # Remove timer
        self.remove_timer = True

        logging.info("We have Internet connection.")
        logging.info("We're connected to a power source.")
        logging.info("We have enough disk space.")

        # Enable forward button
        self.forward_button.set_sensitive(True)
        return True

    def prepare(self, direction=None, show=True):
        """ Load screen """
        self.translate_ui()
        result = self.check_all()
        if result is not None and show:
            self.set_valign(Gtk.Align.START)
            self.show_all()
            self.forward_button.set_sensitive(result)

        # Set timer
        self.timeout_id = GLib.timeout_add(5000, self.on_timer)

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

if __name__ == '__main__':
    from test_screen import _, run

    run('Check')
