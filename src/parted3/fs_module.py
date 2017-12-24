#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# fs_module.py
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


""" Functions to work with file systems """

import subprocess
import shlex
import logging
import os

import misc.extra as misc

from misc.run_cmd import call

# constants
NAMES = [
    'btrfs', 'ext2', 'ext3', 'ext4', 'fat16', 'fat32', 'f2fs', 'ntfs', 'jfs',
    'reiserfs', 'swap', 'xfs']

COMMON_MOUNT_POINTS = ['/', '/boot', '/boot/efi', '/home', '/usr', '/var']


def get_uuid(part):
    """ Get partition UUID """
    info = get_info(part)
    if "UUID" in info.keys():
        return info['UUID']
    else:
        logging.error("Can't get partition %s UUID", part)
        return ""


def get_label(part):
    """ Get partition label """
    info = get_info(part)
    if "LABEL" in info.keys():
        return info['LABEL']
    else:
        logging.debug(
            "Can't get partition %s label (or it does not have any)",
            part)
        return ""


@misc.raise_privileges
def get_info(part):
    """ Get partition info using blkid """

    ret = ''
    partdic = {}
    # Do not try to get extended partition info
    if part and not misc.is_partition_extended(part):
        # -c /dev/null means no cache
        cmd = ['blkid', '-c', '/dev/null', part]
        try:
            ret = subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError as err:
            logging.warning("Error running %s: %s", err.cmd, err.output)

        for info in ret.split():
            if '=' in info:
                info = info.split('=')
                partdic[info[0]] = info[1].strip('"')

    return partdic


@misc.raise_privileges
def get_type(part):
    """ Get partition filesystem type """
    ret = ''
    if part and not misc.is_partition_extended(part):
        #cmd = ['blkid', '-o', 'value', '-s', 'TYPE', part]
        cmd = ['lsblk', part, '-n', '-o', 'FSTYPE', '-l']
        try:
            ret = subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError as err:
            logging.warning("Error running %s: %s", err.cmd, err.output)
    return ret


def get_pknames():
    """ PKNAME: internal parent kernel device name """
    pknames = {}
    info = None
    try:
        cmd = ['lsblk', '-o', 'NAME,PKNAME', '-l']
        info = subprocess.check_output(cmd).decode().strip().split('\n')
    except subprocess.CalledProcessError as err:
        logging.warning("Error running %s: %s", err.cmd, err.output)

    if info:
        # skip header
        info = info[1:]
        skip_list = ["disk", "rom", "loop", "arch_root-image"]
        for line in info:
            skip_line = False
            for skip in skip_list:
                if skip in line:
                    skip_line = True
                    break
            if not skip_line:
                line = line.split()
                try:
                    pknames[line[0]] = line[1]
                except IndexError as err:
                    pass
    return pknames


@misc.raise_privileges
def label_fs(fstype, part, label):
    """ Get filesystem label """
    ladic = {'ext2': 'e2label %(part)s %(label)s',
             'ext3': 'e2label %(part)s %(label)s',
             'ext4': 'e2label %(part)s %(label)s',
             'f2fs': 'blkid -s LABEL -o value %(part)s %(label)s',
             'fat': 'mlabel -i %(part)s ::%(label)s',
             'fat16': 'mlabel -i %(part)s ::%(label)s',
             'fat32': 'mlabel -i %(part)s ::%(label)s',
             'vfat': 'mlabel -i %(part)s ::%(label)s',
             'ntfs': 'ntfslabel %(part)s %(label)s',
             'jfs': 'jfs_tune -L %(label)s %(part)s',
             'reiserfs': 'reiserfstune -l %(label)s %(part)s',
             'xfs': 'xfs_admin -l %(label)s %(part)s',
             'btrfs': 'btrfs filesystem label %(part)s %(label)s',
             'swap': 'swaplabel -L %(label)s %(part)s'}
    fstype = fstype.lower()
    # OK, the below is a quick cheat.  vars() returns all variables
    # in a dictionary.  So 'part' and 'label' will be defined
    # and replaced in above dic
    if fstype in ladic:
        try:
            cmd = shlex.split(ladic[fstype] % vars())
            result = subprocess.check_output(cmd).decode()
            ret = (0, result)
        except subprocess.CalledProcessError as err:
            logging.error("Error running %s: %s", err.cmd, err.output)
            ret = (1, err)
            # check_call returns exit code.  0 should mean success
    else:
        ret = (1, _("Can't label a {0} partition").format(fstype))
    return ret


