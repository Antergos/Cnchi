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

import math
import logging
import os
import re
import shutil
import subprocess
import time

from misc.extra import InstallError
from misc.run_cmd import call
from installation import wrapper

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

#class

# Partition sizes are in MiB
MAX_ROOT_SIZE = 30000
MAX_ROOT_SIZE_GB = MAX_ROOT_SIZE // 1024

# KDE (with all features) needs 8 GB for its files
# (including pacman cache xz files).
MIN_ROOT_SIZE = 8000
MIN_ROOT_SIZE_GB = MIN_ROOT_SIZE // 1024

DEST_DIR = "/install"

ZFS_POOL_TYPES = {0: "None", 1: "Stripe", 2: "Mirror", 3: "RAID-Z", 4: "RAID-Z2", 5: "RAID-Z3"}

def init_device(device_path, scheme="GPT"):
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

    settle()


def get_pool_size(pool_name):
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
            pool_size = pool_size // 1024
        elif 'T' in pool_size_str:
            pool_size = pool_size * 1024
        elif 'P' in pool_size_str:
            # 1024 * 1024 = 1048576
            pool_size = pool_size * 1048576
    except (subprocess.CalledProcessError, ValueError) as err:
        logging.warning("Can't get zfs %s pool size: %s", pool_name, err)
        pool_size = 0
    return pool_size


def get_home_size(pool_name):
    """ Get recommended /home zvol size in GB """
    pool_size = get_pool_size(pool_name)
    home_size = 0

    if pool_size != 0:
        root_needs = pool_size // 5
        if root_needs > MAX_ROOT_SIZE_GB:
            root_needs = MAX_ROOT_SIZE_GB
        elif root_needs < MIN_ROOT_SIZE_GB:
            root_needs = MIN_ROOT_SIZE_GB
        home_size = pool_size - root_needs
    return home_size


def get_swap_size(pool_name):
    """ Gets recommended swap size in GB """

    cmd = ["grep", "MemTotal", "/proc/meminfo"]
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

    pool_size = get_pool_size(pool_name)
    if pool_size > 0:
        # Max swap size is 10% of all available disk size
        max_swap = pool_size * 0.1
        if swap_size > max_swap:
            swap_size = max_swap
    return swap_size


def set_mountpoint(zvol, mount_point):
    """ Sets mount point of zvol and tries to mount it.
        It does it but then ZFS tries to automount it and fails
        because we set mountpoint to / instead of /install. ZFS cannot
        mount it because / is not empty (same for /home if it's in a zvol). """
    try:
        cmd = [
            "/usr/bin/zfs",
            "set",
            "mountpoint={0}".format(mount_point),
            zvol]
        _output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        err_output = err.output.decode().strip("\n")
        # It's ok if it fails
        logging.debug(err_output)


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


def destroy_pools():
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


def pool_name_is_valid(name):
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


def create_pool(pool_name, pool_type, device_paths, force_4k):
    """ Create zpool """

    if pool_type not in ZFS_POOL_TYPES.values():
        raise InstallError("Unknown pool type: {0}".format(pool_type))

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


def create_swap(pool_name, vol_name):
    """ mkswap on a zfs zvol """

    zvol = "{0}/{1}".format(pool_name, vol_name)

    call(["/usr/bin/zfs", "set", "com.sun:auto-snapshot=false", zvol])
    call(["/usr/bin/zfs", "set", "sync=always", zvol])

    path = "/dev/zvol/{0}/swap".format(pool_name)
    if os.path.exists(path):
        logging.debug("Formatting swap (%s)", path)
        call(["mkswap", "-f", path])
    else:
        logging.warning("Can't find %s to create swap on it", path)

def create_vol(pool_name, vol_name, swap_size=None):
    """ Creates zfs vol inside the pool
        if size is given, it should be in GB.
        If vol_name is "swap" it will be setup as a swap space """

    cmd = ["/usr/bin/zfs", "create"]

    if swap_size:
        # If size is given, mountpoint cannot be set (zfs)
        # Round up
        swap_size = math.ceil(swap_size)
        logging.debug(
            "Creating a zfs vol %s/%s of size %dGB",
            pool_name, vol_name, swap_size)
        cmd.extend(["-V", "{0}G".format(swap_size)])
    else:
        logging.debug("Creating a zfs vol %s/%s", pool_name, vol_name)
        if vol_name == "swap":
            cmd.extend(["-o", "mountpoint=none"])
        else:
            cmd.extend(
                ["-o", "mountpoint={0}/{1}".format(DEST_DIR, vol_name)])

    cmd.append("{0}/{1}".format(pool_name, vol_name))
    call(cmd, fatal=True)

    if vol_name == "swap":
        create_swap(pool_name, vol_name)


