#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  broadcom_wl.py
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

""" Broadcom-wl driver installation """

try:
    from hardware.hardware import Hardware
except ImportError:
    from hardware import Hardware

CLASS_NAME = "BroadcomWl"
CLASS_ID = "0x0200"
VENDOR_ID = "0x14e4"

# Broadcom's driver for:
# BCM4311-, BCM4312-, BCM4313-, BCM4321-, BCM4322-, BCM43224- and BCM43225-,
# BCM43227- and BCM43228-based hardware.

DEVICES = ['0x4311', '0x04B5', '0x4727', '0x1361', '0x4328', '0x432B']

# Give this driver more priority so it is chosen instead of
# broadcom_b43 or Broadcom_b43_legacy
PRIORITY = 2


class BroadcomWl(Hardware):
    def __init__(self):
        Hardware.__init__(self, CLASS_NAME, CLASS_ID, VENDOR_ID, DEVICES, PRIORITY)

    def get_packages(self):
        return ["broadcom-wl"]

    def post_install(self, dest_dir):
        pass

    def is_proprietary(self):
        return True
