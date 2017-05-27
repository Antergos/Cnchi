#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# special_dirs.py
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


def _get_mounts():
    """ Gets all mount parameters for each mount """

    # (mount_type, mount_point, mount_fs_type, mount_options)
    # mount_point must be an absolute path
    mounts = [
        ("proc", "/proc", "proc", "nosuid,noexec,nodev"),
        ("sys", "/sys", "sysfs", "nosuid,noexec,nodev,ro"),
        ("udev", "/dev", "devtmpfs", "mode=0755,nosuid"),
        ("devpts", "/dev/pts", "devpts", "mode=0620,gid=5,nosuid,noexec"),
        ("shm", "/dev/shm", "tmpfs", "mode=1777,nosuid,nodev"),
        ("run", "/run", "tmpfs", "nosuid,nodev,mode=0755"),
        ("tmp", "/tmp", "tmpfs", "mode=1777,strictatime,nodev,nosuid"),
        ("/run/dbus", "/run/dbus", "tmpfs", "bind")]

    efi_dir = "/sys/firmware/efi/efivars"
    if os.path.exists(efi_dir):
        mounts.append(("efivarfs", efi_dir, "efivarfs", "nosuid,noexec,nodev"))

    return mounts


def mount(dest_dir):
    """ Mount special directories for our chroot """

    global _SPECIAL_DIRS_MOUNTED

    # Don't try to remount them
    if _SPECIAL_DIRS_MOUNTED:
        msg = _("Special dirs are already mounted. Skipping.")
        logging.debug(msg)
        return

    mounts = _get_mounts()

    for (mount_type, mount_point, mount_fs_type, mount_options) in mounts:
        mount_point = dest_dir + mount_point
        os.makedirs(mount_point, mode=0o755, exist_ok=True)
        cmd = ["mount", mount_type, mount_point, "-t", mount_fs_type, "-o", mount_options]
        try:
            logging.debug("Mounting %s in %s", mount_type, mount_point)
            subprocess.check_call(cmd)
            logging.debug("%s mounted in %s", mount_type, mount_point)
        except subprocess.CalledProcessError as process_error:
            logging.warning(
                "Unable to mount %s, command %s failed: %s",
                mount_point,
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

    mounts = _get_mounts()

    for (mount_type, mount_point, mount_fs_type, mount_options) in reversed(mounts):
        mount_point = dest_dir + mount_point
        logging.debug("Unmounting %s", format(mount_point))
        try:
            subprocess.check_call(["umount", mount_point])
        except subprocess.CalledProcessError:
            logging.debug("Can't unmount %s. Trying -l to force it.", mount_point)
            try:
                subprocess.check_call(["umount", "-l", mount_point])
            except subprocess.CalledProcessError as process_error:
                logging.warning(
                    "Unable to unmount %s, command %s failed: %s",
                    mount_point,
                    process_error.cmd,
                    process_error.output)

    _SPECIAL_DIRS_MOUNTED = False
