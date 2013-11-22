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

from gi.repository import Gtk, GObject

import subprocess
import os

class BootLoader():
    def __init__(self, settings):
        self.settings = settings
        self.ui_dir = self.settings.get('ui')
        self.ui = Gtk.Builder()

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
        for k in self.btns:
            if self.btns[k].get_active():
                return k
        return ""

    def run(self):
        bl_type = ""
        
        response = self.dialog.run()
        
        if response == Gtk.ResponseType.OK:
            bl_type = self.get_type()

        self.dialog.hide()
        
        return bl_type

    def ask(self):
        bt = ""
        
        force_grub_type = self.settings.get('force_grub_type')
        
        if force_grub_type == "ask":
            # Ask bootloader type
            bt = bl.run()
        elif force_grub_type == "efi":
            bt = "UEFI_x86_64"
        elif force_grub_type == "bios":
            bt = "GRUB2"
        elif force_grub_type == "none":
            bt = ""
        else:
            # Guess our bootloader type
            if os.path.exists("/sys/firmware/efi/systab"):
                bt = "UEFI_x86_64"
            else:
                bt = "GRUB2"
        
        if len(bt) > 0:
            self.settings.set('install_bootloader', True)
            self.settings.set('bootloader_type', bt)
        else:
            self.settings.set('install_bootloader', False)
