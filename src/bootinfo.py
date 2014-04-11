#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bootinfo.py
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

""" Detects installed OSes """

import os
import subprocess
import re

# constants
WIN_DIRS = ["windows", "Windows", "WINDOWS"]
SYSTEM_DIRS = ["System32", "system32"]

WINLOAD_NAMES = ["Winload.exe", "winload.exe"]
SECEVENT_NAMES = ["SecEvent.Evt", "secevent.evt"]
DOS_NAMES = ["IO.SYS", "io.sys"]
LINUX_NAMES = ["issue", "slackware_version"]

VISTA_MARK = "W.i.n.d.o.w.s. .V.i.s.t.a"
SEVEN_MARK = "W.i.n.d.o.w.s. .7"
DOS_MARKS = ["MS-DOS", "MS-DOS 6.22", "MS-DOS 6.21", "MS-DOS 6.0",
             "MS-DOS 5.0", "MS-DOS 4.01", "MS-DOS 3.3", "Windows 98",
             "Windows 95"]

if __name__ == '__main__':
    import gettext
    _ = gettext.gettext

def get_os(mountname):
    """ Detect installed OSes """
    #  If partition is mounted, try to identify the Operating System
    # (OS) by looking for files specific to the OS.

    detected_os = _("unknown")

    for windows in WIN_DIRS:
        for system in SYSTEM_DIRS:
            for name in WINLOAD_NAMES:
                path = os.path.join(mountname, windows, system, name)
                if os.path.exists(path):
                    with open(path, "rb") as system_file:
                        if VISTA_MARK in system_file:
                            detected_os = "Windows Vista"
                        elif SEVEN_MARK in system_file:
                            detected_os = "Windows 7"
            if detected_os == _("unknown"):
                for name in SECEVENT_NAMES:
                    path = os.path.join(mountname, windows, system, "config", name)
                    if os.path.exists(path):
                        detected_os = "Windows XP"

    if detected_os == _("unknown"):
        path = os.path.join(mountname, "ReactOS/system32/config/SecEvent.Evt")
        if os.path.exists(path):
            detected_os = "ReactOS"

    for name in DOS_NAMES:
        path = os.path.join(mountname, name)
        if os.path.exists(path):
            with open(path, "rb") as system_file:
                for mark in DOS_MARKS:
                    if mark in system_file:
                        detected_os = mark
    # Linuxes

    if detected_os == _("unknown"):
        for name in LINUX_NAMES:
            path = os.path.join(mountname, "etc", name)
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
                    try:
                        subprocess.call(["mount", device, "/mnt"], stderr=subprocess.DEVNULL)
                        oses[device] = get_os("/mnt")
                        subprocess.call(["umount", "-l", "/mnt"], stderr=subprocess.DEVNULL)
                    except AttributeError:
                        subprocess.call(["mount", device, "/mnt"])
                        oses[device] = get_os("/mnt")
                        subprocess.call(["umount", "-l", "/mnt"])

    return oses

if __name__ == '__main__':
    print(get_os_dict())
