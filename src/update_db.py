#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# update_db.py
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

""" Updates mirrorlists and databases """

import logging
import os
import shutil
import subprocess

import misc

def sync():
    """ Synchronize cached writes to persistent storage """
    try:
        subprocess.check_call(['sync'])
    except subprocess.CalledProcessError as why:
        logging.warning(
            "Can't synchronize cached writes to persistent storage: %s",
            why)

def update_mirrorlists():
    """ Make sure we have the latest mirrorlist files """
    antergos_mirrorlist = "/etc/pacman.d/antergos-mirrorlist"
    with misc.raised_privileges() as __:
        try:
            cmd = [
                'pacman',
                '-Syy',
                '--noconfirm',
                '--noprogressbar',
                '--quiet',
                'pacman-mirrorlist',
                'antergos-mirrorlist']
            with open(os.devnull, 'w') as fnull:
                subprocess.call(cmd, stdout=fnull,
                                stderr=subprocess.STDOUT)
            # Use the new downloaded mirrorlist (.pacnew) files (if any)
            pacnew_path = antergos_mirrorlist + ".pacnew"
            if os.path.exists(pacnew_path):
                shutil.copy(pacnew_path, antergos_mirrorlist)
            sync()
            logging.debug("Mirrorlists updated successfully")
        except subprocess.CalledProcessError as why:
            logging.warning(
                'Cannot update antergos-mirrorlist package: %s', why)
        except OSError as why:
            logging.warning('Error copying new mirrorlist files: %s', why)