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

""" AMD Catalyst driver installation """

from hardware.hardware import Hardware
import os
import logging

from hardware.amd_ati_db import DEVICES

CLASS_NAME = "Catalyst"
CLASS_ID = "0x0300"

class Catalyst(Hardware):
    def __init__(self):
        self.ARCH = os.uname()[-1]

    def get_packages(self):
        pkgs = ["base-devel", "linux-headers", "catalyst", "catalyst-utils", "catalyst-total", "catalyst-hook"]
        if self.ARCH == "x86_64":
            pkgs.extend(["lib32-catalyst-utils"])
        return pkgs

    def post_install(self, dest_dir):
        path = "%s/etc/modprobe.d/radeon-blacklist.conf" % (dest_dir, self.KMS)
        with open(path, 'w') as modprobe:
            modprobe.write("blacklist radeon")
        path = "%s/etc/modules-load/fglrx.conf" % (dest_dir, self.KMS)
        with open(path, 'w') as modprobe:
            modprobe.write("# Load Catalyst (fglrx) driver")
            modprobe.write("fglrx")
        
        super().chroot(self, ["systemctl", "enable", "catalyst-hook"])

    def check_device(self, class_id, vendor_id, product_id):
        """ Checks if the driver supports this device """
        for (vendor, product, description) in DEVICES:
            if (vendor_id, product_id) == (vendor, product):
                logging.debug(_("Found device: %s") % description)
                #return True
                return False
        return False
