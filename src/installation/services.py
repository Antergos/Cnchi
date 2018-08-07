
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# services.py
#
# Copyright © 2013-2018 Antergos
#
# This file is part of Cnchi.
#
# Cnchi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Cnchi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cnchi; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

""" Auxiliary functions to work with services """

import logging
import os

from misc.run_cmd import chroot_call

DEST_DIR = '/install'

def enable_services(services):
    """ Enables all services that are in the list 'services' """
    for name in services:
        path = os.path.join(
            DEST_DIR,
            "usr/lib/systemd/system/{}.service".format(name))
        if os.path.exists(path):
            chroot_call(['systemctl', '-fq', 'enable', name])
            logging.debug("Service '%s' has been enabled.", name)
        else:
            logging.warning("Can't find service %s", name)

def mask_services(services):
    """ Masks services """
    for name in services:
        path = os.path.join(
            DEST_DIR,
            "usr/lib/systemd/system/{}.service".format(name))
        if os.path.exists(path):
            chroot_call(['systemctl', '-fq', 'mask', name])
            logging.debug("Service '%s' has been masked.", name)
        else:
            logging.warning("Cannot find service %s (mask)", name)
