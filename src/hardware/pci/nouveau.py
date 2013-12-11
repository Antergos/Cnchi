#!/usr/bin/env bash

UNAME_M=`uname -m`
KMS="nouveau"
KMS_OPTIONS="modeset=1"
DRI="nouveau-dri"
DDX="xf86-video-nouveau"
DECODER="libva-vdpau-driver"

# Uninstall nvidia
pacman -Rns --noconfirm nvidia
if [ "${UNAME_M}" == "x86_64" ]; then
    pacman -Rdds --noconfirm lib32-nvidia-libgl
fi

if [ -f /etc/X11/xorg.conf ]; then
    mv /etc/X11/xorg.conf /etc/X11/xorg.conf.`date +%y%m%d-%H%M`
fi

if [ -f /etc/modprobe.d/blacklist-nouveau.conf ]; then
    rm -f /etc/modprobe.d/blacklist-nouveau.conf
fi

# Install nouveau
pacman -S --noconfirm --needed ${DRI} ${DDX} ${DECODER} libtxc_dxtn
if [ "${UNAME_M}" == "x86_64" ]; then
    pacman -S --noconfirm --needed lib32-${DRI} lib32-mesa-libgl
fi
echo "options ${KMS} ${KMS_OPTIONS}" > /etc/modprobe.d/${KMS}.conf