def get_partition_path(device, part_num):
    """ Form partition path from device and partition number """

    # Remove /dev/
    path = device.replace('/dev/', '')
    partials = [
        'rd/', 'ida/', 'cciss/', 'sx8/', 'mapper/', 'mmcblk', 'md', 'nvme']
    found = [p for p in partials if path.startswith(p)]
    if found:
        return "{0}p{1}".format(device, part_num)
    return "{0}{1}".format(device, part_num)

#########################################################################################

# BIOS/MBR (Grub)
# 1 Solaris (bf00)

# BIOS/GPT (Grub)
# 1 2M BIOS boot partition (ef02)
# 2 Solaris (bf00)

# UEFI/GPT (rEFInd / systemd-boot)
# 1 512M EFI boot partition (ef00) (/boot) (vfat)
# 2 Solaris (bf00)

# UEFI/GPT (Grub)
# 1 512M EFI boot partition (ef00) (/boot/efi) (vfat)
# 2 512M boot partition (/boot) (ext4)
# 3 Solaris (bf00)

def create_efi_partition(self, device_path, part_num, mount_point):
    """ Create and format EFI partition (512MB) in /boot or in /boot/efi """
    if mount_point == '/boot/efi':
        tag = 'efi'
    else:
        tag = 'boot'

    wrapper.sgdisk_new(device_path, part_num, 'EFI', 512, 'EF00')
    self.devices[tag] = get_partition_path(device_path, part_num)
    self.fs_devices[self.devices[tag]] = 'vfat'
    self.mount_devices[mount_point] = self.devices[tag]
    fs.create_fs(self.devices[tag], 'vfat', 'EFI')

def create_boot_partition(self, device_path, part_num):
    """ Create and format BOOT or EFI partitions (512MB) in /boot or in /boot/efi """
    wrapper.sgdisk_new(device_path, part_num, 'ANTERGOS_BOOT', 512, '8300')
    self.devices['boot'] = get_partition_path(device_path, part_num)
    self.fs_devices[self.devices['boot']] = 'ext4'
    self.mount_devices['/boot'] = self.devices['boot']
    fs.create_fs(self.devices['boot'], 'ext4', 'ANTERGOS_BOOT')

def run_format_gpt(self, device_path):
    """ GPT harddisk schemes """
    solaris_part_num = 2
    if not self.uefi:
        # BIOS/GPT (Grub)
        # 1 2M BIOS boot partition (ef02)
        wrapper.sgdisk_new(device_path, 1, 'BIOS_BOOT', 2, 'EF02')
    else:
        if self.bootloader == 'grub2':
            # UEFI/GPT (Grub)
            # 1 512M EFI boot partition (ef00) (/boot/efi) (vfat)
            self.create_efi_partition(device_path, 1, '/boot/efi')
            # 2 512M boot partition (8300) (/boot) (ext4)
            self.create_boot_partition(device_path, 2)
            solaris_part_num = 3
        else:
            # UEFI/GPT (rEFInd / systemd-boot)
            # 1 512M EFI boot partition (ef00) (/boot) (vfat)
            self.create_efi_partition(device_path, 1, '/boot')
    return solaris_part_num

#########################################################################################

