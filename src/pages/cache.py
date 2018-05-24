#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# cache.py
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


""" Cache selection screen (optional) """

import os
import logging

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import parted

from pages.gtkbasebox import GtkBaseBox

import misc.extra as misc
import parted3.fs_module as fs

DEST_DIR = "/install"


class Cache(GtkBaseBox):
    """ Cache selection screen (optional) """

    def __init__(self, params, prev_page="installation_ask", next_page="summary"):
        super().__init__(self, params, "cache", prev_page, next_page)

        self.cache_device = None
        self.device_store = self.ui.get_object('select_drive')
        self.device_label = self.ui.get_object('select_drive_label')
        self.devices = {}

    def translate_ui(self):
        """ Translate widgets """
        txt = _("Select cache partition:")
        self.device_label.set_markup(txt)

        label = self.ui.get_object('text_info')
        txt = _("Use an additional cache (optional)\n"
                "This installer needs to download a TON of packages from the Internet!")
        txt = "<b>{0}</b>".format(txt)
        label.set_markup(txt)

        label = self.ui.get_object('info_label')
        txt = _("You can use an aditional partition to use as packages' cache.\n"
                "In case you need to restart this installation you won't be\n"
                "needing to download all previous downloaded packages again\n\n"
                "It cannot be the same device where you are installing Antergos\n\n"
                "Please, choose now the device (and partition) to use as cache.\n"
                "It needs to be be already formated and unmounted!")
        label.set_markup(txt)

        self.header.set_subtitle(_("Cache selection (optional)"))

    def populate_devices(self):
        """ Fill list with devices """
        with misc.raised_privileges() as __:
            device_list = parted.getAllDevices()

        self.device_store.remove_all()
        self.devices = {}

        self.device_store.append_text("None")
        self.devices["None"] = None

        for dev in device_list:
            # avoid cdrom and any raid, lvm volumes or encryptfs
            if not dev.path.startswith("/dev/sr") and \
               not dev.path.startswith("/dev/mapper"):
                # hard drives measure themselves assuming kilo=1000, mega=1mil, etc
                size_in_gigabytes = int(
                    (dev.length * dev.sectorSize) / 1000000000)
                line = '{0} [{1} GB] ({2})'.format(dev.model, size_in_gigabytes, dev.path)
                self.device_store.append_text(line)
                self.devices[line] = dev.path
                logging.debug(line)

        self.select_first_combobox_item(self.device_store)

    @staticmethod
    def select_first_combobox_item(combobox):
        """ Selects first item """
        tree_model = combobox.get_model()
        tree_iter = tree_model.get_iter_first()
        combobox.set_active_iter(tree_iter)

    def on_select_drive_changed(self, _widget):
        """ User selected another drive """
        line = self.device_store.get_active_text()
        if line is not None:
            self.cache_device = self.devices[line]
            print("****", self.cache_device)
        self.forward_button.set_sensitive(True)

    def prepare(self, direction):
        """ Get screen ready """
        self.translate_ui()
        self.populate_devices()
        self.show_all()

    def mount_device(self):
        """ Mounts cache device into a temporary folder """
        device = self.cache_device
        if device:
            tmp_dir = tempfile.mkdtemp()
            call(["mount", device, tmp_dir])
            return tmp_dir
        else:
            return None

    def store_values(self):
        """ Store selected values """
        
        xz_cache_dir = self.mount_device()
        if xz_cache_dir:
            xz_cache = self.settings.get('xz_cache', xz_cache)
            xz_cache.append(xz_cache_dir)
        return True

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

