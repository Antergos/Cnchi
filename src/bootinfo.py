#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bootinfo.py
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


""" Detects installed OSes (needs root privileges)"""

import os
import re
import tempfile
import logging

from misc.run_cmd import call

try:
    import misc.extra as misc
except ImportError:
    import extra as misc

if __debug__:
    def _(x): return x

# constants
WIN_DIRS = ["windows", "WINDOWS", "Windows"]
SYSTEM_DIRS = ["system32", "System32"]

WINLOAD_NAMES = ["Winload.exe", "winload.exe"]
SECEVENT_NAMES = ["SecEvent.Evt", "secevent.evt"]
DOS_NAMES = ["IO.SYS", "io.sys"]
LINUX_NAMES = ["issue", "slackware_version"]

VISTA_MARKS = ["Windows Vista", "W.i.n.d.o.w.s. .V.i.s.t.a."]
SEVEN_MARKS = ["Win7", "Windows 7", "W.i.n.7.", "W.i.n.d.o.w.s. .7."]

DOS_MARKS = [
    "MS-DOS",
    "MS-DOS 6.22",
    "MS-DOS 6.21",
    "MS-DOS 6.0",
    "MS-DOS 5.0",
    "MS-DOS 4.01",
    "MS-DOS 3.3",
    "Windows 98",
    "Windows 95"]

# Possible locations for os-release. Do not put a trailing /
OS_RELEASE_PATHS = ["usr/lib/os-release", "etc/os-release"]


def _check_windows(mount_name):
    """ Checks for a Microsoft Windows installed """

    detected_os = _("unknown")
    paths = []
    for windows in WIN_DIRS:
        for system in SYSTEM_DIRS:
            paths.append(os.path.join(mount_name, windows, system))

    for path in paths:
        if _check_vista(path):
            detected_os = "Windows Vista"
        elif _check_win7(path):
            detected_os = "Windows 7"
        elif _check_winxp(path):
            detected_os = "Win XP"
        else:
            detected_os = _("unknown")

    return detected_os


def _check_vista(system_path):
    """ Searches for Windows Vista """

    for name in WINLOAD_NAMES:
        path = os.path.join(system_path, name)
        if os.path.exists(path):
            with open(path, "rb") as system_file:
                lines = system_file.readlines()
            for line in lines:
                for vista_mark in VISTA_MARKS:
                    if vista_mark.encode('utf-8') in line:
                        return True
    return False


def _check_win7(system_path):
    """ Searches for Windows 7 """

    for name in WINLOAD_NAMES:
        path = os.path.join(system_path, name)
        if os.path.exists(path):
            with open(path, "rb") as system_file:
                lines = system_file.readlines()
                for line in lines:
                    for seven_mark in SEVEN_MARKS:
                        if seven_mark.encode('utf-8') in line:
                            return True
    return False


def _check_winxp(system_path):
    """ Searches for Windows XP """

    for name in SECEVENT_NAMES:
        path = os.path.join(system_path, "config", name)
        if os.path.exists(path):
            return True
    return False


@misc.raise_privileges
def _hexdump8081(partition):
    """ Runs hexdump on partition to try to identify the boot sector """
    cmd = ["hexdump", "-v", "-n", "2", "-s",
           "0x80", "-e", '2/1 "%02x"', partition]
    hexdump = call(cmd)
    return hexdump


def _get_partition_info(partition):
    """ Get bytes 0x80-0x81 of VBR to identify Boot sectors. """
    bytes80_to_81 = _hexdump8081(partition)

    bst = {
        '0000': 'Data or Swap',  # Data or swap partition
        '7405': 'Windows 7',  # W7 Fat32
        '0734': 'Dos_1.0',
        '0745': 'Windows Vista',  # WVista Fat32
        '089e': 'MSDOS5.0',  # Dos Fat16
        '08cd': 'Windows XP',  # WinXP Ntfs
        '0bd0': 'MSWIN4.1',  # Fat32
        '2a00': 'ReactOS',
        '2d5e': 'Dos 1.1',
        '3030': 'W95 Extended (LBA)',
        '3a5e': 'Recovery',  # Recovery Fat32
        '5c17': 'Extended (do not use)',  # Extended partition
        '55aa': 'Windows Vista/7/8',  # Vista/7 Ntfs (HPFS/NTFS/exFAT)
        '638b': 'Freedos',  # FreeDos Fat32
        '7cc6': 'MSWIN4.1',  # Fat32
        '8ec0': 'Windows XP',  # WinXP Ntfs
        'b6d1': 'Windows XP',  # WinXP Fat32
        'e2f7': 'FAT32, Non Bootable',
        'e9d8': 'Windows Vista/7/8',  # Vista/7 Ntfs
        'fa33': 'Windows XP'}  # WinXP Ntfs

    if bytes80_to_81 in bst.keys():
        return bst[bytes80_to_81]
    elif bytes80_to_81:
        logging.debug("Unknown partition id %s", bytes80_to_81)
    return _("unknown")


