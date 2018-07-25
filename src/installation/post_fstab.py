#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# post_fstab.py
#
# Copyright © 2013-2018 Antergos
#
# This file is part of Cnchi.
#
# Cnchi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Cnchi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cnchi; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

""" Create /etc/fstab file """

import logging
import os
import re

import parted3.fs_module as fs

class PostFstab():
    """ Setup /etc/fstab """

    DEST_DIR = '/install'

    def __init__(self, method, mount_devices, fs_devices, ssd, settings):
        """ Init class properties """
        self.method = method
        self.mount_devices = mount_devices
        self.fs_devices = fs_devices
        self.ssd = ssd
        self.zfs = settings.get('zfs')
        self.use_lvm = settings.get('use_lvm')
        self.use_luks = settings.get('use_luks')
        self.luks_root_password = settings.get('luks_root_password')
        self.root_uuid = None

    def get_swap_fstab_line(self, uuid, partition_path):
        """ Create swap line for fstab """
        # If using a TRIM supported SSD,
        # discard is a valid mount option for swap
        if partition_path in self.ssd:
            opts = "defaults,discard"
        else:
            opts = "defaults"

        if self.zfs:
            # We can't use UUID with zfs, so we will use device name
            txt = "{0} swap swap {1} 0 0".format(partition_path, opts)
        else:
            txt = "UUID={0} swap swap {1} 0 0".format(uuid, opts)
        return txt

    @staticmethod
    def add_vol_to_crypttab(vol_name, uuid, keyfile='none'):
        """ Modify the crypttab file """
        crypttab_path = os.path.join(PostFstab.DEST_DIR, 'etc/crypttab')
        os.chmod(crypttab_path, 0o666)
        with open(crypttab_path, 'a') as crypttab_file:
            line = "{0} /dev/disk/by-uuid/{1} {2} luks\n"
            line = line.format(vol_name, uuid, keyfile)
            crypttab_file.write(line)
            logging.debug("Added %s to crypttab", line)
        os.chmod(crypttab_path, 0o600)

    @staticmethod
    def get_device_fstab_line(partition_path, mount_point, myfmt, opts='defaults', chk='0'):
        """ Create fstab line """
        txt = "{0} {1} {2} {3} 0 {4}"
        txt = txt.format(partition_path, mount_point, myfmt, opts, chk)
        logging.debug("Added %s to fstab", txt)
        return txt

    @staticmethod
    def get_uuid_fstab_line(uuid, mount_point, myfmt, opts='defaults', chk='0'):
        """ Create fstab line """
        txt = "UUID={0} {1} {2} {3} 0 {4}"
        txt = txt.format(uuid, mount_point, myfmt, opts, chk)
        logging.debug("Added %s to fstab", txt)
        return txt

    @staticmethod
    def get_mount_options(myfmt, is_ssd):
        """ Adds mount options depending on filesystem """
        opts = ""
        if not is_ssd:
            if "btrfs" in myfmt:
                opts = "defaults,relatime,space_cache,autodefrag,inode_cache"
            elif "f2fs" in myfmt:
                opts = "defaults,noatime"
            elif "ext3" in myfmt or "ext4" in myfmt:
                opts = "defaults,relatime,data=ordered"
            else:
                opts = "defaults,relatime"
        else:
            # As of linux kernel version 3.7, the following
            # filesystems support TRIM: ext4, btrfs, JFS, and XFS.
            if myfmt in ["ext4", "jfs", "xfs"]:
                opts = "defaults,noatime,discard"
            elif myfmt == "btrfs":
                opts = ("defaults,noatime,compress=lzo,ssd,discard,"
                        "space_cache,autodefrag,inode_cache")
            else:
                opts = "defaults,noatime"
        return opts

    def run(self):
        """ Create /etc/fstab file """

        all_lines = [
            "# /etc/fstab: static file system information.",
            "#",
            "# Use 'blkid' to print the universally unique identifier for a",
            "# device; this may be used with UUID= as a more robust way to name devices",
            "# that works even if disks are added and removed. See fstab(5).",
            "#",
            "# <file system> <mount point>   <type>  <options>       <dump>  <pass>",
            "#"]

        # Use lsblk to be able to match LUKS UUID with mapper UUID
        pknames = fs.get_pknames()

        for mount_point in self.mount_devices:
            partition_path = self.mount_devices[mount_point]
            uuid = fs.get_uuid(partition_path)
            if uuid == "":
                logging.warning(
                    "Can't get %s partition UUID. It won't be added to fstab",
                    partition_path)
                continue

            if partition_path in self.fs_devices:
                myfmt = self.fs_devices[partition_path]
            else:
                # It hasn't any filesystem defined, skip it.
                continue

            # Take care of swap partitions
            if "swap" in myfmt:
                txt = self.get_swap_fstab_line(uuid, partition_path)
                all_lines.append(txt)
                logging.debug("Added %s to fstab", txt)
                continue

            # Fix for home + luks, no lvm (from Automatic Install)
            if ("/home" in mount_point and
                    self.method == "automatic" and
                    self.use_luks and not self.use_lvm and
                    '/dev/mapper' in partition_path):

                keyfile = '/etc/luks-keys/home'
                if self.luks_root_password:
                    # Use password and not a keyfile
                    keyfile = 'none'

                vol_name = partition_path[len("/dev/mapper/"):]
                self.add_vol_to_crypttab(vol_name, uuid, keyfile)

                # Add cryptAntergosHome line to fstab
                txt = self.get_device_fstab_line(partition_path, mount_point, myfmt)
                all_lines.append(txt)
                continue

            # Add all LUKS partitions from Advanced Install (except root).
            if (self.method == 'advanced' and
                    mount_point is not '/' and
                    self.use_luks and '/dev/mapper' in partition_path):

                # As the mapper with the filesystem will have a different UUID
                # than the partition it is encrypted in, we have to take care
                # of this here. Then we will be able to add it to crypttab
                try:
                    vol_name = partition_path[len("/dev/mapper/"):]
                    luks_partition_path = "/dev/" + pknames[vol_name]
                except KeyError:
                    logging.error(
                        "Can't find the PKNAME value of %s",
                        partition_path)
                    continue

                luks_uuid = fs.get_uuid(luks_partition_path)
                if luks_uuid:
                    self.add_vol_to_crypttab(vol_name, luks_uuid)
                else:
                    logging.error(
                        "Can't add luks uuid to crypttab for %s partition",
                        luks_partition_path)
                    continue

                # Finally, the fstab line to mount the unencrypted file system
                # if a mount point has been specified by the user
                if mount_point:
                    txt = self.get_device_fstab_line(partition_path, mount_point, myfmt)
                    all_lines.append(txt)
                continue

            # Avoid adding a partition to fstab when it has no mount point
            # (swap has been checked above)
            if mount_point == "":
                continue

            # fstab uses vfat to mount fat16 and fat32 partitions
            if "fat" in myfmt:
                myfmt = 'vfat'

            # Create mount point on destination system if it yet doesn't exist
            full_path = os.path.join(PostFstab.DEST_DIR, mount_point)
            os.makedirs(full_path, mode=0o755, exist_ok=True)

            # Is ssd ?
            # Device list example: {'/dev/sdb': False, '/dev/sda': True}
            txt = "Device list : {0}".format(self.ssd)
            logging.debug(txt)
            device = re.sub("[0-9]+$", "", partition_path)
            is_ssd = self.ssd.get(device)
            txt = "Device: {0}, SSD: {1}".format(device, is_ssd)
            logging.debug(txt)

            # Get mount options
            opts = self.get_mount_options(myfmt, is_ssd)
            chk = '0'
            if mount_point == "/":
                if myfmt not in ['btrfs', 'f2fs']:
                    chk = '1'
                self.root_uuid = uuid

            txt = self.get_uuid_fstab_line(uuid, mount_point, myfmt, opts, chk)
            all_lines.append(txt)

        full_text = '\n'.join(all_lines) + '\n'

        fstab_path = os.path.join(PostFstab.DEST_DIR, 'etc/fstab')
        with open(fstab_path, 'w') as fstab_file:
            fstab_file.write(full_text)
