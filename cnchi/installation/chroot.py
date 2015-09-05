#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  chroot.py
#
#  Copyright © 2013-2015 Antergos
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


""" Chroot related functions. Used in the installation process """

import logging
import os
import subprocess

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

_special_dirs_mounted = False


def get_special_dirs():
    """ Get special dirs to be mounted or unmounted """
    special_dirs = ["/dev", "/dev/pts", "/proc", "/sys"]
    efi = "/sys/firmware/efi/efivars"
    if os.path.exists(efi):
        special_dirs.append(efi)
    return special_dirs


def mount_special_dirs(dest_dir):
    """ Mount special directories for our chroot (bind them)"""

    """
    There was an error creating the child process for this terminal
    grantpt failed: Operation not permitted
    """

    global _special_dirs_mounted

    # Don't try to remount them
    if _special_dirs_mounted:
        msg = _("Special dirs are already mounted. Skipping.")
        logging.debug(msg)
        return

    special_dirs = []
    special_dirs = get_special_dirs()

    for special_dir in special_dirs:
        mountpoint = os.path.join(dest_dir, special_dir[1:])
        os.makedirs(mountpoint, mode=0o755, exist_ok=True)
        # os.chmod(mountpoint, 0o755)
        cmd = ["mount", "--bind", special_dir, mountpoint]
        logging.debug("Mounting special dir '{0}' to {1}".format(special_dir, mountpoint))
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as process_error:
            txt = "Unable to mount {0}, command {1} failed: {2}".format(mountpoint, process_error.cmd, process_error.output)
            logging.warning(txt)

    _special_dirs_mounted = True


def umount_special_dirs(dest_dir):
    """ Umount special directories for our chroot """

    global _special_dirs_mounted

    # Do not umount if they're not mounted
    if not _special_dirs_mounted:
        msg = _("Special dirs are not mounted. Skipping.")
        logging.debug(msg)
        return

    special_dirs = []
    special_dirs = get_special_dirs()

    for special_dir in reversed(special_dirs):
        mountpoint = os.path.join(dest_dir, special_dir[1:])
        logging.debug("Unmounting special dir '{0}'".format(mountpoint))
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

    _special_dirs_mounted = False


def run(cmd, dest_dir, timeout=None, stdin=None):
    """ Runs command inside the chroot """
    full_cmd = ['chroot', dest_dir]

    for element in cmd:
        full_cmd.append(element)

    proc = None
    try:
        proc = subprocess.Popen(full_cmd,
                                stdin=stdin,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        outs, errs = proc.communicate(timeout=timeout)
        txt = outs.decode().strip()
        if len(txt) > 0:
            logging.debug(txt)
    except subprocess.TimeoutExpired as timeout_error:
        if proc:
            proc.kill()
            proc.communicate()
        logging.error("Timeout running the command %s", timeout_error.cmd)
    except subprocess.CalledProcessError as process_error:
        logging.error("Error running command %s: %s", process_error.cmd, process_error.output)
    except OSError as os_error:
        logging.error("Error running command %s: %s", " ".join(full_cmd), os_error)
