#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  desktop_info.py
#
#  Copyright © 2013-2016 Antergos
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

DESKTOPS = ["base", "cinnamon", "enlightenment", "gnome", "kde", "mate", "openbox", "xfce"]

DESKTOPS_DEV = DESKTOPS + ["lxqt"]

DESKTOP_ICONS_PATH = "/usr/share/cnchi/data/icons"

'''
MENU - Size appropriate for menus (16px).
SMALL_TOOLBAR - Size appropriate for small toolbars (16px).
LARGE_TOOLBAR - Size appropriate for large toolbars (24px)
BUTTON - Size appropriate for buttons (16px )
DND - Size appropriate for drag and drop (32px )
DIALOG - Size appropriate for dialogs (48px )
'''

# Descriptive names
NAMES = {
    'base': "Base",
    'gnome': "GNOME",
    'cinnamon': "Cinnamon",
    'xfce': "Xfce",
    'openbox': "Openbox",
    'enlightenment': "Enlightenment",
    'kde': "KDE Plasma",
    'lxqt': "LXQt",
    'mate': "MATE"
}

LIBS = {
    'gtk': ["cinnamon", "enlightenment", "gnome", "mate", "openbox", "xfce"],
    'qt': ["kde", "lxqt"]
}

ALL_FEATURES = ["aur", "bluetooth", "cups", "chromium", "firefox", "firewall", "flash",
                "fonts", "games", "graphic_drivers", "lamp", "lts", "office",
                "visual", "smb"]

# Not all desktops have all features
EXCLUDED_FEATURES = {
    'cinnamon': ["lamp", "visual"],
    'gnome': ["lamp", "visual"],
    'kde': ["lamp", "visual"],
    'mate': ["lamp", "visual"],
    'enlightenment': ["lamp", "visual"],
    'base': ["bluetooth", "chromium", "firefox", "firewall", "flash", "games",
             "graphic_drivers", "office", "smb", "visual"],
    'openbox': ["lamp"],
    'lxqt': ["lamp", "visual"],
    'xfce': ["lamp", "visual"]
}

# Session names for lightDM setup
SESSIONS = {
    'cinnamon': 'cinnamon',
    'gnome': 'gnome',
    'kde': 'plasma',
    'mate': 'mate',
    'enlightenment': 'enlightenment',
    'openbox': 'openbox',
    'lxqt': 'lx-session',
    'xfce': 'xfce'
}


# See http://docs.python.org/2/library/gettext.html "22.1.3.4. Deferred translations"
def _(message):
    return message


DESCRIPTIONS = {
    'gnome': _("GNOME 3 is an easy and elegant way to use your "
               "computer. It features the Activities Overview which "
               "is an easy way to access all your basic tasks."),

    'cinnamon': _("Cinnamon is a Linux desktop which provides advanced, "
                  "innovative features and a traditional desktop user experience. "
                  "Cinnamon aims to make users feel at home by providing them with "
                  "an easy-to-use and comfortable desktop experience."),

    'xfce': _("Xfce is a lightweight desktop environment. It aims to "
              "be fast and low on system resources, while remaining visually "
              "appealing and user friendly. It suitable for use on older "
              "computers and those with lower-end hardware specifications. "),

    'openbox': _("Not actually a desktop environment, Openbox is a highly "
                 "configurable window manager. It is known for its "
                 "minimalistic appearance and its flexibility. It is the most "
                 "lightweight graphical option offered by antergos. Please "
                 "Note: Openbox is not recommended for users who are new to Linux."),

    'enlightenment': _("Enlightenment is not just a window manager for Linux/X11 "
                       "and others, but also a whole suite of libraries to help "
                       "you create beautiful user interfaces with much less work"),

    'kde': _("If you are looking for a familiar working environment, KDE's "
             "Plasma Desktop offers all the tools required for a modern desktop "
             "computing experience so you can be productive right from the start."),

    'lxqt': _("LXQt is the next-generation of LXDE, the Lightweight Desktop "
              "Environment. It is lightweight, modular, blazing-fast, and "
              "user-friendly."),

    'base': _("This option will install Antergos as command-line only system, "
              "without any type of graphical interface. After the installation you can "
              "customize Antergos by installing packages with the command-line package manager."),

    'mate': _("MATE is an intuitive, attractive, and lightweight desktop "
              "environment which provides a more traditional desktop "
              "experience. Accelerated compositing is supported, but not "
              "required to run MATE making it suitable for lower-end hardware.")
}

# Delete previous _() dummy declaration
del _
