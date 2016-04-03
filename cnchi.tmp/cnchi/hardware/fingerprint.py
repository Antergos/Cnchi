#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  fingerprint.py
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


""" Various Fingerprint devices driver installation """

# Support for consumer fingerprint reader devices.

try:
    from hardware.hardware import Hardware
except ImportError:
    from hardware import Hardware

CLASS_NAME = "FingerPrint"
CLASS_ID = ""

# This driver works for different vendors
VENDOR_ID = ""

# Special case: (Vendor, Device)
DEVICES = [
    ('0x045e', '0x00bb'),
    ('0x045e', '0x00bc'),
    ('0x045e', '0x00bd'),
    ('0x045e', '0x00ca'),
    ('0x0483', '0x2015'),
    ('0x0483', '0x2016'),
    ('0x05ba', '0x000a'),
    ('0x05ba', '0x0007'),
    ('0x05ba', '0x0008'),
    ('0x061a', '0x0110'),
    ('0x08ff', '0x1600'),
    ('0x08ff', '0x2550'),
    ('0x08ff', '0x2580'),
    ('0x08ff', '0x5501'),
    ('0x147e', '0x2016')]


class FingerPrint(Hardware):
    """ Fingerprint devices driver """
    def __init__(self):
        Hardware.__init__(self, CLASS_NAME, CLASS_ID, VENDOR_ID, DEVICES)

    @staticmethod
    def get_packages():
        """ Get all required packages """
        return ["fprintd"]

    def post_install(self, dest_dir):
        """ Post install commands """
        pass
