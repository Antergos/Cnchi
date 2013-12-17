#!/usr/bin/env bash

UNAME_M=`uname -m`
KMS="i915"
KMS_OPTIONS="modeset=1"
DRI="intel-dri"
DDX="xf86-video-intel"
DECODER="libva-intel-driver"

pacman -S --noconfirm --needed ${DRI} ${DDX} ${DECODER} libtxc_dxtn
if [ "${UNAME_M}" == "x86_64" ]; then
    pacman -S --noconfirm --needed lib32-${DRI} lib32-mesa-libgl
fi
echo "options ${KMS} ${KMS_OPTIONS}" > /etc/modprobe.d/${KMS}.conf
