#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  used_space.py
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

""" Get partition used space """

import subprocess
import shlex
import canonical.misc as misc
import logging
import show_message as show

@misc.raise_privileges
def get_used_ntfs(part):
    """ Gets used space in a NTFS partition """
    used = 0
    try:
        result = subprocess.check_output(shlex.split("ntfsinfo -m %s" % part))
    except subprocess.CalledProcessError as err:
        result = None
        txt = _("Can't detect used space of NTFS partition %s") % part
        logging.error(txt)
        logging.error(err)

    if result:
        csize, vsize, fsize = (0, 0, 0)
        result = result.decode()
        lines = result.split('\n')
        for line in lines:
            if 'Cluster Size:' in line:
                csize = int(line.split(':')[-1].strip())
            elif 'Volume Size in Clusters' in line:
                vsize = int(line.split(':')[-1].strip())
            elif 'Free Clusters:' in line:
                fsize = int(line.strip().split()[2])
        used = (vsize - fsize) / vsize
    return used

@misc.raise_privileges
def get_used_ext(part):
    """ Gets used space in an ext4 partition """
    used = 0
    try:
        result = subprocess.check_output(shlex.split("dumpe2fs -h %s" % part))
    except subprocess.CalledProcessError as err:
        result = None
        txt = _("Can't detect used space of EXTFS partition %s") % part
        logging.error(txt)
        logging.error(err)

    if result:
        csize, vsize, fsize = (0, 0, 0)
        result = result.decode()
        lines = result.split('\n')
        for line in lines:
            if "Block count:" in line:
                vsize = int(line.split(':')[-1].strip())
            elif "Free blocks:" in line:
                fsize = int(line.split(':')[-1].strip())
            elif "Block size:" in line:
                csize = int(line.split(':')[-1].strip())
        used = (vsize - fsize) / vsize
    return used

@misc.raise_privileges
def get_used_fat(part):
    """ Gets used space in a FAT partition """
    used = 0
    try:
        result = subprocess.check_output(shlex.split("dosfsck -n -v %s" % part))
    except subprocess.CalledProcessError as err:
        if b'Dirty bit is set' in err.output:
            result = err.output
        else:
            result = None
            txt = _("Can't detect used space of FAT partition %s") % part
            logging.error(txt)
            logging.error(err)

    if result:
        bperc = 0
        cl = 0
        sbyte = 0
        ucl = 0
        result = result.decode()
        lines = result.split('\n')
        for line in lines:
            if 'bytes per cluster' in line:
                bperc = int(line.split()[0].strip())
            elif 'Data area starts at' in line:
                sbyte = int(line.split()[5])
            elif part in line:
                cl = int(line.split()[3].split('/')[1])
                ucl = int(line.split()[3].split('/')[0])
        used = (sbyte + (bperc * ucl)) / (bperc * cl)
    return used


@misc.raise_privileges
def get_used_jfs(part):
    """ Gets used space in a JFS partition """
    used = 0
    try:
        result = subprocess.check_output(shlex.split("jfs_fsck -n %s" % part))
    except subprocess.CalledProcessError as err:
        result = None
        txt = _("Can't detect used space of JFS partition %s") % part
        logging.error(txt)
        logging.error(err)

    if result:
        vsize, fsize = (0, 0)
        result = result.decode()
        lines = result.split('\n')
        for line in lines:
            if "kilobytes total disk space" in line:
                vsize = int(line.split()[0].strip())
            elif "kilobytes are available for use" in line:
                fsize = int(line.split()[0].strip())
        used = (vsize-fsize) / vsize
    return used

@misc.raise_privileges
def get_used_reiser(part):
    """ Gets used space in a REISER partition """
    used = 0
    try:
        result = subprocess.check_output(shlex.split("debugreiserfs -d %s" % part))
    except subprocess.CalledProcessError as err:
        result = None
        txt = _("Can't detect used space of REISERFS partition %s") % part
        logging.error(txt)
        logging.error(err)

    if result:
        vsize, fsize = (0, 0)

        # Added 'replace' parameter (not tested) as it fails decoding. See issue #90
        result = result.decode('utf-8', 'replace')
        
        lines = result.split('\n')
        for line in lines:
            if "Count of blocks on the device" in line:
                vsize = int(line.split()[-1].strip())
            elif "Free blocks (count of blocks" in line:
                fsize = int(line.split()[-1].strip())
        used = (vsize-fsize) / vsize
    return used

@misc.raise_privileges
def get_used_btrfs(part):
    """ Gets used space in a Btrfs partition """
    used = 0
    try:
        result = subprocess.check_output(shlex.split("btrfs filesystem show %s" % part))
    except Exception as err:
        result = None
        txt = _("Can't detect used space of BTRFS partition %s") % part
        logging.error(txt)
        logging.error(err)

    if result:
        vsize, usize, umult, vmult = (1, 1, 1, 1)
        result = result.decode()
        result = result.split('\n')
        szmap = {"K":1000,
                 "M":1000000,
                 "G":1000000000,
                 "T":1000000000000,
                 "P":1000000000000000,
                }
        for z in result:
            if part in z:
                vsize = z.split()[3]
                usize = z.split()[5]
                for i in szmap:
                    if i in vsize:
                        vmult = szmap[i]
                    if i in usize:
                        umult = szmap[i]
                usize = float(usize.strip("KMGTPBib")) * umult
                vsize = float(vsize.strip("KMGTPBib")) * vmult
        used = usize/vsize
    return used

@misc.raise_privileges
def get_used_xfs(part):
    """ Gets used space in a XFS partition """
    used = 0
    try:
        command = shlex.split("xfs_db -c 'sb 0' -c 'print dblocks' -c 'print fdblocks' -r %s" % part)
        result = subprocess.check_output(command)
    except subprocess.CalledProcessError as err:
        result = None
        txt = _("Can't detect used space of XFS partition %s") % part
        logging.error(txt)
        logging.error(err)

    if result:
        vsize, fsize = (1, 0)
        result = result.decode()
        lines = result.split('\n')
        for line in lines:
            if "fdblocks" in line:
                fsize = int(line.split()[-1].strip())
            elif "dblocks" in line:
                vsize = int(line.split()[-1].strip())
        used = (vsize-fsize) / vsize
    return used

@misc.raise_privileges
def get_used_f2fs(part):
    # Need to do a test install using f2fs so I can get the output format when getting part info.
    used =  0
    return used


def is_btrfs(part):
    """ Checks if part is a Btrfs partition """
    space = get_used_btrfs(part)
    if not space:
        return False
    else:
        return True

def get_used_space(part, part_type):
    """ Get used space in a partition """
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
    elif 'f2fs' in part_type.lower():
         space = get_used_f2fs(part)
    else:
        space = 0
    return space
