#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  catalyst.py
#
#  Copyright © 2013-2018 Antergos
#
#  This file is part of Cnchi.
#  Based on code by Wayne Hartmann
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


""" AMD/ATI proprietary driver installation """

try:
    from hardware.hardware import Hardware
except ImportError:
    from hardware import Hardware

import os

CLASS_NAME = "Catalyst"
CLASS_ID = "0x03"
VENDOR_ID = "0x1002"

# Give this driver more priority so it is chosen instead of catalyst-legacy
PRIORITY = 1

PCI_FILE = "catalyst.ids"

class Catalyst(Hardware):
    """ AMD ATI Catalyst graphics driver """

    # Cnchi uses /tmp/pacman.conf to do the installation
    TMP_PACMAN_CONF = "/tmp/pacman.conf"

    def __init__(self):
        Hardware.__init__(self, CLASS_NAME, CLASS_ID, VENDOR_ID, PCI_FILE, PRIORITY)

    @staticmethod
    def get_packages():
        """ Get all required packages """
        pkgs = ["catalyst-hook", "catalyst-libgl",
                "catalyst-utils", "acpid", "qt4"]
        if os.uname()[-1] == "x86_64":
            pkgs.extend(["lib32-catalyst-libgl",
                         "lib32-catalyst-utils", "lib32-opencl-catalyst"])
        return pkgs

    @staticmethod
    def add_repositories(path):
        """ Adds [xorg116] and [catalyst] repos to pacman.conf """
        txt = (
            "[xorg116]\n"
            "Server = http://catalyst.wirephire.com/repo/xorg116/$arch\n"
            "SigLevel = Optional TrustAll\n"
            "## Mirrors, if the primary server does not work or is too slow:\n"
            "#Server = http://mirror.rts-informatique.fr/archlinux-catalyst/repo/xorg116/$arch\n"
            "#Server = http://mirror.hactar.bz/Vi0L0/xorg116/$arch\n\n"
            "[catalyst]\n"
            "Server = http://catalyst.wirephire.com/repo/catalyst/$arch\n"
            "SigLevel = Optional TrustAll\n"
            "## Mirrors, if the primary server does not work or is too slow:\n"
            "#Server = http://70.239.162.206/catalyst-mirror/repo/catalyst/$arch\n"
            "#Server = http://mirror.rts-informatique.fr/archlinux-catalyst/repo/catalyst/$arch\n"
            "#Server = http://mirror.hactar.bz/Vi0L0/catalyst/$arch\n\n")

        with open(path, 'r') as pacman_conf:
            lines = pacman_conf.readlines()
        with open(path, "w") as pacman_conf:
            for line in lines:
                # xorg11x needs to be present before core repository
                if "[core]" in line:
                    line = txt + "[core]\n"
                pacman_conf.write(line)

    def pre_install(self, dest_dir):
        """ Pre install commands """
        # Catalyst needs an extra repository and a downgraded Xorg

        self.add_repositories(Catalyst.TMP_PACMAN_CONF)

    def post_install(self, dest_dir):
        """ Post install commands """
        # Add repos to user's pacman.conf
        path = os.path.join(dest_dir, "etc/pacman.conf")
        self.add_repositories(path)

        Hardware.chroot(["systemctl", "enable", "atieventsd"])
        Hardware.chroot(["systemctl", "enable", "catalyst-hook"])
        Hardware.chroot(["systemctl", "enable", "temp-links-catalyst"])

        Hardware.chroot(["aticonfig", "--initial"], dest_dir)

    @staticmethod
    def is_proprietary():
        """ Returns True if the driver is a proprietary one """
        return True
