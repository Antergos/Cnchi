#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  catalyst-legacy.py
#
#  Copyright © 2013-2015 Antergos
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

CLASS_NAME = "Catalyst_legacy"
CLASS_ID = "0x0300"
VENDOR_ID = "0x1002"
PRIORITY = 0

"""
Since Catalyst 12.4, AMD has separated its development for Radeon HD 2xxx,
3xxx and 4xxx cards into the legacy Catalyst driver. For Radeon HD 5xxx and
newer, there is the regular Catalyst driver. Regardless of the driver you need,
you will also need the Catalyst utilities.
"""

DEVICES=[
    "0x9640", "0x9641", "0x9642", "0x9643", "0x9644", "0x9645", "0x9647",
    "0x9648", "0x9649", "0x964A", "0x964B", "0x964C", "0x964E", "0x964F",
    "0x9903", "0x9904", "0x990F", "0x9905", "0x9906", "0x9907", "0x9908",
    "0x9909", "0x9992", "0x9993", "0x9994", "0x990A", "0x9900", "0x9901",
    "0x9990", "0x9991", "0x9803", "0x9804", "0x9805", "0x9802", "0x9808",
    "0x9809", "0x9806", "0x9807", "0x9610", "0x9611", "0x9612", "0x9613",
    "0x9614", "0x9615", "0x9616", "0x9710", "0x9711", "0x9712", "0x9713",
    "0x9714", "0x9715", "0x68F8", "0x68F9", "0x68FE", "0x68FA", "0x689B",
    "0x689E", "0x6898", "0x6899", "0x689C", "0x689D", "0x68B8", "0x68B9",
    "0x68BE", "0x68BA", "0x68BF", "0x68DA", "0x68D8", "0x68D9", "0x68DE",
    "0x6738", "0x6739", "0x673E", "0x6778", "0x677B", "0x6772", "0x6779",
    "0x6770", "0x671F", "0x6718", "0x6719", "0x671C", "0x671D", "0x675F",
    "0x6751", "0x675B", "0x675D", "0x6758", "0x6759", "0x6750", "0x9400",
    "0x9401", "0x9402", "0x9403", "0x9405", "0x950F", "0x9513", "0x9451",
    "0x9441", "0x9443", "0x94C0", "0x94C7", "0x94C4", "0x94C5", "0x94C1",
    "0x94C3", "0x94CC", "0x94C6", "0x95C0", "0x95C5", "0x95C7", "0x95C9",
    "0x95C6", "0x958E", "0x958A", "0x9586", "0x9587", "0x9580", "0x9588",
    "0x9589", "0x9590", "0x9598", "0x9599", "0x9596", "0x9597", "0x9500",
    "0x9515", "0x9505", "0x9501", "0x9507", "0x9519", "0x9517", "0x9540",
    "0x9541", "0x9542", "0x954E", "0x954F", "0x9487", "0x948F", "0x9498",
    "0x9490", "0x9495", "0x94B5", "0x94B3", "0x94B1", "0x94B4", "0x944C",
    "0x9450", "0x9452", "0x9442", "0x9440", "0x944E", "0x9460", "0x9462",
    "0x6838", "0x6839", "0x683B", "0x683D", "0x683F", "0x6858", "0x6859",
    "0x6849", "0x6850", "0x6818", "0x6819", "0x6798", "0x679A", "0x6799",
    "0x679E", "0x68A0", "0x68B0", "0x68B1", "0x68A1", "0x68A8", "0x6890",
    "0x68C0", "0x68C1", "0x68D0", "0x68D1", "0x68C7", "0x68E0", "0x68E1",
    "0x68F0", "0x68F1", "0x68E4", "0x68E5", "0x94CB", "0x94C9", "0x94C8",
    "0x9581", "0x9583", "0x958B", "0x95C4", "0x95C2", "0x9591", "0x9593",
    "0x9506", "0x9508", "0x9504", "0x9509", "0x9553", "0x9552", "0x955F",
    "0x9555", "0x9491", "0x9480", "0x9488", "0x948A", "0x94A0", "0x94A1",
    "0x945A", "0x945B", "0x945E", "0x944A", "0x944B", "0x6720", "0x6721",
    "0x6724", "0x6725", "0x6764", "0x6765", "0x6763", "0x6761", "0x6760",
    "0x6744", "0x6745", "0x6742", "0x6743", "0x6741", "0x6740", "0x6820",
    "0x6821", "0x6824", "0x6825", "0x6830", "0x6827", "0x682D", "0x682F",
    "0x6831", "0x6823", "0x6826", "0x6843", "0x6840", "0x6841", "0x6842",
    "0x6800", "0x6801", "0x68F1", "0x68E8", "0x68E9", "0x6888", "0x6889",
    "0x688A", "0x688D", "0x688C", "0x68A9", "0x6880", "0x68C8", "0x68C9",
    "0x958F", "0x9595", "0x959B", "0x9557", "0x9489", "0x94A3", "0x947A",
    "0x947B", "0x946A", "0x946B", "0x6728", "0x6729", "0x6722", "0x6723",
    "0x6726", "0x6727", "0x6766", "0x6767", "0x6768", "0x6762", "0x6700",
    "0x6701", "0x6702", "0x6703", "0x6704", "0x6705", "0x6706", "0x6707",
    "0x6708", "0x6709", "0x674A", "0x6746", "0x6747", "0x6748", "0x6749",
    "0x940F", "0x940B", "0x940A", "0x944F", "0x9447", "0x95CC", "0x958C",
    "0x958D", "0x9511", "0x949C", "0x949F", "0x949E", "0x9444", "0x9456",
    "0x9446", "0x6828", "0x6808", "0x684C", "0x6809", "0x6780", "0x6784",
    "0x6788", "0x678A", "0x68F2", "0x95CD", "0x95CE", "0x95CF"]


