#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# broadcom_b43.py
#
#  Copyright © 2013-2015 Antergos
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

""" Broadcom b43 driver installation """

import os

try:
    from hardware.hardware import Hardware
except ImportError:
    from hardware import Hardware

CLASS_NAME = "Broadcom_b43"
CLASS_ID = "0x0200"
VENDOR_ID = "0x14e4"

DEVICES = [
    '0x0576', '0x4307', '0x4311', '0x4312', '0x4315', '0x4318', '0x4319',
    '0x4320', '0x4322', '0x4324', '0x432a', '0x432c', '0x432d', '0x4331',
    '0x4350', '0x4353', '0x4357', '0x4358', '0x4359', '0x43a9', '0x43aa',
    '0xa8d6', '0xa8d8', '0xa8db', '0xa99d']

# Give this driver more priority so it is chosen instead of Broadcom_b43_legacy
PRIORITY = 1


class Broadcom_b43(Hardware):
    def __init__(self):
        Hardware.__init__(self, CLASS_NAME, CLASS_ID, VENDOR_ID, DEVICES, PRIORITY)

    def get_packages(self):
        return ["b43-firmware"]

    def post_install(self, dest_dir):
        path = os.path.join(dest_dir, "etc/modprobe.d/blacklist-broadcom.conf")
        with open(path, "w") as blacklist:
            blacklist.write("blacklist b43_legacy\n")
            blacklist.write("blacklist wl\n")
