#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  check.py
#
#  Copyright © 2013-2018 Antergos
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
import subprocess
import tarfile
import tempfile
import dbus
import multiprocessing
import requests
import time

from gi.repository import GLib

import info

from misc.gtkwidgets import StateBox
import misc.extra as misc
from misc.run_cmd import call
from pages.gtkbasebox import GtkBaseBox

import show_message as show

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message


class Check(GtkBaseBox):
    """ Check class """

    UPOWER_KEY = 'org.freedesktop.UPower'
    UPOWER_PATH = '/org/freedesktop/UPower'
    MIN_ROOT_SIZE = 8000000000

    def __init__(self, params, prev_page="language", next_page="location"):
        """ Init class ui """
        super().__init__(self, params, "check", prev_page, next_page)

        self.results = multiprocessing.Manager().dict()
        self.results['internet'] = False
        self.results['power'] = False
        self.results['space'] = False
        self.results['packing'] = False
        self.results['updated'] = False
        self.results['check_all'] = False

        self.remove_timer = False
        self.prepare_power_source = None
        self.prepare_network_connection = None
        self.prepare_enough_space = None
        self.timeout_id = None
        self.prepare_best_results = None
        self.updated = None
        self.packaging_issues = None

        self.label_space = self.gui.get_object("label_space")


    def translate_ui(self):
        """ Translates all ui elements """
        txt = _("System Check")
        self.header.set_subtitle(txt)

        self.updated = self.gui.get_object("updated")
        txt = _("Cnchi is up to date")
        self.updated.set_property("label", txt)

        self.prepare_enough_space = self.gui.get_object("prepare_enough_space")
        txt = _("has at least {0}GB available storage space. (*)")
        txt = txt.format(Check.MIN_ROOT_SIZE / 1000000000)
        self.prepare_enough_space.set_property("label", txt)

        txt = _("This highly depends on which desktop environment you choose, "
                "so you might need more space.")
        txt = "(*) <i>{0}</i>".format(txt)
        self.label_space.set_markup(txt)
        self.label_space.set_hexpand(False)
        self.label_space.set_line_wrap(True)
        self.label_space.set_max_width_chars(80)

        self.prepare_power_source = self.gui.get_object("prepare_power_source")
        txt = _("is plugged in to a power source")
        self.prepare_power_source.set_property("label", txt)

        self.prepare_network_connection = self.gui.get_object(
            "prepare_network_connection")
        txt = _("is connected to the Internet")
        self.prepare_network_connection.set_property("label", txt)

        self.packaging_issues = self.gui.get_object("packaging_issues")
        txt = _(
            "There are no temporary packaging issues that would interfere with installation.")
        self.packaging_issues.set_property("label", txt)

        self.prepare_best_results = self.gui.get_object("prepare_best_results")
        txt = _("For best results, please ensure that this computer:")
        txt = '<span weight="bold" size="large">{0}</span>'.format(txt)
        self.prepare_best_results.set_markup(txt)
        self.prepare_best_results.set_hexpand(False)
        self.prepare_best_results.set_line_wrap(True)
        self.prepare_best_results.set_max_width_chars(80)

    def on_timer(self):
        """ If all requirements are meet, enable forward button """
        self.prepare_network_connection.set_state(self.results['internet'])
        self.prepare_power_source.set_state(self.results['power'])
        self.prepare_enough_space.set_state(self.results['space'])
        self.packaging_issues.set_state(self.results['packing'])
        self.updated.set_state(self.results['updated'])

        if not self.remove_timer:
            self.forward_button.set_sensitive(self.results['check_all'])
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

    def go_back(self):
        self.remove_timer = True
        self.proc.terminate()

    def check_partitioning_completion(self):
        temp = self.settings.get('temp')
        path = os.path.join(temp, ".cnchi_partitioning_completed")
        if os.path.exists(path):
            msg = "You must reboot before retrying again."
            logging.error(msg)
            msg = _("You must reboot before retrying again.")
            show.fatal_error(self.main_window, msg)
            return False

    def prepare(self, direction):
        """ Load screen """
        self.translate_ui()
        self.show_all()

        self.forward_button.set_sensitive(self.results['check_all'])

        self.check_partitioning_completion()

        # Set timer
        self.on_timer()
        self.timeout_id = GLib.timeout_add(1000, self.on_timer)

        self.proc = CheckProcess(self.results, self.settings)
        self.proc.daemon = True
        self.proc.name = "check_proc"
        self.proc.start()


