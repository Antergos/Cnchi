# Cnchi

**Graphical Installer for Antergos Linux**

You are viewing the `0.6.x` branch.

## Current Status
This was the previous stable version of Cnchi, AKA: **Cnchi Legacy**. 

|Development Stage|Version| Code State|
----------------- | -------------- | -------- |
|*Cnchi Legacy*|*v0.6.53*|*Frozen*|
|**Cnchi Stable**|**v0.8.x**|**Bug Fixes Only**|
|Cnchi Next | v0.9.x | Active Development|

## Usage:
Command:
```
lang=sh
sudo -E cnchi.py
```

To create logs to help debug problems:
```
lang=sh
sudo -E cnchi.py -dv
```

## Translations

We manage our translations in transifex:

 - https://www.transifex.com/projects/p/antergos/

## Dependencies

 - gtk3
 - python3
 - python-cairo
 - python-dbus
 - python-gobject
 - python-mako
 - pyparted (parted, dosfstools, mtools, ntfs-3g, ntfsprogs)
 - pyalpm (pacman)
 - libtimezonemap
 - webkitgtk 
 - hdparm
 - hwinfo
 - upower
 
## Unit tests
 - python-mock 

## Fonts needed by the keyboard widget
 - ttf-aboriginal-sans
 - ttf-indic-otf
 - ttf-khmer
 - ttf-lohit-fonts
 - ttf-myanmar3
 - ttf-thaana-fonts
 - ttf-tlwg

