# -*- coding: utf-8; Mode: Python; indent-tabs-mode: nil; tab-width: 4 -*-
#
#  zfs_manager.py
#
# Copyright © 2013-2018 Antergos
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

""" ZFS helper methods """

import subprocess
import os
import logging
import shutil
import time
import re

from misc.extra import InstallError
from misc.run_cmd import call
from installation import wrapper

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

# Partition sizes are in MiB
MAX_ROOT_SIZE = 30000
MAX_ROOT_SIZE_GB = MAX_ROOT_SIZE // 1024

# KDE (with all features) needs 8 GB for its files
# (including pacman cache xz files).
MIN_ROOT_SIZE = 8000
MIN_ROOT_SIZE_GB = MIN_ROOT_SIZE // 1024

DEST_DIR = "/install"

ZFS_POOL_TYPES = {0: "None", 1: "Stripe", 2: "Mirror", 3: "RAID-Z", 4: "RAID-Z2", 5: "RAID-Z3"}

def zfs_init_device(device_path, scheme="GPT"):
    """ Initialize device """

    logging.debug("Zapping device %s...", device_path)

    offset = 20480

    # Zero out all GPT and MBR data structures
    wrapper.sgdisk("zap-all", device_path)

    # Clear all magic strings/signatures
    # Wipe out first "offset" sectors
    wrapper.run_dd("/dev/zero", device_path, bytes_block=512, count=offset)

    # Clear the end "offset" sectors of the disk, too.
    try:
        seek = int(call(["blockdev", "--getsz", device_path])) - offset
        wrapper.run_dd("/dev/zero", device_path, bytes_block=512, count=offset, seek=seek)
    except ValueError as ex:
        logging.warning(ex)

    wrapper.wipefs(device_path, fatal=True)

    if scheme == "GPT":
        # Create fresh GPT table
        wrapper.sgdisk("clear", device_path)

        # Inform the kernel of the partition change.
        # Needed if the hard disk had a MBR partition table.
        call(["partprobe", device_path])
    else:
        # Create fresh MBR table
        wrapper.parted_mklabel(device_path, "msdos")

    call(["sync"])


def zfs_get_pool_size(pool_name):
    """ Gets zfs pool size in GB """
    try:
        cmd_line = "zpool list -H -o size {0}".format(pool_name)
        logging.debug(cmd_line)
        cmd = cmd_line.split()
        output = subprocess.check_output(cmd)
        pool_size = output.decode().strip('\n')
        pool_size_str = pool_size.replace(',', '.')
        if '.' in pool_size_str:
            pool_size = int(float(pool_size_str[:-1]))
        else:
            pool_size = int(pool_size_str[:-1])
        if 'M' in pool_size_str:
            pool_size //= 1024
        elif 'T' in pool_size_str:
            pool_size = pool_size * 1024
        elif 'P' in pool_size_str:
            pool_size = pool_size * 1024 * 1024
    except (subprocess.CalledProcessError, ValueError) as err:
        logging.warning(
            "Can't get zfs %s pool size: %s",
            pool_name,
            err)
        pool_size = 0
    return pool_size


def zfs_get_home_size(pool_name):
    """ Get recommended /home zvol size in GB """
    pool_size = zfs_get_pool_size(pool_name)
    home_size = 0

    if pool_size != 0:
        root_needs = pool_size // 5
        if root_needs > MAX_ROOT_SIZE_GB:
            root_needs = MAX_ROOT_SIZE_GB
        elif root_needs < MIN_ROOT_SIZE_GB:
            root_needs = MIN_ROOT_SIZE_GB
        home_size = pool_size - root_needs
    return home_size


def zfs_get_swap_size(pool_name):
    """ Gets recommended swap size in GB """

    cmd = ["/usr/bin/grep", "MemTotal", "/proc/meminfo"]
    try:
        mem_total = subprocess.check_output(cmd).decode().split()
        mem_total = int(mem_total[1])
        mem = mem_total / 1024
    except (subprocess.CalledProcessError, ValueError) as _mem_error:
        logging.warning("Can't get system memory")
        mem = 4096

    swap_size = 0

    # Suggested sizes from Anaconda installer (these are in MB)
    if mem < 2048:
        swap_size = 2 * mem
    elif 2048 <= mem < 8192:
        swap_size = mem
    elif 8192 <= mem < 65536:
        swap_size = mem // 2
    else:
        swap_size = 4096

    # MB to GB
    swap_size = swap_size // 1024

    # Check pool size and adapt swap size if necessary
    # Swap size should not exceed 10% of all available pool size

    pool_size = zfs_get_pool_size(pool_name)
    if pool_size > 0:
        # Max swap size is 10% of all available disk size
        max_swap = pool_size * 0.1
        if swap_size > max_swap:
            swap_size = max_swap
    return swap_size


def set_zfs_mountpoint(zvol, mount_point):
    """ Sets mount point of zvol and tries to mount it.
        It does it but then ZFS tries to automount it and fails
        because we set mountpoint to / instead of /install. ZFS cannot
        mount it because / is not empty (same for /home if it's in a zvol). """
    try:
        cmd = ["/usr/bin/zfs", "set",
               "mountpoint={0}".format(mount_point), zvol]
        _output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        err_output = err.output.decode().strip("\n")
        # It's ok if it fails
        logging.debug(err_output)


