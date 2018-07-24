#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# boot_ui.py
#
# Copyright © 2013-2018 Antergos
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


""" Bootloader UI functions (for automatic and advanced pages) """

import logging
import os
import parted

import misc.extra as misc

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

class BootUI(object):
    """ GUI Helper class to manage bootloaders """
    def __init__(self, page_ui):
        self.page_ui = page_ui
        self.bootloader = "grub2"
        self.bootloader_device = ""
        self.bootloader_entry = self.page_ui.get_object('bootloader_entry')
        self.bootloader_device_entry = self.page_ui.get_object(
            'bootloader_device_entry')
        self.bootloader_devices = {}
        self.is_uefi = os.path.exists('/sys/firmware/efi')

    def translate_ui(self):
        """ Translate labels """
        txt = _("Use the device below for boot loader installation:")
        txt = "<span weight='bold' size='small'>{0}</span>".format(txt)
        label = self.page_ui.get_object('bootloader_device_info_label')
        label.set_markup(txt)

        txt = _("Bootloader:")
        label = self.page_ui.get_object('bootloader_label')
        label.set_markup(txt)

        txt = _("Device:")
        label = self.page_ui.get_object('bootloader_device_label')
        label.set_markup(txt)

    def fill_bootloader_device_entry(self):
        """ Get all devices where we can put our bootloader """

        with misc.raised_privileges():
            device_list = parted.getAllDevices()

        self.bootloader_device_entry.remove_all()
        self.bootloader_devices.clear()

        for dev in device_list:
            # avoid cdrom and any raid, lvm volumes or encryptfs
            if (not dev.path.startswith("/dev/sr") and
                    not dev.path.startswith("/dev/mapper")):
                # hard drives measure themselves assuming kilo=1000, mega=1mil, etc
                size = dev.length * dev.sectorSize
                size_gbytes = int(parted.formatBytes(size, 'GB'))
                line = '{0} [{1} GB] ({2})'
                line = line.format(dev.model, size_gbytes, dev.path)
                self.bootloader_device_entry.append_text(line)
                self.bootloader_devices[line] = dev.path
                logging.debug(line)

        if not self.select_bootdevice(self.bootloader_device_entry, self.bootloader_device):
            # Automatically select first entry
            misc.select_first_combobox_item(self.bootloader_device_entry)

    @staticmethod
    def select_bootdevice(combobox, value):
        """ Update chosen boot device option """
        model = combobox.get_model()
        combo_iter = model.get_iter_first()
        index = 0
        found = False
        while combo_iter and not found:
            if value.lower() in model[combo_iter][0].lower():
                combobox.set_active_iter(combo_iter)
                combo_iter = None
                found = True
            else:
                index += 1
                combo_iter = model.iter_next(combo_iter)
        return found

    def fill_bootloader_entry(self):
        """ Put the bootloaders for the user to choose """

        self.bootloader_entry.remove_all()

        if self.is_uefi:
            self.bootloader_entry.append_text("Grub2")
            self.bootloader_entry.append_text("Systemd-boot")

            # TODO: rEFInd needs more testing
            # self.bootloader_entry.append_text("rEFInd")

            if not misc.select_combobox_value(self.bootloader_entry, self.bootloader):
                # Automatically select first entry
                self.bootloader_entry.set_active(0)
            self.bootloader_entry.show()
        else:
            self.bootloader_entry.hide()
            widget_ids = ["bootloader_label", "bootloader_device_label"]
            for widget_id in widget_ids:
                widget = self.page_ui.get_object(widget_id)
                widget.hide()

    def bootloader_device_check_toggled(self, status):
        """ Enable / disable bootloader installation """
        widget_ids = [
            "bootloader_device_entry", "bootloader_entry",
            "bootloader_label", "bootloader_device_label"]

        for widget_id in widget_ids:
            widget = self.page_ui.get_object(widget_id)
            widget.set_sensitive(status)

    def bootloader_device_entry_changed(self):
        """ Get new selected bootloader device """
        line = self.bootloader_device_entry.get_active_text()
        if line:
            self.bootloader_device = self.bootloader_devices[line]

    def bootloader_entry_changed(self):
        """ Get new selected bootloader """
        line = self.bootloader_entry.get_active_text()
        if line:
            self.bootloader = line.lower()

    def set_bootloader(self, settings):
        """ Set bootloader setting from the user selection checkbox """
        checkbox = self.page_ui.get_object('bootloader_device_check')
        if not checkbox.get_active():
            settings.set('bootloader_install', False)
            logging.info("Cnchi will not install any bootloader")
        else:
            settings.set('bootloader_install', True)
            settings.set('bootloader_device', self.bootloader_device)

            settings.set('bootloader', self.bootloader)
            msg = "Antergos will install the {0} bootloader in device {1}"
            msg = msg.format(self.bootloader, self.bootloader_device)
            logging.info(msg)
