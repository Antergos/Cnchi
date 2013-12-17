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

"""  driver installation """

from hardware import Hardware

# 10de:040c
# 10de:040f

class XXXXX(Hardware):
    def __init__(self):
        pass
        
    def get_packages(self):
        pass    
    def postinstall(self):
        pass

    def check_device(self, device):
        """ Device is (VendorID, ProductID) """
        pass

UNAME_M=`uname -m`

# Uninstall nouveau
rm /etc/modprobe.d/nouveau.conf
pacman -Rdds --noconfirm nouveau-dri xf86-video-nouveau libtxc_dxtn
pacman -Rdds --noconfirm mesa-libgl
if [ "${UNAME_M}" == "x86_64" ]; then
    pacman -Rdds --noconfirm lib32-nouveau-dri lib32-mesa-libgl
fi

# Install nvidia
echo -en "\ny\n" | pacman -S --needed --noconfirm nvidia libva-vdpau-driver
if [ "${UNAME_M}" == "x86_64" ]; then
    pacman -S --noconfirm --needed lib32-nvidia-libgl
fi

if [ -f /etc/X11/xorg.conf ]; then
    mv /etc/X11/xorg.conf /etc/X11/xorg.conf.`date +%y%m%d-%H%M`
fi

cat << XORG > /etc/X11/xorg.conf
Section "Device"
   Identifier     "Device0"
   Driver         "nvidia"
   Option         "NoLogo"
   Option         "RegistryDwords"      "EnableBrightnessControl=1"
   VendorName     "NVIDIA Corporation"
EndSection
XORG

echo "blacklist nouveau" > /etc/modprobe.d/blacklist-nouveau.conf
echo "options nvidia NVreg_EnableMSI=1" > /etc/modprobe.d/nvidia.conf
