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

    def get_fs_uuid(self, device):
        return subprocess.check_output("blkid -p -i -s UUID -o value %s" % device)
    
    def get_fs_label(self, device):
        return subprocess.check_output("blkid -p -i -s LABEL -o value %s" % device)

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
            subprocess.call(["swapoff", device])
            subprocess.call(["mkswap", "-L", label_name, device])
            subprocess.call(["swapon", device])
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
            subprocess.call(command)
            

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
        # TODO: support UEFI
        uefi = False

        key_file = "/tmp/.keyfile"
    
        if uefi:
            guid_part_size = "2"
            gpt_bios_grub_part_size = "2"
            uefisys_part_size = "512"
        else:
            guid_part_size = "0"
            uefisys_part_size = "0"

        # get just the disk size in 1000*1000 MB
        device = subprocess.check_output("basename %s" % self.auto_device)
        base_path = "/sys/block/%s" % device
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

        # we assume a /dev/hdX format (or /dev/sdX)
        if uefi:
            '''
            PART_ROOT="${DEVICE}5"
            # GPT (GUID) is supported only by 'parted' or 'sgdisk'
            printk off
            # clean partition table to avoid issues!
            sgdisk --zap ${DEVICE} &>/dev/null
            # clear all magic strings/signatures - mdadm, lvm, partition tables etc.
            dd if=/dev/zero of=${DEVICE} bs=512 count=2048 &>/dev/null
            wipefs -a ${DEVICE} &>/dev/null
            # create fresh GPT
            sgdisk --clear ${DEVICE} &>/dev/null
            # create actual partitions
            sgdisk --set-alignment="2048" --new=1:1M:+${GPT_BIOS_GRUB_PART_SIZE}M --typecode=1:EF02 --change-name=1:BIOS_GRUB ${DEVICE} >> ${LOG}
            sgdisk --set-alignment="2048" --new=2:0:+${UEFISYS_PART_SIZE}M --typecode=2:EF00 --change-name=2:UEFI_SYSTEM ${DEVICE} >> ${LOG}
            sgdisk --set-alignment="2048" --new=3:0:+${BOOT_PART_SIZE}M --typecode=3:8300 --attributes=3:set:2 --change-name=3:ANTERGOS_BOOT ${DEVICE} >> ${LOG}

            if [ "$USE_LVM" == "1" ]; then
                sgdisk --set-alignment="2048" --new=4:0:+${LVM_PV_PART_SIZE}M --typecode=4:8200 --change-name=4:ANTERGOS_LVM ${DEVICE} >> ${LOG}
            else
                sgdisk --set-alignment="2048" --new=4:0:+${SWAP_PART_SIZE}M --typecode=4:8200 --change-name=4:ANTERGOS_SWAP ${DEVICE} >> ${LOG}
                sgdisk --set-alignment="2048" --new=5:0:+${ROOT_PART_SIZE}M --typecode=5:8300 --change-name=5:ANTERGOS_ROOT ${DEVICE} >> ${LOG}        
            fi
            
            sgdisk --print ${DEVICE} >> ${LOG}
            '''
    else:
        PART_ROOT="${DEVICE}3"
        # start at sector 1 for 4k drive compatibility and correct alignment
        printk off

        # clean partitiontable to avoid issues!
        dd if=/dev/zero of=${DEVICE} bs=512 count=2048 >/dev/null 2>&1
        wipefs -a ${DEVICE} &>/dev/null
        # create DOS MBR with parted
        parted -a optimal -s ${DEVICE} mktable msdos >/dev/null 2>&1
        parted -a optimal -s ${DEVICE} mkpart primary 1 $((${GUID_PART_SIZE}+${BOOT_PART_SIZE})) >>${LOG}
        parted -a optimal -s ${DEVICE} set 1 boot on >>${LOG}
        
        if [ "$USE_LVM" == "1" ]; then
            parted -a optimal -s ${DEVICE} mkpart primary $((${GUID_PART_SIZE}+${BOOT_PART_SIZE})) $((${GUID_PART_SIZE}+${BOOT_PART_SIZE}+${LVM_PV_PART_SIZE})) >>${LOG}
        else
            parted -a optimal -s ${DEVICE} mkpart primary $((${GUID_PART_SIZE}+${BOOT_PART_SIZE})) $((${GUID_PART_SIZE}+${BOOT_PART_SIZE}+${SWAP_PART_SIZE})) >>${LOG}
            parted -a optimal -s ${DEVICE} mkpart primary $((${GUID_PART_SIZE}+${BOOT_PART_SIZE}+${SWAP_PART_SIZE})) 100% >>${LOG}
        fi
    fi
    
    partprobe ${DISC}
    if [[ $? -gt 0 ]]; then
        echo "Error partitioning ${DEVICE} (see ${LOG} for details)" 0 0
        printk on
        return 1
    fi
    printk on
    ## wait until /dev initialized correct devices
    udevadm settle
    
    # if using LVM, data_device will store root and swap partitions
    # if not using LVM, data_device will be root partition
    if [ "$USE_LVM" == "1" ]; then
        DATA_DEVICE=${DEVICE}2
    else
        DATA_DEVICE=${DEVICE}3
    
        if [[ "${GUIDPARAMETER}" == "yes" ]]; then
            DATA_DEVICE=${DEVICE}5
        fi
    fi
    
    if [ "$USE_LUKS" == "1" ]; then
        # Wipe LUKS header (just in case we're installing on a pre LUKS setup)
        # For 512 bit key length the header is 2MB
        # If in doubt, just be generous and overwrite the first 10MB or so
        dd if=/dev/zero of=${DATA_DEVICE} bs=512 count=20480
    
        # Create a random keyfile
        dd if=/dev/urandom of=${KEY_FILE} bs=1024 count=4
        
        # Setup luks
        cryptsetup luksFormat -q -c aes-xts-plain -s 512 ${DATA_DEVICE} ${KEY_FILE}
        #cryptsetup luksAddKey ${DATA_DEVICE} --key-file ${KEY_FILE}
        cryptsetup luksOpen ${DATA_DEVICE} cryptAntergos -q --key-file ${KEY_FILE}
        
    fi

    BOOT_DEVICE="${DEVICE}1"

    if [ "${GUIDPARAMETER}" == "yes" ]; then
        BOOT_DEVICE="${DEVICE}3"
    fi  

    if [ "$USE_LVM" == "1" ]; then
        # /dev/sdX1 is /boot
        # /dev/sdX2 is the PV
        
        if [ "$USE_LUKS" == "1" ]; then
            # setup LVM on LUKS
            pvcreate /dev/mapper/cryptAntergos
            vgcreate -v AntergosVG /dev/mapper/cryptAntergos
        else
            pvcreate ${DATA_DEVICE}
            vgcreate -v AntergosVG ${DATA_DEVICE}
        fi
        
        lvcreate -n AntergosRoot -L ${ROOT_PART_SIZE} AntergosVG
        
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
