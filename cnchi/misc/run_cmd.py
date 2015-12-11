#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# chroot.py
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
import os
import subprocess

from misc.extra import InstallError


def check_call(cmd, warning=True, error=False, fatal=True, msg=""):
    check_output(cmd, warning, error, fatal, msg)


def check_output(cmd, warning=True, error=False, fatal=False, msg=""):
    output = None
    try:
        output = subprocess.check_call(cmd, stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as process_error:
        if not msg:
            msg = "Error running {0}: {1}".format(err.cmd, err.output.decode())
        else:
            msg = "{0}: {1}".format(msg, err.output.decode())
        if not error:
            if not warning:
                logging.debug(msg)
            else:
                logging.warning(msg)
        else:
            logging.error(msg)
        if fatal:
            raise InstallError(msg)
    return output
