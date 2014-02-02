#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  radeon.py
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

""" AMD/ATI driver installation """

from hardware.hardware import Hardware
import os
import logging

from hardware.amd_ati_db import DEVICES

CLASS_NAME = "Radeon"
CLASS_ID = "0x0300"

class Radeon(Hardware):
    def __init__(self):
        self.KMS = "radeon"
        self.KMS_OPTIONS = "modeset=1"
        self.DRI = "ati-dri"
        self.DDX = "xf86-video-ati"
        self.DECODER = "libva-vdpau-driver"
        self.ARCH = os.uname()[-1]

    def get_packages(self):
        pkgs = [self.DRI, self.DDX, self.DECODER, "libtxc_dxtn"]
        if self.ARCH == "x86_64":
            pkgs.extend(["lib32-%s" % self.DRI, "lib32-mesa-libgl"])
        return pkgs

    def post_install(self, dest_dir):
        path = "%s/etc/modprobe.d/%s.conf" % (dest_dir, self.KMS)
        with open(path, 'w') as modprobe:
            modprobe.write("options %s %s\n" % (self.KMS, self.KMS_OPTIONS))

    def check_device(self, class_id, vendor_id, product_id):
        """ Checks if the driver supports this device """
        for (vendor, product, description) in DEVICES:
            if (vendor_id, product_id) == (vendor, product):
                logging.debug(_("Found device: %s") % description)
                return True
        return False
