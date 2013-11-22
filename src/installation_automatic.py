#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  installation_automatic.py
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

import xml.etree.ElementTree as etree

from gi.repository import Gtk
import subprocess
import os
import sys
import misc
import logging
import installation_process

# To be able to test this installer in other systems
# that do not have pyparted3 installed
try:
    import parted
except:
    print("Can't import parted module! This installer won't work.")


_next_page = "timezone"
_prev_page = "installation_ask"

class InstallationAutomatic(Gtk.Box):

    def __init__(self, params):
        self.title = params['title']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        self.callback_queue = params['callback_queue']
        self.settings = params['settings']
        self.alternate_package_list = params['alternate_package_list']
        
        super().__init__()
        self.ui = Gtk.Builder()
        self.ui.add_from_file(os.path.join(self.ui_dir, "installation_automatic.ui"))

        self.ui.connect_signals(self)

        self.device_store = self.ui.get_object('part_auto_select_drive')
        self.device_label = self.ui.get_object('part_auto_select_drive_label')

        self.entry = {}
        self.entry['luks_password'] = self.ui.get_object('entry_luks_password')
        self.entry['luks_password_confirm']= self.ui.get_object('entry_luks_password_confirm')
        
        self.image_password_ok = self.ui.get_object('image_password_ok')
        
        super().add(self.ui.get_object("installation_automatic"))

        self.devices = dict()
        self.process = None

    def translate_ui(self):
        txt = _("Automatic Installation Mode")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.title.set_markup(txt)

        txt = _("Select drive:")
        self.device_label.set_markup(txt)

        label = self.ui.get_object('text_automatic')
        txt = _("WARNING! This will overwrite everything currently on your drive!")
        txt = "<b>%s</b>" % txt
        label.set_markup(txt)

        label = self.ui.get_object('text_automatic2')
        txt = _("Select the drive we should use to install Antergos " \
        "and then click below to start the process.")
        label.set_markup(txt)
        
        label = self.ui.get_object('label_luks_password')
        txt = _("Encryption Password:")
        label.set_markup(txt)

        label = self.ui.get_object('label_luks_password_confirm')
        txt = _("Confirm your password:")
        label.set_markup(txt)

        txt = _("Install Now!")
        self.forward_button.set_label(txt)

    @misc.raise_privileges
    def populate_devices(self):
        device_list = parted.getAllDevices()
        
        self.device_store.remove_all()
        self.devices = {}
                   
        for dev in device_list:
            ## avoid cdrom and any raid, lvm volumes or encryptfs
            if not dev.path.startswith("/dev/sr") and \
               not dev.path.startswith("/dev/mapper"):
                # hard drives measure themselves assuming kilo=1000, mega=1mil, etc
                size_in_gigabytes = int((dev.length * dev.sectorSize) / 1000000000)
                line = '{0} [{1} GB] ({2})'.format(dev.model, size_in_gigabytes, dev.path)
                self.device_store.append_text(line)
                self.devices[line] = dev.path
                logging.debug(line)

        self.select_first_combobox_item(self.device_store)

    def select_first_combobox_item(self, combobox):
        tree_model = combobox.get_model()
        tree_iter = tree_model.get_iter_first()
        combobox.set_active_iter(tree_iter)

    def on_select_drive_changed(self, widget):
        line = self.device_store.get_active_text()
        if line != None:
            self.auto_device = self.devices[line]
        self.forward_button.set_sensitive(True)

    def prepare(self, direction):
        self.translate_ui()
        self.populate_devices()
        self.show_all()
        
        if not self.settings.get('use_luks'):
            f = self.ui.get_object('frame_luks')
            f.hide()
            
        #self.forward_button.set_sensitive(False)

    def store_values(self):
        luks_password = self.entry['luks_password'].get_text()
        self.settings.set('luks_key_pass', luks_password)
        if luks_password != "":
            logging.debug("A LUKS password has been set")
            
        logging.info(_("Automatic install on %s") % self.auto_device)
        self.start_installation()
        return True

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page

    def refresh(self):
        while Gtk.events_pending():
            Gtk.main_iteration()
    
    def on_luks_password_changed(self, widget):
        luks_password = self.entry['luks_password'].get_text()
        luks_password_confirm = self.entry['luks_password_confirm'].get_text()
        install_ok = True
        if len(luks_password) <= 0:
            self.image_password_ok.set_opacity(0)
            self.forward_button.set_sensitive(True)
        else:
            if luks_password == luks_password_confirm:
                icon = "gtk-yes"
            else:
                icon = "gtk-no"
                install_ok = False
            self.image_password_ok.set_from_stock(icon, Gtk.IconSize.BUTTON)
            self.image_password_ok.set_opacity(1)

        self.forward_button.set_sensitive(install_ok)
    
    def start_installation(self):
        #self.install_progress.set_sensitive(True)
        logging.info(_("Cnchi will install Antergos on %s") % self.auto_device)      

        # Ask (if guessing doesn't work) bootloader type
        import bootloader
        bl = bootloader.BootLoader(self.settings)
        bl.ask()

        if self.settings.get('install_bootloader'):
            self.settings.set('bootloader_device', self.auto_device)
            logging.info(_("Antergos will install the %s bootloader on %s") % \
                (self.settings.get('bootloader_type'), self.settings.get('bootloader_device')))
        else:
            logging.warning("Antergos will not install any boot loader")

        # We don't need to pass neither which devices will be mounted nor which filesystems
        # the devices will be formated with, as auto_partition.py takes care of everything
        # in an automatic installation.
        mount_devices = {}
        fs_devices = {}
        
        self.settings.set('auto_device', self.auto_device)

        self.process = installation_process.InstallationProcess( \
                        self.settings, \
                        self.callback_queue, \
                        mount_devices, \
                        fs_devices, \
                        None, \
                        self.alternate_package_list)
                        
        self.process.start()
