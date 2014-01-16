#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bootloader.py
#
#  Copyright 2013 Antergos
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

""" Detects which bootloader type must be installed. """

from gi.repository import Gtk
import os

class BootLoader(object):
    """ Detects which bootloader type must be installed. """
    def __init__(self, settings):
        """ Init class, load ui """
        self.settings = settings
        self.ui = Gtk.Builder()

        self.ui_dir = self.settings.get('ui')
        self.ui.add_from_file(os.path.join(self.ui_dir, "bootloader.ui"))
        self.ui.connect_signals(self)

        self.btns = {}
        self.btns["GRUB2"] = self.ui.get_object("GRUB2")
        self.btns["UEFI_x86_64"] = self.ui.get_object("UEFI_x86_64")
        self.btns["UEFI_i386"] = self.ui.get_object("UEFI_i386")

        # set bios as default
        self.btns["GRUB2"].set_active(True)

        self.dialog = self.ui.get_object("bootloader")
        self.title = self.ui.get_object("title")
        self.translate_ui()

    def translate_ui(self):
        """ Translates all ui widgets """
        txt = _("What type of boot system are you using?")
        txt = '<span weight="bold" size="large">%s</span>' % txt
        self.title.set_markup(txt)

        label = self.ui.get_object("GRUB2_label")
        txt = _("BIOS (Most Common)")
        label.set_markup(txt)

        label = self.ui.get_object("UEFI_x86_64_label")
        txt = _("64-bit UEFI")
        label.set_markup(txt)

        label = self.ui.get_object("UEFI_i386_label")
        txt = _("32-bit UEFI (old Macs)")
        label.set_markup(txt)

        label = self.ui.get_object("help_label")
        txt = _("Select 'cancel' if you don't want to install a boot loader.")
        label.set_markup(txt)

    def get_type(self):
        """ Return type """
        for k in self.btns:
            if self.btns[k].get_active():
                return k
        return ""

    def run(self):
        """ Shows dialog to choose bootloader type """
        bootloader_type = ""

        response = self.dialog.run()

        if response == Gtk.ResponseType.OK:
            bootloader_type = self.get_type()

        self.dialog.hide()

        return bootloader_type

    def ask(self):

        # Guess our bootloader type
        if os.path.exists("/sys/firmware/efi"):
            bootloader_type = "UEFI_x86_64"
        else:
            bootloader_type = "GRUB2"

        if len(bootloader_type) > 0:
            self.settings.set('install_bootloader', True)
            self.settings.set('bootloader_type', bootloader_type)
        else:
            self.settings.set('install_bootloader', False)
