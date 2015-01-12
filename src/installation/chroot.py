#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  chroot.py
#
#  Copyright © 2013,2014 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

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

def mount_special_dirs(dest_dir):
    """ Mount special directories for our chroot """

    global _special_dirs_mounted

    # Don't try to remount them
    if _special_dirs_mounted:
        msg = _("Special dirs are already mounted. Skipping.")
        logging.debug(msg)
        return

    special_dirs = ["sys", "proc", "dev", "dev/pts"]
    for s_dir in special_dirs:
        mydir = os.path.join(dest_dir, s_dir)
        if not os.path.exists(mydir):
            os.makedirs(mydir)

    efi = "/sys/firmware/efi"
    if os.path.exists(efi):
        mydir = os.path.join(dest_dir, efi[1:])
        if not os.path.exists(mydir):
            os.makedirs(mydir)

    try:
        mydir = os.path.join(dest_dir, "sys")
        cmd = ["mount", "-t", "sysfs", "/sys", mydir]
        subprocess.check_call(cmd)
        os.chmod(mydir, 0o555)

        mydir = os.path.join(dest_dir, "proc")
        cmd = ["mount", "-t", "proc", "/proc", mydir]
        subprocess.check_call(cmd)
        os.chmod(mydir, 0o555)

        mydir = os.path.join(dest_dir, "dev")
        cmd = ["mount", "-o", "bind", "/dev", mydir]
        subprocess.check_call(cmd)

        mydir = os.path.join(dest_dir, "dev/pts")
        cmd = ["mount", "-t", "devpts", "/dev/pts", mydir]
        subprocess.check_call(cmd)
        os.chmod(mydir, 0o555)
    except subprocess.CalledProcessError as err:
        logging.error(err)

    if os.path.exists(efi):
        mydir = os.path.join(dest_dir, efi[1:])
        try:
            subprocess.check_call(["mount", "-o", "bind", efi, mydir])
        except subprocess.CalledProcessError as err:
            logging.error(err)

    _special_dirs_mounted = True

def umount_special_dirs(dest_dir):
    """ Umount special directories for our chroot """

    global _special_dirs_mounted

    # Do not umount if they're not mounted
    if not _special_dirs_mounted:
        msg = _("Special dirs are not mounted. Skipping.")
        logging.debug(msg)
        return

    efi = "/sys/firmware/efi"
    if os.path.exists(efi):
        special_dirs = ["dev/pts", "sys/firmware/efi", "sys", "proc", "dev"]
    else:
        special_dirs = ["dev/pts", "sys", "proc", "dev"]

    for s_dir in special_dirs:
        mydir = os.path.join(dest_dir, s_dir)
        try:
            subprocess.check_call(["umount", mydir])
        except subprocess.CalledProcessError as err:
            # Can't unmount. Try -l to force it.
            try:
                subprocess.check_call(["umount", "-l", mydir])
            except subprocess.CalledProcessError as err:
                logging.warning(_("Unable to umount %s"), mydir)
                cmd = _("Command %s has failed.")
                logging.warning(cmd, err.cmd)
                out = _("Output : %s")
                logging.warning(out, err.output)

    _special_dirs_mounted = False

def run(cmd, dest_dir, timeout=None, stdin=None):
    """ Runs command inside the chroot """
    full_cmd = ['chroot', dest_dir]

    for element in cmd:
        full_cmd.append(element)

    try:
        proc = subprocess.Popen(full_cmd,
                                stdin=stdin,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        outs, errs = proc.communicate(timeout=timeout)
        txt = outs.decode().strip()
        if len(txt) > 0:
            logging.debug(txt)
    except subprocess.TimeoutExpired as err:
        proc.kill()
        outs, errs = proc.communicate()
        logging.error(_("Timeout running the command %s"), err.cmd)
        raise
    except OSError as err:
        logging.error(_("Error running command: %s"), err.strerror)
        raise