@misc.raise_privileges
def create_fs(part, fstype, label='', other_opts=''):
    """ Create filesystem using mkfs """

    # Set some default options
    # -m 1 reserves 1% for root, because I think 5% is too much on
    # newer bigger drives.
    # Also turn on dir_index for ext.  Not sure about other fs opts

    # The return value is tuple.
    # (failed, msg)
    # First arg is False for success, True for fail
    # Second arg is either output from call if successful
    # or exception message error if failure

    if not fstype:
        msg = "Cannot make a filesystem of type None in partition %s"
        logging.error(msg, part)
        msg = _("Cannot make a filesystem of type None in partition {0}")
        msg = msg.format(part)
        return True, msg

    fstype = fstype.lower()

    comdic = {'ext2': 'mkfs.ext2 -F -q',
              'ext3': 'mkfs.ext3 -F -q',
              'ext4': 'mkfs.ext4 -F -q',
              'f2fs': 'mkfs.f2fs -f',
              'fat': 'mkfs.vfat -F 32',
              'fat16': 'mkfs.vfat -F 16',
              'fat32': 'mkfs.vfat -F 32',
              'vfat': 'mkfs.vfat -F 32',
              'ntfs': 'mkfs.ntfs -f',
              'jfs': 'mkfs.jfs -q',
              'reiserfs': 'mkfs.reiserfs -q',
              'xfs': 'mkfs.xfs -f',
              'btrfs': 'mkfs.btrfs -f',
              'swap': 'mkswap'}

    if fstype not in comdic.keys():
        msg = _("Unknown filesystem {0} for partition {1}")
        msg = msg.format(fstype, part)
        return True, msg

    cmd = comdic[fstype]

    if label:
        lbldic = {'ext2': '-L "%(label)s"',
                  'ext3': '-L "%(label)s"',
                  'ext4': '-L "%(label)s"',
                  'f2fs': '-l "%(label)s"',
                  'fat': '-n "%(label)s"',
                  'fat16': '-n "%(label)s"',
                  'fat32': '-n "%(label)s"',
                  'vfat': '-n "%(label)s"',
                  'ntfs': '-L "%(label)s"',
                  'jfs': '-L "%(label)s"',
                  'reiserfs': '-l "%(label)s"',
                  'xfs': '-L "%(label)s"',
                  'btrfs': '-L "%(label)s"',
                  'swap': '-L "%(label)s"'}
        cmd += " " + lbldic[fstype]

    if not other_opts:
        default_opts = {'ext2': '-m 1',
                        'ext3': '-m 1 -O dir_index',
                        'ext4': '-m 1 -O dir_index',
                        'f2fs': '',
                        'fat': '',
                        'fat16': '',
                        'fat32': '',
                        'vfat': '',
                        'ntfs': '',
                        'jfs': '',
                        'reiserfs': '',
                        'btrfs': '',
                        'xfs': '',
                        'swap': ''}
        other_opts = default_opts[fstype]

    if other_opts:
        cmd += " %(other_opts)s"

    cmd += " %(part)s"

    try:
        cmd = shlex.split(cmd % vars())
        result = subprocess.check_output(cmd).decode()
        ret = (False, result)
    except subprocess.CalledProcessError as err:
        logging.error("Error running %s: %s", err.cmd, err.output)
        ret = (True, err)
    return ret


@misc.raise_privileges
def is_ssd(disk_path):
    """ Checks if given disk is actually a ssd disk. """
    disk_name = disk_path.split('/')[-1]
    filename = os.path.join("/sys/block", disk_name, "queue/rotational")
    if not os.path.exists(filename):
        # Should not happen unless sysfs changes, but better safe than sorry
        txt = "Cannot verify if {0} is a Solid State Drive or not".format(
            disk_path)
        logging.warning(txt)
        return False
    with open(filename) as my_file:
        return my_file.read() == "0\n"


# To shrink a partition:
# 1. Shrink fs
# 2. Shrink partition (resize)

# To expand a partition:
# 1. Expand partition
# 2. Expand fs (resize)

def resize(part, fs_type, new_size_in_mb):
    """ Resize partition """
    fs_type = fs_type.lower()

    res = False

    if 'ntfs' in fs_type:
        res = resize_ntfs(part, new_size_in_mb)
    elif 'fat' in fs_type:
        res = resize_fat(part, new_size_in_mb)
    elif 'ext' in fs_type:
        res = resize_ext(part, new_size_in_mb)
    else:
        logging.error("Filesystem %s can't be shrinked", fs_type)

    return res


@misc.raise_privileges
def resize_ntfs(part, new_size_in_mb):
    """ Resize a ntfs partition """
    txt = "ntfsresize -P --size {0}M {1}".format(new_size_in_mb, part)
    logging.debug(txt)

    try:
        cmd = ["ntfsresize", "-v", "-P", "--size",
               "{0}M".format(new_size_in_mb), part]
        result = subprocess.check_output(cmd)
        logging.debug(result)
    except subprocess.CalledProcessError as err:
        logging.error("Error running %s: %s", err.cmd, err.output)
        return False

    return True


@misc.raise_privileges
def resize_fat(part, new_size_in_mb):
    """ Resize a fat partition """
    # https://bbs.archlinux.org/viewtopic.php?id=131728
    # the only Linux tool that was capable of resizing fat32, isn't capable of it anymore?
    return False


@misc.raise_privileges
def resize_ext(part, new_size_in_mb):
    """ Resize an ext partition """
    txt = "resize2fs {0} {1}M".format(part, new_size_in_mb)
    logging.debug(txt)

    try:
        cmd = ["resize2fs", part, "{0}M".format(new_size_in_mb)]
        result = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as err:
        logging.error("Error running %s: %s", err.cmd, err.output)
        return False

    logging.debug(result)

    return True
