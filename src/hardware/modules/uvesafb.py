#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  uvesafb.py
#
#  Copyright © 2013-2017 Antergos
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


""" VESA driver installation """

try:
    from hardware.hardware import Hardware
except ImportError:
    from hardware import Hardware

CLASS_NAME = "VesaFB"
CLASS_ID = "0x03"
VENDOR_ID = ""

# All modern cards support Vesa. This will be used as a fallback.
DEVICES = []

# Give this driver less priority than the others so it is never choosen instead.
PRIORITY = -2


class VesaFB(Hardware):
    """ Vesa (generic) graphics driver """

    def __init__(self):
        Hardware.__init__(self, CLASS_NAME, CLASS_ID,
                          VENDOR_ID, DEVICES, PRIORITY)

    @staticmethod
    def get_packages():
        """ Get all required packages """
        return ["xf86-video-vesa"]

    def post_install(self, dest_dir):
        """ Post install commands """
        pass
