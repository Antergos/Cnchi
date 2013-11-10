#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  installation_ask.py
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

from gi.repository import Gtk

import subprocess
import os
import logging
import bootinfo

import config

_prev_page = "features"

class InstallationAsk(Gtk.Box):

    def __init__(self, params):
        self.title = params['title']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        self.settings = params['settings']
        
        super().__init__()
        self.ui = Gtk.Builder()
        self.ui.add_from_file(os.path.join(self.ui_dir, "installation_ask.ui"))

        partitioner_dir = os.path.join(self.settings.get("data"), "partitioner/small/")

        image = self.ui.get_object("automatic_image")
        image.set_from_file(partitioner_dir + "automatic.png")

        image = self.ui.get_object("alongside_image")
        image.set_from_file(partitioner_dir + "alongside.png")

        image = self.ui.get_object("advanced_image")
        image.set_from_file(partitioner_dir + "advanced.png")

        self.ui.connect_signals(self)

        super().add(self.ui.get_object("installation_ask"))
        
        oses = {}
        oses = bootinfo.get_os_dict()
        
        self.otherOS = ""
        for k in oses:
            if "sda" in k and oses[k] != "unknown":
                self.otherOS = oses[k]
                
        # by default, select automatic installation
        self.next_page = "installation_automatic"
        
    def enable_automatic_options(self, status):
        objects = [ "encrypt_checkbutton", "encrypt_label", "lvm_checkbutton", "lvm_label" ]
        for o in objects:
            ob = self.ui.get_object(o)
            ob.set_sensitive(status)
        
    def prepare(self, direction):
        self.translate_ui()
        self.show_all()
        
        # Always hide alongside option. It is not ready yet
        # if "windows" not in self.otherOS.lower():
        radio = self.ui.get_object("alongside_radiobutton")
        radio.hide()
        label = self.ui.get_object("alongside_description")
        label.hide()

    def translate_ui(self):
        txt = _("Installation Type")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.title.set_markup(txt)
        
        # In case we're coming from an installer screen, we change
        # to forward stock button and we activate it
        self.forward_button.set_label("gtk-go-forward")
        self.forward_button.set_sensitive(True)

        ## AUTOMATIC INSTALL
        radio = self.ui.get_object("automatic_radiobutton")
        radio.set_label(_("Erase disk and install Antergos"))

        label = self.ui.get_object("automatic_description")
        txt = _("Warning: This will erase ALL data on your disk.")
        txt = '<span weight="light" size="small">%s</span>' % txt
        label.set_markup(txt)
        label.set_line_wrap(True)
        
        button = self.ui.get_object("encrypt_checkbutton")
        txt = _("Encrypt this installation for increased security.")
        button.set_label(txt)
        
        label = self.ui.get_object("encrypt_label")
        txt = _("You will be asked to create an encryption password in the next step.")
        txt = '<span weight="light" size="small">%s</span>' % txt
        label.set_markup(txt)
        
        button = self.ui.get_object("lvm_checkbutton")
        txt = "Use LVM with this installation."
        button.set_label(txt)
        
        label = self.ui.get_object("lvm_label")
        txt = _("This will setup LVM and allow you to easily manage partitions and create snapshots.")
        txt = '<span weight="light" size="small">%s</span>' % txt
        label.set_markup(txt)
        
        ## ALONGSIDE INSTALL (still experimental. Needs a lot of testing)
        if "windows" in self.otherOS.lower():
            radio = self.ui.get_object("alongside_radiobutton")
            label = self.ui.get_object("alongside_description")
            radio.set_label(_("Install Antergos alongside %s") % self.otherOS)

            txt = _("Install Antergos alongside %s") % self.otherOS
            txt = '<span weight="light" size="small">%s</span>' % txt
            label.set_markup(txt)
            label.set_line_wrap(True)
        
        ## ADVANCED INSTALL
        radio = self.ui.get_object("advanced_radiobutton")
        radio.set_label(_("Choose exactly where Antergos should be installed. (advanced)"))

        label = self.ui.get_object("advanced_description")
        txt = _("Edit partition table and choose mount points.")
        txt = '<span weight="light" size="small">%s</span>' % txt
        label.set_markup(txt)
        label.set_line_wrap(True)

    def store_values(self):
        check = self.ui.get_object("encrypt_checkbutton")
        use_luks = check.get_active()
        
        check = self.ui.get_object("lvm_checkbutton")
        use_lvm = check.get_active()
                
        if self.next_page == "installation_automatic":
            self.settings.set('use_lvm', use_lvm)
            self.settings.set('use_luks', use_luks)
        else:
            self.settings.set('use_lvm', False)
            self.settings.set('use_luks', False)

        if self.settings.get('use_luks'):
            logging.info(_("Antergos installation will be encrypted using LUKS"))
            
        if self.settings.get('use_lvm'):
            logging.info(_("Antergos will be installed using LVM volumes"))
            
        if self.next_page == "installation_alongside":
            self.settings.set('partition_mode', 'alongside')
        elif self.next_page == "installation_advanced":
            self.settings.set('partition_mode', 'advanced')
        elif self.next_page == "installation_automatic":
            self.settings.set('partition_mode', 'automatic')
                
        return True

    def get_next_page(self):
        return self.next_page

    def get_prev_page(self):
        return _prev_page

    def on_automatic_radiobutton_toggled(self, widget):
        if widget.get_active():
            self.next_page = "installation_automatic"
            self.enable_automatic_options(True)

    def on_easy_radiobutton_toggled(self, widget):
        if widget.get_active():
            self.next_page = "installation_alongside"
            self.enable_automatic_options(False)

    def on_advanced_radiobutton_toggled(self, widget):
        if widget.get_active():
            self.next_page = "installation_advanced"
            self.enable_automatic_options(False)
