#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  nvidia.py
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

""" Nvidia driver installation """

from hardware.hardware import Hardware
import os
import logging

from hardware.nvidia_db import DEVICES

CLASS_NAME = "NVidia"
CLASS_ID = "0x0300"

class NVidia(Hardware):
    def __init__(self):
        pass

    def get_packages(self):
        pkgs = ["nvidia", "libva-vdpau-driver"]
        if os.uname()[-1] == "x86_64":
            pkgs.append("lib32-nvidia-libgl")
        return pkgs

    def post_install(self, dest_dir):
        path = "%s/etc/X11/xorg.conf.d/10-nvidia.conf" % dest_dir
        with open(path, 'w') as video:
            video.write('Section "Device"\n')
            video.write('\tIdentifier     "Device0"\n')
            video.write('\tDriver         "nvidia"\n')
            video.write('\tOption         "NoLogo"\n')
            video.write('\tOption         "RegistryDwords"      "EnableBrightnessControl=1"\n')
            video.write('\tVendorName     "NVIDIA Corporation"\n')
            video.write('EndSection\n')

        path = "%s/etc/modprobe.d/blacklist-nouveau.conf" % dest_dir
        with open(path, 'w') as blacklist:
            blacklist.write("blacklist nouveau\n")

        path = "%s/etc/modprobe.d/nvidia.conf" % dest_dir
        with open(path, 'w') as modprobe:
            modprobe.write("options nvidia NVreg_EnableMSI=1\n")

    def check_device(self, class_id, vendor_id, product_id):
        """ Checks if the driver supports this device """
        for (vendor, product, description) in DEVICES:
            if (vendor_id, product_id) == (vendor, product):
                #logging.debug(_("Found device: %s") % description)
                #return True
                return False
        return False
