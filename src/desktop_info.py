#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  desktop_info.py
#
#  Copyright © 2013-2017 Antergos
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


""" Desktop Environments information """

# Enabled desktops

DESKTOPS = ["base", "cinnamon", "deepin",
            "gnome", "kde", "mate", "openbox", "xfce"]

DESKTOPS_DEV = DESKTOPS + ["budgie", "enlightenment", "i3", "lxqt"]

DESKTOPS_A11Y = ["gnome", "mate"]

DESKTOP_ICONS_PATH = "/usr/share/cnchi/data/icons"

'''
MENU - Size appropriate for menus (16px).
SMALL_TOOLBAR - Size appropriate for small toolbars (16px).
LARGE_TOOLBAR - Size appropriate for large toolbars (24px)
BUTTON - Size appropriate for buttons (16px)
DND - Size appropriate for drag and drop (32px)
DIALOG - Size appropriate for dialogs (48px)
'''

# Descriptive names
NAMES = {
    'base': "Base",
    'cinnamon': "Cinnamon",
    'deepin': "Deepin",
    'gnome': "GNOME",
    'kde': "KDE",
    'mate': "MATE",
    'openbox': "Openbox",
    'xfce': "Xfce",
    'budgie': "Budgie",
    'enlightenment': "Enlightenment",
    'i3': "i3",
    'lxqt': "LXQt"
}

LIBS = {
    'gtk': [
        "cinnamon", "deepin", "gnome", "mate", "openbox", "xfce", "budgie", "enlightenment", "i3"],
    'qt': [
        "kde", "lxqt"]
}

ALL_FEATURES = ["a11y", "aur", "bluetooth", "cups", "chromium", "firefox", "firewall", "flash",
                "games", "graphic_drivers", "lamp", "lts", "office", "sshd", "visual", "vivaldi"]

# Not all desktops have all features
EXCLUDED_FEATURES = {
    'base': ["bluetooth", "chromium", "firefox", "firewall", "flash", "games",
             "graphic_drivers", "office", "visual", "vivaldi"],
    'cinnamon': ["lamp", "visual"],
    'deepin': ["lamp", "visual"],
    'gnome': ["lamp", "visual"],
    'kde': ["lamp", "visual"],
    'mate': ["lamp", "visual"],
    'openbox': ["lamp"],
    'xfce': ["lamp", "visual"],
    'budgie': ["lamp", "visual"],
    'enlightenment': ["lamp", "visual"],
    'i3': ["lamp"],
    'lxqt': ["lamp", "visual"]
}

# Session names for lightDM setup (/usr/share/xsessions)
SESSIONS = {
    'cinnamon': 'cinnamon',
    'deepin': 'deepin',
    'gnome': 'gnome',
    'kde': 'plasma',
    'mate': 'mate',
    'openbox': 'openbox',
    'xfce': 'xfce',
    'budgie': 'budgie-desktop',
    'enlightenment': 'enlightenment',
    'i3': 'i3',
    'lxqt': 'lxsession'
}


# See http://docs.python.org/2/library/gettext.html "22.1.3.4. Deferred translations"
def _(message):
    return message


DESCRIPTIONS = {
    'base':     _("This option will install Antergos as command-line only system, "
                  "without any type of graphical interface. After the installation "
                  "you can customize Antergos by installing packages with the "
                  "command-line package manager."),

    'cinnamon': _("Cinnamon is a Linux desktop which provides advanced, "
                  "innovative features and a traditional desktop user experience. "
                  "Cinnamon aims to make users feel at home by providing them with "
                  "an easy-to-use and comfortable desktop experience."),

    'deepin':   _("Deepin desktop is a lightweight, elegant desktop environment. "
                  "It was originally created for Linux Deepin distribution. Now, "
                  "DDE will support most Linux operating systems such as Arch Linux, "
                  "Ubuntu, Fedora, openSUSE etc."),

    'gnome':    _("GNOME 3 is an easy and elegant way to use your computer. "
                  "It features the Activities Overview which is an easy way to "
                  "access all your basic tasks."),

    'kde':      _("If you are looking for a familiar working environment, KDE's "
                  "Plasma Desktop offers all the tools required for a modern desktop "
                  "computing experience so you can be productive right from the start."),

    'mate':     _("MATE is an intuitive, attractive, and lightweight desktop "
                  "environment which provides a more traditional desktop "
                  "experience. Accelerated compositing is supported, but not "
                  "required to run MATE making it suitable for lower-end hardware."),

    'openbox':  _("Not actually a desktop environment, Openbox is a highly "
                  "configurable window manager. It is known for its "
                  "minimalistic appearance and its flexibility. It is the most "
                  "lightweight graphical option offered by antergos. Please "
                  "Note: Openbox is not recommended for users who are new to Linux."),

    'xfce':     _("Xfce is a lightweight desktop environment. It aims to "
                  "be fast and low on system resources, while remaining visually "
                  "appealing and user friendly. It suitable for use on older "
                  "computers and those with lower-end hardware specifications. "),

    'budgie':   _("Budgie is the flagship desktop of Solus and is a Solus project. "
                  "It focuses on simplicity and elegance. Written from scratch with "
                  "integration in mind, the Budgie desktop tightly integrates with "
                  "the GNOME stack, but offers an alternative desktop experience."),

    'enlightenment': _("Enlightenment is not just a window manager for Linux/X11 "
                       "and others, but also a whole suite of libraries to help "
                       "you create beautiful user interfaces with much less work"),

    'i3':       _("i3 is a tiling window manager, completely written from scratch. "
                  "The target platforms are GNU/Linux and BSD operating systems, "
                  "its code is Free and Open Source Software (FOSS) under the BSD "
                  "license. i3 is primarily targeted at advanced users and developers."),

    'lxqt':     _("LXQt is the next-generation of LXDE, the Lightweight Desktop "
                  "Environment. It is lightweight, modular, blazing-fast, and "
                  "user-friendly.")
}

# Delete previous _() dummy declaration
del _
