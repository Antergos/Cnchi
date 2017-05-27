#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# mkinitcpio.py
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


""" Module to setup and run mkinitcpio """

import logging
import os

from misc.run_cmd import chroot_call


def run(dest_dir, settings, mount_devices, blvm):
    """ Runs mkinitcpio """

    cpu = get_cpu()

    # Add lvm and encrypt hooks if necessary
    hooks = ['base', 'udev', 'autodetect', 'modconf', 'block', 'keyboard', 'keymap']
    modules = []
    files = []

    # It is important that the plymouth hook comes before any encrypt hook
    plymouth_bin = os.path.join(dest_dir, "usr/bin/plymouth")
    if os.path.exists(plymouth_bin):
        hooks.append('plymouth')

    # It is important that the encrypt hook comes before the filesystems hook
    # (in case you are using LVM on LUKS, the order should be: encrypt lvm2 filesystems)
    if settings.get('use_luks'):
        if os.path.exists(plymouth_bin):
            hooks.append('plymouth-encrypt')
        else:
            hooks.append('encrypt')

        modules.extend(['dm_mod', 'dm_crypt', 'ext4'])

        arch = os.uname()[-1]
        if arch == 'x86_64':
            modules.extend(['aes_x86_64'])
        else:
            modules.extend(['aes_i586'])

        modules.extend(['sha256', 'sha512'])

    if blvm or settings.get('use_lvm'):
        hooks.append('lvm2')

    if 'swap' in mount_devices:
        hooks.append('resume')

    if settings.get('zfs'):
        # the zfs hook must come before the filesystems hook
        hooks.append('zfs')
        libgcc_path = '/usr/lib/libgcc_s.so.1'
        if os.path.exists(libgcc_path):
            files.append(libgcc_path)

    hooks.append('filesystems')

    crc32 = ['crc32', 'libcrc32c', 'crc32c_generic', 'crc32c-intel', 'crc32-pclmul']

    if settings.get('f2fs'):
        modules.append('f2fs')

    if settings.get('btrfs') or settings.get('f2fs'):
        modules.extend(crc32)

    if not settings.get('btrfs') and not settings.get('zfs'):
        # Use the fsck hook only if not using btrfs or zfs
        hooks.append('fsck')

    set_hooks_modules_and_files(dest_dir, hooks, modules, files)

    # Run mkinitcpio on the target system
    # Fix for bsdcpio error. See: http://forum.antergos.com/viewtopic.php?f=5&t=1378&start=20#p5450
    locale = settings.get('locale')
    cmd = ['sh', '-c', 'LANG={0} /usr/bin/mkinitcpio -p linux'.format(locale)]
    chroot_call(cmd, dest_dir)
    if settings.get('feature_lts'):
        cmd = ['sh', '-c', 'LANG={0} /usr/bin/mkinitcpio -p linux-lts'.format(locale)]
        chroot_call(cmd, dest_dir)


def set_hooks_modules_and_files(dest_dir, hooks, modules, files):
    """ Set up mkinitcpio.conf """

    logging.debug("Setting hooks, modules and files in mkinitcpio.conf")
    logging.debug('HOOKS="%s"', ' '.join(hooks))
    logging.debug('MODULES="%s"', ' '.join(modules))
    logging.debug('FILES="%s"', ' '.join(files))

    with open("/etc/mkinitcpio.conf") as mkinitcpio_file:
        mklines = mkinitcpio_file.readlines()

    path = os.path.join(dest_dir, "etc/mkinitcpio.conf")
    with open(path, "w") as mkinitcpio_file:
        for line in mklines:
            if line.startswith("HOOKS"):
                line = 'HOOKS="{0}"\n'.format(' '.join(hooks))
            elif line.startswith("MODULES"):
                line = 'MODULES="{0}"\n'.format(' '.join(modules))
            elif line.startswith("FILES"):
                line = 'FILES="{0}"\n'.format(' '.join(files))
            mkinitcpio_file.write(line)


def get_cpu():
    """ Gets CPU string definition """
    with open("/proc/cpuinfo") as proc_file:
        lines = proc_file.readlines()

    for line in lines:
        if "vendor_id" in line:
            return line.split(":")[1].replace(" ", "").lower()
    return ""
