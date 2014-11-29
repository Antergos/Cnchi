#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  features.py
#
#  Copyright © 2013,2014 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

""" Features screen """

from gi.repository import Gtk
import subprocess
import os
import logging
import desktop_environments as desktops
import canonical.misc as misc

from gtkbasebox import GtkBaseBox

_features_icon_names = {
    'aur' : 'system-software-install',
    'bluetooth' : 'bluetooth',
    'cups' : 'printer',
    'firewall' : 'network-server',
    'fonts' : 'preferences-desktop-font',
    'office' : 'accessories-text-editor',
    'visual' : 'video-display'}

COL_IMAGE = 0
COL_TITLE = 1
COL_LABEL = 2
COL_SWITCH = 3

class Features(GtkBaseBox):
    """ Features screen class """
    def __init__(self, params, prev_page="desktop", next_page="installation_ask"):
        """ Initializes features ui """
        super().__init__(self, params, "features", prev_page, next_page)

        # Set up list box
        self.listbox = self.ui.get_object("listbox")
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.listbox.set_sort_func(self.listbox_sort_by_name, None)

        # Available features (for reference)
        # if you add a feature, remember to add it's setup in installation_process.py
        self.all_features = desktops.ALL_FEATURES

        # Each desktop has its own features
        self.features_by_desktop = desktops.FEATURES

        # This is initialized each time this screen is shown in prepare()
        self.features = None

        self.listbox_rows = {}

        # The first time we load this screen, we try to guess some defaults
        self.defaults = True

        # Only show ufw rules and aur disclaimer info once
        self.info_already_shown = { "ufw":False, "aur":False }

    def fill_listbox(self):
        for listbox_row in self.listbox.get_children():
            listbox_row.destroy()

        for feature in self.all_features:
            box = Gtk.Box(spacing=25)
            box.set_name(feature + "-row")

            self.listbox_rows[feature] = []

            if feature in _features_icon_names:
                icon_name = _features_icon_names[feature]
            else:
                icon_name = "missing"

            object_name= "image_" + feature
            image = Gtk.Image.new_from_icon_name(
                icon_name,
                Gtk.IconSize.DND)
            image.set_property('margin_start', 10)
            self.listbox_rows[feature].append(image)
            box.pack_start(image, False, False, 0)

            text_box = Gtk.VBox()
            object_name = "label_title_" + feature
            label_title = Gtk.Label.new()
            label_title.set_halign(Gtk.Align.START)
            label_title.set_justify(Gtk.Justification.LEFT)
            label_title.set_name(object_name)
            self.listbox_rows[feature].append(label_title)
            text_box.pack_start(label_title, False, False, 0)

            object_name = "label_" + feature
            label = Gtk.Label.new()
            label.set_name(object_name)
            self.listbox_rows[feature].append(label)
            text_box.pack_start(label, False, False, 0)

            box.pack_start(text_box, False, False, 0)

            object_name = "switch_" + feature
            switch = Gtk.Switch.new()
            switch.set_name(object_name)
            switch.set_property('margin_top', 10)
            switch.set_property('margin_bottom', 10)
            switch.set_property('margin_end', 10)
            self.listbox_rows[feature].append(switch)
            box.pack_end(switch, False, False, 0)

            # Add row to our gtklist
            self.listbox.add(box)

        self.listbox.show_all()

    def listbox_sort_by_name(self, row1, row2, user_data):
        """ Sort function for listbox
            Returns : < 0 if row1 should be before row2, 0 if they are equal and > 0 otherwise
            WARNING: IF LAYOUT IS CHANGED IN fill_listbox THEN THIS SHOULD BE CHANGED ACCORDINGLY. """
        box1 = row1.get_child()
        txt_box1 = box1.get_children()[0]
        label1 = txt_box1.get_children()[1]

        box2 = row2.get_child()
        txt_box2 = box2.get_children()[0]
        label2 = txt_box2.get_children()[1]

        text = [label1.get_text(), label2.get_text()]
        #sorted_text = misc.sort_list(text, self.settings.get("locale"))
        sorted_text = misc.sort_list(text)

        # If strings are already well sorted return < 0
        if text[0] == sorted_text[0]:
            return -1

        # Strings must be swaped, return > 0
        return 1

    def translate_ui(self):
        """ Translates all ui elements """
        desktop = self.settings.get('desktop')

        txt = desktops.NAMES[desktop] + " - " + _("Feature Selection")
        self.header.set_subtitle(txt)

        # AUR
        row = self.listbox_rows['aur']
        txt = _("Arch User Repository (AUR) Support")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        row[COL_TITLE].set_markup(txt)
        txt = _("The AUR is a community-driven repository for Arch users.")
        txt = "<span size='small'>%s</span>" % txt
        row[COL_LABEL].set_markup(txt)
        txt = _("Use yaourt to install AUR packages.\n"
                "The AUR was created to organize and share new packages\n"
                "from the community and to help expedite popular packages'\n"
                "inclusion into the [community] repository.")
        for widget in row:
            widget.set_tooltip_markup(txt)

        # Bluetooth
        row = self.listbox_rows['bluetooth']
        txt = _("Bluetooth Support")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        row[COL_TITLE].set_markup(txt)
        txt = _("Enables your system to make wireless connections via Bluetooth.")
        txt = "<span size='small'>%s</span>" % txt
        row[COL_LABEL].set_markup(txt)
        txt = _("Bluetooth is a standard for the short-range wireless\n"
                "interconnection of cellular phones, computers, and\n"
                "other electronic devices. In Linux, the canonical\n"
                "implementation of the Bluetooth protocol stack is BlueZ")
        for widget in row:
            widget.set_tooltip_markup(txt)

        # Extra TTF Fonts
        row = self.listbox_rows['fonts']
        txt = _("Extra Truetype Fonts")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        row[COL_TITLE].set_markup(txt)
        txt = _("Installation of extra TrueType fonts")
        txt = "<span size='small'>%s</span>" % txt
        row[COL_LABEL].set_markup(txt)
        txt = _("TrueType is an outline font standard developed by\n"
                "Apple and Microsoft in the late 1980s as a competitor\n"
                "to Adobe's Type 1 fonts used in PostScript. It has\n"
                "become the most common format for fonts on both the\n"
                "Mac OS and Microsoft Windows operating systems.")
        for widget in row:
            widget.set_tooltip_markup(txt)

        # Printing support (cups)
        row = self.listbox_rows['cups']
        txt = _("Printing Support")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        row[COL_TITLE].set_markup(txt)
        txt = _("Installation of printer drivers and management tools.")
        txt = "<span size='small'>%s</span>" % txt
        row[COL_LABEL].set_markup(txt)
        txt = _("CUPS is the standards-based, open source printing\n"
                "system developed by Apple Inc. for OS® X and other\n"
                "UNIX®-like operating systems.")
        for widget in row:
            widget.set_tooltip_markup(txt)

        # LibreOffice
        row = self.listbox_rows['office']
        txt = _("LibreOffice")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        row[COL_TITLE].set_markup(txt)
        txt = _("Open source office suite. Supports editing MS Office files.")
        txt = "<span size='small'>%s</span>" % txt
        row[COL_LABEL].set_markup(txt)
        txt = _("LibreOffice is the free power-packed Open Source\n"
                "personal productivity suite for Windows, Macintosh\n"
                "and Linux, that gives you six feature-rich applications\n"
                "for all your document production and data processing\n"
                "needs: Writer, Calc, Impress, Draw, Math and Base.")
        for widget in row:
            widget.set_tooltip_markup(txt)

        # Visual effects
        row = self.listbox_rows['visual']
        txt = _("Visual Effects")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        row[COL_TITLE].set_markup(txt)
        txt = _("Enable transparency, shadows, and other desktop effects.")
        txt = "<span size='small'>%s</span>" % txt
        row[COL_LABEL].set_markup(txt)
        txt = _("Compton is a lightweight, standalone composite manager,\n"
                "suitable for use with window managers that do not natively\n"
                "provide compositing functionality. Compton itself is a fork\n"
                "of xcompmgr-dana, which in turn is a fork of xcompmgr.\n"
                "See the compton github page for further information.")
        for widget in row:
            widget.set_tooltip_markup(txt)

        # Firewall
        row = self.listbox_rows['firewall']
        txt = _("Uncomplicated Firewall")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        row[COL_TITLE].set_markup(txt)
        txt = _("Control the incoming and outgoing network traffic.")
        txt = "<span size='small'>%s</span>" % txt
        row[COL_LABEL].set_markup(txt)
        txt = _("Ufw stands for Uncomplicated Firewall, and is a program for\n"
                "managing a netfilter firewall. It provides a command line\n"
                "interface and aims to be uncomplicated and easy to use.")
        for widget in row:
            widget.set_tooltip_markup(txt)

        # Sort listbox items
        self.listbox.invalidate_sort()

    def enable_defaults(self):
        """ Enable some features by default """
        if 'bluetooth' in self.features:
            process1 = subprocess.Popen(["lsusb"], stdout=subprocess.PIPE)
            process2 = subprocess.Popen(["grep", "-i", "bluetooth"], stdin=process1.stdout, stdout=subprocess.PIPE)
            process1.stdout.close()
            out, err = process2.communicate()
            if out.decode() is not '':
                logging.debug(_("Detected bluetooth device, so Cnchi will enable the 'bluetooth' feature."))
                row = self.listbox_rows['bluetooth']
                row[COL_SWITCH].set_active(True)

        # I do not think firewall should be enabled by default (karasu)
        #if 'firewall' in self.features:
        #    row = self.listbox_rows['firewall']
        #    row[COL_SWITCH].set_active(True)

        if 'cups' in self.features:
            row = self.listbox_rows['cups']
            row[COL_SWITCH].set_active(True)

    def store_values(self):
        """ Get switches values and store them """
        for feature in self.features:
            row = self.listbox_rows[feature]
            isactive = row[COL_SWITCH].get_active()
            self.settings.set("feature_" + feature, isactive)
            if isactive:
                logging.debug(_("Selected '%s' feature to install"), feature)

        # Show ufw info message if ufw is selected (only once)
        if self.settings.get("feature_firewall") and not self.info_already_shown["ufw"]:
            info = self.show_info_dialog("ufw")
            self.info_already_shown["ufw"] = True

        # Show AUR disclaimer if AUR is selected (only once)
        if self.settings.get("feature_aur") and not self.info_already_shown["aur"]:
            info = self.show_info_dialog("aur")
            self.info_already_shown["aur"] = True

        return True

    def show_info_dialog(self, feature):
        """ Some features show an information dialog when this screen is accepted """
        if feature == "aur":
            # Aur disclaimer
            txt1 = _("Arch User Repository - Disclaimer")
            txt2 = _("The Arch User Repository is a collection of user-submitted PKGBUILDs\n" \
                "that supplement software available from the official repositories.\n\n" \
                "The AUR is community driven and NOT supported by Arch or Antergos.\n")
        elif feature == "ufw":
            # Ufw rules info
            txt1 = _("Uncomplicated Firewall will be installed with these rules:")
            toallow = misc.get_network()
            txt2 = _("ufw default deny\nufw allow from %s\nufw allow Transmission\nufw allow SSH") % toallow

        txt1 = "<big>%s</big>" % txt1
        txt2 = "<i>%s</i>" % txt2

        info = Gtk.MessageDialog(
            transient_for=self.get_toplevel(),
            modal=True,
            destroy_with_parent=True,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.CLOSE)
        info.set_markup(txt1)
        info.format_secondary_markup(txt2)
        info.run()
        info.destroy()

    def prepare(self, direction):
        """ Prepare features screen to get ready to show itself """
        desktop = self.settings.get('desktop')
        self.features = self.features_by_desktop[desktop]
        self.fill_listbox()
        self.translate_ui()
        self.show_all()
        if self.defaults:
            self.enable_defaults()
            self.defaults = False

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message): return message

if __name__ == '__main__':
    from test_screen import _,run
    run('Features')
