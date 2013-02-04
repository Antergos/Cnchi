#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  fs_module.py
#  
#  Copyright 2013 Cinnarch
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
#  Cinnarch Team:
#   Alex Filgueira (faidoc) <alexfilgueira.cinnarch.com>
#   Raúl Granados (pollitux) <raulgranados.cinnarch.com>
#   Gustau Castells (karasu) <karasu.cinnarch.com>
#   Kirill Omelchenko (omelcheck) <omelchek.cinnarch.com>
#   Marc Miralles (arcnexus) <arcnexus.cinnarch.com>
#   Alex Skinner (skinner) <skinner.cinnarch.com>

import subprocess
import shlex

_names = [ 'ext2', 'ext3', 'ext4', 'fat16', 'fat32', 'ntfs', 'jfs', \
           'reiserfs', 'xfs', 'btrfs', 'swap']

_common_mount_points = [ '/', '/boot', '/home', '/usr', '/var']


def get_info(part):
    try:
        ret = subprocess.check_output(shlex.split('blkid %s' % part)).decode().strip()
    except:
        ret = ''
    partdic = {}
    i = ret.split()
    for e in i:
        if '=' in e:
            e = e.split('=')
            partdic[e[0]] = e[1]
    return(partdic)

def label_fs(fstype, part, label):
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
        y = subprocess.check_output(shlex.split(ladic[fstype] % vars())).decode()
        ret = (0, y)
    except Exception as e:
        ret = (1, e)
        # check_call returns exit code.  0 should mean success
    return ret

def create_fs(part, fstype, label='', other_opts=None):
    #set some default options
    #-m 1 reserves 1% for root, because I think 5% is too much on
    #newer bigger drives.  
    #Also turn on dir_index for ext.  Not sure about other fs opts

    #The return value is tuple.  First arg is 0 for success, 1 for fail
    #Secong arg is either output from call if successful
    #or exception if failure

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
    
    comdic = {'ext2':'mkfs.ext2 -c -L %(label)s %(other_opts)s %(part)s',
             'ext3':'mkfs.ext3 -c -L %(label)s %(other_opts)s %(part)s',
             'ext4':'mkfs.ext4 -c -L %(label)s %(other_opts)s %(part)s',
             'fat16':'mkfs.vfat -c -n %(label)s -F 16 %(other_opts) %(part)s',
             'fat32':'mkfs.vfat -c -n %(label)s -F 32 %(other_opts) %(part)s',
             'ntfs':'mkfs.ntfs -L %(label)s %(other_opts)s %(part)s',
             'jfs':'mkfs.jfs -c -L %(label)s %(other_opts)s %(part)s',
             'reiserfs':'mkfs.reiserfs -l %(label)s %(other_opts)s %(part)s',
             'xfs':'mkfs.xfs -L %(label)s %(other_opts)s %(part)s',
             'btrfs':'mkfs.btrfs -L %(label)s %(other_opts)s %(part)s',
             'swap':'mkswap %(part)s'}
    try:
        y = subprocess.check_output(shlex.split(comdic[fstype] % vars())).decode()
        ret = (0, y)
    except Exception as e:
        ret = (1, e)
    return ret
