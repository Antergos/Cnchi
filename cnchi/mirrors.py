#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# mirrors.py
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


""" Let advanced users manage mirrorlist files """

import os
import sys
import queue
import time
import logging
import subprocess

import bootinfo

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from gtkbasebox import GtkBaseBox

import misc.extra as misc


class Mirrors(GtkBaseBox):
    def __init__(self, params, prev_page="features", next_page=None):
        super().__init__(self, params, "mirrors", prev_page, next_page)

        data_dir = self.settings.get("data")

        self.disable_rank_mirrors = params["disable_rank_mirrors"]

        self.listbox_rows = {}

        # Set up list box
        self.listbox = self.ui.get_object("listbox")
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.listbox.set_sort_func(self.listbox_sort_by_name, None)

        # TODO: By default, select automatic mirror list ranking

    def prepare(self, direction):
        """ Prepares screen """
        self.translate_ui()
        self.show_all()

        self.forward_button.set_sensitive(True)

    def translate_ui(self):
        """ Translates screen before showing it """
        self.header.set_subtitle(_("Mirrors Selection"))

        self.forward_button.set_always_show_image(True)
        self.forward_button.set_sensitive(True)

        bold_style = '<span weight="bold">{0}</span>'

        radio = self.ui.get_object("rank_radiobutton")
        txt = _("Let Cnchi sort my mirror list (recommended)")
        radio.set_label(txt)
        radio.set_name('rank_radio_btn')

        radio = self.ui.get_object("leave_radiobutton")
        txt = _("Do not touch the mirrors list")
        radio.set_label(txt)
        radio.set_name('leave_radio_btn')

        radio = self.ui.get_object("user_radiobutton")
        txt = _("Let me manage my mirror list (advanced)")
        radio.set_label(txt)
        radio.set_name('user_radio_btn')

        intro_txt = _("How would you like to proceed?")
        intro_label = self.ui.get_object("introduction")
        # intro_txt = bold_style.format(intro_txt)
        intro_label.set_text(intro_txt)
        intro_label.set_name("intro_label")
        intro_label.set_hexpand(False)
        intro_label.set_line_wrap(True)
        intro_label.set_max_width_chars(max_width_chars)

    def add_mirror(self, mirror_url, box):
        """ Adds mirror url to listbox row box """

        # Add mirror switch
        object_name = "switch_" + mirror_url
        switch = Gtk.Switch.new()
        switch.set_name(object_name)
        switch.set_property('margin_top', 10)
        switch.set_property('margin_bottom', 10)
        switch.set_property('margin_end', 10)
        switch.connect("notify::active", self.on_switch_activated)
        self.listbox_rows[mirror_url].append(switch)
        box.pack_end(switch, False, False, 0)

        # Add mirror url label
        object_name = mirror_url
        label_url = Gtk.Label.new()
        label_url.set_halign(Gtk.Align.START)
        label_url.set_justify(Gtk.Justification.LEFT)
        label_url.set_name(mirror_url)
        self.listbox_rows[mirror_url].append(label_url)
        box.pack_start(label_url, False, True, 0)


    def on_switch_activated(self, switch, gparam):
        pass
        '''
        for feature in self.features:
            row = self.listbox_rows[feature]
            if row[Features.COL_SWITCH] == switch:
                is_active = switch.get_active()
                self.settings.set("feature_" + feature, is_active)
        '''
    '''
    def fill_listbox(self):
        for listbox_row in self.listbox.get_children():
            listbox_row.destroy()

        self.listbox_rows = {}

        # Only add graphic-driver feature if an AMD or Nvidia is detected
        if "graphic_drivers" in self.features:
            allow = False
            if self.detect.amd():
                allow = True
            if self.detect.nvidia() and not self.detect.bumblebee():
                allow = True
            if not allow:
                logging.debug("Removing proprietary graphic drivers feature.")
                self.features.remove("graphic_drivers")

        for feature in self.features:
            box = Gtk.Box(spacing=20)
            box.set_name(feature + "-row")

            self.listbox_rows[feature] = []

            self.add_feature_icon(feature, box)
            self.add_feature_label(feature, box)
            self.add_feature_switch(feature, box)
            # Add row to our gtklist
            self.listbox.add(box)

        self.listbox.show_all()
    '''














    def store_values(self):
        """ Store selected values """
        check = self.ui.get_object("encrypt_checkbutton")
        use_luks = check.get_active()

        check = self.ui.get_object("lvm_checkbutton")
        use_lvm = check.get_active()

        check = self.ui.get_object("zfs_checkbutton")
        use_zfs = check.get_active()

        check = self.ui.get_object("home_checkbutton")
        use_home = check.get_active()

        if self.next_page == "installation_automatic":
            self.settings.set('use_lvm', use_lvm)
            self.settings.set('use_luks', use_luks)
            self.settings.set('use_luks_in_root', True)
            self.settings.set('luks_root_volume', "cryptAntergos")
            self.settings.set('use_zfs', False)
            self.settings.set('use_home', use_home)
        elif self.next_page == "installation_zfs":
            self.settings.set('use_lvm', False)
            self.settings.set('use_luks', use_luks)
            self.settings.set('use_luks_in_root', False)
            self.settings.set('luks_root_volume', "")
            self.settings.set('use_zfs', True)
            self.settings.set('zfs', True)
            self.settings.set('use_home', use_home)
        else:
            # Set defaults. We don't know these yet.
            self.settings.set('use_lvm', False)
            self.settings.set('use_luks', False)
            self.settings.set('use_luks_in_root', False)
            self.settings.set('luks_root_volume', "")
            self.settings.set('use_zfs', False)
            self.settings.set('use_home', False)

        if not self.settings.get('use_zfs'):
            if self.settings.get('use_luks'):
                logging.info("Antergos installation will be encrypted using LUKS")
            if self.settings.get('use_lvm'):
                logging.info("Antergos will be installed using LVM volumes")
                if self.settings.get('use_home'):
                    logging.info("Antergos will be installed using a separate /home volume.")
            elif self.settings.get('use_home'):
                logging.info("Antergos will be installed using a separate /home partition.")
        else:
            logging.info("Antergos will be installed using ZFS")
            if self.settings.get('use_luks'):
                logging.info("Antergos ZFS installation will be encrypted")
            if self.settings.get('use_home'):
                logging.info("Antergos will be installed using a separate /home volume.")

        if self.next_page == "installation_alongside":
            self.settings.set('partition_mode', 'alongside')
        elif self.next_page == "installation_advanced":
            self.settings.set('partition_mode', 'advanced')
        elif self.next_page == "installation_automatic":
            self.settings.set('partition_mode', 'automatic')
        elif self.next_page == "installation_zfs":
            self.settings.set('partition_mode', 'zfs')

        # Check if there are still processes running...
        self.wait()

        return True

    def get_next_page(self):
        return self.next_page

    def on_automatic_radiobutton_toggled(self, widget):
        """ Automatic selected, enable all options """
        if widget.get_active():
            check = self.ui.get_object("zfs_checkbutton")
            if check.get_active():
                self.next_page = "installation_zfs"
            else:
                self.next_page = "installation_automatic"
            self.enable_automatic_options(True)

    def on_alongside_radiobutton_toggled(self, widget):
        """ Alongside selected, disable all automatic options """
        if widget.get_active():
            self.next_page = "installation_alongside"
            self.enable_automatic_options(False)

    def on_advanced_radiobutton_toggled(self, widget):
        """ Advanced selected, disable all automatic options """
        if widget.get_active():
            self.next_page = "installation_advanced"
            self.enable_automatic_options(False)


if __name__ == '__main__':
    from test_screen import _, run

    run('Mirrors')
