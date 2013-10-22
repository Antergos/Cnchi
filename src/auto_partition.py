#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  auto_partition.py
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

import os
import subprocess
import logging
import time

class AutoPartition():
    def __init__(self, dest_dir, auto_device, use_luks, use_lvm):
        self.dest_dir = dest_dir
        self.auto_device = auto_device

        self.uefi = False
        
        if os.path.exists("/sys/firmware/efi/systab"):
            self.uefi = True

        self.luks = use_luks
        self.lvm = use_lvm
        
    def check_output(self, command):
        return subprocess.check_output(command.split()).decode().strip("\n")
    
    def get_fs_uuid(self, device):
        return self.check_output("blkid -p -i -s UUID -o value %s" % device)
    
    def get_fs_label(self, device):
        return self.check_output("blkid -p -i -s LABEL -o value %s" % device)
        
    def printk(self, enable):
        with open("/proc/sys/kernel/printk", "wt") as f:
            if enable:
                f.write("4")
            else:
                f.write("0")

    def umount_all(self):
        subprocess.check_call(["swapoff", "-a"])

        mount = subprocess.check_output("mount").decode().split("\n")

        # umount all devices mounted inside self.dest_dir (if any)
        devices = []
        for m in mount:
            if self.dest_dir+"/" in m:
                devices.append(m.split()[0])

        for d in devices:
            subprocess.call(["umount", d])

        # umount the device that is mounted in self.dest_dir (if any)
        devices = []
        for m in mount:
            if self.dest_dir+" " in m:
                devices.append(m.split()[0])

        for d in devices:
            subprocess.call(["umount", d])
        
        # Remove all previous LVM 
        if os.path.exists("/dev/mapper/AntergosRoot"):
            subprocess.checK_call(["lvremove", "-f", "/dev/mapper/AntergosRoot"])
        if os.path.exists("/dev/mapper/AntergosSwap"):
            subprocess.checK_call(["lvremove", "-f", "/dev/mapper/AntergosSwap"])
        if os.path.exists("/dev/AntergosVG"):
            subprocess.check_call(["vgremove", "-f", "AntergosVG"])
        pvolumes = self.check_output("pvs -o pv_name --noheading").split("\n")
        if len(pvolumes[0]) > 0:
            for pv in pvolumes:
                pv = pv.strip(" ")
                subprocess.check_call(["pvremove", "-f", pv])

        # close cryptAntergos (it may have been left open because of a previous failed installation)
        if os.path.exists("/dev/mapper/cryptAntergos"):
            subprocess.check_call(["cryptsetup", "luksClose", "/dev/mapper/cryptAntergos"])


    def mkfs(self, device, fs_type, mount_point, label_name, fs_options="", btrfs_devices=""):
        # we have two main cases: "swap" and everything else.
        if fs_type == "swap":
            try:
                swap_devices = self.check_output("swapon -s")
                if device in swap_devices:
                    subprocess.check_call(["swapoff", device])
                subprocess.check_call(["mkswap", "-L", label_name, device])
                subprocess.check_call(["swapon", device])
            except subprocess.CalledProcessError as e:
                logging.warning(e.output)
        else:
            mkfs = { "xfs" : "mkfs.xfs %s -L %s -f %s" % (fs_options, label_name, device),
                     "jfs" : "yes | mkfs.jfs %s -L %s %s" % (fs_options, label_name, device),
                     "reiserfs" : "yes | mkreiserfs %s -l %s %s" % (fs_options, label_name, device),
                     "ext2" : "mkfs.ext2 -q -L %s %s %s" % (fs_options, label_name, device),
                     "ext3" : "mke2fs -q %s -L %s -t ext3 %s" % (fs_options, label_name, device),
                     "ext4" : "mke2fs -q %s -L %s -t ext4 %s" % (fs_options, label_name, device),
                     "btrfs" : "mkfs.btrfs %s -L %s %s" % (fs_options, label_name, btrfs_devices),
                     "nilfs2" : "mkfs.nilfs2 %s -L %s %s" % (fs_options, label_name, device),
                     "ntfs-3g" : "mkfs.ntfs %s -L %s %s" % (fs_options, label_name, device),
                     "vfat" : "mkfs.vfat %s -n %s %s" % (fs_options, label_name, device) }

            # make sure the fs type is one we can handle
            if fs_type not in mkfs.keys():
                logging.error("Unkown filesystem type %s" % fs_type)
                return
            
            command = mkfs[fs_type]
            
            try:
                subprocess.check_call(command.split())
            except subprocess.CalledProcessError as e:
                logging.error(e.output)
                return

            time.sleep(4)

            # create our mount directory
            path = self.dest_dir + mount_point
            subprocess.check_call(["mkdir", "-p", path])

            # mount our new filesystem
            subprocess.check_call(["mount", "-t", fs_type, device, path])

            # change permission of base directories to correct permission
            # to avoid btrfs issues
            mode = "755"
            
            if mount_point == "/tmp":
                mode = "1777"
            elif mount_point == "/root":
                mode = "750"
                    
            subprocess.check_call(["chmod", mode, path])
        
        fs_uuid = self.get_fs_uuid(device)
        fs_label = self.get_fs_label(device)
        logging.debug("Device details: %s UUID=%s LABEL=%s" % (device, fs_uuid, fs_label))

    def get_devices(self):
        d = self.auto_device
        
        boot = ""
        swap = ""
        root = ""

        luks = ""    
        lvm = ""

        if self.uefi:
            boot = d + "3"
            swap = d + "4"
            root = d + "5"
        else:
            boot = d + "1"
            swap = d + "2"
            root = d + "3"

        if self.luks:
            if self.lvm:
                # LUKS and LVM
                luks = swap
                lvm = "/dev/mapper/cryptAntergos"
            else:
                # LUKS and no LVM
                luks = root
                root = "/dev/mapper/cryptAntergos"
        elif self.lvm:
            # no LUKS and LVM
            lvm = swap

        if self.lvm:
            swap = "/dev/AntergosVG/AntergosSwap"
            root = "/dev/AntergosVG/AntergosRoot"
                
        return (boot, swap, root, luks, lvm)
    
    def run(self):
        key_file = "/tmp/.keyfile"
    
        if self.uefi:
            guid_part_size = 2
            uefisys_part_size = 512
        else:
            guid_part_size = 0
            uefisys_part_size = 0

        # get just the disk size in 1000*1000 MB
        device = self.auto_device
        device_name = self.check_output("basename %s" % device)
        base_path = "/sys/block/%s" % device_name
        disc_size = 0
        if os.path.exists("%s/size" % base_path):
            with open("%s/queue/logical_block_size" % base_path, "rt") as f:
                logical_block_size = int(f.read())
            with open("%s/size" % base_path, "rt") as f:
                size = int(f.read())
            
            disc_size = ((logical_block_size * size) / 1024) / 1024
        else:
            logging.error("Setup cannot detect size of your device, please use normal "
                "installation routine for partitioning and mounting devices.")
            return
        
        boot_part_size = 256
        
        mem_total = self.check_output("grep MemTotal /proc/meminfo")
        mem_total = int(mem_total.split()[1])
        
        swap_part_size = 1536
        if mem_total <= 1572864:
            swap_part_size = mem_total / 1024

        root_part_size = disc_size - (guid_part_size + uefisys_part_size + boot_part_size + swap_part_size)

        lvm_pv_part_size = swap_part_size + root_part_size
        
        logging.debug("disc_size %dMB" % disc_size)
        logging.debug("guid_part_size %dMB" % guid_part_size)
        logging.debug("uefisys_part_size %dMB" % uefisys_part_size)
        logging.debug("boot_part_size %dMB" % boot_part_size)
        
        if self.lvm:
            logging.debug("lvm_pv_part_size %dMB" % lvm_pv_part_size)
            
        logging.debug("swap_part_size %dMB" % swap_part_size)
        logging.debug("root_part_size %dMB" % root_part_size)

        # disable swap and all mounted partitions, umount / last!
        self.umount_all()

        self.printk(False)
                
        # we assume a /dev/hdX format (or /dev/sdX)
        if self.uefi:
            # GPT (GUID) is supported only by 'parted' or 'sgdisk'
            # clean partition table to avoid issues!
            subprocess.check_call(["sgdisk", "--zap", device])

            # clear all magic strings/signatures - mdadm, lvm, partition tables etc.
            subprocess.check_call(["dd", "if=/dev/zero", "of=%s" % device, "bs=512", "count=2048", "status=noxfer"])
            subprocess.check_call(["wipefs", "-a", device])
            # create fresh GPT
            subprocess.check_call(["sgdisk", "--clear", device])
            # create actual partitions
            subprocess.check_call(['sgdisk', '--set-alignment="2048"', '--new=1:1M:+%dM' % gpt_bios_grub_part_size, '--typecode=1:EF02', '--change-name=1:BIOS_GRUB', device])
            subprocess.check_call(['sgdisk', '--set-alignment="2048"', '--new=2:0:+%dM' % uefisys_part_size, '--typecode=2:EF00', '--change-name=2:UEFI_SYSTEM', device])
            subprocess.check_call(['sgdisk', '--set-alignment="2048"', '--new=3:0:+%dM' % boot_part_size, '--typecode=3:8300', '--attributes=3:set:2', '--change-name=3:ANTERGOS_BOOT', device])

            if self.lvm:
                subprocess.check_call(['sgdisk', '--set-alignment="2048"', '--new=4:0:+%dM' % lvm_pv_part_size, '--typecode=4:8200', '--change-name=4:ANTERGOS_LVM', device])
            else:
                subprocess.check_call(['sgdisk', '--set-alignment="2048"', '--new=4:0:+%dM' % swap_part_size, '--typecode=4:8200', '--change-name=4:ANTERGOS_SWAP', device])
                subprocess.check_call(['sgdisk', '--set-alignment="2048"', '--new=5:0:+%dM' % root_part_size, ' --typecode=5:8300', '--change-name=5:ANTERGOS_ROOT', device])
            
            logging.debug(self.check_output("sgdisk --print %s" % device))
        else:
            # start at sector 1 for 4k drive compatibility and correct alignment
            # clean partitiontable to avoid issues!
            subprocess.check_call(["dd", "if=/dev/zero", "of=%s" % device, "bs=512", "count=2048", "status=noxfer"])
            subprocess.check_call(["wipefs", "-a", device])

            # create DOS MBR with parted
            subprocess.check_call(["parted", "-a", "optimal", "-s", device, "mktable", "msdos"])

            # create boot partition
            subprocess.check_call(["parted", "-a", "optimal", "-s", device, "mkpart", "primary", "1", str(boot_part_size)])
            subprocess.check_call(["parted", "-a", "optimal", "-s", device, "set", "1", "boot", "on"])
            
            if self.lvm:
                start = boot_part_size
                end = start + lvm_pv_part_size
                # create partition for lvm (will store root and swap logical volumes)
                subprocess.check_call(["parted", "-a", "optimal", "-s", device, "mkpart", "primary", str(start), "100%"])
            else:
                start = boot_part_size
                end = start + swap_part_size
                # create swap partition
                subprocess.check_call(["parted", "-a", "optimal", "-s", device, "mkpart", "primary", str(start), str(end)])
                # create root partition
                subprocess.check_call(["parted", "-a", "optimal", "-s", device, "mkpart", "primary", str(end), "100%"])

        self.printk(True)

        ## wait until /dev initialized correct devices
        subprocess.check_call(["udevadm", "settle"])
        
        (boot_device, swap_device, root_device, luks_device, lvm_device) = self.get_devices()
        
        logging.debug("Boot %s, Swap %s, Root %s" % (boot_device, swap_device, root_device))
        
        if self.luks:
            logging.debug("Will setup LUKS on device %s" % luks_device)
                        
            # Wipe LUKS header (just in case we're installing on a pre LUKS setup)
            # For 512 bit key length the header is 2MB
            # If in doubt, just be generous and overwrite the first 10MB or so
            subprocess.check_call(["dd", "if=/dev/zero", "of=%s" % luks_device, "bs=512", "count=20480", "status=noxfer"])
        
            # Create a random keyfile
            subprocess.check_call(["dd", "if=/dev/urandom", "of=%s" % key_file, "bs=1024", "count=4", "status=noxfer"])
            
            # Setup luks
            subprocess.check_call(["cryptsetup", "luksFormat", "-q", "-c", "aes-xts-plain", "-s", "512", luks_device, key_file])
            subprocess.check_call(["cryptsetup", "luksOpen", luks_device, "cryptAntergos", "-q", "--key-file", key_file])

        if self.lvm:
            # /dev/sdX1 is /boot
            # /dev/sdX2 is the PV
            
            logging.debug("Will setup LVM on device %s" % lvm_device)

            subprocess.check_call(["pvcreate", "-ff", lvm_device])
            subprocess.check_call(["vgcreate", "-v", "AntergosVG", lvm_device])
            
            subprocess.check_call(["lvcreate", "-n", "AntergosRoot", "-L", str(int(root_part_size)), "AntergosVG"])
            
            # Use the remainig space for our swap volume
            subprocess.check_call(["lvcreate", "-n", "AntergosSwap", "-l", "100%FREE", "AntergosVG"])

        ## Make sure the "root" partition is defined first
        self.mkfs(root_device, "ext4", "/", "AntergosRoot")
        self.mkfs(swap_device, "swap", "", "AntergosSwap")
        self.mkfs(boot_device, "ext2", "/boot", "AntergosBoot")
        
        if self.luks:
            # https://wiki.archlinux.org/index.php/Encrypted_LVM

            # NOTE: encrypted and/or lvm2 hooks will be added to mkinitcpio.conf in installation_process.py
            # NOTE: /etc/default/grub will be modified in installation_process.py, too.
            
            # Copy keyfile to boot partition, user will choose what to do with it
            # THIS IS NONSENSE (BIG SECURITY HOLE), BUT WE TRUST THE USER TO FIX THIS
            # User shouldn't store the keyfiles unencrypted unless the medium itself is reasonably safe
            # (boot partition is not)
            # Maybe instead of using a keyfile we should use a password...
            subprocess.check_call(['chmod', '0400', key_file])
            subprocess.check_call(['cp', key_file, '%s/boot' % self.dest_dir])
            subprocess.check_call(['rm', key_file])

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)
    logger.addHandler(sh)


    ap = AutoPartition("/install", "/dev/sdb", use_luks=False, use_lvm=True)
    ap.run()
