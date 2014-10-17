#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bootinfo.py
#
#  Copyright © 2013,2014 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

""" Detects installed OSes (needs root privileges)"""

import os
import subprocess
import re
import tempfile

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message): return message

# constants
WIN_DIRS = ["windows", "Windows", "WINDOWS"]
SYSTEM_DIRS = ["System32", "system32"]

WINLOAD_NAMES = ["Winload.exe", "winload.exe"]
SECEVENT_NAMES = ["SecEvent.Evt", "secevent.evt"]
DOS_NAMES = ["IO.SYS", "io.sys"]
LINUX_NAMES = ["issue", "slackware_version"]

VISTA_MARKS = [b"Windows Vista"]
SEVEN_MARKS = [b"Windows 7", b"Win7"]
DOS_MARKS = ["MS-DOS", "MS-DOS 6.22", "MS-DOS 6.21", "MS-DOS 6.0",
             "MS-DOS 5.0", "MS-DOS 4.01", "MS-DOS 3.3", "Windows 98",
             "Windows 95"]

# Possible locations for os-release. Do not put a trailing /
OS_RELEASE_PATHS = ["etc/os-release", "usr/lib/os-release"]

if __name__ == '__main__':
    import gettext
    _ = gettext.gettext

def _check_windows(mount_name):
    detected_os = _("unknown")
    for windows in WIN_DIRS:
        for system in SYSTEM_DIRS:
            # Search for Windows Vista and 7
            for name in WINLOAD_NAMES:
                path = os.path.join(mount_name, windows, system, name)
                if os.path.exists(path):
                    with open(path, "rb") as system_file:
                        lines = system_file.readlines()
                        for line in lines:
                            for vista_mark in VISTA_MARKS:
                                if vista_mark in line:
                                    print("windows vista: ", path)
                                    detected_os = "Windows Vista"
                        if detected_os == _("unknown"):
                            for line in lines:
                                for seven_mark in SEVEN_MARKS:
                                    if seven_mark in line:
                                        print("windows 7: ", path)
                                        detected_os = "Windows 7"
            # Search for Windows XP
            if detected_os == _("unknown"):
                for name in SECEVENT_NAMES:
                    path = os.path.join(mount_name, windows, system, "config", name)
                    if os.path.exists(path):
                        print("windows XP: ", path)
                        detected_os = "Windows XP"
    return detected_os

def _check_reactos(mount_name):
    detected_os = _("unknown")
    path = os.path.join(mount_name, "ReactOS/system32/config/SecEvent.Evt")
    if os.path.exists(path):
        print("reactos: ", path)
        detected_os = "ReactOS"
    return detected_os

def _check_dos(mount_name):
    detected_os = _("unknown")
    for name in DOS_NAMES:
        path = os.path.join(mount_name, name)
        if os.path.exists(path):
            with open(path, "rb") as system_file:
                for mark in DOS_MARKS:
                    if mark in system_file:
                        detected_os = mark
    return detected_os  

def _check_linux(mount_name):
    detected_os = _("unknown")

    for os_release in OS_RELEASE_PATHS:
        path = os.path.join(mount_name, os_release)
        if os.path.exists(path):
            with open(path, 'r') as os_release_file:
                lines = os_release_file.readlines()
            for line in lines:
                # Let's use the "PRETTY_NAME"
                if line.startswith("PRETTY_NAME"):
                    detected_os = line[len("PRETTY_NAME="):]
            if detected_os == _("unknown"):
                # Didn't find PRETTY_NAME, we will use ID
                if line.startswith("ID"):
                    os_id = line[len("ID="):]
                if line.startswith("VERSION"):
                    os_version = line[len("VERSION="):]
                detected_os = os_id
                if len(os_version) > 0:
                    detected_os += " " + os_version
    detected_os = detected_os.replace('"', '').strip('\n')

    # If os_release was not found, try old issue file
    if detected_os == _("unknown"):
        for name in LINUX_NAMES:
            path = os.path.join(mount_name, "etc", name)
            if os.path.exists(path):
                with open(path, 'r') as system_file:
                    line = system_file.readline()
                textlist = line.split()
                text = ""
                for element in textlist:
                    if not "\\" in element:
                        text = text + element
                detected_os = text
    return detected_os

def _get_os(mount_name, device):
    """ Detect installed OSes """
    #  If partition is mounted, try to identify the Operating System
    # (OS) by looking for files specific to the OS.

    print("Checking windows on %s..." % device)
    detected_os = _check_windows(mount_name)    
    print(detected_os)

    if detected_os == _("unknown"):
        print("Checking Linux on %s..." % device)
        detected_os = _check_linux(mount_name)
        print(detected_os)

    if detected_os == _("unknown"):
        print("Checking reactos on %s..." % device)
        detected_os = _check_reactos(mount_name)
        print(detected_os)

    if detected_os == _("unknown"):
        print("Checking dos and w9x on %s..." % device)
        detected_os = _check_dos(mount_name)
        print(detected_os)

    return detected_os

def get_os_dict():
    """ Returns all detected OSes in a dict """
    oses = {}

    with open("/proc/partitions", 'r') as partitions_file:
        for line in partitions_file:
            line_split = line.split()
            if len(line_split) > 0:
                device = line_split[3]
                if "sd" in device and re.search(r'\d+$', device):
                    # ok, it has sd and ends with a number
                    device = "/dev/" + device
                    tmp_dir = tempfile.mkdtemp()
                    try:
                        subprocess.call(["mount", device, tmp_dir], stderr=subprocess.DEVNULL)
                        oses[device] = _get_os(tmp_dir, device)
                        subprocess.call(["umount", "-l", tmp_dir], stderr=subprocess.DEVNULL)
                    except AttributeError:
                        subprocess.call(["mount", device, tmp_dir])
                        oses[device] = _get_os(tmp_dir, device)
                        subprocess.call(["umount", "-l", tmp_dir])
    return oses

if __name__ == '__main__':
    print(get_os_dict())
