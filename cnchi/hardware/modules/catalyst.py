#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  catalyst.py
#
#  Copyright © 2013-2017 Antergos
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

# Disable this driver
ENABLED = False

"""
Since Catalyst 12.4, AMD has separated its development for Radeon HD 2xxx,
3xxx and 4xxx cards into the legacy Catalyst driver. For Radeon HD 5xxx and
newer, there is the regular Catalyst driver. Regardless of the driver you need,
you will also need the Catalyst utilities.
"""

DEVICES = [
    "0x9850", "0x9851", "0x9852", "0x9853", "0x98b0", "0x98b1", "0x9874",
    "0x9830", "0x9831", "0x9832", "0x9833", "0x9834", "0x9835", "0x9836",
    "0x9837", "0x9838", "0x9839", "0x983a", "0x983b", "0x983c", "0x983d",
    "0x983e", "0x983f", "0x1309", "0x130a", "0x1304", "0x1305", "0x1306",
    "0x1307", "0x130f", "0x1313", "0x1315", "0x131d", "0x1318", "0x130c",
    "0x130d", "0x130e", "0x1310", "0x1311", "0x131c", "0x1316", "0x131b",
    "0x1312", "0x1317", "0x130b", "0x9854", "0x9856", "0x9857", "0x9858",
    "0x9859", "0x985a", "0x985b", "0x985c", "0x985d", "0x985e", "0x985f",
    "0x9855", "0x999c", "0x999d", "0x9999", "0x999a", "0x999b", "0x990b",
    "0x990d", "0x9995", "0x9997", "0x990c", "0x990e", "0x9996", "0x9998",
    "0x990f", "0x9647", "0x9648", "0x9649", "0x964a", "0x964b", "0x964c",
    "0x964e", "0x964f", "0x9640", "0x9641", "0x9642", "0x9643", "0x9644",
    "0x9645", "0x99a4", "0x9919", "0x9918", "0x9917", "0x99a2", "0x99a0",
    "0x9913", "0x9910", "0x9903", "0x9904", "0x9905", "0x9906", "0x9907",
    "0x9908", "0x9909", "0x9992", "0x9993", "0x9994", "0x990a", "0x9900",
    "0x9901", "0x9990", "0x9991", "0x9803", "0x9804", "0x9805", "0x9808",
    "0x9809", "0x9802", "0x9806", "0x9807", "0x980a", "0x6650", "0x6651",
    "0x665c", "0x6658", "0x665d", "0x665f", "0x6610", "0x6613", "0x6611",
    "0x6631", "0x68fa", "0x68f8", "0x68f9", "0x68fe", "0x6898", "0x6899",
    "0x689e", "0x689b", "0x689c", "0x689d", "0x68b8", "0x68b9", "0x68be",
    "0x68ba", "0x68bf", "0x68d8", "0x68d9", "0x68de", "0x68da", "0x6738",
    "0x6739", "0x673e", "0x6778", "0x677b", "0x6772", "0x6771", "0x6779",
    "0x6770", "0x6718", "0x6719", "0x671c", "0x671d", "0x671f", "0x6858",
    "0x6859", "0x6849", "0x6850", "0x675f", "0x6751", "0x675b", "0x675d",
    "0x6758", "0x6759", "0x6750", "0x7300", "0x6835", "0x683d", "0x683f",
    "0x6838", "0x6839", "0x683b", "0x6837", "0x6810", "0x6811", "0x6806",
    "0x6818", "0x6819", "0x679e", "0x6798", "0x679a", "0x6799", "0x6790",
    "0x679b", "0x6792", "0x67b0", "0x67b1", "0x67a0", "0x67b9", "0x67ba",
    "0x67b8", "0x67a1", "0x67a2", "0x67be", "0x6938", "0x6939", "0x6930",
    "0x6604", "0x6647", "0x6646", "0x6605", "0x6600", "0x6601", "0x6602",
    "0x6603", "0x6606", "0x6607", "0x6620", "0x6621", "0x6623", "0x6640",
    "0x6641", "0x6660", "0x6663", "0x6667", "0x666f", "0x6665", "0x6664",
    "0x68a0", "0x68b0", "0x68a1", "0x68a8", "0x68c0", "0x68c1", "0x68c7",
    "0x68e4", "0x68e5", "0x68e0", "0x68e1", "0x6720", "0x6721", "0x6724",
    "0x6725", "0x6764", "0x6765", "0x6761", "0x6760", "0x6763", "0x6741",
    "0x6740", "0x6744", "0x6745", "0x6742", "0x6743", "0x6820", "0x6821",
    "0x6824", "0x6825", "0x6830", "0x6823", "0x6826", "0x6827", "0x682d",
    "0x682f", "0x6831", "0x682b", "0x6822", "0x682a", "0x6843", "0x6840",
    "0x6841", "0x6842", "0x6800", "0x6801", "0x6920", "0x6921", "0x6907",
    "0x6900", "0x6901", "0x6902", "0x6903", "0x6649", "0x6608", "0x68f1",
    "0x68e8", "0x68e9", "0x6888", "0x6889", "0x688d", "0x688c", "0x688a",
    "0x68a9", "0x6880", "0x68c8", "0x68c9", "0x6722", "0x6723", "0x6726",
    "0x6727", "0x6728", "0x6729", "0x6768", "0x6766", "0x6767", "0x6762",
    "0x6700", "0x6701", "0x6702", "0x6703", "0x6704", "0x6705", "0x6706",
    "0x6707", "0x6708", "0x6709", "0x6746", "0x6747", "0x6748", "0x6749",
    "0x674a", "0x6828", "0x682c", "0x6808", "0x684c", "0x6809", "0x6780",
    "0x6784", "0x6788", "0x678a", "0x692f", "0x692b", "0x6929", "0x68f2"]

class Catalyst(Hardware):
    """ AMD ATI Catalyst graphics driver """
    def __init__(self):
        Hardware.__init__(self, CLASS_NAME, CLASS_ID, VENDOR_ID, DEVICES, PRIORITY, ENABLED)

    @staticmethod
    def get_packages():
        """ Get all required packages """
        pkgs = ["catalyst-hook", "catalyst-libgl", "catalyst-utils", "acpid", "qt4"]
        if os.uname()[-1] == "x86_64":
            pkgs.extend(["lib32-catalyst-libgl", "lib32-catalyst-utils", "lib32-opencl-catalyst"])
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
        # Cnchi uses /tmp/pacman.conf to do the installation
        self.add_repositories("/tmp/pacman.conf")

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
