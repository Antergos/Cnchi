#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  nvidia.py
#
#  Copyright © 2013-2018 Antergos
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


""" Nvidia (propietary) driver installation """

try:
    from hardware.hardware import Hardware
except ImportError:
    from hardware import Hardware

import os

CLASS_NAME = "Nvidia"
CLASS_ID = "0x03"
VENDOR_ID = "0x10de"

# Give this driver more priority so it is chosen instead of
# nvidia-340xx or nvidia-304xx
PRIORITY = 2

# See https://wiki.archlinux.org/index.php/NVIDIA#Installing
# nvidia, nvidia-340xx, nvidia-304xx
# lib32-nvidia-libgl, lib32-nvidia-340xx-libgl or lib32-nvidia-304xx-libgl

"""
For GeForce 400 series cards and newer [NVCx and newer], install the nvidia or
    nvidia-lts package along with nvidia-libgl, available in the official repositories.
"""

PCI_FILE = "nvidia.ids"

class Nvidia(Hardware):
    """ Nvidia proprietary graphics driver """

    def __init__(self):
        Hardware.__init__(self, CLASS_NAME, CLASS_ID, VENDOR_ID, PCI_FILE, PRIORITY)

    @staticmethod
    def get_packages():
        """ Get all required packages """
        pkgs = ["nvidia", "libvdpau"]
        if os.uname()[-1] == "x86_64":
            pkgs.extend(["lib32-nvidia-utils", "lib32-libvdpau"])
        return pkgs

    @staticmethod
    def get_conflicts():
        """ Get conflicting packages """
        pkgs = ["xf86-video-nouveau"]
        return pkgs

    @staticmethod
    def post_install(dest_dir):
        """ Post install commands """
        pass

    @staticmethod
    def is_proprietary():
        """ Returns True if the driver is a proprietary one """
        return True
