#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sense títol.py
#  
#  Copyright 2013 Cinnarch  <karasu@cinnarch.com>
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
#  
#  

import os

def bootinfo(mountname):
    #  If partition is mounted, try to identify the Operating System (OS) by looking for files specific to the OS.
    OS=""

    win7_dir1 = ["windows", "Windows", "WINDOWS"]
    win7_dir2 = ["System32", "system32"]
    win7_names = ["Winload.exe", "winload.exe"]
    
    vista_mark = "W.i.n.d.o.w.s. .V.i.s.t.a"
    seven_mark = "W.i.n.d.o.w.s. .7"
    
    for p1 in win7_dir1:
        for p2 in win7_dir2:
            for name in win7_names:
                p = os.path.join(mountname, p1, p2, name)
                if os.path.exists(p):
                    with open(p, "rb") as f:
                        if vista_mark in f:
                            OS = "Windows Vista"
                        elif seven_mark in f:
                            OS = "Windows 7"

    dos_marks = ["MS-DOS", "MS-DOS 6.22", "MS-DOS 6.21", "MS-DOS 6.0", \
                 "MS-DOS 5.0", "MS-DOS 4.01", "MS-DOS 3.3", "Windows 98" \
                 "Windows 95"]

    dos_names = ["IO.SYS", "io.sys"]
    
    for name in dos_names:
        p = os.path.join(mountname, name)
        if os.path.exists(p):
            with open(p, "rb") as f:
                for mark in dos_marks:
                    if mark in f:
                        OS = mark

    print(OS)

'''
[ -s "${mountname}/Windows/System32/config/SecEvent.Evt" ] || [ -s "${mountname}/WINDOWS/system32/config/SecEvent.Evt" ] || [ -s "${mountname}/WINDOWS/system32/config/secevent.evt" ] || [ -s "${mountname}/windows/system32/config/secevent.evt" ] && OS='Windows XP';

[ -s "${mountname}/ReactOS/system32/config/SecEvent.Evt" ] && OS='ReactOS';

[ -s "${mountname}/etc/issue" ] && OS=$(sed -e 's/\\. //g' -e 's/\\.//g' -e 's/^[ \t]*//' "${mountname}"/etc/issue);

[ -s "${mountname}/etc/slackware-version" ] && OS=$(sed -e 's/\\. //g' -e 's/\\.//g' -e 's/^[ \t]*//' "${mountname}"/etc/slackware-version);
'''
