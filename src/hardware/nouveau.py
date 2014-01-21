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

from hardware.hardware import Hardware
import os

CLASS_NAME = "Nouveau"

# Supported cards http://nouveau.freedesktop.org/wiki/CodeNames/
# NV04	Riva TNT, TNT2	Fahrenheit
# NV10	GeForce 256, GeForce 2, GeForce 4 MX	Celsius
# NV20	GeForce 3, GeForce 4 Ti	Kelvin
# NV30	GeForce 5 / GeForce FX	Rankine
# NV40	GeForce 6, GeForce 7	Curie
# NV50	GeForce 8, GeForce 9, GeForce 100, GeForce 200, GeForce 300	Tesla
# NVC0	GeForce 400, GeForce 500	Fermi
# NVE0	GeForce 600, GeForce 700, GeForce GTX Titan	Kepler


# TODO: Add all nouveau supported cards

DEVICES = [
('0x10DE', '0x0020'), # Riva TNT
('0x10DE', '0x002D'), # Riva TNT2
('0x10DE', '0x0029'), # Riva TNT2 Ultra
('0x10DE', '0x002B'), # Riva TNT2
('0x10DE', '0x00A0'), # Aladdin TNT2
('0x10DE', '0x0101'), # GeForce DDR
('0x10DE', '0x0103'), # Quadro
('0x10DE', '0x0110'), # GeForce2 MX
('0x10DE', '0x0111'), # GeForce2 MMX
('0x10DE', '0x0112'), # GeForce2 Go
('0x10DE', '0x0113'), # Quadro 2
('0x10DE', '0x9876'), # GeForce2 MX
('0x10DE', '0x0150'), # GeForce2 GTS
('0x10DE', '0x0151'), # GeForce2 Ti
('0x10DE', '0x0152'), # GeForce2 Ultra
('0x10DE', '0x0153') # Quadro2 Pro
]

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
            pkgs.extend([ "lib32-%s" % self.DRI, "lib32-mesa-libgl" ])
        return pkgs

    def post_install(self, dest_dir):
        path = "%s/etc/modprobe.d/%s.conf" % (dest_dir, self.KMS)
        with open(path, 'w') as modprobe:
            modprobe.write("options %s %s\n" % (self.KMS, self.KMS_OPTIONS))

    def check_device(self, device):
        """ Device is (VendorID, ProductID) """
        if device in DEVICES:
            return True
        return False
            
