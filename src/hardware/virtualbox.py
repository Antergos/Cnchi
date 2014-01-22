#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  virtualbox.py
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

from hardware.hardware import Hardware
import os
import logging

DEVICES = [('0x80ee', '0xbeef', "InnoTek Systemberatung GmbH VirtualBox Graphics Adapter")]

CLASS_NAME = "Virtualbox"

class Virtualbox(Hardware):
    def __init__(self):
        pass

    def get_packages(self):
        return [ "virtualbox-guest-modules", "virtualbox-guest-utils" ]

    def post_install(self, dest_dir):
        path = os.path.join(dest_dir, "etc/modules-load.d")
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(dest_dir, "etc/modules-load.d/virtualbox-guest.conf")
        with open(path, 'w') as modules:
            modules.write('# Virtualbox modules added by Cnchi - Antergos Installer\n')
            modules.write("vboxguest\n")
            modules.write("vboxsf\n")
            modules.write("vboxvideo\n")
        super().chroot(self, ["systemctl", "disable", "openntpd"], dest_dir)
        super().chroot(self, ["systemctl", "enable", "vboxservice"], dest_dir)

    def check_device(self, device):
        """ Device is (VendorID, ProductID) """
        if device in DEVICES:
            return True
        return False

    def check_device(self, device):
        """ Device is (VendorID, ProductID)
            DEVICES is (VendorID, ProductID, Description) """
        for (vendor, product, description) in DEVICES:
            if device == (vendor, product):
                logging.debug(_("Found device: %s") % description)
                return True
        return False
        
