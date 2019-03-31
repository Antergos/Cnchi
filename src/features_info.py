#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  features_info.py
#
#  Copyright © 2013-2018 Antergos
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

ICON_NAMES = {
    'a11y': 'a11y',
    'aur': 'system-software-install',
    'bluetooth': 'bluetooth',
    'cups': 'printer',
    'chromium': 'chromium',
    'energy': 'gnome-power-manager',
    'firefox': 'firefox',
    'vivaldi': 'vivaldi',
    'firewall': 'network-server',
    'flash': 'flash',
    'games': 'applications-games',
    'graphic_drivers': 'gnome-system',
    'lamp': 'applications-internet',
    'lembrame': 'com.antergos.Lembrame',
    'lts': 'applications-accessories',
    'office': 'accessories-text-editor',
    'sshd': 'network-connect',
    'visual': 'video-display'}
""" dict: Icon names for each feature.

As each desktop has its own features, these are listed
in desktop_info module instead of here. """


ADVANCED = [
    'aur', 'firefox', 'vivaldi', 'firewall', 'flash', 'graphic_drivers',
    'lamp', 'lts', 'sshd', 'visual']
""" list: These features are considered 'advanced' so it won't be shown by default """


def _(message):
    """ See http://docs.python.org/2/library/gettext.html "22.1.3.4. Deferred translations" """
    return message


TITLES = {
    'a11y': _("Adds accessibility packages"),
    'aur': _("Arch User Repository (AUR) Support"),
    'bluetooth': _("Bluetooth Support"),
    'cups': _("Printing Support"),
    'chromium': _("Chromium Web Browser"),
    'energy': _("Advanced power management"),
    'firefox': _("Firefox Web Browser"),
    'vivaldi': _("Vivaldi Web Browser"),
    'firewall': _("Uncomplicated Firewall"),
    'flash': _("Flash plugins"),
    'games': _("Steam + PlayonLinux"),
    'graphic_drivers': _("Graphic drivers (Proprietary)"),
    'lamp': _("Apache (or Nginx) + Mariadb + PHP"),
    'lembrame': _("Lembrame"),
    'lts': _("Kernel (LTS version)"),
    'office': _("LibreOffice"),
    'sshd': _("SSH Service"),
    'visual': _("Visual Effects")}
""" dict: Feature titles """

DESCRIPTIONS = {
    'a11y': _("Useful packages for individuals who are blind or visually impaired."),
    'aur': _("The AUR is a community-driven repository for Arch users."),
    'bluetooth': _("Enables your system to make wireless connections via Bluetooth."),
    'chromium': _("Open-source web browser from Google."),
    'energy': _("Brings you the benefits of advanced power management for Linux."),
    'firefox': _("A popular open-source graphical web browser from Mozilla."),
    'vivaldi': _("Vivaldi is a free, fast web browser designed for power-users."),
    'flash': _("Freeware software normally used for multimedia."),
    'graphic_drivers': _("Installs AMD or Nvidia proprietary graphic driver."),
    'games': _("Installs Steam and Playonlinux for gaming enthusiasts."),
    'lamp': _("Apache (or Nginx) + Mariadb + PHP installation and setup."),
    'lembrame': _("Sync your Gnome and system settings between installations"),
    'cups': _("Installation of printer drivers and management tools."),
    'office': _("Open source office suite. Supports editing MS Office files."),
    'visual': _("Enable transparency, shadows, and other desktop effects."),
    'firewall': _("Control the incoming and outgoing network traffic."),
    'sshd': _("Enables Secure SHell service."),
    'lts': _("Long term support (LTS) Linux kernel and modules.")}
""" dict: Feature descriptions """

