#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# run_cmd.py
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


""" Chroot related functions. Used in the installation process """

import logging
import subprocess

from misc.extra import InstallError

DEST_DIR = "/install"


def call(cmd, warning=True, error=False, fatal=False, msg=None, timeout=None,
         stdin=subprocess.STDIN):
    """ Helper function to make a system call
    warning: If true will log a warning message if an error is detected
    error: If true will log an error message if an error is detected
    fatal: If true will log an error message AND will raise an InstallError exception
    msg: Error message to log (if empty the command called will be logged) """

    output = None
    try:
        output = subprocess.check_output(
            cmd,
            stdin=stdin,
            stderr=subprocess.STDOUT,
            timeout=timeout)
        output = output.decode().strip('\n')
        if output:
            logging.debug(output)
        return output
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as err:
        err_output = err.output.decode().strip("'").strip("\n")
        if not msg:
            msg = "Error running {0}: {1}".format(err.cmd, err_output)
        else:
            msg = "{0}: {1}".format(msg, err_output)
        if not error and not fatal:
            if not warning:
                logging.debug(msg)
            else:
                logging.warning(msg)
        else:
            logging.error(msg)
            if fatal:
                raise InstallError(msg)
        return False


def chroot_call(cmd, chroot_dir=DEST_DIR, fatal=False, msg=None, timeout=None,
                stdin=subprocess.PIPE):
    """ Runs command inside the chroot """
    full_cmd = ['chroot', chroot_dir]

    for element in cmd:
        full_cmd.append(element)

    try:
        proc = subprocess.Popen(
            full_cmd,
            stdin=stdin,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        output, errs = proc.communicate(timeout=timeout)
        output = output.decode().strip()
        if output:
            logging.debug(output)
        return output
    except subprocess.TimeoutExpired as err:
        if proc:
            proc.kill()
            proc.communicate()
        logging.error("Timeout running the command %s", err.cmd)
        if fatal:
            raise InstallError(err.output)
        else:
            return False
    except subprocess.CalledProcessError as err:
        if msg:
            logging.error("%s: %s", msg, err.output)
        else:
            logging.error("Error running %s: %s", err.cmd, err.output)
        if fatal:
            raise InstallError(err.output)
        else:
            return False
    except OSError as os_error:
        if msg:
            logging.error("%s: %s", msg, os_error)
        else:
            logging.error("Error running %s: %s", " ".join(full_cmd), os_error)
        if fatal:
            raise InstallError(os_error)
        else:
            return False


def popen(cmd, warning=True, error=False, fatal=False, msg=None, stdin=subprocess.PIPE):
    """ Helper function that calls Popen (useful if we need to use pipes) """
    proc = None
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stdin=stdin,
            stderr=subprocess.STDOUT)
        return proc
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as err:
        if not msg:
            msg = "Error running {0}: {1}".format(err.cmd, err.output.decode())
        else:
            msg = "{0}: {1}".format(msg, err.output.decode())
        if not error and not fatal:
            if not warning:
                logging.debug(msg)
            else:
                logging.warning(msg)
        else:
            logging.error(msg)
            if fatal:
                raise InstallError(msg)
        return False
