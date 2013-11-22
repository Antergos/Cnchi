#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  lvm.py
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

import subprocess
import misc

@misc.raise_privileges
def get_lvm_partitions():
    vgmap = {}
    x = subprocess.getoutput("pvdisplay")
    for e in x.split("\n"):
        if "PV Name" in e:
            pvn = e.split()[-1]
        if "VG Name" in e:
            vgn = e.split()[-1]
            try:
                vgmap[vgn].append(pvn)
            except:
                vgmap[vgn] = [pvn]
    return vgmap

@misc.raise_privileges
def get_volume_groups():
    vg = []
    x = subprocess.getoutput("vgdisplay")
    for e in x.split("\n"):
        if "VG Name" in e:
            vg.append(e.split()[-1])
    return vg

@misc.raise_privileges
def get_logical_volumes(vg):
    lv = []
    x = subprocess.getoutput("lvdisplay %s" % vg)
    for e in x.split("\n"):
        if "LV Name" in e:
            lv.append(e.split()[-1])
    return lv

# When removing, we use -f flag to avoid warnings and confirmation messages

@misc.raise_privileges
def remove_logical_volume(lv):
    subprocess.checK_call(["lvremove", "-f", lv])

@misc.raise_privileges
def remove_volume_group(vg):
    # Before removing the volume group, remove its logical volumes
    lvm_logical_volumes = get_logical_volumes(vg)
    for lv in lvm_logical_volumes:
        remove_logical_volume(lv)
    # Now, remove the volume group
    subprocess.check_call(["vgremove", "-f", vg])

@misc.raise_privileges
def remove_physical_volume(pv):
    subprocess.check_call(["pvremove", "-f", pv])
