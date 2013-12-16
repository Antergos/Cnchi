#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  features.py
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

""" Features screen """

from gi.repository import Gtk
import subprocess
import os
import logging
import desktop_environments as desktops
import canonical.misc as misc

_next_page = "installation_ask"
_prev_page = "desktop"

class Features(Gtk.Box):
    """ Features screen class """
    def __init__(self, params):
        """ Initializes features ui """
        self.header = params['header']
        self.ui_dir = params['ui_dir']
        self.settings = params['settings']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']

        super().__init__()

        self.ui = Gtk.Builder()

        self.ui.add_from_file(os.path.join(self.ui_dir, "features.ui"))
        self.ui.connect_signals(self)

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
        
        self.labels = {}
        self.titles = {}
        self.switches = {}

        for feature in self.all_features:
            object_name = "label_" + feature
            self.labels[feature] = self.ui.get_object(object_name)

            object_name = "label_title_" + feature
            self.titles[feature] = self.ui.get_object(object_name)

            object_name = "switch_" + feature
            self.switches[feature] = self.ui.get_object(object_name)

        # The first time we load this screen, we try to guess some defaults
        self.defaults = True

        # Only show ufw rules and aur disclaimer info once
        self.info_already_shown = { "ufw":False, "aur":False }

        super().add(self.ui.get_object("features"))

    def listbox_sort_by_name(self, row1, row2, user_data):
        """ Sort function for listbox
            Returns : < 0 if row1 should be before row2, 0 if they are equal and > 0 otherwise
            WARNING: IF LAYOUT IS CHANGED IN features.ui THEN THIS SHOULD BE CHANGED ACCORDINGLY. """
        label1 = row1.get_children()[0].get_children()[1].get_children()[0]
        label2 = row2.get_children()[0].get_children()[1].get_children()[0]

        text = [label1.get_text(), label2.get_text()]
        sorted_text = misc.sort_list(text, self.settings.get("locale"))

        # If strings are already well sorted return < 0
        if text[0] == sorted_text[0]:
            return -1

        # Strings must be swaped, return > 0
        return 1

    def translate_ui(self):
        """ Translates features ui """
        desktop = self.settings.get('desktop')

        txt = desktops.NAMES[desktop] + " - " + _("Feature Selection")
        #txt = '<span weight="bold" size="large">%s</span>' % txt
        #self.title.set_markup(txt)

        #self.header.set_title("Cnchi")
        self.header.set_subtitle(txt)

        # AUR
        txt = _("Arch User Repository (AUR) Support")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["aur"].set_markup(txt)
        txt = _("The AUR is a community-driven repository for Arch users.")
        self.labels["aur"].set_markup(txt)

        # Bluetooth
        txt = _("Bluetooth Support")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["bluetooth"].set_markup(txt)
        txt = _("Enables your system to make wireless connections via Bluetooth.")
        self.labels["bluetooth"].set_markup(txt)

        # Extra Fonts
        txt = _("Extra Fonts")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["fonts"].set_markup(txt)
        txt = _("Installation of extra fonts")
        self.labels["fonts"].set_markup(txt)

        # Gnome Extra
        txt = _("Gnome Extra")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["gnome_extra"].set_markup(txt)
        # https://www.archlinux.org/groups/x86_64/gnome-extra/
        txt = _("Installation of extra Gnome applications")
        self.labels["gnome_extra"].set_markup(txt)

        # Printing support (cups)
        txt = _("Printing Support")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["cups"].set_markup(txt)
        txt = _("Installation of printer drivers and management tools.")
        self.labels["cups"].set_markup(txt)

        # LibreOffice
        txt = _("LibreOffice")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["office"].set_markup(txt)
        txt = _("Open source office suite. Supports editing MS Office files.")
        self.labels["office"].set_markup(txt)

        # Visual effects
        txt = _("Visual Effects")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["visual"].set_markup(txt)
        txt = _("Enable transparency, shadows, and other desktop effects.")
        self.labels["visual"].set_markup(txt)

        # Firewall
        txt = _("Uncomplicated Firewall")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["firewall"].set_markup(txt)
        # String too large
        #txt = _("Network security system that controls the incoming and outgoing network traffic.")
        txt = _("Control the incoming and outgoing network traffic.")
        self.labels["firewall"].set_markup(txt)

        # Proprietary packages (third_party)
        txt = _("Proprietary Software")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["third_party"].set_markup(txt)
        txt = _("Software to play Flash videos, MP3 audio, and other media.")
        self.labels["third_party"].set_markup(txt)

        self.listbox.invalidate_sort()

    def hide_features(self):
        """ Hide unused features """
        for feature in self.all_features:
            if feature not in self.features:
                name = feature + "-row"
                obj = self.ui.get_object(name)
                obj.hide()

    def enable_defaults(self):
        """ Enable some features by default """
        if 'bluetooth' in self.features:
            process1 = subprocess.Popen(["lsusb"], stdout=subprocess.PIPE)
            process2 = subprocess.Popen(["grep", "-i", "bluetooth"], stdin=process1.stdout, stdout=subprocess.PIPE)
            process1.stdout.close()
            out, err = process2.communicate()
            if out.decode() is not '':
                logging.debug("Detected bluetooth device. Enabling by default...")
                self.switches['bluetooth'].set_active(True)

        if 'firewall' in self.features:
            self.switches['firewall'].set_active(True)

        if 'cups' in self.features:
            self.switches['cups'].set_active(True)

    def store_values(self):
        """ Get switches values and store them """
        for feature in self.features:
            isactive = self.switches[feature].get_active()
            self.settings.set("feature_" + feature, isactive)
            if isactive:
                logging.debug("Selected '%s' feature to install", feature)

        # Show ufw info message if ufw is selected (only once)
        if self.settings.get("feature_firewall") and not self.info_already_shown["ufw"]:
            info = self.prepare_info_dialog("ufw")
            info.run()
            info.hide()
            self.info_already_shown["ufw"] = True

        # Show AUR disclaimer if AUR is selected (only once)
        if self.settings.get("feature_aur") and not self.info_already_shown["aur"]:
            info = self.prepare_info_dialog("aur")
            info.run()
            info.hide()
            self.info_already_shown["aur"] = True

        return True

    def prepare_info_dialog(self, feature):
        """ Some features show an information dialog when this screen is accepted """
        if feature == "aur":
            # Aur disclaimer
            txt1 = _("Arch User Repository - Disclaimer")
            txt2 = _("The Arch User Repository is a collection of user-submitted PKGBUILDs\n" \
                "that supplement software available from the official repositories.\n\n" \
                "The AUR is community driven and NOT supported by Arch or Antergos.\n")

        if feature == "ufw":
            # Ufw rules info
            txt1 = _("Uncomplicated Firewall will be installed with these rules:")
            toallow = misc.get_network()
            txt2 = _("ufw default deny\nufw allow from %s\nufw allow Transmission\nufw allow SSH") % toallow

        txt1 = "<big>%s</big>" % txt1
        txt2 = "<i>%s</i>" % txt2

        info = self.ui.get_object("info")
        info.set_markup(txt1)
        info.format_secondary_markup(txt2)

        return info

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page

    def prepare(self, direction):
        """ Prepare features screen to get ready to show itself """
        desktop = self.settings.get('desktop')
        self.features = self.features_by_desktop[desktop]
        self.translate_ui()
        self.show_all()
        self.hide_features()
        if self.defaults:
            self.enable_defaults()
            self.defaults = False
