#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# refind.py
#
# Copyright © 2013-2015 Antergos
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


""" rEFInd bootloader installation """

import logging
import os
import shutil
import subprocess
import re
import random
import string

import parted3.fs_module as fs

from installation import special_dirs
from misc.run_cmd import call, chroot_call

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message


class REFInd(object):
    """ Class to perform boot loader installation """
    def __init__(self, dest_dir, settings, mount_devices):
        self.dest_dir = dest_dir
        self.settings = settings
        self.mount_devices = mount_devices
        self.method = settings.get("partition_mode")
        self.root_device = self.mount_devices["/"]

        self.root_uuid = fs.get_uuid(self.root_device)

        if "swap" in self.mount_devices:
            swap_partition = self.mount_devices["swap"]
            self.swap_uuid = fs.get_uuid(swap_partition)

        if "/boot" in self.mount_devices:
            boot_device = self.mount_devices["/boot"]
        else:
            # No dedicated /boot partition
            boot_device = self.mount_devices["/"]
        self.boot_uuid = fs.get_uuid(boot_device)

    def install(self):
        """ Installs rEFInd boot loader """
        # Details: https://wiki.archlinux.org/index.php/REFInd#Scripted_configuration
        logging.debug("Installing and configuring rEFInd bootloader...")
        cmd = ["refind-install"]
        self.settings.set('bootloader_installation_successful', False)
        if chroot_call(cmd, self.dest_dir, timeout=300) != False:
            # This script will attempt to find the kernel in /boot and
            # automatically generate refind_linux.conf.
            # The script will only set up the most basic kernel
            # parameters, so be sure to check the file it created for
            # correctness.
            cmd = ["refind-mkrlconf"]
            if chroot_call(cmd, self.dest_dir, timeout=300) != False:
                self.settings.set('bootloader_installation_successful', True)
                logging.debug("rEFIind installed.")
