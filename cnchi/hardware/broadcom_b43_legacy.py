#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Broadcom_b43_legacy.py
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

""" Broadcom b43legacy driver installation """

import os

try:
    from hardware.hardware import Hardware
except ImportError:
    from hardware import Hardware

CLASS_NAME = "BroadcomB43Legacy"
CLASS_ID = "0x0200"
VENDOR_ID = "0x14e4"
DEVICES = ['0x4301', '0x4306', '0x4320', '0x4324', '0x4325']


class BroadcomB43Legacy(Hardware):
    def __init__(self):
        Hardware.__init__(self, CLASS_NAME, CLASS_ID, VENDOR_ID, DEVICES)

    def get_packages(self):
        return ["b43-firmware-legacy"]

    def post_install(self, dest_dir):
        path = os.path.join(dest_dir, "etc/modprobe.d/blacklist-broadcom.conf")
        with open(path, "w") as blacklist:
            blacklist.write("blacklist b43\n")
            blacklist.write("blacklist wl\n")
