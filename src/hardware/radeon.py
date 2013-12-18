#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  radeon.py
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

"""  driver installation """

from hardware import Hardware

DEVICES = [
('0x1002','0x3154'),
('0x1002', '0x4c66'),
('0x1002', '0x5460'),
('0x1002', '0x68f9')]

CLASS_NAME = "Radeon"

class Radeon(Hardware):
    def __init__(self):
        pass
        
    def get_packages(self):
        return []
    
    def postinstall(self):
        pass

    def check_device(self, device):
        """ Device is (VendorID, ProductID) """
        if device in DEVICES:
            return True
        return False

#UNAME_M=`uname -m`
#KMS="radeon"
#KMS_OPTIONS="modeset=1"
#DRI="ati-dri"
#DDX="xf86-video-ati"
#DECODER="libva-vdpau-driver"
#
#pacman -S --noconfirm --needed ${DRI} ${DDX} ${DECODER} libtxc_dxtn
#if [ "${UNAME_M}" == "x86_64" ]; then
#    pacman -S --noconfirm --needed lib32-${DRI} lib32-mesa-libgl
#fi
#echo "options ${KMS} ${KMS_OPTIONS}" > /etc/modprobe.d/${KMS}.conf
