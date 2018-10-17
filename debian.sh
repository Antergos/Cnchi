#!/usr/bin/bash
# Install debian dependencies

# Python gobject
sudo apt -y install python3-gi python3-cairo python3-dbus

# Git
sudo apt -y install git

# debian-pacman
sudo apt -y install build-essential automake libarchive-dev
git clone https://github.com/mingw-deb/debian-pacman.git /tmp/debian-pacman
cd /tmp/debian-pacman
./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var
make
sudo make install

# pyalpm
git clone https://github.com/jelly/pyalpm.git /tmp/pyalpm
cd /tmp/pyalpm
python3 setup.py build
sudo python3 setup.py install --root=/

# maxminddb and geoip2
sudo apt -y install python3-maxminddb libmaxminddb0 python3-geoip2

# parted
sudo apt install -y libparted-dev python3-parted

# python-libnacl and python-feedparser
sudo apt install -y python3-libnacl python3-feedparser