class CheckProcess(multiprocessing.Process):
    """ Thread that asks our server for user's location """

    def __init__(self, results, settings):
        super(CheckProcess, self).__init__()
        self.results = results
        self.settings = settings
        self.remote_version = None

    def run(self):
        while True:
            self.check_all()
            time.sleep(5)

    def check_all(self):
        """ Check that all requirements are meet """
        on_power = not self.on_battery()
        self.results['power'] = on_power

        space = self.has_enough_space()
        self.results['space'] = space

        temp = self.settings.get('temp')
        path = os.path.join(temp, ".cnchi_partitioning_completed")
        packaging_issues = os.path.exists(path)
        self.results['packing'] = not packaging_issues

        has_internet = misc.has_connection()
        self.results['internet'] = has_internet

        if has_internet:
            self.results['updated']  = self.is_updated()
        else:
            self.results['updated']  = False

        if has_internet and space and not packaging_issues:
            self.results['check_all'] = True


    def on_battery(self):
        """ Checks if we are on battery power """
        if self.has_battery():
            bus = dbus.SystemBus()
            upower = bus.get_object(Check.UPOWER_KEY, Check.UPOWER_PATH)
            result = misc.get_prop(upower, Check.UPOWER_PATH, 'OnBattery')
            if result is None:
                # Cannot read property, something is wrong.
                logging.warning("Cannot read %s/OnBattery dbus property", Check.UPOWER_PATH)
                # We will assume we are connected to a power supply
                result = False
            return result

        return False

    def has_battery(self):
        """ Checks if latptop is connected to a power supply """
        # UPower doesn't seem to have an interface for this.
        path = '/sys/class/power_supply'
        if os.path.exists(path):
            for folder in os.listdir(path):
                type_path = os.path.join(path, folder, 'type')
                if os.path.exists(type_path):
                    with open(type_path) as power_file:
                        if power_file.read().startswith('Battery'):
                            self.settings.set('laptop', 'True')
                            return True
        return False

    @staticmethod
    def has_enough_space():
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

        return max_size >= Check.MIN_ROOT_SIZE

    def is_updated(self):
        """ Checks that we're running the latest stable cnchi version """
        if not self.remote_version:
            self.remote_version = self.get_cnchi_version_in_repo()

        if self.remote_version:
            return self.compare_versions(self.remote_version, info.CNCHI_VERSION)
        return False

    @staticmethod
    def compare_versions(remote, local):
        """ Compares Cnchi versions (local vs remote) and returns true
            if local is at least as new as remote """

        remote = remote.split('.')
        local = local.split('.')
        for i, remote_val in enumerate(remote):
            remote[i] = int(remote_val)
        for i, local_val in enumerate(local):
            local[i] = int(local_val)
        if remote[0] < local[0]:
            return True
        if remote[0] > local[0]:
            return False
        if remote[1] < local[1]:
            return True
        if remote[1] > local[1]:
            return False
        if remote[2] > local[2]:
            return False
        return True

    @staticmethod
    def get_cnchi_version_in_repo():
        """ Checks cnchi version in the Antergos repository """
        mirrors = [
            ("info.antergos.repo", "/antergos/x86_64/antergos.db"),
            ("net.leaseweb.de.mirror", "/antergos/antergos/x86_64/antergos.db")]

        for fdqn, path in mirrors:
            fdqn = '.'.join(fdqn.split('.')[::-1])
            url = 'https://' + fdqn + path
            pkg = None
            try:
                ant_db = tempfile.NamedTemporaryFile(delete=False)
                response = requests.get(url)
                ant_db.write(response.content)
                ant_db.close()

                with tarfile.open(ant_db.name) as tar:
                    members = tar.getmembers()
                    for tarinfo in members:
                        if ("desc" not in tarinfo.name and
                                "cnchi" in tarinfo.name and
                                "cnchi-dev" not in tarinfo.name):
                            pkg = tarinfo.name
                            break
                if pkg:
                    version = pkg.split('-')[1]
                    logging.debug('Cnchi version in the Antergos repository is: %s', version)
                    return version
            except (requests.exceptions.ConnectionError, tarfile.ReadError) as err:
                logging.warning(err)

        logging.error("Cannot get Cnchi's version from Antergos repository!")
        return None
