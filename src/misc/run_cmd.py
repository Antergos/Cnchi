#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# run_cmd.py
#
# Copyright © 2013-2018 Antergos
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
import sys
import traceback
import os
import shutil

from misc.extra import InstallError, raised_privileges

DEST_DIR = "/install"


def ensured_executable(cmd):
    """
    Ensures file is executable before attempting to execute it.

    Args:
        cmd (list): The command to check.

    Returns:
        True if successful, False otherwise.

    """
    cmd = list(cmd)

    if cmd and not shutil.which(cmd[0]) and os.path.exists(cmd[0]):
        with raised_privileges():
            os.chmod(cmd[0], 0o777)

    return shutil.which(cmd[0]) is not None


def log_exception_info():
    """ This function logs information about the exception that is currently
        being handled. The information returned is specific both to the current
        thread and to the current stack frame. """

    # If no exception is being handled anywhere on the stack,
    # a tuple containing three None values is returned by sys.exc_info()
    exc_type, exc_value, exc_traceback = sys.exc_info()
    if not (exc_type is None and exc_value is None and exc_traceback is None):
        # The return value of format_exception is a list of strings,
        # each ending in a newline and some containing internal newlines.
        trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
        lines = ''.join(trace).split('\n')
        for line in lines:
            logging.error(line.rstrip())


def call(cmd, warning=True, error=False, fatal=False, msg=None, timeout=None,
         stdin=None, debug=True):
    """ Helper function to make a system call
    warning: If true will log a warning message if an error is detected
    error: If true will log an error message if an error is detected
    fatal: If true will log an error message AND will raise an InstallError exception
    msg: Error message to log (if empty the command called will be logged) """

    output = None

    if not os.environ.get('CNCHI_RUNNING', False):
        os.environ['CNCHI_RUNNING'] = 'True'

    if not ensured_executable(cmd):
        logging.error('ensured_executable failed for cmd: %s', cmd)

    try:
        output = subprocess.check_output(
            cmd,
            stdin=stdin,
            stderr=subprocess.STDOUT,
            timeout=timeout)
        output = output.decode()
        if output and debug:
            _output = output.strip('\n')
            logging.debug(_output)
        return output
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as err:
        err_output = err.output.decode().strip("\n")
        if not msg:
            msg = "Error running {0}: {1}".format(err.cmd, err_output)
        else:
            msg = "{0}: {1}".format(msg, err_output)
        if not error and not fatal:
            if not warning or "['umount', '-l'," in msg:
                logging.debug(msg)
            else:
                logging.warning(msg)
                log_exception_info()
        else:
            logging.error(msg)
            if fatal:
                raise InstallError(msg)
            else:
                log_exception_info()
        return False


def chroot_call(cmd, chroot_dir=DEST_DIR, fatal=False, msg=None, timeout=None,
                stdin=None):
    """ Runs command inside the chroot """
    full_cmd = ['chroot', chroot_dir]

    for element in cmd:
        full_cmd.append(element)

    if not os.environ.get('CNCHI_RUNNING', False):
        os.environ['CNCHI_RUNNING'] = 'True'

    try:
        proc = subprocess.Popen(
            full_cmd,
            stdin=stdin,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        stdout_data, _stderr_data = proc.communicate(timeout=timeout)
        stdout_data = stdout_data.decode().strip()
        if stdout_data:
            logging.debug(stdout_data)
        return stdout_data
    except subprocess.TimeoutExpired as err:
        if proc:
            # The child process is not killed if the timeout expires, so in
            # order to cleanup let's kill the child process and finish communication
            proc.kill()
            proc.communicate()
        msg = "Timeout running the command {0}".format(err.cmd)

        logging.error(msg)
        if fatal:
            raise InstallError(err.output)
        else:
            log_exception_info()
            return False
    except subprocess.CalledProcessError as err:
        if msg:
            msg = "{0}: {1}".format(msg, err.output)
        else:
            msg = "Error running {0}: {1}".format(err.cmd, err.output)

        logging.error(msg)
        if fatal:
            raise InstallError(err.output)
        else:
            log_exception_info()
        return False
    except OSError as os_error:
        if msg:
            msg = "{0}: {1}".format(msg, os_error)
        else:
            msg = "Error running {0}: {1}".format(" ".join(full_cmd), os_error)

        logging.error(msg)
        if fatal:
            raise InstallError(os_error)
        else:
            log_exception_info()
        return False


def popen(cmd, warning=True, error=False, fatal=False, msg=None, stdin=subprocess.PIPE):
    """ Helper function that calls Popen (useful if we need to use pipes) """

    if not os.environ.get('CNCHI_RUNNING', False):
        os.environ['CNCHI_RUNNING'] = 'True'

    if not ensured_executable(cmd):
        logging.error('ensured_executable failed for cmd: %s', cmd)

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
                log_exception_info()
        else:
            logging.error(msg)
            if fatal:
                raise InstallError(msg)
            else:
                log_exception_info()
        return None
