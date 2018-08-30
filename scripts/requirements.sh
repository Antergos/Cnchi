#!/bin/bash
sudo pacman -Syy --noconfirm
sudo pacman -Scc --noconfirm
sudo pacman -S geoip2-database
sudo pacman -Scc --noconfirm
sudo pacman -S python
sudo pacman -Scc --noconfirm
sudo pacman -S webkit2gtk
sudo pacman -Scc --noconfirm
sudo pacman -S iso-codes gptfdisk python python-bugsnag \
python-cairo python-chardet python-dbus python-defusedxml \
python-feedparser python-geoip2 python-gobject python-idna \
python-libnacl python-mako python-maxminddb python-parted \
python-requests upower
sudo pacman -Scc --noconfirm


