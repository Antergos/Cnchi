#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  i915.py
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

from hardware.hardware import Hardware
import os
import logging

CLASS_NAME = "i915"

# X.org Intel i810/i830/i915/945G/G965+ video drivers
# Source: http://en.wikipedia.org/wiki/Comparison_of_Intel_graphics_processing_units

DEVICES = [
('0x8086', '0x7121', "i815 Whitney"),
('0x8086', '0x7123', "i815 Whitney"),
('0x8086', '0x7125', "i815 Whitney"),
('0x8086', '0x1132', "i815 Solano"),
('0x8086', '0x2572', "i865 Springdale"),
('0x8086', '0x2582', "i910,i915 Grantsdale"),
('0x8086', '0x2782', "i910,i915 Grantsdale"),
('0x8086', '0x2592', "i915 Alviso"),
('0x8086', '0x2792', "i915 Alviso"),
('0x8086', '0x2772', "i945G Lakeport"),
('0x8086', '0x2776', "i945G Lakeport"),
('0x8086', '0x27A2', "Mobile i945 family Calistoga"),
('0x8086', '0x27A6', "Mobile i945 family Calistoga"),
('0x8086', '0x27AE', "Mobile i945 family Calistoga"),
('0x8086', '0x29A2', "G965 Broadwater"),
('0x8086', '0x29A3', "G965 Broadwater"),
('0x8086', '0x29C2', "i945 G33 Bearlake"),
('0x8086', '0x29C3', "i945 G33 Bearlake"),
('0x8086', '0x2E22', "G4x Eaglelake"),
('0x8086', '0x2E22', "G4x Eaglelake"),
('0x8086', '0x0042', "5th Generation Ironlake"),
('0x8086', '0x0046', "5th Generation Ironlake"),
('0x8086', '0x0102', "6th Generation Sandy Bridge"),
('0x8086', '0x0106', "6th Generation Sandy Bridge"),
('0x8086', '0x0112', "6th Generation Sandy Bridge"),
('0x8086', '0x0116', "6th Generation Sandy Bridge"),
('0x8086', '0x0122', "6th Generation Sandy Bridge"),
('0x8086', '0x0126', "6th Generation Sandy Bridge"),
('0x8086', '0x010A', "6th Generation Sandy Bridge")]

class i915(Hardware):
    def __init__(self):
        self.KMS = "i915"
        self.KMS_OPTIONS = "modeset=1"
        self.DRI = "intel-dri"
        self.DDX = "xf86-video-intel"
        self.DECODER = "libva-intel-driver"
        self.ARCH = os.uname()[-1]

    def get_packages(self):
        pkgs = [ self.DRI, self.DDX, self.DECODER, "libtxc_dxtn" ]
        if self.ARCH == "x86_64":
            pkgs.extend([ "lib32-%s" % self.DRI, "lib32-mesa-libgl" ])
        return pkgs

    def post_install(self, dest_dir):
        path = "%s/etc/modprobe.d/%s.conf" % (dest_dir, self.KMS)
        with open(path, 'w') as modprobe:
            modprobe.write("options %s %s\n" % (self.KMS, self.KMS_OPTIONS))

    def check_device(self, device):
        """ Device is (VendorID, ProductID)
            DEVICES is (VendorID, ProductID, Description) """
        for (vendor, product, description) in DEVICES:
            if device == (vendor, product):
                logging.debug(_("Found device: %s") % description)
                return True
        return False
        
