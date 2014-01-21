#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  catalyst.py
#
#  Copyright 2013 Antergos
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

"""  driver installation """

from hardware.hardware import Hardware, chroot
import os

# TODO: Add all catalyst (amd/ati) supported cards ¿?
# TODO: User should be able to choose between radeon and catalyst
# TODO : One should disable kernel mode setting for this driver
# TODO: Packages are from AUR. They should be added to Antergos repo, shouldn't they?

# From https://wiki.archlinux.org/index.php/AMD_Catalyst :
# Owners of ATI/AMD video cards have a choice between AMD's proprietary driver (catalyst)
# and the open source driver (xf86-video-ati). This article covers the proprietary driver.
# AMD's Linux driver package catalyst was previously named fglrx (FireGL and Radeon X).
# Only the package name has changed, while the kernel module retains its original fglrx.ko filename.
# Therefore, any mention of fglrx below is specifically in reference to the kernel module, not the package.
# Catalyst packages are no longer offered in the official repositories.
# In the past, Catalyst has been dropped from official Arch support because of dissatisfaction with the quality
# and speed of development. After a brief return they were dropped again in April 2013 and they have not returned since.
# Compared to the open source driver, Catalyst performs worse in 2D graphics, but has a better support for 3D rendering
# and power management. Supported devices are ATI/AMD Radeon video cards with chipset R600 and newer
# (Radeon HD 2xxx and newer). See the Xorg decoder ring or this table, to translate model names (X1900, HD4850)
# to/from chip names (R580, RV770 respectively) (http://en.wikipedia.org/wiki/Comparison_of_AMD_graphics_processing_units)

DEVICES = [
('0x1002','0x3154'),
('0x1002', '0x4c66'),
('0x1002', '0x5460'),
('0x1002', '0x68f9')]

CLASS_NAME = "Catalyst"

class Catalyst(Hardware):
    def __init__(self):
        self.ARCH = os.uname()[-1]

    def get_packages(self):
        pkgs = [ "base-devel", "linux-headers", "catalyst", "catalyst-utils", "catalyst-total", "catalyst-hook" ]
        if self.ARCH == "x86_64":
            pkgs.extend(["lib32-catalyst-utils"])
        return pkgs

    def post_install(self, dest_dir):
        path = "%s/etc/modprobe.d/radeon.conf" % (dest_dir, self.KMS)
        with open(path, 'w') as modprobe:
            modprobe.write("blacklist radeon")
        path = "%s/etc/modules-load/fglrx.conf" % (dest_dir, self.KMS)
        with open(path, 'w') as modprobe:
            modprobe.write("# Load Catalyst (fglrx) driver")
            modprobe.write("fglrx")
        
        chroot(["systemctl", "enable", "catalyst-hook"])

    def check_device(self, device):
        """ Device is (VendorID, ProductID) """
        if device in DEVICES:
            return True
        return False
