#!/usr/bin/env bash

UNAME_M=`uname -m`

# Uninstall nouveau
rm /etc/modprobe.d/nouveau.conf
pacman -Rdds --noconfirm nouveau-dri xf86-video-nouveau libtxc_dxtn
pacman -Rdds --noconfirm mesa-libgl
if [ "${UNAME_M}" == "x86_64" ]; then
    pacman -Rdds --noconfirm lib32-nouveau-dri lib32-mesa-libgl
fi

# Install nvidia
echo -en "\ny\n" | pacman -S --needed --noconfirm nvidia libva-vdpau-driver
if [ "${UNAME_M}" == "x86_64" ]; then
    pacman -S --noconfirm --needed lib32-nvidia-libgl
fi

if [ -f /etc/X11/xorg.conf ]; then
    mv /etc/X11/xorg.conf /etc/X11/xorg.conf.`date +%y%m%d-%H%M`
fi

cat << XORG > /etc/X11/xorg.conf
Section "Device"
   Identifier     "Device0"
   Driver         "nvidia"
   Option         "NoLogo"
   Option         "RegistryDwords"      "EnableBrightnessControl=1"
   VendorName     "NVIDIA Corporation"
EndSection
XORG

echo "blacklist nouveau" > /etc/modprobe.d/blacklist-nouveau.conf
echo "options nvidia NVreg_EnableMSI=1" > /etc/modprobe.d/nvidia.conf