TOOLTIPS = {
    'a11y': _("Useful packages for individuals who are blind or visually impaired."),
    'aur': _("Use yay to install packages from the Arch User Repository.\n"
             "The AUR was created to organize and share new packages\n"
             "from the community and to help expedite popular packages'\n"
             "inclusion into the [community] repository."),
    'bluetooth': _("Bluetooth is a standard for the short-range wireless\n"
                   "interconnection of cellular phones, computers, and\n"
                   "other electronic devices. In Linux, the canonical\n"
                   "implementation of the Bluetooth protocol stack is BlueZ."),
    'cups': _("CUPS is the standards-based, open source printing\n"
              "system developed by Apple Inc. for OS® X and other\n"
              "UNIX®-like operating systems."),
    'chromium': _("Chromium is an open-source browser project that aims to build a\n"
                  "safer, faster, and more stable way for all users to experience the web.\n"
                  "(this is the default)"),
    'energy': _("TLP brings you the benefits of advanced power management for Linux\n"
                "without the need to understand every technical detail. TLP comes with\n"
                "a default configuration already optimized for battery life, so you may\n"
                "just install and forget it. Nevertheless TLP is highly customizable to\n"
                "fulfill your specific requirements."),
    'firefox': _("Mozilla Firefox (known simply as Firefox) is a free and\n"
                 "open-source web browser developed for Windows, OS X, and Linux,\n"
                 "with a mobile version for Android, by the Mozilla Foundation and\n"
                 "its subsidiary, the Mozilla Corporation. Firefox uses the Gecko\n"
                 "layout engine to render web pages, which implements current and\n"
                 "anticipated web standards.  Enable this option to install Firefox\n"
                 "instead of Chromium"),
    'vivaldi': _("Vivaldi is a freeware, cross-platform web browser developed by\n"
                 "Vivaldi Technologies. It was officially launched on April 12, 2016.\n"
                 "The browser is aimed at staunch technologists, heavy Internet users,\n"
                 "and previous Opera web browser users disgruntled by Opera's transition\n"
                 "from the Presto layout engine to the Blink layout engine, which\n"
                 "removed many popular features."),
    'firewall': _("Ufw stands for Uncomplicated Firewall, and is a program for\n"
                  "managing a netfilter firewall. It provides a command line\n"
                  "interface and aims to be uncomplicated and easy to use."),
    'flash': _("Adobe Flash Player is freeware software for using content created\n"
               "on the Adobe Flash platform, including viewing multimedia, executing\n"
               "rich internet applications and streaming video and audio."),
    'games': _("Steam is one of the most popular gaming clients that supports\n"
               "linux in technology and gaming, while PlayOnLinux\n"
               "is a very easy manager to setting up games to play\n"
               "through wine, instead of doing it manually."),
    'graphic_drivers': _("Installs AMD or Nvidia proprietary graphics driver instead\n"
                         "of the open-source variant. Do NOT install this if you have a\n"
                         "Nvidia Optimus laptop"),
    'lamp': _("This option installs a web server (you can choose\n"
              "Apache or Nginx) plus a database server (Mariadb)\n"
              "and PHP."),
    'lembrame': _("Lembrame is a concept tool to sync your settings to the cloud\n"
                  "and reuse them on your next install to have the same desktop settings,\n"
                  "packages and more."),
    'lts': _("The linux-lts package is an alternative Arch kernel package.\n"
             "This particular kernel version enjoys long-term support from upstream,\n"
             "including security fixes and some feature backports. Additionally, this\n"
             "package includes ext4 support. For Antergos users seeking a long-term\n"
             "support kernel, or who want a fallback kernel in case the latest kernel\n"
             "version causes problems, this option is the answer."),
    'office': _("LibreOffice is the free power-packed Open Source\n"
                "personal productivity suite for Windows, Macintosh\n"
                "and Linux, that gives you six feature-rich applications\n"
                "for all your document production and data processing\n"
                "needs: Writer, Calc, Impress, Draw, Math and Base."),
    'sshd': _("Secure Shell (SSH) is a network protocol that allows data to be\n"
              "exchanged over a secure channel between two computers.\n"
              "SSH is typically used to log into a remote machine and execute commands.\n"),
    'visual': _("Compton is a lightweight, standalone composite manager,\n"
                "suitable for use with window managers that do not natively\n"
                "provide compositing functionality. Compton itself is a fork\n"
                "of xcompmgr-dana, which in turn is a fork of xcompmgr.\n"
                "See the compton github page for further information.")}
""" dict: Feature tooltips """

# Delete previous _() dummy declaration
del _
