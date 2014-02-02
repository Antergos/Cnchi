#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  firewire.py
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

""" Firewire driver installation """

from hardware.hardware import Hardware
import logging

DEVICES = [('0x1180','0x0832', "Firewire")]

CLASS_NAME = "Firewire"
CLASS_ID = ""

class Firewire(Hardware):
    def __init__(self):
        pass

    def get_packages(self):
        return ["libffado", "libraw1394"]

    def post_install(self, dest_dir):
        pass

    def check_device(self, class_id, vendor_id, product_id):
        """ Checks if the driver supports this device """
        for (vendor, product, description) in DEVICES:
            if (vendor_id, product_id) == (vendor, product):
                logging.debug(_("Found device: %s") % description)
                return True
        return False
