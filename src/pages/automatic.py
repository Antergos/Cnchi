#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# automatic.py
#
# Copyright © 2013-2017 Antergos
#
# This file is part of Cnchi.
#
# Cnchi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Cnchi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# The following additional terms are in effect as per Section 7 of the license:
#
# The preservation of all legal notices and author attributions in
# the material or in the Appropriate Legal Notices displayed
# by works containing it is required.
#
# You should have received a copy of the GNU General Public License
# along with Cnchi; If not, see <http://www.gnu.org/licenses/>.


""" Automatic installation screen """

import os
import logging

import parted

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from pages.gtkbasebox import GtkBaseBox

from installation import install
from installation import action
from installation import auto_partition

import misc.extra as misc
import parted3.fs_module as fs

DEST_DIR = "/install"


class InstallationAutomatic(GtkBaseBox):
    """ Automatic Installation Screen """

    def __init__(self, params, prev_page="installation_ask", next_page="summary"):
        super().__init__(self, params, "automatic", prev_page, next_page)

        self.auto_device = None

        self.device_store = self.ui.get_object('part_auto_select_drive')
        self.device_label = self.ui.get_object('part_auto_select_drive_label')

        self.entry = {
            'luks_password': self.ui.get_object('entry_luks_password'),
            'luks_password_confirm': self.ui.get_object('entry_luks_password_confirm')}

        self.image_password_ok = self.ui.get_object('image_password_ok')

        self.devices = {}
        self.installation = None

        self.bootloader = "grub2"
        self.bootloader_entry = self.ui.get_object('bootloader_entry')
        self.bootloader_device_entry = self.ui.get_object(
            'bootloader_device_entry')
        self.bootloader_devices = {}
        self.bootloader_device = {}

        self.mount_devices = {}
        self.fs_devices = {}

    def translate_ui(self):
        """ Translate widgets """
        txt = _("Select drive:")
        self.device_label.set_markup(txt)

        label = self.ui.get_object('text_automatic')
        txt = _("WARNING! This will overwrite everything currently on your drive!")
        txt = "<b>{0}</b>".format(txt)
        label.set_markup(txt)

        label = self.ui.get_object('info_label')
        txt = _("Select the drive we should use to install Antergos and then "
                "click above to start the process.")
        label.set_markup(txt)

        label = self.ui.get_object('label_luks_password')
        txt = _("Encryption Password:")
        label.set_markup(txt)

        label = self.ui.get_object('label_luks_password_confirm')
        txt = _("Confirm your password:")
        label.set_markup(txt)

        label = self.ui.get_object('label_luks_password_warning')
        txt = _(
            "LUKS Password. We do not recommend using special characters or accents!")
        label.set_markup(txt)

        btn = self.ui.get_object('checkbutton_show_password')
        btn.set_label(_("Show password"))

        self.header.set_subtitle(_("Automatic Installation Mode"))

        txt = _("Use the device below for boot loader installation:")
        txt = "<span weight='bold' size='small'>{0}</span>".format(txt)
        label = self.ui.get_object('bootloader_device_info_label')
        label.set_markup(txt)

        txt = _("Bootloader:")
        label = self.ui.get_object('bootloader_label')
        label.set_markup(txt)

        txt = _("Device:")
        label = self.ui.get_object('bootloader_device_label')
        label.set_markup(txt)

    def on_checkbutton_show_password_toggled(self, widget):
        """ show/hide LUKS passwords """
        btn = self.ui.get_object('checkbutton_show_password')
        show = btn.get_active()
        self.entry['luks_password'].set_visibility(show)
        self.entry['luks_password_confirm'].set_visibility(show)

    def populate_devices(self):
        """ Fill list with devices """
        with misc.raised_privileges() as __:
            device_list = parted.getAllDevices()

        self.device_store.remove_all()
        self.devices = {}

        self.bootloader_device_entry.remove_all()
        self.bootloader_devices.clear()

        for dev in device_list:
            # avoid cdrom and any raid, lvm volumes or encryptfs
            if not dev.path.startswith("/dev/sr") and \
               not dev.path.startswith("/dev/mapper"):
                # hard drives measure themselves assuming kilo=1000, mega=1mil, etc
                size_in_gigabytes = int(
                    (dev.length * dev.sectorSize) / 1000000000)
                line = '{0} [{1} GB] ({2})'
                line = line.format(dev.model, size_in_gigabytes, dev.path)
                self.device_store.append_text(line)
                self.devices[line] = dev.path
                self.bootloader_device_entry.append_text(line)
                self.bootloader_devices[line] = dev.path
                logging.debug(line)

        self.select_first_combobox_item(self.device_store)
        self.select_first_combobox_item(self.bootloader_device_entry)

    @staticmethod
    def select_first_combobox_item(combobox):
        """ Selects first item """
        tree_model = combobox.get_model()
        tree_iter = tree_model.get_iter_first()
        combobox.set_active_iter(tree_iter)

    def on_select_drive_changed(self, widget):
        """ User selected another drive """
        line = self.device_store.get_active_text()
        if line is not None:
            self.auto_device = self.devices[line]
        self.forward_button.set_sensitive(True)

    def prepare(self, direction):
        """ Get screen ready """
        self.translate_ui()
        self.populate_devices()

        self.show_all()
        self.fill_bootloader_entry()

        luks_grid = self.ui.get_object('luks_grid')
        luks_grid.set_sensitive(self.settings.get('use_luks'))

    def store_values(self):
        """ User clicks on Install now! """
        luks_password = self.entry['luks_password'].get_text()
        self.settings.set('luks_root_password', luks_password)
        if luks_password != "":
            logging.debug("A root LUKS password has been set")

        self.set_bootloader()

        return True

    def on_luks_password_changed(self, widget):
        """ User has changed LUKS password """
        luks_password = self.entry['luks_password'].get_text()
        luks_password_confirm = self.entry['luks_password_confirm'].get_text()
        install_ok = True
        if len(luks_password) <= 0:
            self.image_password_ok.set_opacity(0)
            self.forward_button.set_sensitive(True)
        else:
            if luks_password == luks_password_confirm:
                icon = "emblem-default"
            else:
                icon = "dialog-warning"
                install_ok = False

            self.image_password_ok.set_from_icon_name(
                icon,
                Gtk.IconSize.LARGE_TOOLBAR)
            self.image_password_ok.set_opacity(1)

        self.forward_button.set_sensitive(install_ok)

    def fill_bootloader_entry(self):
        """ Put the bootloaders for the user to choose """
        self.bootloader_entry.remove_all()

        if os.path.exists('/sys/firmware/efi'):
            self.bootloader_entry.append_text("Grub2")
            self.bootloader_entry.append_text("Systemd-boot")
            # TODO: add rEFInd bootloader
            # self.bootloader_entry.append_text("rEFInd")
            self.bootloader_entry.set_active(0)
            self.bootloader_entry.show()
        else:
            self.bootloader_entry.hide()
            widget_ids = ["bootloader_label", "bootloader_device_label"]
            for widget_id in widget_ids:
                widget = self.ui.get_object(widget_id)
                widget.hide()

    def on_bootloader_device_check_toggled(self, checkbox):
        """ User wants to install (or not) boot loader """
        status = checkbox.get_active()

        widget_ids = [
            "bootloader_device_entry",
            "bootloader_entry",
            "bootloader_label",
            "bootloader_device_label"]

        for widget_id in widget_ids:
            widget = self.ui.get_object(widget_id)
            widget.set_sensitive(status)

        self.settings.set('bootloader_install', status)

    def on_bootloader_device_entry_changed(self, widget):
        """ Get new selected bootloader device """
        line = self.bootloader_device_entry.get_active_text()
        if line is not None:
            self.bootloader_device = self.bootloader_devices[line]

    def on_bootloader_entry_changed(self, widget):
        """ Get new selected bootloader """
        line = self.bootloader_entry.get_active_text()
        if line is not None:
            self.bootloader = line.lower()

    def get_changes(self):
        """ Grab all changes for confirmation """
        change_list = [action.Action("delete", self.auto_device)]

        auto = auto_partition.AutoPartition(
            dest_dir=DEST_DIR,
            auto_device=self.auto_device,
            use_luks=self.settings.get("use_luks"),
            luks_password=self.settings.get("luks_root_password"),
            use_lvm=self.settings.get("use_lvm"),
            use_home=self.settings.get("use_home"),
            bootloader=self.settings.get("bootloader"),
            callback_queue=self.callback_queue)

        devices = auto.get_devices()
        mount_devices = auto.get_mount_devices()
        fs_devices = auto.get_fs_devices()

        mount_points = {}
        for mount_point in mount_devices:
            device = mount_devices[mount_point]
            mount_points[device] = mount_point

        for device in sorted(fs_devices.keys()):
            try:
                txt = _("Device {0} will be created ({1} filesystem) as {2}")
                txt = txt.format(
                    device, fs_devices[device], mount_points[device])
            except KeyError:
                txt = _("Device {0} will be created ({1} filesystem)")
                txt = txt.format(device, fs_devices[device])
            act = action.Action("info", txt)
            change_list.append(act)

        return change_list

    def run_format(self):
        """ Create partitions and format them """

        logging.debug(
            "Creating partitions and their filesystems in %s",
            self.auto_device)

        # If no key password is given a key file is generated and stored in /boot
        # (see auto_partition.py)

        auto = auto_partition.AutoPartition(
            dest_dir=DEST_DIR,
            auto_device=self.auto_device,
            use_luks=self.settings.get("use_luks"),
            luks_password=self.settings.get("luks_root_password"),
            use_lvm=self.settings.get("use_lvm"),
            use_home=self.settings.get("use_home"),
            bootloader=self.settings.get("bootloader"),
            callback_queue=self.callback_queue)
        auto.run()

        # Get mount_devices and fs_devices
        # (mount_devices will be used when configuring GRUB in
        #  modify_grub_default)
        # (fs_devices will be used when configuring the fstab file)
        self.mount_devices = auto.get_mount_devices()
        self.fs_devices = auto.get_fs_devices()

    def set_bootloader(self):
        """ Store bootloader options """
        checkbox = self.ui.get_object("bootloader_device_check")
        if not checkbox.get_active():
            self.settings.set('bootloader_install', False)
            logging.info("Cnchi will not install any bootloader")
        else:
            self.settings.set('bootloader_install', True)
            self.settings.set('bootloader_device', self.bootloader_device)

            self.settings.set('bootloader', self.bootloader)
            msg = _(
                "Antergos will install the bootloader '{0}' in device '{1}'")
            msg = msg.format(self.bootloader, self.bootloader_device)
            logging.info(msg)

    def run_install(self, packages, metalinks):
        """ Perform installation """
        txt = _("Cnchi will install Antergos on device %s")
        logging.info(txt, self.auto_device)

        self.settings.set('auto_device', self.auto_device)

        ssd = {self.auto_device: fs.is_ssd(self.auto_device)}

        self.installation = install.Installation(
            self.settings,
            self.callback_queue,
            packages,
            metalinks,
            self.mount_devices,
            self.fs_devices,
            ssd)

        self.installation.start()


# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

if __name__ == '__main__':
    from test_screen import _, run
    run('InstallationAutomatic')
