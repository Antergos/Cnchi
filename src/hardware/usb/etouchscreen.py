#!/usr/bin/env bash

# Errata
if [ -f /etc/modprobe.d/egalax.conf ]; then
    mv -f /etc/modprobe.d/egalax.conf /etc/modprobe.d/blacklist-usbtouchscreen.conf
fi

# References
# - http://www.x.org/archive/X11R7.5/doc/man/man4/evdev.4.html
# - https://bbs.archlinux.org/viewtopic.php?id=126208
# #xinput set-int-prop "eGalax Inc. Touch" "Evdev Axis Calibration" 32 3975 107 -147 3582
packer -S --noedit --noconfirm xinput_calibrator xournal
if [ ! -f /etc/modprobe.d/blacklist-usbtouchscreen.conf ]; then
    rmmod usbtouchscreen 2>/dev/null

    # Do not load the 'usbtouchscreen' module, as it conflicts with eGalax
    echo "blacklist usbtouchscreen" > /etc/modprobe.d/blacklist-usbtouchscreen.conf
fi

#TODO - This should be computer specific
cat >/etc/X11/xorg.conf.d/99-calibration.conf<<ENDCALIB
Section "InputClass"
    Identifier      "calibration"
    MatchProduct    "eGalax Inc. USB TouchController"
    Option          "Calibration"   "3996 122 208 3996"
    Option          "InvertY" "1"
    Option          "SwapAxes" "0"
EndSection
ENDCALIB
