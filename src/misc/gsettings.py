#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# gsettings.py
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


import logging

from misc.run_cmd import chroot_call


def set(installation_user, schema, key, value):
    cmd = [
        'runuser',
        '-l', installation_user,
        '-c', "dbus-launch gsettings set " + schema + " " + key + " " + value
    ]

    logging.debug("Running set on gsettings: %s", ''.join(str(e) + ' ' for e in cmd))
    return chroot_call(cmd)


def get(installation_user, schema, key):
    cmd = [
        'runuser',
        '-l', installation_user,
        '-c', "dbus-launch gsettings get " + schema + " " + key
    ]

    logging.debug("Running get on gsettings: %s", ''.join(str(e) + ' ' for e in cmd))
    return chroot_call(cmd)