def setup(zfs_options, use_home=False):
    """ Setup ZFS system """
    # https://wiki.archlinux.org/index.php/Installing_Arch_Linux_on_ZFS
    # https://wiki.archlinux.org/index.php/ZFS#GRUB-compatible_pool_creation

    device_paths = zfs_options['device_paths']
    logging.debug("Configuring ZFS in %s", ",".join(device_paths))

    # Read all preexisting zfs pools. If there's an antergos one, delete it.
    destroy_pools()

    # Wipe all disks that will be part of the installation.
    # This cannot be undone!
    scheme = zfs_options['scheme']
    init_device(device_paths[0], scheme)
    for device_path in device_paths[1:]:
        init_device(device_path, scheme)

    device_path = device_paths[0]

    self.settings.set('bootloader_device', device_path)

    if scheme == 'GPT':
        solaris_partition_number = self.run_format_gpt(device_path)
        # The rest of the disk will be of solaris type
        # (2 or 3) Solaris (bf00)
        wrapper.sgdisk_new(device_path, solaris_part_num, 'ANTERGOS_ZFS', 0, 'BF00')
    else:
        # BIOS/MBR (Grub)
        # 1 Solaris (bf00)
        start = -1
        wrapper.parted_mkpart(device_path, 'primary', start, '-1s')
        # Set boot partition as bootable
        wrapper.parted_set(device_path, '1', 'boot', 'on')
        solaris_partition_number = 1

    root_device = get_partition_path(device_path, solaris_partition_number)

    zfs.settle()

    # Make sure the ZFS modules are loaded
    call(['modprobe', 'zfs'])

    # Empty DEST_DIR or zfs pool will fail to mount on it
    # (this will delete preexisting installing attempts, too)
    if os.path.exists(DEST_DIR):
        clear_dest_dir()

    device_paths = zfs_options['device_paths']
    if not device_paths:
        txt = _("No devices were selected for the ZFS pool")
        raise InstallError(txt)

    # Using by-id (recommended) does not work atm
    # https://github.com/zfsonlinux/zfs/issues/3708

    # Can't use the whole first disk, just the dedicated zfs partition
    device_paths[0] = get_partition_path(device_paths[0], solaris_partition_number)

    line = ", ".join(device_paths)
    logging.debug("Cnchi will create a ZFS pool using %s devices", line)

    # Just in case...
    if os.path.exists('/etc/zfs/zpool.cache'):
        os.remove('/etc/zfs/zpool.cache')

    try:
        os.mkdir(DEST_DIR, mode=0o755)
    except OSError:
        pass

    pool_name = zfs_options['pool_name']
    pool_type = zfs_options['pool_type']

    if not pool_name_is_valid(pool_name):
        txt = _(
            "Pool name {0} is invalid. It must contain only alphanumeric characters (a-zA-Z0-9_), "
            "hyphens (-), colons (:), and/or spaces ( ). Names starting with the letter 'c' "
            "followed by a number (c[0-9]) are not allowed. The following names are also not "
            "allowed: 'mirror', 'raidz', 'spare' and 'log'.")
        txt = txt.format(pool_name)
        raise InstallError(txt)

    # Create zpool
    create_pool(pool_name, pool_type, device_paths, zfs_options['force_4k'])

    # Set the mount point of the root filesystem
    set_mountpoint(pool_name, "/")

    # Set the bootfs property on the descendant root filesystem so the
    # boot loader knows where to find the operating system.
    cmd = ["/usr/bin/zpool", "set", "bootfs={0}".format(pool_name), pool_name]
    call(cmd, fatal=True)

    # Create zpool.cache file
    cmd = ["/usr/bin/zpool", "set", "cachefile=/etc/zfs/zpool.cache", pool_name]
    call(cmd, fatal=True)

    if use_home:
        # Create home zvol
        logging.debug("Creating zfs subvolume 'home'")
        create_vol(pool_name, "home")
        set_mountpoint("{0}/home".format(pool_name), "/home")
        # ZFS automounts, we have to unmount /install/home and delete the folder,
        # otherwise we won't be able to import the zfs pool later
        home_path = "{0}/home".format(DEST_DIR)
        call(["/usr/bin/zfs", "umount", home_path], warning=False)
        shutil.rmtree(path=home_path, ignore_errors=True)

    # Create swap zvol (it has to be named "swap")
    swap_size = get_swap_size(pool_name)
    create_vol(pool_name, "swap", swap_size)
    settle()

    # Export the pool
    # Makes the kernel to flush all pending data to disk, writes data to
    # the disk acknowledging that the export was done, and removes all
    # knowledge that the storage pool existed in the system
    logging.debug("Exporting pool %s...", pool_name)
    call(["/usr/bin/zpool", "export", "-f", pool_name], fatal=True)

    # Let's get the id of the pool (to import it)
    pool_id, _status = get_pool_id(pool_name)

    if not pool_id:
        # Something bad has happened. Will try using the pool name instead.
        logging.warning("Can't get %s zpool id", pool_name)
        pool_id = pool_name

    # Finally, re-import the pool by-id
    # DEST_DIR must be empty or importing will fail!
    logging.debug("Importing pool %s (%s)...", pool_name, pool_id)
    cmd = ["/usr/bin/zpool", "import", "-f", "-d", "/dev/disk/by-id", "-R", DEST_DIR, pool_id]
    call(cmd, fatal=True)

    # Copy zpool cache file to destination
    try:
        dst_dir = os.path.join(DEST_DIR, "etc/zfs")
        os.makedirs(dst_dir, mode=0o755, exist_ok=True)
        src = "/etc/zfs/zpool.cache"
        dst = os.path.join(dst_dir, "zpool.cache")
        shutil.copyfile(src, dst)
    except OSError as copy_error:
        logging.warning(copy_error)

    # Store hostid
    hostid = call(["/usr/bin/hostid"])
    if hostid:
        hostid_path = os.path.join(DEST_DIR, "etc/hostid")
        with open(hostid_path, 'w') as hostid_file:
            hostid_file.write("{0}\n".format(hostid))

    return (pool_id, root_device)
