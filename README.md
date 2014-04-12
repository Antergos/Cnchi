# Cnchi

Graphical Installer for Antergos Linux (FKA Cinnarch Linux)

Usage: sudo -E cnchi.py

To create logs to help debug problems: sudo -E cnchi.py -dv

## Dependencies

 * gtk 3
 * python 3
 * python-gobject 3
 * python-dbus
 * python-cairo
 * python-mako
 * libtimezonemap
 * webkitgtk
 * parted (dosfstools, mtools, ntfs-3g, ntfsprogs)
 * py3parted (pyparted on python3) -> https://github.com/antergos/antergos-packages/tree/master/py3parted
 * pacman
 * pyalpm
 * hwinfo
 * hdparm
 * upower
 * python-mock (only needed for unit tests)

## Translations

We manage our translations in transifex:

* https://www.transifex.com/projects/p/antergos/
