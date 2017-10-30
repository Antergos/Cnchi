#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  virtualbox.py
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


""" Virtualbox driver installation """

try:
    from hardware.hardware import Hardware
except ImportError:
    from hardware import Hardware

import os

CLASS_NAME = "Virtualbox"
CLASS_ID = "0x03"
VENDOR_ID = "0x80ee"
DEVICES = ['0xbeef']


class Virtualbox(Hardware):
    """ Virtualbox modules """

    def __init__(self):
        Hardware.__init__(self, CLASS_NAME, CLASS_ID, VENDOR_ID, DEVICES)

    @staticmethod
    def get_packages():
        """ Get all required packages """
        # return ["virtualbox-guest-modules", "virtualbox-guest-utils"]
        return ["linux-headers", "virtualbox-guest-dkms", "virtualbox-guest-utils"]

    @staticmethod
    def post_install(dest_dir):
        """ Post install commands """
        path = os.path.join(dest_dir, "etc/modules-load.d")
        os.makedirs(path, mode=0o755, exist_ok=True)
        path = os.path.join(
            dest_dir, "etc/modules-load.d/virtualbox-guest.conf")
        with open(path, 'w') as modules:
            modules.write(
                '# Virtualbox modules added by Cnchi - Antergos Installer\n')
            modules.write("vboxguest\n")
            modules.write("vboxsf\n")
            modules.write("vboxvideo\n")

        Hardware.chroot(["systemctl", "disable", "openntpd"], dest_dir)
        Hardware.chroot(["systemctl", "-f", "enable", "vboxservice"], dest_dir)

        # This fixes bug in virtualbox-guest-modules package
        Hardware.chroot(["depmod", "-a"], dest_dir)
