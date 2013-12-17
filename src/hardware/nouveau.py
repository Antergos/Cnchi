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

""" Nouveau driver installation """

import os
from hardware import Hardware

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
        pkgs = [ self.DRI, self.DDX, self.DECODER, "libtxc_dxtn" ]
        if self.ARCH == "x86_64":
            pkgs.expand([ "lib32-%s" % self.DRI, "lib32-mesa-libgl" ])
    
    def postinstall(self):
        path = os.path.join("/etc/modprobe.d", self.KMS, ".conf")
        with open(path, 'w') as modprobe:
            modprobe.write("options %s %s\n" % (self.KMS, self.KMS_OPTIONS))
