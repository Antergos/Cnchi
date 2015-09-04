#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  desktop_info.py
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


""" Desktop Environments information """

# Enabled desktops

DESKTOPS = ["base", "cinnamon", "gnome", "kde4", "mate", "openbox", "xfce"]

DESKTOPS_DEV = DESKTOPS + ["enlightenment", "lxqt", "plasma5"]

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
    'kde4': "KDE 4",
    'plasma5': "KDE Plasma 5",
    'lxqt': "LXQt",
    'mate': "MATE"}

LIBS = {
    'gtk': ["cinnamon", "enlightenment", "gnome", "mate", "openbox", "xfce"],
    'qt': ["kde4", "lxqt", "plasma5"]}

ALL_FEATURES = ["aur", "bluetooth", "cups", "firefox", "fonts", "games", "graphic_drivers", "lamp", "lts", "office",
                "visual", "firewall", "smb"]

# Each desktop has its own available features
FEATURES = {
    'cinnamon': ["aur", "bluetooth", "cups", "firefox", "firewall", "fonts", "games", "graphic_drivers", "lts",
                 "office", "smb"],
    'gnome': ["aur", "bluetooth", "cups", "firefox", "firewall", "fonts", "games", "graphic_drivers", "lts",
              "office", "smb"],
    'kde4': ["aur", "bluetooth", "cups", "firefox", "firewall", "fonts", "games", "graphic_drivers", "lts",
             "office", "smb"],
    'plasma5': ["aur", "bluetooth", "cups", "firefox", "firewall", "fonts", "games", "graphic_drivers", "lts",
                "office", "smb"],
    'mate': ["aur", "bluetooth", "cups", "firefox", "firewall", "fonts", "lts", "office", "games", "graphic_drivers", "smb"],
    'enlightenment': ["aur", "bluetooth", "cups", "firefox", "firewall", "fonts", "games", "graphic_drivers", "lts",
                      "office", "smb"],
    'base': ["aur", "cups", "fonts", "lamp", "lts"],
    'openbox': ["aur", "bluetooth", "cups", "firefox", "firewall", "fonts", "games", "graphic_drivers", "lts",
                "office", "smb", "visual"],
    'lxqt': ["aur", "bluetooth", "cups", "firefox", "firewall", "fonts", "games", "graphic_drivers", "lts",
             "office", "smb"],
    'xfce': ["aur", "bluetooth", "cups", "firefox", "firewall", "fonts", "games", "graphic_drivers", "lts",
             "office", "smb"]}

# Session names for lightDM setup
SESSIONS = {
    'cinnamon': 'cinnamon',
    'gnome': 'gnome',
    'kde4': 'kde-plasma',
    'plasma5': 'kde-plasma',
    'mate': 'mate',
    'enlightenment': 'enlightenment',
    'openbox': 'openbox',
    'lxqt': 'lx-session',  # FIXME: check this!
    'xfce': 'xfce'}


# See http://docs.python.org/2/library/gettext.html "22.1.3.4. Deferred translations"
def _(message):
    return message


DESCRIPTIONS = {
    'gnome': _("GNOME 3 is an easy and elegant way to use your "
               "computer. It features the Activities Overview which "
               "is an easy way to access all your basic tasks. GNOME 3 is "
               "the default desktop in Antergos."),

    'cinnamon': _("Cinnamon is a fork of GNOME 3 developed "
                  "by (and for) Linux Mint. It provides users a more traditional desktop "
                  "interface along with the newest compositing techniques of GNOME 3. "
                  "Cinnamon is for users of all experience levels. "),

    'xfce': _("Xfce is a lightweight desktop environment. It aims to "
              "be fast and low on system resources, while remaining visually "
              "appealing and user friendly. It is a great option for use "
              "on older computers or those with low hardware specifications. "),

    'openbox': _("Openbox is a highly configurable, next generation window "
                 "manager with extensive standards support. It's default theme "
                 "is well known for its minimalistic appearance and flexibility. "
                 "Your desktop becomes cleaner, faster. Perfect for low hardware specifications, too."),

    'enlightenment': _("Enlightenment is not just a window manager for Linux/X11 "
                       "and others, but also a whole suite of libraries to help "
                       "you create beautiful user interfaces with much less work"),

    'kde4': _("If you are looking for a familiar working environment, KDE's "
              "Plasma Desktop offers all the tools required for a modern desktop "
              "computing experience so you can be productive right from the start."),

    'plasma5': _("Plasma 5.0 introduces a new major version of KDE's workspace offering. "
                 "It provides a visually updated core desktop experience that is easy to use "
                 "and familiar to the user. "),

    'lxqt': _("LXQt is an advanced, easy-to-use, and fast desktop environment "
              "based on Qt technologies. It has been tailored for users who "
              "value simplicity, speed, and an intuitive interface."),

    'base': _("This option will install Antergos as command-line only system, "
              "without any type of graphical interface. After the installation you can "
              "customize Antergos by installing packages with the command-line package manager."),

    'mate': _("An intuitive, attractive and lightweight desktop environment, fork of GNOME 2. "
              "MATE is one of the best options for use on older computers or those with low hardware "
              "specifications due to its lightweight yet very customizable set of features.")}

# Delete previous _() dummy declaration
del _
