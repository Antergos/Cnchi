#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  i915.py
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


""" Intel driver installation """

try:
    from hardware.hardware import Hardware
except ImportError:
    from hardware import Hardware

import os

CLASS_NAME = "Intel915"
CLASS_ID = "0x03"
VENDOR_ID = "0x8086"
DEVICES = []


class Intel915(Hardware):
    """ Intel i915 graphics driver """
    def __init__(self):
        Hardware.__init__(self, CLASS_NAME, CLASS_ID, VENDOR_ID, DEVICES)

    @staticmethod
    def get_packages():
        """ Get all required packages """
        pkgs = ["xf86-video-intel", "libva-intel-driver", "libtxc_dxtn"]
        if os.uname()[-1] == "x86_64":
            pkgs.extend(["lib32-mesa"])
        return pkgs

    @staticmethod
    def post_install(dest_dir):
        """ Post install commands """
        path = os.path.join(dest_dir, "etc/modprobe.d/i915.conf")
        with open(path, 'w') as modprobe:
            modprobe.write("options i915 modeset=1\n")

    @staticmethod
    def is_proprietary():
        """ Returns True if the driver is a proprietary one """
        return False
