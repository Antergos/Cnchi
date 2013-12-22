#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  via.py
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

""" VIA (openchrome) driver installation """

from hardware import Hardware
import os

CLASS_NAME = "Via"

DEVICES = [
('0x1106', '0x3122'),
('0x1106', '0x7205'),
('0x1106', '0x3118'),
('0x1106', '0x3230'),
('0x1106', '0x0505'),
('0x1106', '0x0581'),
('0x1106', '0x3205'),
('0x1106', '0x3343'),
('0x1106', '0x3344'),
('0x1106', '0x0581')]

class Via(Hardware):
    def __init__(self):
        pass

    def get_packages(self):
        return [ "xf86-video-openchrome" ]

    def post_install(self, dest_dir):
        path = "%s/etc/X11/xorg.conf.d/10-via.conf" % dest_dir
        with open(path, 'w') as video:
            video.write('Section "Device"\n')
            video.write('\tIdentifier     "Device0"\n')
            video.write('\tDriver         "openchrome"\n')
            #video.write('\tOption         "EnableAGPDMA" "false"\n')
            #video.write('\tOption         "XaaNoImageWriteRect"\n')
            video.write('\tVendorName     "VIA"\n')
            video.write('EndSection\n')

    def check_device(self, device):
        """ Device is (VendorID, ProductID) """
        if device in DEVICES:
            return True
        return False
