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

class AutoPartition():
    def __init__(self, dest_dir, settings):
        answer = "/tmp/.setup"
        self.dest_dir = dest_dir
        
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

    def set_device_name_scheme(self):
        self.NAME_SCHEME_PARAMETER = "FSUUID /dev/disk/by-uuid/<uuid>"
        self.NAME_SCHEME_PARAMETER_RUN = "1"

    def mkfs(self, params):
        device = params['device']
        fs_type = params['fs_type']
        dest = params['dest']
        mount_point = params['mount_point']
        label_name = params['label_name']
        fs_options = params['fs_options']
        
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
                     "btrfs" : "mkfs.btrfs %s -L %s %s" % (fs_options, label_name, btrfsdevices),
                     "nilfs2" : "mkfs.nilfs2 %s -L %s %s" % (fs_options, label_name, device),
                     "ntfs-3g" : "mkfs.ntfs %s -L %s %s" % (fs_options, label_name, device),
                     "vfat" : "mkfs.vfat %s -n %s %s" % (fs_options, label_name, device) }

            # make sure the fs type is one we can handle
            if fs_type not in mkfs.keys():
                logging.error("Unkown filesystem type %s" % fs_type)
                return
            
            command = mkfs[fs_type]
            
            
        '''
             "xfs" : "mkfs.xfs ${_fsoptions} -L ${_labelname} -f ${_device} >>${LOG} 2>&1; ret=$? ;;
                jfs)      yes | mkfs.jfs ${_fsoptions} -L ${_labelname} ${_device} >>${LOG} 2>&1; ret=$? ;;
                reiserfs) yes | mkreiserfs ${_fsoptions} -l ${_labelname} ${_device} >>${LOG} 2>&1; ret=$? ;;
                ext2)     mkfs.ext2 -L ${_fsoptions} ${_labelname} ${_device} >>${LOG} 2>&1; ret=$? ;;
                ext3)     mke2fs ${_fsoptions} -L ${_labelname} -t ext3 ${_device} >>${LOG} 2>&1; ret=$? ;;
                ext4)     mke2fs ${_fsoptions} -L ${_labelname} -t ext4 ${_device} >>${LOG} 2>&1; ret=$? ;;
                btrfs)    mkfs.btrfs ${_fsoptions} -L ${_labelname} ${_btrfsdevices} >>${LOG} 2>&1; ret=$? ;;
                nilfs2)   mkfs.nilfs2 ${_fsoptions} -L ${_labelname} ${_device} >>${LOG} 2>&1; ret=$? ;;
                ntfs-3g)  mkfs.ntfs ${_fsoptions} -L ${_labelname} ${_device} >>${LOG} 2>&1; ret=$? ;;
                vfat)     mkfs.vfat ${_fsoptions} -n ${_labelname} ${_device} >>${LOG} 2>&1; ret=$? ;;
                # don't handle anything else here, we will error later
            esac
            if [[ ${ret} != 0 ]]; then
                echo "Error creating filesystem ${_fstype} on ${_device}"
                return 1
            fi
            sleep 2
        fi

        sleep 2
        # create our mount directory
        mkdir -p ${_dest}${_mountpoint}
      
        mount -t ${_fstype} ${_device} ${_dest}${_mountpoint} >>${LOG} 2>&1

        if [[ $? != 0 ]]; then
            echo "Error mounting ${_dest}${_mountpoint}"
            return 1
        fi
        # change permission of base directories to correct permission
        # to avoid btrfs issues
        if [[ "${_mountpoint}" = "/tmp" ]]; then
            chmod 1777 ${_dest}${_mountpoint}
        elif [[ "${_mountpoint}" = "/root" ]]; then
            chmod 750 ${_dest}${_mountpoint}
        else
            chmod 755 ${_dest}${_mountpoint}
        fi
    fi
    # add to .device-names for config files
    local _fsuuid="$(getfsuuid ${_device})"
    local _fslabel="$(getfslabel ${_device})"
    echo "# DEVICE DETAILS: ${_device} UUID=${_fsuuid} LABEL=${_fslabel}" >> /tmp/.device-names
    # add to temp fstab
    if [[ "${NAME_SCHEME_PARAMETER}" == "FSUUID" ]]; then
        if [[ -n "${_fsuuid}" ]]; then
            _device="UUID=${_fsuuid}"
        fi
    elif [[ "${NAME_SCHEME_PARAMETER}" == "FSLABEL" ]]; then
        if [[ -n "${_fslabel}" ]]; then
            _device="LABEL=${_fslabel}"
        fi
    fi
    
    echo -n "${_device} ${_mountpoint} ${_fstype} defaults 0 " >>/tmp/.fstab
    
    if [[ "${_fstype}" = "swap" ]]; then
        echo "0" >>/tmp/.fstab
    else
        echo "1" >>/tmp/.fstab
    fi
}



autoprepare() {
    # check on encrypted devices, else weird things can happen!
    # _stopluks
    # check on raid devices, else weird things can happen during partitioning!
    # _stopmd
    # check on lvm devices, else weird things can happen during partitioning!
    # _stoplvm
    
    NAME_SCHEME_PARAMETER_RUN=""
    # switch for mbr usage

    DISC=$1

    DEFAULTFS=""
    BOOT_PART_SET=""
    SWAP_PART_SET=""
    ROOT_PART_SET=""
    FSTYPE='ext4'
    
    KEY_FILE="/tmp/.keyfile"
    
    # Do not support UEFI
    GUIDPARAMETER="no"
    
    if [[ "${GUIDPARAMETER}" = "yes" ]]; then
        GUID_PART_SIZE="2"
        GPT_BIOS_GRUB_PART_SIZE="${GUID_PART_SIZE}"
        UEFISYS_PART_SIZE="512"
    else
        GUID_PART_SIZE="0"
        UEFISYS_PART_SIZE="0"
    fi
    # get just the disk size in 1000*1000 MB
    if [[ "$(cat ${block}/$(basename ${DISC} 2>/dev/null)/size 2>/dev/null)" ]]; then
        DISC_SIZE="$(($(expr $(cat ${block}/$(basename ${DISC})/queue/logical_block_size) '*' $(cat ${block}/$(basename ${DISC})/size))/1000000))"
    else
        echo "ERROR: Setup cannot detect size of your device, please use normal installation routine for partitioning and mounting devices."
        return 1
    fi
    
    while [[ "${DEFAULTFS}" = "" ]]; do

        # create 1 MB bios_grub partition for grub-bios GPT support
        if [[ "${GUIDPARAMETER}" = "yes" ]]; then
            GUID_PART_SIZE="2"
            GPT_BIOS_GRUB_PART_SIZE="${GUID_PART_SIZE}"
            UEFISYS_PART_SIZE="512"
        else
            GUID_PART_SIZE="0"
            UEFISYS_PART_SIZE="0"
        fi
        DISC_SIZE=$((${DISC_SIZE}-${GUID_PART_SIZE}-${UEFISYS_PART_SIZE}))
        while [[ "${BOOT_PART_SET}" = "" ]]; do
            BOOT_PART_SIZE="200"
                if [[ "${BOOT_PART_SIZE}" -ge "${DISC_SIZE}" || "${BOOT_PART_SIZE}" -lt "16" || "${SBOOT_PART_SIZE}" = "${DISC_SIZE}" ]]; then
                    echo "ERROR: Invalid size for boot."
                else
                    BOOT_PART_SET=1
                fi
        done
        DISC_SIZE=$((${DISC_SIZE}-${BOOT_PART_SIZE}))
        MEMTOTAL=`grep MemTotal /proc/meminfo | awk '{print $2}'`
        if [[ MEMTOTAL -gt 1572864 ]];then
            SWAP_PART_SIZE=1536
        else
            let SWAP_PART_SIZE=`grep MemTotal /proc/meminfo | awk '{print $2}'`/1024
        fi

        SWAP_PART_SET=1

        DISC_SIZE=$((${DISC_SIZE}-${SWAP_PART_SIZE}))
        ROOT_SIZE="${DISC_SIZE}"
        [[ "${DISC_SIZE}" -lt "7500" ]] && ROOT_SIZE="${DISC_SIZE}"
        ROOT_PART_SIZE="${DISC_SIZE}"

        LVM_PV_PART_SIZE=$((${SWAP_PART_SIZE}+${ROOT_PART_SIZE}))
        
        DEFAULTFS=1
    done

    DEVICE=${DISC}

    # validate DEVICE
    if [[ ! -b "${DEVICE}" ]]; then
      echo "Device '${DEVICE}' is not valid"
      return 1
    fi

    # validate DEST
    if [[ ! -d "${DESTDIR}" ]]; then
        echo "Destination directory '${DESTDIR}' is not valid"
        return 1
    fi

    [[ -e /tmp/.fstab ]] && rm -f /tmp/.fstab
    # disable swap and all mounted partitions, umount / last!
    _umountall
    if [[ "${NAME_SCHEME_PARAMETER_RUN}" == "" ]]; then
        set_device_name_scheme || return 1
    fi

    # we assume a /dev/hdX format (or /dev/sdX)
    if [[ "${GUIDPARAMETER}" == "yes" ]]; then
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
    else
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
