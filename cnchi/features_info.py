#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  features_info.py
#
#  Copyright © 2013-2015 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  The following additional terms are in effect as per Section 7 of the license:
#
#  The preservation of all legal notices and author attributions in
#  the material or in the Appropriate Legal Notices displayed
#  by works containing it is required.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; If not, see <http://www.gnu.org/licenses/>.


""" Features information """

# Note: As each desktop has its own features, these are listed
# in desktop_info file instead of here.

ICON_NAMES = {
    'aur': 'system-software-install',
    'bluetooth': 'bluetooth',
    'cups': 'printer',
    'firefox': 'firefox',
    'firewall': 'network-server',
    'fonts': 'preferences-desktop-font',
    'graphic_drivers' : 'gnome-system',
    'lamp': 'applications-internet',
    'lts': 'applications-accessories',
    'office': 'accessories-text-editor',
    'smb': 'gnome-mime-x-directory-smb-share',
    'visual': 'video-display'}

# See http://docs.python.org/2/library/gettext.html "22.1.3.4. Deferred translations"
def _(message):
    return message

TITLES = {
    'aur': _("Arch User Repository (AUR) Support"),
    'bluetooth': _("Bluetooth Support"),
    'fonts': _("Extra Truetype Fonts"),
    'graphic_drivers': _("Graphic drivers (Proprietary)"),
    'lamp': _("Apache (or Nginx) + Mariadb + PHP"),
    'cups': _("Printing Support"),
    'office': _("LibreOffice"),
    'visual': _("Visual Effects"),
    'firewall': _("Uncomplicated Firewall"),
    'lts': _("Kernel (LTS version)"),
    'firefox': _("Firefox Web Browser"),
    'smb': _("Windows sharing SMB")}

DESCRIPTIONS = {
    'aur': _("The AUR is a community-driven repository for Arch users."),
    'bluetooth': _("Enables your system to make wireless connections via Bluetooth."),
    'fonts': _("Installation of extra TrueType fonts"),
    'graphic_drivers': _("Installs AMD or Nvidia proprietary graphic driver"),
    'lamp': _("Apache (or Nginx) + Mariadb + PHP installation and setup"),
    'cups': _("Installation of printer drivers and management tools."),
    'office': _("Open source office suite. Supports editing MS Office files."),
    'visual': _("Enable transparency, shadows, and other desktop effects."),
    'firewall': _("Control the incoming and outgoing network traffic."),
    'lts': _("Long term support (LTS) Linux kernel and modules."),
    'firefox': _("A popular open-source graphical web browser from Mozilla"),
    'smb': _("SMB provides shared access to files and printers")}

TOOLTIPS = {
    'aur': _("Use yaourt to install AUR packages.\n"
                "The AUR was created to organize and share new packages\n"
                "from the community and to help expedite popular packages'\n"
                "inclusion into the [community] repository."),
    'bluetooth': _("Bluetooth is a standard for the short-range wireless\n"
                    "interconnection of cellular phones, computers, and\n"
                    "other electronic devices. In Linux, the canonical\n"
                    "implementation of the Bluetooth protocol stack is BlueZ"),
    'fonts':_("TrueType is an outline font standard developed by\n"
                "Apple and Microsoft in the late 1980s as a competitor\n"
                "to Adobe's Type 1 fonts used in PostScript. It has\n"
                "become the most common format for fonts on both the\n"
                "Mac OS and Microsoft Windows operating systems."),
    'graphic_drivers': _("Installs AMD or Nvidia proprietary graphic driver"),
    'lamp': _("This option installs a web server (you can choose\n"
                "Apache or Nginx) plus a database server (Mariadb)\n"
                "and PHP"),
    'cups': _("CUPS is the standards-based, open source printing\n"
                "system developed by Apple Inc. for OS® X and other\n"
                "UNIX®-like operating systems."),
    'office': _("LibreOffice is the free power-packed Open Source\n"
                "personal productivity suite for Windows, Macintosh\n"
                "and Linux, that gives you six feature-rich applications\n"
                "for all your document production and data processing\n"
                "needs: Writer, Calc, Impress, Draw, Math and Base."),
    'visual': _("Compton is a lightweight, standalone composite manager,\n"
                "suitable for use with window managers that do not natively\n"
                "provide compositing functionality. Compton itself is a fork\n"
                "of xcompmgr-dana, which in turn is a fork of xcompmgr.\n"
                "See the compton github page for further information."),
    'firewall': _("Ufw stands for Uncomplicated Firewall, and is a program for\n"
                "managing a netfilter firewall. It provides a command line\n"
                "interface and aims to be uncomplicated and easy to use."),
    'lts': _("The linux-lts package is an alternative Arch kernel package\n"
                "based upon Linux kernel 3.14 and is available in the core repository.\n"
                "This particular kernel version enjoys long-term support from upstream,\n"
                "including security fixes and some feature backports. Additionally, this\n"
                "package includes ext4 support. For Antergos users seeking a long-term\n"
                "support kernel, or who want a fallback kernel in case the latest kernel\n"
                "version causes problems, this option is the answer."),
    'firefox': _("Mozilla Firefox (known simply as Firefox) is a free and\n"
                "open-source web browser developed for Windows, OS X, and Linux,\n"
                "with a mobile version for Android, by the Mozilla Foundation and\n"
                "its subsidiary, the Mozilla Corporation. Firefox uses the Gecko\n"
                "layout engine to render web pages, which implements current and\n"
                "anticipated web standards."),
    'smb': _("In computer networking, Server Message Block (SMB)\n"
                "operates as an application-layer network protocol mainly used\n"
                "for providing shared access to files, printers, serial ports,\n"
                "and miscellaneous communications between nodes on a network.\n"
                "Most usage of SMB involves computers running Microsoft Windows.")}

# Delete previous _() dummy declaration
del _
