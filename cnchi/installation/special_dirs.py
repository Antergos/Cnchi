#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# special_dirs.py
#
# Copyright © 2013-2016 Antergos
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


""" Mount / Unmount /dev et al. Used in the installation process """

import logging
import os
import subprocess

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

_SPECIAL_DIRS_MOUNTED = False


def _get_special_dirs():
    """ Get special dirs to be mounted or unmounted """
    special_dirs = ["/dev", "/dev/pts", "/proc", "/sys"]
    efi = "/sys/firmware/efi/efivars"
    if os.path.exists(efi):
        special_dirs.append(efi)
    return special_dirs


def mount(dest_dir):
    """ Mount special directories for our chroot (bind them)"""

    global _SPECIAL_DIRS_MOUNTED

    # Don't try to remount them
    if _SPECIAL_DIRS_MOUNTED:
        msg = _("Special dirs are already mounted. Skipping.")
        logging.debug(msg)
        return

    special_dirs = []
    special_dirs = _get_special_dirs()

    for special_dir in special_dirs:
        mountpoint = os.path.join(dest_dir, special_dir[1:])
        os.makedirs(mountpoint, mode=0o755, exist_ok=True)
        # os.chmod(mountpoint, 0o755)
        cmd = ["mount", "--bind", special_dir, mountpoint]
        logging.debug(
            "Mounting special dir '%s' to %s",
            special_dir,
            mountpoint)
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as process_error:
            logging.warning(
                "Unable to mount %s, command %s failed: %s",
                mountpoint,
                process_error.cmd,
                process_error.output)

    _SPECIAL_DIRS_MOUNTED = True


def umount(dest_dir):
    """ Umount special directories for our chroot """

    global _SPECIAL_DIRS_MOUNTED

    # Do not umount if they're not mounted
    if not _SPECIAL_DIRS_MOUNTED:
        msg = _("Special dirs are not mounted. Skipping.")
        logging.debug(msg)
        return

    special_dirs = []
    special_dirs = _get_special_dirs()

    for special_dir in reversed(special_dirs):
        mountpoint = os.path.join(dest_dir, special_dir[1:])
        logging.debug("Unmounting special dir '%s'", format(mountpoint))
        try:
            subprocess.check_call(["umount", mountpoint])
        except subprocess.CalledProcessError:
            logging.debug("Can't unmount. Trying -l to force it.")
            try:
                subprocess.check_call(["umount", "-l", mountpoint])
            except subprocess.CalledProcessError as process_error:
                txt = "Unable to unmount {0}, command {1} failed: {2}".format(
                    mountpoint, process_error.cmd, process_error.output)
                logging.warning(txt)

    _SPECIAL_DIRS_MOUNTED = False