class Catalyst_legacy(Hardware):
    def __init__(self):
        Hardware.__init__(self, CLASS_NAME, CLASS_ID, VENDOR_ID, DEVICES, PRIORITY)

    def get_packages(self):
        pkgs = [
            "catalyst-hook",
            "catalyst-libgl",
            "catalyst-utils",
            "acpid",
            "qt4"]
        if os.uname()[-1] == "x86_64":
            pkgs.extend([
                "lib32-catalyst-libgl",
                "lib32-catalyst-utils",
                "lib32-opencl-catalyst"])
        return pkgs

    def add_repositories(self, path):
        """ Adds [xorg116] and [catalyst-hd234k] repos to pacman.conf """
        with open(path, 'r') as pacman_conf:
            lines = pacman_conf.readlines()
        with open(path, "w") as pacman_conf:
            for line in lines:
                # xorg11x needs to be present before core repository
                if "[core]" in line:
                    line = "[xorg116]\n"
                    line += "Server = http://catalyst.wirephire.com/repo/xorg116/$arch\n"
                    line += "SigLevel = Optional TrustAll\n"
                    line += "## Mirrors, if the primary server does not work or is too slow:\n"
                    line += "#Server = http://mirror.rts-informatique.fr/archlinux-catalyst/repo/xorg116/$arch\n"
                    line += "#Server = http://mirror.hactar.bz/Vi0L0/xorg116/$arch\n\n"
                    line += "[catalyst-hd234k]\n"
                    line += "http://catalyst.wirephire.com/repo/catalyst-hd234k/$arch\n"
                    line += "SigLevel = Optional TrustAll\n"
                    line += "## Mirrors, if the primary server does not work or is too slow:\n"
                    line += "#Server = http://70.239.162.206/catalyst-mirror/repo/catalyst-hd234k/$arch\n"
                    line += "#Server = http://mirror.rts-informatique.fr/archlinux-catalyst/repo/catalyst-hd234k/$arch\n"
                    line += "#Server = http://mirror.hactar.bz/Vi0L0/catalyst-hd234k/$arch\n\n"
                    line += "[core]\n"
                pacman_conf.write(line)

    def pre_install(self, dest_dir):
        # Catalyst needs an extra repository and a downgraded Xorg
        # Cnchi uses /tmp/pacman.conf to do the installation
        self.add_repositories("/tmp/pacman.conf")

    def post_install(self, dest_dir):
        # Add repos to user's pacman.conf
        path = os.path.join(dest_dir, "etc/pacman.conf")
        self.add_repositories(path)

        super().chroot(["systemctl", "enable", "atieventsd"])
        super().chroot(["systemctl", "enable", "catalyst-hook"])
        super().chroot(["systemctl", "enable", "temp-links-catalyst"])

        super().chroot(["aticonfig", "--initial"], dest_dir)

    def is_proprietary(self):
        return True