def _check_reactos(mount_name):
    """ Checks for ReactOS """
    detected_os = _("unknown")
    path = os.path.join(mount_name, "ReactOS/system32/config/SecEvent.Evt")
    if os.path.exists(path):
        detected_os = "ReactOS"
    return detected_os


def _check_dos(mount_name):
    """ Checks for DOS and W9x """
    detected_os = _("unknown")
    paths = []
    for name in DOS_NAMES:
        path = os.path.join(mount_name, name)
        if os.path.exists(path):
            paths.append(path)

    for path in paths:
        with open(path, "rb") as system_file:
            for mark in DOS_MARKS:
                if mark in system_file:
                    detected_os = mark
    return detected_os


def _check_linux(mount_name):
    """ Checks for linux """
    detected_os = _("unknown")

    paths = []
    for os_release in OS_RELEASE_PATHS:
        path = os.path.join(mount_name, os_release)
        if os.path.exists(path):
            paths.append(path)

    for path in paths:
        with open(path, 'r') as os_release_file:
            lines = os_release_file.readlines()
        os_info = {
            "pretty_name": "",
            "id": "",
            "version": ""}
        for line in lines:
            if line.startswith("PRETTY_NAME"):
                os_info["pretty_name"] = line[len("PRETTY_NAME="):]
            elif line.startswith("ID"):
                os_info["id"] = line[len("ID="):]
            elif line.startswith("VERSION"):
                os_info["version"] = line[len("VERSION="):]

        if os_info["pretty_name"]:
            detected_os = os_info["pretty_name"]
        elif os_info["id"]:
            detected_os = os_info["id"]
            if os_info["version"]:
                detected_os = "{0} {1}".format(detected_os, os_info["version"])

    detected_os = detected_os.replace('"', '').strip('\n')

    # If os_release was not found, try old issue file
    if detected_os == _("unknown"):
        paths = []
        for name in LINUX_NAMES:
            path = os.path.join(mount_name, "etc", name)
            if os.path.exists(path):
                paths.append(path)
        for path in paths:
            with open(path, 'r') as system_file:
                line = system_file.readline()
            textlist = line.split()
            text = ""
            for element in textlist:
                if "\\" not in element:
                    text += element
            detected_os = text
    return detected_os


def _get_os(mount_name):
    """ Detect installed OSes """
    #  If partition is mounted, try to identify the Operating System
    # (OS) by looking for files specific to the OS.

    detected_os = _check_windows(mount_name)

    if detected_os == _("unknown"):
        detected_os = _check_linux(mount_name)

    if detected_os == _("unknown"):
        detected_os = _check_reactos(mount_name)

    if detected_os == _("unknown"):
        detected_os = _check_dos(mount_name)

    return detected_os


def get_os_dict():
    """ Returns all detected OSes in a dict """
    oses = {}

    tmp_dir = tempfile.mkdtemp()

    with open("/proc/partitions", 'r') as partitions_file:
        for line in partitions_file:
            line_split = line.split()
            if len(line_split) > 0:
                device = line_split[3]
                if "sd" in device and re.search(r'\d+$', device):
                    # ok, it has sd and ends with a number
                    device = "/dev/" + device
                    call(["mount", device, tmp_dir])
                    oses[device] = _get_os(tmp_dir)
                    call(["umount", "-l", tmp_dir])
                    if oses[device] == _("unknown"):
                        # As a last resort, try reading partition info
                        # with hexdump
                        oses[device] = _get_partition_info(device)

    try:
        os.rmdir(tmp_dir)
    except OSError:
        pass

    return oses


def windows_startup_folder(mount_path):
    locations = [
        # Windows 8
        'ProgramData/Microsoft/Windows/Start Menu/Programs/StartUp',
        # Windows 7
        'ProgramData/Microsoft/Windows/Start Menu/Programs/Startup',
        # Windows XP
        'Documents and Settings/All Users/Start Menu/Programs/Startup',
        # Windows NT
        'Winnt/Profiles/All Users/Start Menu/Programs/Startup',
    ]
    for location in locations:
        path = os.path.join(mount_path, location)
        if os.path.exists(path):
            return path
    return ''


if __name__ == '__main__':
    print(get_os_dict())
