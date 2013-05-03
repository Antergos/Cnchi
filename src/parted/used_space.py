#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  used_space.py
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
#  
#  Antergos Team:
#   Alex Filgueira (faidoc) <alexfilgueira.antergos.com>
#   Raúl Granados (pollitux) <raulgranados.antergos.com>
#   Gustau Castells (karasu) <karasu.antergos.com>
#   Kirill Omelchenko (omelcheck) <omelchek.antergos.com>
#   Marc Miralles (arcnexus) <arcnexus.antergos.com>
#   Alex Skinner (skinner) <skinner.antergos.com>

import subprocess
import shlex
import misc

@misc.raise_privileges
def get_used_ntfs(part):
    used = 0
    try:
        x = subprocess.check_output(shlex.split("ntfsinfo -m %s" % part))
    except Exception as e:
        x = None
        print(e)
    if x:
        csize, vsize, fsize = (0,0,0)
        x = x.decode()
        y = x.split('\n')
        for z in y:
            if 'Cluster Size:' in z:
                csize = int(z.split(':')[-1].strip())
            elif 'Volume Size in Clusters' in z:
                vsize = int(z.split(':')[-1].strip())
            elif 'Free Clusters:' in z:
                fsize = int(z.strip().split()[2])
        used = (vsize - fsize) / vsize
    return used

@misc.raise_privileges
def get_used_ext(part):
    used = 0
    try:
        x = subprocess.check_output(shlex.split("dumpe2fs -h %s" % part))
    except Exception as e:
        x = None
        print(e)
    if x:
        csize, vsize, fsize = (0,0,0)
        x = x.decode()
        y = x.split('\n')
        for z in y:
            if "Block count:" in z:
                vsize = int(z.split(':')[-1].strip())
            elif "Free blocks:" in z:
                fsize = int(z.split(':')[-1].strip())
            elif "Block size:" in z:
                csize = int(z.split(':')[-1].strip())
        used = (vsize - fsize)/vsize
    return used

@misc.raise_privileges
def get_used_fat(part):
    used = 0
    try:
        x = subprocess.check_output(shlex.split("dosfsck -n -v %s" % part))
    except Exception as e:
        x = None
        print(e)
    if x:
        bperc = 0
        cl = 0
        sbyte = 0
        ucl = 0
        x = x.decode()
        y = x.split('\n')
        for z in y:
            if 'bytes per cluster' in z:
                bperc = int(z.split()[0].strip())
            elif 'Data area starts at' in z:
                sbyte = int(z.split()[5])
            elif part in z:
                cl = int(z.split()[3].split('/')[1])
                ucl = int(z.split()[3].split('/')[0])
        used = (sbyte + (bperc * ucl))/(bperc * cl)
    return used

@misc.raise_privileges
def get_used_jfs(part):
    used = 0
    try:
        x = subprocess.check_output(shlex.split("jfs_fsck -n %s" % part))
    except Exception as e:
        x = None
        print(e)
    if x:
        vsize, fsize = (0, 0)
        x = x.decode()
        y = x.split('\n')
        for z in y:
            if "kilobytes total disk space" in z:
                vsize = int(z.split()[0].strip())
            elif "kilobytes are available for use" in z:
                fsize = int(z.split()[0].strip())
        used = (vsize-fsize)/vsize
    return used

@misc.raise_privileges
def get_used_reiser(part):
    used = 0
    try:
        x = subprocess.check_output(shlex.split("debugreiserfs -d %s" % part))
    except Exception as e:
        x = None
        print(e)
    if x:
        vsize, fsize = (0, 0)
        x = x.decode()
        y = x.split('\n')
        for z in y:
            if "Count of blocks on the device" in z:
                vsize = int(z.split()[-1].strip())
            elif "Free blocks (count of blocks" in z:
                fsize = int(z.split()[-1].strip())
        used = (vsize-fsize)/vsize
    return used

@misc.raise_privileges
def get_used_btrfs(part):
    used = 0
    try:
        x = subprocess.check_output(shlex.split("btrfs filesystem show %s" % part))
    except Exception as e:
        x = None
        #print(e)
    if x:
        vsize, usize = (1, 0)
        x = x.decode()
        y = x.split('\n')
        for z in y:
            if part in z:
                vsize = z.split()[3]
                usize = z.split()[5]
                vunits = vsize[-2:]
                vsize = float(vsize[:-2])
                uunits = usize[-2:]
                usize = float(usize[:-2])
                if vunits == 'MB':
                    vmult = 1000000
                elif vunits == 'GB':
                    vmult = 1000000000
                elif vunits == 'KB':
                    vmult = 1000
                if uunits == 'MB':
                    umult = 1000000
                elif uunits == 'GB':
                    umult = 1000000000
                elif uunits == 'KB':
                    umult = 1000
                usize = usize * umult
                vsize = vsize * umult
        used = usize/vsize
    return used

@misc.raise_privileges
def get_used_xfs(part):
    used = 0
    try:
        x = subprocess.check_output(shlex.split("xfs_db -c 'sb 0' -c 'print dblocks' -c 'print fdblocks' -r %s" % part))
    except Exception as e:
        x = None
        print(e)
    if x:
        vsize, fsize = (1, 0)
        x = x.decode()
        y = x.split('\n')
        for z in y:
            if "fdblocks" in z:
                fsize = int(z.split()[-1].strip())
            elif "dblocks" in z:
                vsize = int(z.split()[-1].strip())
        used = (vsize-fsize)/vsize
    return used

def is_btrfs(part):
    space = get_used_btrfs(part)
    if not space:
        return False
    else:
        return True

def get_used_space(part, part_type):
    if 'ntfs' in part_type.lower():
        space = get_used_ntfs(part)
    elif 'ext' in part_type.lower():
        space = get_used_ext(part)
    elif 'fat' in part_type.lower():
        space = get_used_fat(part)
    elif 'jfs' in part_type.lower():
        space = get_used_jfs(part)
    elif 'reiser' in part_type.lower():
        space = get_used_reiser(part)
    elif 'btrfs' in part_type.lower():
        space = get_used_btrfs(part)
    elif 'xfs' in part_type.lower():
        space = get_used_xfs(part)
    else:
        space = 0
    return space
