#!/usr/bin/env bash

pacman -S --needed --noconfirm virtualbox-guest-utils

systemctl disable openntpd
systemctl enable vboxservice

echo 'vboxguest' >  /etc/modules-load.d/virtualbox-guest.conf
echo 'vboxsf'    >> /etc/modules-load.d/virtualbox-guest.conf
echo 'vboxvideo' >> /etc/modules-load.d/virtualbox-guest.conf
