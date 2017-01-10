#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  broadcom_wl.py
#
#  Copyright © 2013-2016 Antergos
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


""" Broadcom-wl driver installation """

import os

try:
    from hardware.hardware import Hardware
except ImportError:
    from hardware import Hardware

CLASS_NAME = "BroadcomWl"
CLASS_ID = "0x02"
VENDOR_ID = "0x14e4"

# Broadcom's driver for:
# BCM4311-, BCM4312-, BCM4313-, BCM4321-, BCM4322-, BCM43224- and BCM43225-,
# BCM43227- and BCM43228-based hardware.

DEVICES = ['0x4311', '0x04b5', '0x4727', '0x1361', '0x4328', '0x432b', '0x43b1']

# Give this driver more priority so it is chosen instead of
# broadcom_b43 or Broadcom_b43_legacy
PRIORITY = 2


class BroadcomWl(Hardware):
    """ Broadcom wl proprietary driver """
    def __init__(self):
        Hardware.__init__(self, CLASS_NAME, CLASS_ID, VENDOR_ID, DEVICES, PRIORITY)

    @staticmethod
    def get_packages():
        """ Get all required packages """
        return ["broadcom-wl"]

    @staticmethod
    def post_install(dest_dir):
        """ Post install commands """
        path = os.path.join(dest_dir, "etc/modprobe.d/blacklist-broadcom.conf")
        with open(path, "w") as blacklist:
            blacklist.write("blacklist b43\n")
            blacklist.write("blacklist b43_legacy\n")

    @staticmethod
    def is_proprietary():
        """ Returns True if the driver is a proprietary one """
        return True
