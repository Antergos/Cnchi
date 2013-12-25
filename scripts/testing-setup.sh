#!/bin/bash

echo "Updating mirrorlist..."
reflector -p http -l 15 -f 5 --save /etc/pacman.d/mirrorlist

echo "Installing git..."
pacman -Sy git --noconfirm

echo "Removing current Cnchi..."
rm -R /usr/share/cnchi
cd /usr/share

echo "Getting latest version of Cnchi..."
git clone https://github.com/lots0logs/Cnchi.git cnchi;
cd cnchi
git checkout testing

echo "Starting Cnchi..."
cnchi -dv -p /usr/share/cnchi/data/packages.xml &

exit;
