#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# systemd_boot.py
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


""" Systemd-boot (gummiboot) installation """

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


class SystemdBoot(object):
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
        """ Install Systemd-boot bootloader to the EFI System Partition """
        logging.debug("Cnchi will install the Systemd-boot (Gummiboot) loader")

        # Setup bootloader menu
        menu_dir = os.path.join(self.dest_dir, "boot/loader")
        os.makedirs(menu_dir, mode=0o755, exist_ok=True)
        menu_path = os.path.join(menu_dir, "loader.conf")
        with open(menu_path, 'w') as menu_file:
            menu_file.write("default antergos")

        # Setup boot entries
        conf = {}

        if not self.settings.get('use_luks'):
            conf['default'] = []
            conf['default'].append("title\tAntergos\n")
            conf['default'].append("linux\t/vmlinuz-linux\n")
            conf['default'].append("initrd\t/initramfs-linux.img\n")
            conf['default'].append("options\troot=UUID={0}"
                                   " rw quiet\n\n".format(self.root_uuid))

            conf['fallback'] = []
            conf['fallback'].append("title\tAntergos (fallback)\n")
            conf['fallback'].append("linux\t/vmlinuz-linux\n")
            conf['fallback'].append("initrd\t/initramfs-linux-fallback.img\n")
            conf['fallback'].append("options\troot=UUID={0}"
                                    " rw quiet\n\n".format(self.root_uuid))

            if self.settings.get('feature_lts'):
                conf['lts'] = []
                conf['lts'].append("title\tAntergos LTS\n")
                conf['lts'].append("linux\t/vmlinuz-linux-lts\n")
                conf['lts'].append("initrd\t/initramfs-linux-lts.img\n")
                conf['lts'].append("options\troot=UUID={0}"
                                   " rw quiet\n\n".format(self.root_uuid))

                conf['lts_fallback'] = []
                conf['lts_fallback'].append("title\tAntergos LTS (fallback)\n\n")
                conf['lts_fallback'].append("linux\t/vmlinuz-linux-lts\n")
                conf['lts_fallback'].append("initrd\t/initramfs-linux-lts-fallback.img\n")
                conf['lts_fallback'].append("options\troot=UUID={0}"
                                            " rw quiet\n\n".format(self.root_uuid))
        else:
            luks_root_volume = self.settings.get('luks_root_volume')
            mapper = "/dev/mapper/{0}".format(luks_root_volume)
            luks_root_volume_uuid = fs.get_uuid(mapper)

            # In automatic mode, root_device is in self.mount_devices
            root_device = self.root_device

            if (self.method == "advanced" and
                    self.settings.get('use_luks_in_root')):
                root_device = self.settings.get('luks_root_device')

            root_uuid = fs.get_uuid(root_device)

            key = ""
            if self.settings.get("luks_root_password") == "":
                key = "cryptkey=UUID={0}:ext2:/.keyfile-root".format(self.boot_uuid)

            root_uuid_line = "cryptdevice=UUID={0}:{1} {2} root=UUID={3} rw quiet"
            root_uuid_line = root_uuid_line.format(
                root_uuid,
                luks_root_volume,
                key,
                luks_root_volume_uuid)

            conf['default'] = []
            conf['default'].append("title\tAntergos\n")
            conf['default'].append("linux\t/vmlinuz-linux\n")
            conf['default'].append("options\tinitrd=/initramfs-linux.img"
                                   " {0}\n\n".format(root_uuid_line))

            conf['fallback'] = []
            conf['fallback'].append("title\tAntergos (fallback)\n")
            conf['fallback'].append("linux\t/vmlinuz-linux\n")
            conf['fallback'].append("options\tinitrd=/initramfs-linux-fallback.img"
                                    " {0}\n\n".format(root_uuid_line))

            if self.settings.get('feature_lts'):
                conf['lts'] = []
                conf['lts'].append("title\tAntergos LTS\n")
                conf['lts'].append("linux\t/vmlinuz-linux-lts\n")
                conf['lts'].append("options\tinitrd=/initramfs-linux-lts.img"
                                   " {0}\n\n".format(root_uuid_line))

                conf['lts_fallback'] = []
                conf['lts_fallback'].append("title\tAntergos LTS (fallback)\n")
                conf['lts_fallback'].append("linux\t/vmlinuz-linux-lts\n")
                conf['lts_fallback'].append("options\tinitrd=/initramfs-linux-lts-fallback.img"
                                            " {0}\n\n".format(root_uuid_line))

        # Write boot entries
        entries_dir = os.path.join(self.dest_dir, "boot/loader/entries")
        os.makedirs(entries_dir, mode=0o755, exist_ok=True)

        entry_path = os.path.join(entries_dir, "antergos.conf")
        with open(entry_path, 'w') as entry_file:
            for line in conf['default']:
                entry_file.write(line)

        entry_path = os.path.join(entries_dir, "antergos-fallback.conf")
        with open(entry_path, 'w') as entry_file:
            for line in conf['fallback']:
                entry_file.write(line)

        if self.settings.get('feature_lts'):
            entry_path = os.path.join(entries_dir, "antergos-lts.conf")
            with open(entry_path, 'w') as entry_file:
                for line in conf['lts']:
                    entry_file.write(line)

            entry_path = os.path.join(entries_dir, "antergos-lts-fallback.conf")
            with open(entry_path, 'w') as entry_file:
                for line in conf['lts_fallback']:
                    entry_file.write(line)

        # Install bootloader
        logging.debug("Installing systemd-boot bootloader...")
        cmd = ['bootctl', '--path=/boot', 'install']
        if chroot_call(cmd, self.dest_dir, 300) is False:
            self.settings.set('bootloader_installation_successful', False)
        else:
            self.settings.set('bootloader_installation_successful', True)
