#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# loader.py
#
# Copyright © 2013-2017 Antergos
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


""" Bootloader installation """

import os

from misc.run_cmd import call
import parted3.fs_module as fs
import logging


class Bootloader(object):
    """ Class to perform boot loader installation """

    def __init__(self, dest_dir, settings, mount_devices):
        self.dest_dir = dest_dir
        self.settings = settings
        self.mount_devices = mount_devices

        self.uuids = {}

        if "/" in self.mount_devices:
            self.uuids["/"] = fs.get_uuid(self.mount_devices["/"])
        else:
            logging.error(
                "Cannot install bootloader, root device has not been specified!")

        if "swap" in self.mount_devices:
            self.uuids["swap"] = fs.get_uuid(self.mount_devices["swap"])

        if "/boot" in self.mount_devices:
            self.uuids["/boot"] = fs.get_uuid(self.mount_devices["/boot"])
        elif "/" in self.mount_devices:
            # No dedicated /boot partition
            self.uuids["/boot"] = self.uuids["/"]
        else:
            logging.error(
                "Cannot install bootloader, root device has not been specified!")

    def install(self):
        """ Installs the bootloader """

        # Freeze and unfreeze xfs filesystems to enable bootloader
        # installation on xfs filesystems
        self.freeze_unfreeze_xfs()

        bootloader = self.settings.get('bootloader').lower()
        boot = None
        if bootloader == "grub2":
            from installation.boot.grub2 import Grub2
            boot = Grub2(self.dest_dir, self.settings, self.uuids)
        elif bootloader == "systemd-boot":
            from installation.boot.systemd_boot import SystemdBoot
            boot = SystemdBoot(self.dest_dir, self.settings, self.uuids)
        elif bootloader == "refind":
            from installation.boot.refind import REFInd
            boot = REFInd(self.dest_dir, self.settings, self.uuids)

        if boot:
            boot.install()

    def freeze_unfreeze_xfs(self):
        """ Freeze and unfreeze xfs, as hack for grub(2) installing """
        if not os.path.exists("/usr/bin/xfs_freeze"):
            return

        xfs_boot = False
        xfs_root = False

        call(["sync"])
        with open("/proc/mounts") as mounts_file:
            mounts = mounts_file.readlines()
        # We leave a blank space in the end as we want to search
        # exactly for this mount points
        boot_mount_point = self.dest_dir + "/boot "
        root_mount_point = self.dest_dir + " "
        for line in mounts:
            if " xfs " in line:
                if boot_mount_point in line:
                    xfs_boot = True
                elif root_mount_point in line:
                    xfs_root = True
        if xfs_boot:
            boot_mount_point = boot_mount_point.rstrip()
            call(["xfs_freeze", "-f", boot_mount_point])
            call(["xfs_freeze", "-u", boot_mount_point])
        if xfs_root:
            call(["xfs_freeze", "-f", self.dest_dir])
            call(["xfs_freeze", "-u", self.dest_dir])
