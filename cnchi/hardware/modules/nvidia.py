#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  nvidia.py
#
#  Copyright © 2013-2016 Antergos
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


""" Nvidia (propietary) driver installation """

try:
    from hardware.hardware import Hardware
except ImportError:
    from hardware import Hardware

import os

CLASS_NAME = "Nvidia"
CLASS_ID = "0x03"
VENDOR_ID = "0x10de"

# Give this driver more priority so it is chosen instead of
# nvidia-340xx or nvidia-304xx
PRIORITY = 2

# See https://wiki.archlinux.org/index.php/NVIDIA#Installing
# nvidia, nvidia-340xx, nvidia-304xx
# lib32-nvidia-libgl, lib32-nvidia-340xx-libgl or lib32-nvidia-304xx-libgl

"""
For GeForce 400 series cards and newer [NVCx and newer], install the nvidia or
    nvidia-lts package along with nvidia-libgl, available in the official repositories.
"""
DEVICES = [
    "0x06c0", "0x06c4", "0x06ca", "0x06cd", "0x06d1", "0x06d2", "0x06d8",
    "0x06d9", "0x06da", "0x06dc", "0x06dd", "0x06de", "0x06df", "0x0dc0",
    "0x0dc4", "0x0dc5", "0x0dc6", "0x0dcd", "0x0dce", "0x0dd1", "0x0dd2",
    "0x0dd3", "0x0dd6", "0x0dd8", "0x0dda", "0x0de0", "0x0de1", "0x0de2",
    "0x0de3", "0x0de4", "0x0de5", "0x0de7", "0x0de8", "0x0de9", "0x0dea",
    "0x0deb", "0x0dec", "0x0ded", "0x0dee", "0x0def", "0x0df0", "0x0df1",
    "0x0df2", "0x0df3", "0x0df4", "0x0df5", "0x0df6", "0x0df7", "0x0df8",
    "0x0df9", "0x0dfa", "0x0dfc", "0x0e22", "0x0e23", "0x0e24", "0x0e30",
    "0x0e31", "0x0e3a", "0x0e3b", "0x0f00", "0x0f01", "0x0f02", "0x0fc0",
    "0x0fc1", "0x0fc2", "0x0fc6", "0x0fc8", "0x0fc9", "0x0fcd", "0x0fce",
    "0x0fd1", "0x0fd2", "0x0fd3", "0x0fd4", "0x0fd5", "0x0fd8", "0x0fd9",
    "0x0fdf", "0x0fe0", "0x0fe1", "0x0fe2", "0x0fe3", "0x0fe4", "0x0fe9",
    "0x0fea", "0x0fec", "0x0fef", "0x0ff2", "0x0ff3", "0x0ff6", "0x0ff8",
    "0x0ff9", "0x0ffa", "0x0ffb", "0x0ffc", "0x0ffd", "0x0ffe", "0x0fff",
    "0x1001", "0x1004", "0x1005", "0x1007", "0x1008", "0x100a", "0x100c",
    "0x1021", "0x1022", "0x1023", "0x1024", "0x1026", "0x1027", "0x1028",
    "0x1029", "0x103a", "0x103c", "0x1040", "0x1042", "0x1048", "0x1049",
    "0x104a", "0x104b", "0x104c", "0x1050", "0x1051", "0x1052", "0x1054",
    "0x1055", "0x1056", "0x1057", "0x1058", "0x1059", "0x105a", "0x105b",
    "0x107c", "0x107d", "0x1080", "0x1081", "0x1082", "0x1084", "0x1086",
    "0x1087", "0x1088", "0x1089", "0x108b", "0x1091", "0x1094", "0x1096",
    "0x109a", "0x109b", "0x1180", "0x1183", "0x1184", "0x1185", "0x1187",
    "0x1188", "0x1189", "0x118a", "0x118e", "0x118f", "0x1193", "0x1194",
    "0x1195", "0x1198", "0x1199", "0x119a", "0x119d", "0x119e", "0x119f",
    "0x11a0", "0x11a1", "0x11a2", "0x11a3", "0x11a7", "0x11b4", "0x11b6",
    "0x11b7", "0x11b8", "0x11ba", "0x11bc", "0x11bd", "0x11be", "0x11bf",
    "0x11c0", "0x11c2", "0x11c3", "0x11c4", "0x11c5", "0x11c6", "0x11c8",
    "0x11e0", "0x11e1", "0x11e2", "0x11e3", "0x11fa", "0x11fc", "0x1200",
    "0x1201", "0x1203", "0x1205", "0x1206", "0x1207", "0x1208", "0x1210",
    "0x1211", "0x1212", "0x1213", "0x1241", "0x1243", "0x1244", "0x1245",
    "0x1246", "0x1247", "0x1248", "0x1249", "0x124b", "0x124d", "0x1251",
    "0x1280", "0x1281", "0x1282", "0x1284", "0x1286", "0x1287", "0x1288",
    "0x1289", "0x1290", "0x1291", "0x1292", "0x1293", "0x1295", "0x1296",
    "0x1298", "0x1299", "0x12b9", "0x12ba", "0x1340", "0x1341", "0x1346",
    "0x1347", "0x1380", "0x1381", "0x1382", "0x1390", "0x1391", "0x1392",
    "0x1393", "0x139a", "0x139b", "0x13b3", "0x13ba", "0x13bb", "0x13bc",
    "0x13c0", "0x13c2", "0x13d7", "0x13d8", "0x13d9", "0x1401", "0x17c2",
    "0x17f0", "0x1140"]


class Nvidia(Hardware):
    """ Nvidia proprietary graphics driver """
    def __init__(self):
        Hardware.__init__(self, CLASS_NAME, CLASS_ID, VENDOR_ID, DEVICES, PRIORITY)

    @staticmethod
    def get_packages():
        """ Get all required packages """
        pkgs = ["nvidia", "nvidia-utils", "nvidia-libgl", "libvdpau"]
        if os.uname()[-1] == "x86_64":
            pkgs.extend(["lib32-nvidia-libgl", "lib32-libvdpau"])
        return pkgs

    @staticmethod
    def get_conflicts():
        """ Get conflicting packages """
        pkgs = ["mesa-libgl", "xf86-video-nouveau"]
        if os.uname()[-1] == "x86_64":
            pkgs.append("lib32-mesa-libgl")
        return pkgs

    @staticmethod
    def post_install(dest_dir):
        """ Post install commands """
        pass

    @staticmethod
    def is_proprietary():
        """ Returns True if the driver is a proprietary one """
        return True
