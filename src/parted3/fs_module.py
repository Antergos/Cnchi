#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  fs_module.py
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

""" Functions to work with file systems """

import subprocess
import shlex
import canonical.misc as misc
import logging

# constants
NAMES = [ 'ext2', 'ext3', 'ext4', 'fat16', 'fat32', 'ntfs', 'jfs', \
           'reiserfs', 'xfs', 'btrfs', 'swap']

COMMON_MOUNT_POINTS = [ '/', '/boot', '/home', '/usr', '/var' ]

@misc.raise_privileges
def get_info(part):
    """ Get partition info using blkid """
    try:
        ret = subprocess.check_output(shlex.split('blkid %s' % part)).decode().strip()
    except subprocess.CalledProcessError as err:
        logging.warning(err)
        ret = ''
    partdic = {}
    for info in ret.split():
        if '=' in info:
            info = info.split('=')
            partdic[info[0]] = info[1].strip('"')
    return(partdic)

@misc.raise_privileges
def get_type(part):
    """ Get filesystem type using blkid """
    try:
        ret = subprocess.check_output(shlex.split('blkid -o value -s TYPE %s' % part)).decode().strip()
    except subprocess.CalledProcessError as err:
        logging.warning(err)
        ret = ''
    return ret

@misc.raise_privileges
def label_fs(fstype, part, label):
    """ Get filesystem label """
    ladic = {'ext2':'e2label %(part)s %(label)s',
             'ext3':'e2label %(part)s %(label)s',
             'ext4':'e2label %(part)s %(label)s',
             'fat':'mlabel -i %(part)s ::%(label)s',
             'fat16':'mlabel -i %(part)s ::%(label)s',
             'fat32':'mlabel -i %(part)s ::%(label)s',
             'ntfs':'ntfslabel %(part)s %(label)s',
             'jfs':'jfs_tune -L %(label)s %(part)s',
             'reiserfs':'reiserfstune -l %(label)s %(part)s',
             'xfs':'xfs_admin -l %(label)s %(part)s',
             'btrfs':'btrfs filesystem label %(part)s %(label)s'}
    fstype = fstype.lower()
    # OK, the below is a quick cheat.  vars() returns all variables
    # in a dictionary.  So 'part' and 'label' will be defined
    # and replaced in above dic
    try:
        result = subprocess.check_output(shlex.split(ladic[fstype] % vars())).decode()
        ret = (0, result)
    except subprocess.CalledProcessError as err:
        logging.error(err)
        ret = (1, err)
        # check_call returns exit code.  0 should mean success
    return ret

@misc.raise_privileges
def create_fs(part, fstype, label='', other_opts=''):
    """ Create filesystem using mkfs """

    # Set some default options
    # -m 1 reserves 1% for root, because I think 5% is too much on
    # newer bigger drives.
    # Also turn on dir_index for ext.  Not sure about other fs opts

    # The return value is tuple.  First arg is 0 for success, 1 for fail
    # Secong arg is either output from call if successful
    # or exception if failure

    opt_dic = {'ext2':'-m 1',
               'ext3':'-m 1 -O dir_index',
               'ext4':'-m 1 -O dir_index',
               'fat16':'',
               'fat32':'',
               'ntfs':'',
               'jfs':'',
               'reiserfs':'',
               'btrfs':'',
               'xfs':'',
               'swap':''}
    fstype = fstype.lower()
    if not other_opts:
        other_opts = opt_dic[fstype]
    comdic = {'ext2':'mkfs.ext2 -L "%(label)s" %(other_opts)s %(part)s',
             'ext3':'mkfs.ext3 -L "%(label)s" %(other_opts)s %(part)s',
             'ext4':'mkfs.ext4 -L "%(label)s" %(other_opts)s %(part)s',
             'fat16':'mkfs.vfat -n "%(label)s" -F 16 %(other_opts)s %(part)s',
             'fat32':'mkfs.vfat -n "%(label)s" -F 32 %(other_opts)s %(part)s',
             'ntfs':'mkfs.ntfs -L "%(label)s" %(other_opts)s %(part)s',
             'jfs':'mkfs.jfs -q -L "%(label)s" %(other_opts)s %(part)s',
             'reiserfs':'mkfs.reiserfs -q -l "%(label)s" %(other_opts)s %(part)s',
             'xfs':'mkfs.xfs -f -L "%(label)s" %(other_opts)s %(part)s',
             'btrfs':'mkfs.btrfs -f -L "%(label)s" %(other_opts)s %(part)s',
             'swap':'mkswap %(part)s'}
    try:
        result = subprocess.check_output(shlex.split(comdic[fstype] % vars())).decode()
        ret = (0, result)
    except subprocess.CalledProcessError as err:
        logging.error(err)
        ret = (1, err)
    return ret

@misc.raise_privileges
def is_ssd(disk_path):
    """ Check if is sdd """
    ssd = False
    try:
        process1 = subprocess.Popen(["hdparm", "-I", disk_path], stdout=subprocess.PIPE)
        process2 = subprocess.Popen(["grep", "Rotation Rate"], stdin=process1.stdout, stdout=subprocess.PIPE)
        process1.stdout.close()
        output = process2.communicate()[0].decode()
        if "Solid State" in output:
            ssd = True
    except subprocess.CalledProcessError as err:
        logging.error(err)
        logging.warning(_("Can't verify if %s is a Solid State Drive or not"), disk_path)

    return ssd

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
        logging.error(_("Sorry but filesystem %s can't be shrinked"), fs_type)

    return res

@misc.raise_privileges
def resize_ntfs(part, new_size_in_mb):
    """ Resize a ntfs partition """
    logging.debug("ntfsresize -P --size %s %s", str(new_size_in_mb)+"M", part)

    try:
        result = subprocess.check_output(["ntfsresize", "-v", "-P", "--size", str(new_size_in_mb)+"M", part])
    except subprocess.CalledProcessError as err:
        result = None
        logging.error(err)
        return False

    logging.debug(result)

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
    logging.debug("resize2fs %s %sM", part, str(new_size_in_mb))

    try:
        subprocess.check_output(["resize2fs", part, str(new_size_in_mb)+"M"])
    except subprocess.CalledProcessError as err:
        logging.error(err)
        return False

    return True