def get_partition_path(device, part_num):
    """ Form partition path from device and partition number """
    full_path = ""
    # Remove /dev/
    path = device.replace('/dev/', '')
    partials = ['rd/', 'ida/', 'cciss/', 'sx8/', 'mapper/', 'mmcblk', 'md', 'nvme']
    found = [p for p in partials if path.startswith(p)]
    if found:
        full_path = "{0}p{1}".format(device, part_num)
    else:
        full_path = "{0}{1}".format(device, part_num)
    return full_path


def clear_dest_dir():
    """ Empties /install """

    boot = "{0}/boot".format(DEST_DIR)

    # Check that /install/boot and /install are not mounted
    call(["/usr/bin/umount", boot], warning=False)
    call(["/usr/bin/umount", DEST_DIR], warning=False)
    call(["/usr/bin/zfs", "umount", "-a"], warning=False)

    # Delete /install contents
    for file_name in os.listdir(DEST_DIR):
        file_path = os.path.join(DEST_DIR, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except OSError as err:
            logging.warning(err)


def load_existing_pools():
    """ Fills existing_pools dict with pool's name,
        identifier and status """

    existing_pools = {}
    output = call(["zpool", "import"])
    if output:
        name = identifier = state = None
        lines = output.split("\n")
        for line in lines:
            if "pool:" in line:
                # Pool info starts
                name = line.split(": ")[1]
                identifier = state = None
            elif "id:" in line:
                identifier = line.split(": ")[1]
            elif "state:" in line:
                state = line.split(": ")[1]
                existing_pools[name] = (identifier, state)
    return existing_pools


def do_destroy_zfs_pools():
    """ Try to destroy existing antergos zfs pools """
    existing_pools = load_existing_pools()

    for pool_name in existing_pools:
        if "antergos" in pool_name.lower():
            #pool_id, pool_state = self.existing_pools[pool_name]
            destroy_cmd = ['/usr/bin/zpool', 'destroy', '-f', pool_name]
            if not call(destroy_cmd, warning=False):
                destroy_cmd = ['/usr/bin/zfs', 'destroy', '-R', '-f', pool_name]
                call(destroy_cmd, warning=False)


def get_pool_id(pool_name, include_offline=False):
    """ Returns pool's identifier and status """

    existing_pools = load_existing_pools()

    if pool_name in existing_pools:
        identifier, state = existing_pools[pool_name]
        if "ONLINE" in state or include_offline:
            return identifier, state
    return None, None


def zfs_pool_name_is_valid(name):
    """ Checks that pool name is a valid name """
    allowed = re.search(r'([a-zA-Z0-9_\-\.: ])+', name)
    reserved = re.match(r'c[0-9]([a-zA-Z0-9_\-\.: ])+', name)

    reserved = ['mirror', 'raidz', 'spare', 'log'] if not reserved else []
    valid = False

    if allowed and reserved and name not in reserved:
        valid = True

    return valid

def settle():
    """ Wait until in /dev initialized correct devices """
    call(["/usr/bin/udevadm", "settle"])
    call(["/usr/bin/sync"])


def create_zfs_pool(pool_name, pool_type, device_paths, force_4k):
    """ Create zpool """

    if pool_type not in ZFS_POOL_TYPES.values():
        raise InstallError("Unknown pool type: {0}".format(pool_type))

    # for device_path in device_paths:
    #    cmd = ["zpool", "labelclear", device_path]
    #    call(cmd)

    cmd = ["/usr/bin/zpool", "create"]

    if force_4k:
        cmd.extend(["-o", "ashift=12"])

    cmd.extend(["-m", DEST_DIR, pool_name])

    pool_type = pool_type.lower().replace("-", "")

    if pool_type in ["none", "stripe"]:
        # Add first device
        cmd.append(device_paths[0])
    elif pool_type == "mirror":
        if len(device_paths) > 2 and len(device_paths) % 2 == 0:
            # Try to mirror pair of devices
            # (mirrors of two devices each)
            for i, k in zip(device_paths[0::2], device_paths[1::2]):
                cmd.append(pool_type)
                cmd.extend([i, k])
        else:
            cmd.append(pool_type)
            cmd.extend(device_paths)
    else:
        cmd.append(pool_type)
        cmd.extend(device_paths)

    settle()

    logging.debug("Creating zfs pool %s...", pool_name)
    if call(cmd, warning=False) is False:
        # Try again, now with -f
        cmd.insert(2, "-f")
        if call(cmd, warning=False) is False:
            # Wait 10 seconds more and try again.
            # (Waiting a bit sometimes works)
            time.sleep(10)
            call(cmd, fatal=True)

    settle()

    if pool_type == "stripe":
        # Add the other devices that were left out
        cmd = ["zpool", "add", pool_name]
        cmd.extend(device_paths[1:])
        call(cmd, fatal=True)

    logging.debug("Pool %s created.", pool_name)
