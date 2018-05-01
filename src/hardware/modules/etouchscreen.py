#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  etouchscreen.py
#
#  Copyright © 2013-2018 Antergos
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


""" eGalax Touch Screen driver installation """

# References
# - http://www.x.org/archive/X11R7.5/doc/man/man4/evdev.4.html
# - https://bbs.archlinux.org/viewtopic.php?id=126208

try:
    from hardware.hardware import Hardware
except ImportError:
    from hardware import Hardware

import subprocess
import os

CLASS_NAME = "ETouchScreen"
CLASS_ID = ""
VENDOR_ID = "0x0eef"
DEVICES = ['0x0001']


class ETouchScreen(Hardware):
    """ eGalax Touch Screen driver """

    def __init__(self):
        Hardware.__init__(self, CLASS_NAME, CLASS_ID, VENDOR_ID, DEVICES)

    @staticmethod
    def get_packages():
        """ Get all required packages """
        return ["xinput_calibrator", "xournal"]

    @staticmethod
    def post_install(dest_dir):
        """ Post install commands """
        try:
            subprocess.check_call(["rmmod", "usbtouchscreen"])
        except subprocess.CalledProcessError as err:
            pass
        # Do not load the 'usbtouchscreen' module, as it conflicts with eGalax
        path = os.path.join(
            dest_dir, "etc/modprobe.d/blacklist-usbtouchscreen.conf")
        with open(path, 'w') as conf_file:
            conf_file.write("blacklist usbtouchscreen\n")

        # TODO: This should be computer specific
        path = os.path.join(
            dest_dir, "etc/X11/xorg.conf.d/99-calibration.conf")
        with open(path, 'w') as conf_file:
            conf_file.write('Section "InputClass"\n')
            conf_file.write('\tIdentifier      "calibration"\n')
            conf_file.write(
                '\tMatchProduct    "eGalax Inc. USB TouchController"\n')
            conf_file.write(
                '\tOption          "Calibration"   "3996 122 208 3996"\n')
            conf_file.write('\tOption          "InvertY" "1"\n')
            conf_file.write('\tOption          "SwapAxes" "0"\n')
            conf_file.write('EndSection\n')
