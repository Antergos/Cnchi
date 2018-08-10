#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# mount.py
#
# Copyright © 2013-2018 Antergos
#
# This file is part of Cnchi.
#
# Cnchi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Cnchi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# The following additional terms are in effect as per Section 7 of the license:
#
# The preservation of all legal notices and author attributions in
# the material or in the Appropriate Legal Notices displayed
# by works containing it is required.
#
# You should have received a copy of the GNU General Public License
# along with Cnchi; If not, see <http://www.gnu.org/licenses/>.

""" Mount functions for auto_partition and install modules """

import logging
from misc.run_cmd import call


def unmount(directory):
    """ Unmount """
    logging.debug("Unmounting %s", directory)
    call(["/usr/bin/umount", "-l", directory])


def unmount_swap():
    """ Unmount all swap devices """
    cmd = ["/usr/bin/swapon", "--show=NAME", "--noheadings"]
    swaps = call(cmd)
    if swaps:
        swaps = swaps.split("\n")
        for name in filter(None, swaps):
            if "/dev/zram" not in name:
                call(["/usr/bin/swapoff", name])


def unmount_all_in_directory(dest_dir):
    """ Unmounts all devices that are mounted inside dest_dir """

    # Unmount all swap devices
    unmount_swap()

    # Get all mounted devices
    mount_result = call(["/usr/bin/mount"]).split("\n")

    # Umount all devices mounted inside dest_dir (if any)
    dirs = []
    for mount in mount_result:
        if dest_dir in mount:
            try:
                directory = mount.split()[2]
                # Do not unmount dest_dir now (we will do it later)
                if directory != dest_dir:
                    dirs.append(directory)
            except IndexError:
                pass

    for directory in dirs:
        unmount(directory)

    # Now is the time to unmount the device that is mounted in dest_dir (if any)
    unmount(dest_dir)


def unmount_all_in_device(device):
    """ Unmounts all partitions from device """

    # Unmount all swap devices
    unmount_swap()

    # Get all mounted devices
    mount_result = call(["/usr/bin/mount"]).split("\n")

    # Umount all partitions of device
    dirs = []
    for mount in mount_result:
        if device in mount:
            try:
                directory = mount.split()[0]
                dirs.append(directory)
            except IndexError:
                pass

    for directory in dirs:
        unmount(directory)
