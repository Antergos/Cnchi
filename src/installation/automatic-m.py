#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  installation_automatic.py
#
#  This file was forked from Cnchi (graphical installer from Antergos)
#  Check it at https://github.com/antergos
#
#  Copyright 2013 Antergos (http://antergos.com/)
#  Copyright 2013 Manjaro (http://manjaro.org)
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
import os
import canonical.misc as misc
import logging
from installation import process as installation_process

# To be able to test this installer in other systems that do not have pyparted3 installed
try:
    import parted
except:
    print("Can't import parted module! This installer won't work.")

_next_page = "user_info"
_prev_page = "installation_ask"

class InstallationAutomatic(Gtk.Box):

    def __init__(self, params):
        self.title = params['title']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        self.callback_queue = params['callback_queue']
        self.settings = params['settings']
        self.alternate_package_list = params['alternate_package_list']
        self.testing = params['testing']

        super().__init__()
        self.ui = Gtk.Builder()
        self.ui_dir = self.settings.get('ui')
        self.ui.add_from_file(os.path.join(self.ui_dir, "installation_automatic.ui"))

        self.ui.connect_signals(self)

        self.device_store = self.ui.get_object('part_auto_select_drive')
        self.device_label = self.ui.get_object('part_auto_select_drive_label')

        self.entry = {}
        self.entry['luks_password'] = self.ui.get_object('entry_luks_password')
        self.entry['luks_password_confirm'] = self.ui.get_object('entry_luks_password_confirm')

        self.image_password_ok = self.ui.get_object('image_password_ok')

        super().add(self.ui.get_object("installation_automatic"))

        self.devices = dict()
        self.process = None

    def translate_ui(self):
        txt = _("Automatic installation mode")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.title.set_markup(txt)

        txt = _("Select drive:")
        self.device_label.set_markup(txt)

        label = self.ui.get_object('text_automatic')
        txt = _("WARNING! This installation mode will overwrite everything on your drive!")
        txt = "<b>%s</b>" % txt
        label.set_markup(txt)

        label = self.ui.get_object('text_automatic2')
        txt = _("Please choose the drive where you want to install Manjaro\nand click the button below to start the process.")
        txt = "%s" % txt
        label.set_markup(txt)

        label = self.ui.get_object('label_luks_password')
        txt = _("Encryption Password:")
        label.set_markup(txt)

        label = self.ui.get_object('label_luks_password_confirm')
        txt = _("Confirm your password:")
        label.set_markup(txt)

        btn = self.ui.get_object('checkbutton_show_password')
        btn.set_label(_("Show password"))

        txt = _("Install now!")
        self.forward_button.set_label(txt)

    def on_checkbutton_show_password_toggled(self, widget):
        """ show/hide LUKS passwords """
        btn = self.ui.get_object('checkbutton_show_password')
        show = btn.get_active()
        self.entry['luks_password'].set_visibility(show)
        self.entry['luks_password_confirm'].set_visibility(show)

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
        if line is not None:
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
        """ The user clicks 'Install now!' """
        response = self.show_warning()
        if response == Gtk.ResponseType.NO:
            return False

        luks_password = self.entry['luks_password'].get_text()
        self.settings.set('luks_key_pass', luks_password)
        if luks_password != "":
            logging.debug(_("A LUKS password has been set"))

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

    def show_warning(self):
        txt = _("Do you really want to proceed and delete all your content on your hard drive?\n\n%s") % self.device_store.get_active_text()
        message = Gtk.MessageDialog(None,
                          Gtk.DialogFlags.MODAL,
                          Gtk.MessageType.QUESTION,
                          Gtk.ButtonsType.YES_NO,
                          txt)
        response = message.run()
        message.destroy()
        return response

    def start_installation(self):
        #self.install_progress.set_sensitive(True)
        logging.info(_("Thus will use %s as installation device") % self.auto_device)

        self.settings.set('install_bootloader', True)
        if self.settings.get('install_bootloader'):
            if self.settings.get('efi'):
                self.settings.set('bootloader_type', "UEFI_x86_64")
                self.settings.set('bootloader_location', '/boot/efi')
            else:
                self.settings.set('bootloader_type', "GRUB2")
                self.settings.set('bootloader_location', self.auto_device)

            logging.info(_("Thus will install the bootloader of type %s in %s") %
                          (self.settings.get('bootloader_type'),
                           self.settings.get('bootloader_location')))
        else:
            logging.warning(_("Thus will not install any boot loader"))

        # We don't need to pass neither which devices will be mounted nor which filesystems
        # the devices will be formated with, as auto_partition.py takes care of everything
        # in an automatic installation.
        mount_devices = {}
        fs_devices = {}

        self.settings.set('auto_device', self.auto_device)

        if not self.testing:
            self.process = installation_process.InstallationProcess(
                            self.settings,
                            self.callback_queue,
                            mount_devices,
                            fs_devices,
                            None,
                            self.alternate_package_list)

            self.process.start()
        else:
            logging.warning(_("Testing mode. Thus won't apply any changes to your system!"))