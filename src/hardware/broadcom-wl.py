#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  broadcom-wl.py
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

""" Broadcom-wl driver installation """

from hardware.hardware import Hardware
import logging

# Broadcom's driver for:
# BCM4311-, BCM4312-, BCM4313-, BCM4321-, BCM4322-, BCM43224- and BCM43225-, BCM43227- and BCM43228-based hardware. 

DEVICES = [
('0x14e4', '0x4311', "BCM4311"),
('0x14e4', '0x04B5', "BCM4312"),
('0x14e4', '0x4727', "BCM4313"),
('0x14e4', '0x1361', "BCM4313"),
('0x14e4', '0x4315', "BCM4315"), # (not sure about this one)
('0x14e4', '0x4328', "BCM4321KFBG"),
('0x14e4', '0x432B', "BCM4322")]

CLASS_NAME = "Broadcom_wl"

class Broadcom_wl(Hardware):
    def __init__(self):
        pass

    def get_packages(self):
        return ["broadcom-wl"]

    def post_install(self, dest_dir):
        pass

    def check_device(self, device):
        """ Device is (VendorID, ProductID)
            DEVICES is (VendorID, ProductID, Description) """
        for (vendor, product, description) in DEVICES:
            if device == (vendor, product):
                self.device_found = device
                logging.debug(_("Found device: %s") % description)
                return True
        return False
