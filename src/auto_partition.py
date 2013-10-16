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
    def __init__(self, dest_dir, auto_device, settings):
        
        self.dest_dir = dest_dir
        self.auto_device = auto_device
        
        # destination of blockdevices in /sys
        block="/sys/block"
        
        self.luks = settings.get('use_luks')
        self.lvm = settings.get('use_lvm')

        # TODO: support UEFI
        self.uefi = False


    def get_fs_uuid(self, device):
        return subprocess.check_output("blkid -p -i -s UUID -o value %s" % device)
    
    def get_fs_label(self, device):
        return subprocess.check_output("blkid -p -i -s LABEL -o value %s" % device)
        
    def printk(self, enable):
        if enable:
            subprocess.call("echo 4 >/proc/sys/kernel/printk")
        else
            subprocess.call("echo 0 >/proc/sys/kernel/printk")

    def umount_all(self):
        subprocess.call(["swapoff", "-a"])

        command = "mount | grep -v %s | grep %s | sed 's|\ .*||g'" % (self.dest_dir, self.dest_dir)
        devices = subprocess.check_output(command)
        subprocess.call("umount %s" % devices)

        command = "mount | grep %s | sed 's|\ .*||g'" % self.dest_dir
        devices = subprocess.check_output(command)
        subprocess.call("umount %s" % devices)

    def mkfs(self, params):
        device = params['device']
        fs_type = params['fs_type']
        dest = params['dest']
        mount_point = params['mount_point']
        label_name = params['label_name']
        fs_options = params['fs_options']

        btrfs_devices = params['brtfs_devices']
        '''
        local _btrfsdevices="$(echo ${8} | sed -e 's|#| |g')"
        local _btrfslevel=${9}
        local _btrfssubvolume=${10}
        local _dosubvolume=${11}
        local _btrfscompress=${12}
        local _btrfsssd=${13}
        '''
        # we have two main cases: "swap" and everything else.
        if fs_type == "swap":
            try:
                subprocess.check_call(["swapoff", device])
                subprocess.check_call(["mkswap", "-L", label_name, device])
                subprocess.check_call(["swapon", device])
            except subprocess.CalledProcessError as e:
                logging.warning(e.output)
        else:
            mkfs = { "xfs" : "mkfs.xfs %s -L %s -f %s" % (fs_options, label_name, device),
                     "jfs" : "yes | mkfs.jfs %s -L %s %s" % (fs_options, label_name, device),
                     "reiserfs" : "yes | mkreiserfs %s -l %s %s" % (fs_options, label_name, device),
                     "ext2" : "mkfs.ext2 -L %s %s %s" % (fs_options, label_name, device),
                     "ext3" : "mke2fs %s -L %s -t ext3 %s" % (fs_options, label_name, device),
                     "ext4" : "mke2fs %s -L %s -t ext4 %s" % (fs_options, label_name, device),
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
                subprocess.check_call(command)
            except subprocess.CalledProcessError as e:
                logging.error(e.output)
                return

            time.sleep(4)

            # create our mount directory
            subprocess.call("mkdir -p %s%s" % (dest, mount_point))

            # mount our new filesystem
            subprocess.call("mount -t %s %s %s%s" % (fs_type, device, dest, mount_point))

            # change permission of base directories to correct permission
            # to avoid btrfs issues
            mode = "755"
            
            if mount_point == "/tmp":
                mode = "1777"
            elif mount_point == "/root":
                mode = "750"
                    
            subprocess.call("chmod %s %s%s" % (mode, dest, mount_point))
        
        fs_uuid = self.get_fs_uuid(device)
        fs_label = self.get_fs_label(device)
        logging.debug("Device details: %s UUID=%s LABEL=%s" % (device, fs_uuid, fs_label))
    
    def run(self):
        key_file = "/tmp/.keyfile"
    
        if self.uefi:
            guid_part_size = "2"
            gpt_bios_grub_part_size = "2"
            uefisys_part_size = "512"
        else:
            guid_part_size = "0"
            uefisys_part_size = "0"

        # get just the disk size in 1000*1000 MB
        device_name = subprocess.check_output("basename %s" % self.auto_device)
        base_path = "/sys/block/%s" % device_name
        if os.path.exists("%s/size" % base_path):
            with open("%s/queue/logical_block_size" % base_path, "rt") as f:
                logical_block_size = f.read()
            with open(("%s/size" % base_path, "rt") as f:
                size = f.read()
            
            disc_size = logical_block_size * size

            logical_block_size = "/sys/block/%s/size" % device
        
        disc_size = disc_size - guid_part_size - uefisys_part_size
        
        boot_part_size = 200
        disc_size = disc_size - boot_part_size
        
        mem_total = subprocess.check_output("grep MemTotal /proc/meminfo | awk '{print $2}'")
        swap_part_size = 1536
        if mem_total <= 1572864:
            swap_part_size = mem_total / 1024
        disc_size = disc_size - swap_part_size
        
        root_part_size = disc_size

        lvm_pv_part_size = swap_part_size + root_part_size

        # disable swap and all mounted partitions, umount / last!
        self.umount_all()

        self.printk(False)
        
        device = self.auto_device
        
        # we assume a /dev/hdX format (or /dev/sdX)
        if self.uefi:
            part_root = self.auto_device + "5"
            
            # GPT (GUID) is supported only by 'parted' or 'sgdisk'
            # clean partition table to avoid issues!
            subprocess.call("sgdisk --zap %s" % device)

            # clear all magic strings/signatures - mdadm, lvm, partition tables etc.
            subprocess.call("dd if=/dev/zero of=%s bs=512 count=2048" % device)
            subprocess.call("wipefs -a %s" % device)
            # create fresh GPT
            subprocess.call("sgdisk --clear %s" % device)
            # create actual partitions
            subprocess.call('sgdisk --set-alignment="2048" --new=1:1M:+%dM --typecode=1:EF02 --change-name=1:BIOS_GRUB %s' % (gpt_bios_grub_part_size, device))
            subprocess.call('sgdisk --set-alignment="2048" --new=2:0:+%dM --typecode=2:EF00 --change-name=2:UEFI_SYSTEM %s' % (uefisys_part_size, device))
            subprocess.call('sgdisk --set-alignment="2048" --new=3:0:+%dM --typecode=3:8300 --attributes=3:set:2 --change-name=3:ANTERGOS_BOOT %s' % (boot_part_size, device))

            if self.lvm:
                subprocess.call('sgdisk --set-alignment="2048" --new=4:0:+%dM --typecode=4:8200 --change-name=4:ANTERGOS_LVM %s' % (lvm_pv_part_size, device))
            else:
                subprocess.call('sgdisk --set-alignment="2048" --new=4:0:+%dM --typecode=4:8200 --change-name=4:ANTERGOS_SWAP %s' % (swap_part_size, device))
                subprocess.call('sgdisk --set-alignment="2048" --new=5:0:+%dM --typecode=5:8300 --change-name=5:ANTERGOS_ROOT %s' % (root_part_size, device))
            
            logging.debug(subprocess.check_output("sgdisk --print %s" % device))
            
        else:
            part_root = self.auto_device + "3"
            # start at sector 1 for 4k drive compatibility and correct alignment
            # clean partitiontable to avoid issues!
            subprocess.call("dd if=/dev/zero of=%s bs=512 count=2048" % device)
            subprocess.call("wipefs -a %s" % device)

            # create DOS MBR with parted
            subprocess.call("parted -a optimal -s %s mktable msdos" % device)
            subprocess.call("parted -a optimal -s %s mkpart primary 1 %d" % (device, guid_part_size + boot_part_size))
            subprocess.call("parted -a optimal -s %s set 1 boot on" % device)
            
            if self.lvm:
                start = guid_part_size + boot_part_size
                end = start + lvm_pv_part_size
                subprocess.call("parted -a optimal -s %s mkpart primary %d %d" % (device, start, end))
            else:
                start = guid_part_size + boot_part_size
                end = start + swap_part_size
                subprocess.call("parted -a optimal -s %s mkpart primary %d %d" % (device, start, end))
                subprocess.call("parted -a optimal -s %s mkpart primary %d 100%" % (device, end))
            
    
    self.printk(True)

    ## wait until /dev initialized correct devices
    subprocess.call("udevadm settle")
    
    # if using LVM, data_device will store root and swap partitions
    # if not using LVM, data_device will be root partition
    if self.lvm:
        val = 2
    else:
        val = 3
    
    if self.uefi:
        val += 2

    data_device = self.auto_device + str(val)

    if self.luks:
        # Wipe LUKS header (just in case we're installing on a pre LUKS setup)
        # For 512 bit key length the header is 2MB
        # If in doubt, just be generous and overwrite the first 10MB or so
        subprocess.call("dd if=/dev/zero of=%s bs=512 count=20480" % data_device)
    
        # Create a random keyfile
        subprocess.call("dd if=/dev/urandom of=%s bs=1024 count=4" % key_file)
        
        # Setup luks
        subprocess.call("cryptsetup luksFormat -q -c aes-xts-plain -s 512 %s %s" % (data_device, key_file))
        subprocess.call("cryptsetup luksOpen %s cryptAntergos -q --key-file %s" % (data_device, key_file))
    fi

    val = 1
    
    if self.uefi:
        val = 3

    if self.lvm:
        # /dev/sdX1 is /boot
        # /dev/sdX2 is the PV
        
        if self.luks:
            # setup LVM on LUKS
            subprocess.call("pvcreate -f /dev/mapper/cryptAntergos")
            subprocess.call("vgcreate -v AntergosVG /dev/mapper/cryptAntergos")
        else:
            subprocess.call("pvcreate -f %s" % data_device)
            subprocess.call("vgcreate -v AntergosVG %s" % data_device)
        
        subprocess.call("lvcreate -n AntergosRoot -L %d AntergosVG" % root_part_size)
        
        
        
        
        
        # Use the remainig space for our swap volume
        lvcreate -n AntergosSwap -l 100%FREE AntergosVG

        ## Make sure the "root" partition is defined first
        _mkfs yes /dev/AntergosVG/AntergosRoot ext4 "${DESTDIR}" / AntergosRoot || return 1
        _mkfs yes /dev/AntergosVG/AntergosSwap swap "${DESTDIR}" "" AntergosSwap || return 1

        _mkfs yes "${BOOT_DEVICE}" ext2 "${DESTDIR}" /boot AntergosBoot || return 1    
    else
        # Not using LVM
        if [ "$USE_LUKS" == "1" ]; then
            ## Make sure the "root" partition is defined first
            _mkfs yes /dev/mapper/cryptAntergos ext4 "${DESTDIR}" / AntergosRoot || return 1
            FSSPECS="1:/boot:${BOOT_PART_SIZE}:ext2::+:BOOT_ANTERGOS 2:swap:${SWAP_PART_SIZE}:swap:::SWAP_ANTERGOS"
            if [ "${GUIDPARAMETER}" == "yes" ]; then
                FSSPECS="3:/boot:${BOOT_PART_SIZE}:ext2::+:BOOT_ANTERGOS 2:/boot/efi:512:vfat:-F32::ESP 4:swap:${SWAP_PART_SIZE}:swap:::SWAP_ANTERGOS"
            fi
        else
            ## FSSPECS - default filesystem specs (the + is bootable flag)
            ## <partnum>:<mountpoint>:<partsize>:<fstype>[:<fsoptions>][:+]:labelname
            ## The partitions in FSSPECS list should be listed in the "mountpoint" order.
            ## Make sure the "root" partition is defined first in the FSSPECS list
            FSSPECS="3:/:${ROOT_PART_SIZE}:${FSTYPE}:::ROOT_ANTERGOS 1:/boot:${BOOT_PART_SIZE}:ext2::+:BOOT_ANTERGOS 2:swap:${SWAP_PART_SIZE}:swap:::SWAP_ANTERGOS"

            if [ "${GUIDPARAMETER}" == "yes" ]; then
                FSSPECS="5:/:${ROOT_PART_SIZE}:${FSTYPE}:::ROOT_ANTERGOS 3:/boot:${BOOT_PART_SIZE}:ext2::+:BOOT_ANTERGOS 2:/boot/efi:512:vfat:-F32::ESP 4:swap:${SWAP_PART_SIZE}:swap:::SWAP_ANTERGOS"
            fi
        fi

        ## make and mount filesystems
        for fsspec in ${FSSPECS}; do
            part="$(echo ${fsspec} | tr -d ' ' | cut -f1 -d:)"
            mountpoint="$(echo ${fsspec} | tr -d ' ' | cut -f2 -d:)"
            fstype="$(echo ${fsspec} | tr -d ' ' | cut -f4 -d:)"
            fsoptions="$(echo ${fsspec} | tr -d ' ' | cut -f5 -d:)"
            [[ "${fsoptions}" == "" ]] && fsoptions="NONE"
            labelname="$(echo ${fsspec} | tr -d ' ' | cut -f7 -d:)"
            btrfsdevices="${DEVICE}${part}"
            btrfsssd="NONE"
            btrfscompress="NONE"
            btrfssubvolume="NONE"
            btrfslevel="NONE"
            dosubvolume="no"
            # if echo "${mountpoint}" | tr -d ' ' | grep '^/$' 2>&1 >/dev/null; then
            # if [[ "$(echo ${mountpoint} | tr -d ' ' | grep '^/$' | wc -l)" -eq 0 ]]; then
            _mkfs yes "${DEVICE}${part}" "${fstype}" "${DESTDIR}" "${mountpoint}" "${labelname}" "${fsoptions}" "${btrfsdevices}" "${btrfssubvolume}" "${btrfslevel}" "${dosubvolume}" "${btrfssd}" "${btrfscompress}" || return 1
            # fi
        done
    fi

    if [ "$USE_LUKS" == "1" ]; then
        # https://wiki.archlinux.org/index.php/Encrypted_LVM

        # NOTE: encrypted and/or lvm2 hooks will be added to mkinitcpio.conf in installation_process.py
        # NOTE: /etc/default/grub will be modified in installation_process.py, too.
        
        # Copy keyfile to boot partition, user will choose what to do with it
        # THIS IS NONSENSE (BIG SECURITY HOLE), BUT WE TRUST THE USER TO FIX THIS
        # User shouldn't store the keyfiles unencrypted unless the medium itself is reasonably safe
        # (boot partition is not)
        # Maybe instead of using a keyfile we should use a password...
        sudo chmod 0400 "${KEY_FILE}"
        cp ${KEY_FILE} ${DESTDIR}/boot
        rm ${KEY_FILE}
    fi
    
    S_MKFSAUTO=1
}

touch /tmp/.auto_partition.lock
autoprepare $1
rm /tmp/.auto_partition.lock
