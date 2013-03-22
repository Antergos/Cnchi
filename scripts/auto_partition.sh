#!/bin/bash

unset LANG
ANSWER="/tmp/.setup"

# use the first VT not dedicated to a running console
LOG="/dev/tty7"

# don't use /mnt because it's intended to mount other things there!
DESTDIR="/install"
EDITOR=""
_BLKID="blkid -c /dev/null"
# destination of blockdevices in /sys
block="/sys/block"



getfsuuid()
{
    echo "$(${_BLKID} -p -i -s UUID -o value ${1})"
}

# parameters: device file
# outputs:    LABEL on success
#             nothing on failure
# returns:    nothing
getfslabel()
{
    echo "$(${_BLKID} -p -i -s LABEL -o value ${1})"
}

# Disable all luks encrypted devices
_stopluks()
{
    DISABLELUKS=""
    DETECTED_LUKS=""
    LUKSDEVICE=""

    # detect already running luks devices
    LUKS_DEVICES="$(ls /dev/mapper/ | grep -v control)"
    for i in ${LUKS_DEVICES}; do
        cryptsetup status ${i} 2>/dev/null && LUKSDEVICE="${LUKSDEVICE} ${i}"
    done
    ! [[ "${LUKSDEVICE}" = "" ]] && DETECTED_LUKS=1
    if [[ "${DETECTED_LUKS}" = "1" ]]; then
        echo "Setup detected running luks encrypted devices, do you want to remove them completely?"
    fi
    if [[ "${DISABLELUKS}" = "1" ]]; then
        echo "Removing luks encrypted devices ..."
        for i in ${LUKSDEVICE}; do
            LUKS_REAL_DEVICE="$(echo $(cryptsetup status ${i} | grep device: | sed -e 's#device:##g'))"
            cryptsetup remove ${i} > ${LOG}
            # delete header from device
            dd if=/dev/zero of=${LUKS_REAL_DEVICE} bs=512 count=2048 >/dev/null 2>&1
        done
    fi
    
    DISABLELUKS=""
    DETECTED_LUKS=""

    # detect not running luks devices
    [[ "$(${_BLKID} | grep "TYPE=\"crypto_LUKS\"")" ]] && DETECTED_LUKS=1
    if [[ "${DETECTED_LUKS}" = "1" ]]; then
        echo "Setup detected not running luks encrypted devices, do you want to remove them completely?"
    fi
    if [[ "${DISABLELUKS}" = "1" ]]; then
        echo "Removing not running luks encrypted devices ..."
        for i in $(${_BLKID} | grep "TYPE=\"crypto_LUKS\"" | sed -e 's#:.*##g'); do
            # delete header from device
            dd if=/dev/zero of=${i} bs=512 count=2048 >/dev/null 2>&1
        done
    fi
    [[ -e /tmp/.crypttab ]] && rm /tmp/.crypttab
}

_stopmd()
{
    if [[ "$(cat /proc/mdstat 2>/dev/null | grep ^md)" ]]; then
        DISABLEMD=""
        echo "Setup detected already running raid devices, do you want to disable them completely?"
        if [[ "${DISABLEMD}" = "1" ]]; then
            echo "Disabling all software raid devices..."
            for i in $(cat /proc/mdstat 2>/dev/null | grep ^md | sed -e 's# :.*##g'); do
                mdadm --manage --stop /dev/${i} > ${LOG}
            done
            echo "Cleaning superblocks of all software raid devices..."
            for i in $(${_BLKID} | grep "TYPE=\"linux_raid_member\"" | sed -e 's#:.*##g'); do
                mdadm --zero-superblock ${i} > ${LOG}
            done
        fi
    fi
    DISABLEMDSB=""
    if [[ "$(${_BLKID} | grep "TYPE=\"linux_raid_member\"")" ]]; then
        DIALOG --defaultno --yesno "Setup detected superblock of raid devices, do you want to clean the superblock of them?" 0 0 && DISABLEMDSB="1"
        if [[ "${DISABLEMDSB}" = "1" ]]; then
            DIALOG --infobox "Cleaning superblocks of all software raid devices..." 0 0
            for i in $(${_BLKID} | grep "TYPE=\"linux_raid_member\"" | sed -e 's#:.*##g'); do
                mdadm --zero-superblock ${i} > ${LOG}
            done
        fi
    fi
}


_stoplvm()
{
    DISABLELVM=""
    DETECTED_LVM=""
    LV_VOLUMES="$(lvs -o vg_name,lv_name --noheading --separator - 2>/dev/null)"
    LV_GROUPS="$(vgs -o vg_name --noheading 2>/dev/null)"
    LV_PHYSICAL="$(pvs -o pv_name --noheading 2>/dev/null)"
    ! [[ "${LV_VOLUMES}" = "" ]] && DETECTED_LVM=1
    ! [[ "${LV_GROUPS}" = "" ]] && DETECTED_LVM=1
    ! [[ "${LV_PHYSICAL}" = "" ]] && DETECTED_LVM=1
    if [[ "${DETECTED_LVM}" = "1" ]]; then
        DIALOG --defaultno --yesno "Setup detected lvm volumes, volume groups or physical devices, do you want to remove them completely?" 0 0 && DISABLELVM="1"
    fi
    if [[ "${DISABLELVM}" = "1" ]]; then
        DIALOG --infobox "Removing logical volumes ..." 0 0
        for i in ${LV_VOLUMES}; do
            lvremove -f /dev/mapper/${i} 2>/dev/null> ${LOG}
        done
        DIALOG --infobox "Removing logical groups ..." 0 0
        for i in ${LV_GROUPS}; do
            vgremove -f ${i} 2>/dev/null > ${LOG}
        done
        DIALOG --infobox "Removing physical volumes ..." 0 0
        for i in ${LV_PHYSICAL}; do
            pvremove -f ${i} 2>/dev/null > ${LOG}
        done
    fi
}


_umountall()
{
    swapoff -a >/dev/null 2>&1
    umount $(mount | grep -v "${DESTDIR} " | grep "${DESTDIR}" | sed 's|\ .*||g') >/dev/null 2>&1
    umount $(mount | grep "${DESTDIR} " | sed 's|\ .*||g') >/dev/null 2>&1
}


set_device_name_scheme() {
    NAME_SCHEME_PARAMETER=""
    NAME_SCHEME_PARAMETER="FSUUID /dev/disk/by-uuid/<uuid>"
    NAME_SCHEME_PARAMETER_RUN="1"
}

printk()
{
    case ${1} in
        "on")  echo 4 >/proc/sys/kernel/printk ;;
        "off") echo 0 >/proc/sys/kernel/printk ;;
    esac
}


