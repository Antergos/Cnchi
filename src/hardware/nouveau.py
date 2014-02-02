#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  nouveau.py
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

""" Nouveau (Nvidia) driver installation """

from hardware.hardware import Hardware
import os
import logging

from hardware.nvidia_db import DEVICES

CLASS_NAME = "Nouveau"

class Nouveau(Hardware):
    def __init__(self):
        self.KMS = "nouveau"
        self.KMS_OPTIONS = "modeset=1"
        self.DRI = "nouveau-dri"
        self.DDX = "xf86-video-nouveau"
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

    def check_device(self, device):
        """ Device is (VendorID, ProductID)
            DEVICES is (VendorID, ProductID, Description) """
        #for (vendor, product, description) in DEVICES:
        #    if device == (vendor, product):
        #        print(description)
        #        return True
        #return False
        
        (vendor, product) = device
        if vendor == "0x10de":
            # Check that this is really a graphics card
            (d_vendor, d_model) = super().get_graphics_card(self)
            if vendor == d_vendor:
                logging.debug(_("Found device: %s") % d_model)
                return True
        return False
