#!/bin/bash
previous="/tmp/dev-setup"
if ! [ -f "$previous" ]; then
touch /tmp/dev-setup;
modprobe -a vboxsf && systemctl start vboxservice;
echo "Updating mirrorlist..."
reflector -p http -l 15 -f 5 --save /etc/pacman.d/mirrorlist;
echo "Installing git..."
pacman -Sy git grub efibootmgr os-prober --noconfirm --needed;
echo "Removing current Cnchi..."
rm -R /usr/share/cnchi;
cd /usr/share;
echo "Getting latest version of Cnchi..."
git clone https://github.com/lots0logs/Cnchi.git cnchi;
else
echo "Previous setup detected, skipping downloads"
fi
cd /usr/share/cnchi
if [ "$1" = "-c" ]; then
echo "Switching to uefi-testing branch..."
git checkout uefi-testing;
else
echo "Switching to testing branch..."
git checkout testing;
fi
echo "Starting Cnchi..."
if [ "$1" = "-c" ]; then
dbus-launch cnchi -d -v -c /media/sf_data/PKG-CACHE/pkg/ -p /usr/share/cnchi/data/packages.xml & exit;
else
dbus-launch cnchi -d -v -p /usr/share/cnchi/data/packages.xml & exit;
fi
exit;