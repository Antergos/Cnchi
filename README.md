# Cnchi

**Graphical Installer for Antergos Linux (FKA Cinnarch Linux)**

Usage:
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
 - python-requests
 - pyparted (parted, dosfstools, mtools, ntfs-3g, ntfsprogs)
 - pyalpm (alpm)
 - libtimezonemap (needed by Cnchi 0.6.x and older versions)
 - webkitgtk 
 - hdparm
 - hwinfo (needed by Cnchi 0.6.x and older versions)
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

