#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# used_space.py
#
# Copyright © 2013-2017 Antergos
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


""" Get partition used space """

import subprocess
import shlex
import logging

import misc.extra as misc


@misc.raise_privileges
def get_used_ntfs(part):
    """ Gets used space in a NTFS partition """
    used = 0
    try:
        result = subprocess.check_output(["ntfsinfo", "-mf", part])
    except subprocess.CalledProcessError as err:
        result = None
        txt = _("Can't detect used space of NTFS partition %s")
        logging.error(txt, part)
        logging.error(err)

    if result:
        vsize, fsize = (0, 0)
        result = result.decode()
        lines = result.split('\n')
        for line in lines:
            if 'Volume Size in Clusters' in line:
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
        result = subprocess.check_output(["dumpe2fs", "-h", part])
    except subprocess.CalledProcessError as err:
        result = None
        txt = _("Can't detect used space of EXTFS partition %s")
        logging.error(txt, part)
        logging.error(err)

    if result:
        vsize, fsize = (0, 0)
        result = result.decode()
        lines = result.split('\n')
        for line in lines:
            if "Block count:" in line:
                vsize = int(line.split(':')[-1].strip())
            elif "Free blocks:" in line:
                fsize = int(line.split(':')[-1].strip())
        used = (vsize - fsize) / vsize
    return used


@misc.raise_privileges
def get_used_fat(part):
    """ Gets used space in a FAT partition """
    used = 0
    try:
        result = subprocess.check_output(["fsck.fat", "-n", "-v", part])
    except subprocess.CalledProcessError as err:
        if b'Dirty bit is set' in err.output:
            result = err.output
        else:
            result = None
            txt = _("Can't detect used space of FAT partition %s : %s")
            logging.error(txt, part, str(err.output))

    if result:
        bytes_per_cluster, cluster, sbyte, ucl = (0, 0, 0, 0)
        result = result.decode()
        lines = result.split('\n')
        for line in lines:
            if 'bytes per ' in line:
                bytes_per_cluster = int(line.split()[0].strip())
            elif 'Data area starts at' in line:
                sbyte = int(line.split()[5])
            elif part in line:
                cluster = int(line.split()[3].split('/')[1])
                ucl = int(line.split()[3].split('/')[0])
        try:
            used = (sbyte + (bytes_per_cluster * ucl)) / (bytes_per_cluster * cluster)
        except ZeroDivisionError as zero_error:
            logging.error("Error in get_used_fat: %s", zero_error)

    return used


@misc.raise_privileges
def get_used_jfs(part):
    """ Gets used space in a JFS partition """
    used = 0
    try:
        result = subprocess.check_output(["jfs_fsck", "-n", part])
    except subprocess.CalledProcessError as err:
        result = None
        txt = _("Can't detect used space of JFS partition %s")
        logging.error(txt, part)
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
        used = (vsize - fsize) / vsize

    return used


@misc.raise_privileges
def get_used_reiser(part):
    """ Gets used space in a REISER partition """
    used = 0
    try:
        result = subprocess.check_output(["debugreiserfs", "-d", part])
    except subprocess.CalledProcessError as err:
        result = None
        txt = _("Can't detect used space of REISERFS partition %s")
        logging.error(txt, part)
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
        used = (vsize - fsize) / vsize

    return used


@misc.raise_privileges
def get_used_btrfs(part, show_error=True):
    """ Gets used space in a Btrfs partition """
    used = 0
    try:
        result = subprocess.check_output(["btrfs", "filesystem", "show", part])
    except subprocess.CalledProcessError as err:
        result = None
        if show_error:
            message = "Can't detect used space of BTRFS partition {0}: {1}".format(part, err.output)
            logging.error(message)
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(err).__name__, err.args)
            logging.error(message)

    if result:
        vsize, usize, umult, vmult = (1, 1, 1, 1)
        result = result.decode()
        result = result.split('\n')
        szmap = {"KiB": 1024,
                 "MiB": 1048576,
                 "GiB": 1073741824,
                 "TiB": 1099511627776,
                 "PiB": 1125899906842624}
        for params in result:
            if part in params:
                vsize = params.split()[3]
                usize = params.split()[5]
                for element in szmap:
                    if element in vsize:
                        vmult = szmap[element]
                    if element in usize:
                        umult = szmap[element]
                usize = float(usize.strip("KMGTPBib")) * umult
                vsize = float(vsize.strip("KMGTPBib")) * vmult
        used = int(usize / vsize)

    return used


@misc.raise_privileges
def get_used_xfs(part):
    """ Gets used space in a XFS partition """
    used = 0
    try:
        cmd = "xfs_db -c 'sb 0' -c 'print dblocks' -c 'print fdblocks' -r {0}"
        cmd = cmd.format(part)
        result = subprocess.check_output(shlex.split(cmd))
    except subprocess.CalledProcessError as err:
        result = None
        txt = _("Can't detect used space of XFS partition %s")
        logging.error(txt, part)
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
        used = (vsize - fsize) / vsize

    return used


@misc.raise_privileges
def get_used_f2fs(part):
    """ Get f2fs partition used space """
    # TODO: Use a f2fs installation to check the output format when getting part info.
    used = 0
    return used


def is_btrfs(part):
    """ Checks if part is a Btrfs partition """
    space = get_used_btrfs(part, show_error=False)
    if not space:
        return False
    else:
        return True


def get_used_space(part, part_type):
    """ Get used space in a partition """

    part_type = part_type.lower()

    if 'ntfs' in part_type:
        space = get_used_ntfs(part)
    elif 'ext' in part_type:
        space = get_used_ext(part)
    elif 'fat' in part_type:
        space = get_used_fat(part)
    elif 'jfs' in part_type:
        space = get_used_jfs(part)
    elif 'reiser' in part_type:
        space = get_used_reiser(part)
    elif 'btrfs' in part_type:
        space = get_used_btrfs(part)
    elif 'xfs' in part_type:
        space = get_used_xfs(part)
    elif 'f2fs' in part_type:
        space = get_used_f2fs(part)
    else:
        space = 0

    return space
