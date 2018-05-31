#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  amdgpu.py
#
#  Copyright © 2013-2018 Antergos
#
#  This file is part of Cnchi.
#  Based on code by Wayne Hartmann
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


""" AMD/ATI proprietary driver installation """

try:
    from hardware.hardware import Hardware
except ImportError:
    from hardware import Hardware

import os

CLASS_NAME = "AMDGpu"
CLASS_ID = "0x03"
VENDOR_ID = "0x1002"

# Give this driver more priority so it is chosen instead of the catalyst and radeon ones
PRIORITY = 3

ENABLED = False
PCI_FILE = "amdgpu.ids"

class AMDGpu(Hardware):
    """ AMD ATI Catalyst graphics driver """

    def __init__(self):
        Hardware.__init__(self, CLASS_NAME, CLASS_ID, VENDOR_ID, PCI_FILE, ENABLED, PRIORITY)

    @staticmethod
    def get_packages():
        """ Get all required packages """
        pkgs = ["xf86-video-amdgpu", "vulkan-radeon", "libva-mesa-driver"]
        if os.uname()[-1] == "x86_64":
            pkgs.extend(["lib32-mesa", "lib32-libva-mesa-driver"])
        return pkgs

    def pre_install(self, dest_dir):
        """ Pre install commands """
        pass

    def post_install(self, dest_dir):
        """ Post install commands """
        pass

    @staticmethod
    def is_proprietary():
        """ Returns True if the driver is a proprietary one """
        return False