_mkfs() {
    local _domk=${1}
    local _device=${2}
    local _fstype=${3}
    local _dest=${4}
    local _mountpoint=${5}
    local _labelname=${6}
    local _fsoptions=${7}
    local _btrfsdevices="$(echo ${8} | sed -e 's|#| |g')"
    local _btrfslevel=${9}
    local _btrfssubvolume=${10}
    local _dosubvolume=${11}
    local _btrfscompress=${12}
    local _btrfsssd=${13}
    # correct empty entries
    [[ "${_fsoptions}" = "NONE" ]] && _fsoptions=""
    [[ "${_btrfsssd}" = "NONE" ]] && _btrfsssd=""
    [[ "${_btrfscompress}" = "NONE" ]] && _btrfscompress=""
    [[ "${_btrfssubvolume}" = "NONE" ]] && _btrfssubvolume=""
    # add btrfs raid level, if needed
    [[ ! "${_btrfslevel}" = "NONE" && "${_fstype}" = "btrfs" ]] && _fsoptions="${_fsoptions} -d ${_btrfslevel}"
    # we have two main cases: "swap" and everything else.
    if [[ "${_fstype}" = "swap" ]]; then
        swapoff ${_device} >/dev/null 2>&1
        if [[ "${_domk}" = "yes" ]]; then
            mkswap -L ${_labelname} ${_device} >${LOG} 2>&1
            if [[ $? != 0 ]]; then
                echo "Error creating swap: mkswap ${_device}"
                return 1
            fi
        fi
        swapon ${_device} >${LOG} 2>&1
        if [[ $? != 0 ]]; then
            echo "Error activating swap: swapon ${_device}"
            return 1
        fi
    else
        # make sure the fstype is one we can handle
        local knownfs=0
        for fs in xfs jfs reiserfs ext2 ext3 ext4 btrfs nilfs2 ntfs-3g vfat; do
            [[ "${_fstype}" = "${fs}" ]] && knownfs=1 && break
        done
        if [[ ${knownfs} -eq 0 ]]; then
            echo "unknown fstype ${_fstype} for ${_device}"
            return 1
        fi
        # if we were tasked to create the filesystem, do so
        if [[ "${_domk}" = "yes" ]]; then
            local ret
            case ${_fstype} in
                xfs)      mkfs.xfs ${_fsoptions} -L ${_labelname} -f ${_device} >${LOG} 2>&1; ret=$? ;;
                jfs)      yes | mkfs.jfs ${_fsoptions} -L ${_labelname} ${_device} >${LOG} 2>&1; ret=$? ;;
                reiserfs) yes | mkreiserfs ${_fsoptions} -l ${_labelname} ${_device} >${LOG} 2>&1; ret=$? ;;
                ext2)     mkfs.ext2 -L ${_fsoptions} ${_labelname} ${_device} >${LOG} 2>&1; ret=$? ;;
                ext3)     mke2fs ${_fsoptions} -L ${_labelname} -t ext3 ${_device} >${LOG} 2>&1; ret=$? ;;
                ext4)     mke2fs ${_fsoptions} -L ${_labelname} -t ext4 ${_device} >${LOG} 2>&1; ret=$? ;;
                btrfs)    mkfs.btrfs ${_fsoptions} -L ${_labelname} ${_btrfsdevices} >${LOG} 2>&1; ret=$? ;;
                nilfs2)   mkfs.nilfs2 ${_fsoptions} -L ${_labelname} ${_device} >${LOG} 2>&1; ret=$? ;;
                ntfs-3g)  mkfs.ntfs ${_fsoptions} -L ${_labelname} ${_device} >${LOG} 2>&1; ret=$? ;;
                vfat)     mkfs.vfat ${_fsoptions} -n ${_labelname} ${_device} >${LOG} 2>&1; ret=$? ;;
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
      
        mount -t ${_fstype} ${_device} ${_dest}${_mountpoint} >${LOG} 2>&1

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
        sgdisk --set-alignment="2048" --new=1:1M:+${GPT_BIOS_GRUB_PART_SIZE}M --typecode=1:EF02 --change-name=1:BIOS_GRUB ${DEVICE} > ${LOG}
        sgdisk --set-alignment="2048" --new=2:0:+${UEFISYS_PART_SIZE}M --typecode=2:EF00 --change-name=2:UEFI_SYSTEM ${DEVICE} > ${LOG}
        sgdisk --set-alignment="2048" --new=3:0:+${BOOT_PART_SIZE}M --typecode=3:8300 --attributes=3:set:2 --change-name=3:CINNARCH_BOOT ${DEVICE} > ${LOG}
        sgdisk --set-alignment="2048" --new=4:0:+${SWAP_PART_SIZE}M --typecode=4:8200 --change-name=4:CINNARCH_SWAP ${DEVICE} > ${LOG}
        sgdisk --set-alignment="2048" --new=5:0:+${ROOT_PART_SIZE}M --typecode=5:8300 --change-name=5:CINNARCH_ROOT ${DEVICE} > ${LOG}
        sgdisk --print ${DEVICE} > ${LOG}
    else
        PART_ROOT="${DEVICE}3"
        # start at sector 1 for 4k drive compatibility and correct alignment
        printk off

        # clean partitiontable to avoid issues!
        dd if=/dev/zero of=${DEVICE} bs=512 count=2048 >/dev/null 2>&1
        wipefs -a ${DEVICE} &>/dev/null
        # create DOS MBR with parted
        parted -a optimal -s ${DEVICE} mktable msdos >/dev/null 2>&1
        parted -a optimal -s ${DEVICE} mkpart primary 1 $((${GUID_PART_SIZE}+${BOOT_PART_SIZE})) >${LOG}
        parted -a optimal -s ${DEVICE} set 1 boot on >${LOG}
        parted -a optimal -s ${DEVICE} mkpart primary $((${GUID_PART_SIZE}+${BOOT_PART_SIZE})) $((${GUID_PART_SIZE}+${BOOT_PART_SIZE}+${SWAP_PART_SIZE})) >${LOG}
        parted -a optimal -s ${DEVICE} mkpart primary $((${GUID_PART_SIZE}+${BOOT_PART_SIZE}+${SWAP_PART_SIZE})) 100% >${LOG}
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

    ## FSSPECS - default filesystem specs (the + is bootable flag)
    ## <partnum>:<mountpoint>:<partsize>:<fstype>[:<fsoptions>][:+]:labelname
    ## The partitions in FSSPECS list should be listed in the "mountpoint" order.
    ## Make sure the "root" partition is defined first in the FSSPECS list
    FSSPECS="3:/:${ROOT_PART_SIZE}:${FSTYPE}:::ROOT_CINNARCH 1:/boot:${BOOT_PART_SIZE}:ext2::+:BOOT_CINNARCH 2:swap:${SWAP_PART_SIZE}:swap:::SWAP_CINNARCH"

    if [[ "${GUIDPARAMETER}" == "yes" ]]; then
        FSSPECS="5:/:${ROOT_PART_SIZE}:${FSTYPE}:::ROOT_CINNARCH 3:/boot:${BOOT_PART_SIZE}:ext2::+:BOOT_CINNARCH 2:/boot/efi:512:vfat:-F32::ESP 4:swap:${SWAP_PART_SIZE}:swap:::SWAP_CINNARCH"
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

    S_MKFSAUTO=1
}

touch /tmp/.auto_partition.lock
autoprepare $1
rm /tmp/.auto_partition.lock
