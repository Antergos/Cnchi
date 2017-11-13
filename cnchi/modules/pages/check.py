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

import os
import shutil
from socket import gethostname

import dbus

import misc.extra as misc
from modules._base_module import CnchiModule
from misc.run_cmd import call

# Constants
NM = 'org.freedesktop.NetworkManager'
NM_STATE_CONNECTED_GLOBAL = 70
UPOWER = 'org.freedesktop.UPower'
UPOWER_PATH = '/org/freedesktop/UPower'
MIN_ROOT_SIZE = 8000000000


class SystemCheckModule(CnchiModule):
    """
    Utility class for performing various system and environment checks.

    Attributes:
        name (str): a name for this object.
    """

    def __init__(self, name='_system_check', *args, **kwargs):

        super().__init__(name=name, *args, *kwargs)

        self.has_space = None

    def do_iso_check(self):
        """ Hostname contains the ISO version """
        # TODO: Make this actually check if iso version is recent

        hostname = gethostname()
        # ant-year.month[-min]
        prefix = 'ant-'
        if hostname.startswith(prefix):
            # We're running form the ISO, register which version.
            self.settings.is_iso = True
            suffix = '-min' if hostname.endswith('-min') else ''
            version = hostname[len(prefix):-len(suffix)]

            self.logger.debug('Running from ISO version %s', version)

            cache_dir = '/home/antergos/.cache/chromium'
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
        else:
            self.logger.debug('Not running from ISO (dev mode?)')

        return True

    def has_battery(self):
        """ Checks if we have a battery """
        self.settings.laptop = False

        # UPower doesn't seem to have an interface for this.
        path = '/sys/class/power_supply'

        if not os.path.exists(path):
            return False

        for folder in os.listdir(path):
            type_path = os.path.join(path, folder, 'type')
            if os.path.exists(type_path):
                with open(type_path) as power_file:
                    if power_file.read().startswith('Battery'):
                        self.settings.laptop = True
                        return True

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

    def on_battery_power(self):
        """ Checks if we are on battery power """
        if not self.has_battery():
            return False

        bus = dbus.SystemBus()
        upower = bus.get_object(UPOWER, UPOWER_PATH)
        if misc.get_prop(upower, UPOWER_PATH, 'OnBattery'):
            return True

