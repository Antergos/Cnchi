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

from gtkbasebox import GtkBaseBox

class Features(Gtk.Box):
    """ Features screen class """
    def __init__(self, params):
        """ Initializes features ui """
        self.next_page = "installation_ask"
        self.prev_page = "desktop"

        super().__init__(params, "features")

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

        self.add(self.ui.get_object("features"))

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
        self.header.set_subtitle(txt)

        # AUR
        txt = _("Arch User Repository (AUR) Support")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["aur"].set_markup(txt)
        txt = _("The AUR is a community-driven repository for Arch users.")
        txt = "<span size='small'>%s</span>" % txt
        self.labels["aur"].set_markup(txt)

        txt = _("Use yaourt to install AUR packages.\n"
                "The AUR was created to organize and share new packages\n"
                "from the community and to help expedite popular packages'\n"
                "inclusion into the [community] repository.")
        self.titles["aur"].set_tooltip_markup(txt)
        self.switches["aur"].set_tooltip_markup(txt)
        self.labels["aur"].set_tooltip_markup(txt)

        # Bluetooth
        txt = _("Bluetooth Support")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["bluetooth"].set_markup(txt)
        txt = _("Enables your system to make wireless connections via Bluetooth.")
        txt = "<span size='small'>%s</span>" % txt
        self.labels["bluetooth"].set_markup(txt)

        txt = _("Bluetooth is a standard for the short-range wireless\n"
                "interconnection of cellular phones, computers, and\n"
                "other electronic devices. In Linux, the canonical\n"
                "implementation of the Bluetooth protocol stack is BlueZ")
        self.titles["bluetooth"].set_tooltip_markup(txt)
        self.switches["bluetooth"].set_tooltip_markup(txt)
        self.labels["bluetooth"].set_tooltip_markup(txt)

        # Extra TTF Fonts
        txt = _("Extra Truetype Fonts")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["fonts"].set_markup(txt)
        txt = _("Installation of extra TrueType fonts")
        txt = "<span size='small'>%s</span>" % txt
        self.labels["fonts"].set_markup(txt)

        txt = _("TrueType is an outline font standard developed by\n"
                "Apple and Microsoft in the late 1980s as a competitor\n"
                "to Adobe's Type 1 fonts used in PostScript. It has\n"
                "become the most common format for fonts on both the\n"
                "Mac OS and Microsoft Windows operating systems.")
        self.titles["fonts"].set_tooltip_markup(txt)
        self.switches["fonts"].set_tooltip_markup(txt)
        self.labels["fonts"].set_tooltip_markup(txt)

        # Gnome Extra
        txt = _("Gnome Extra")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["gnome_extra"].set_markup(txt)
        txt = _("Installation of extra Gnome applications")
        txt = "<span size='small'>%s</span>" % txt
        self.labels["gnome_extra"].set_markup(txt)

        txt = _("Contains various optional tools such as a media\n"
                "player, a calculator, an editor and other non-critical\n"
                "applications that go well with the GNOME desktop.\n")
        self.titles["gnome_extra"].set_tooltip_markup(txt)
        self.switches["gnome_extra"].set_tooltip_markup(txt)
        self.labels["gnome_extra"].set_tooltip_markup(txt)

        # Printing support (cups)
        txt = _("Printing Support")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["cups"].set_markup(txt)
        txt = _("Installation of printer drivers and management tools.")
        txt = "<span size='small'>%s</span>" % txt
        self.labels["cups"].set_markup(txt)

        txt = _("CUPS is the standards-based, open source printing\n"
                "system developed by Apple Inc. for OS® X and other\n"
                "UNIX®-like operating systems.")
        self.titles["cups"].set_tooltip_markup(txt)
        self.switches["cups"].set_tooltip_markup(txt)
        self.labels["cups"].set_tooltip_markup(txt)

        # LibreOffice
        txt = _("LibreOffice")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["office"].set_markup(txt)
        txt = _("Open source office suite. Supports editing MS Office files.")
        txt = "<span size='small'>%s</span>" % txt
        self.labels["office"].set_markup(txt)

        txt = _("LibreOffice is the free power-packed Open Source\n"
                "personal productivity suite for Windows, Macintosh\n"
                "and Linux, that gives you six feature-rich applications\n"
                "for all your document production and data processing\n"
                "needs: Writer, Calc, Impress, Draw, Math and Base.")
        self.titles["office"].set_tooltip_markup(txt)
        self.switches["office"].set_tooltip_markup(txt)
        self.labels["office"].set_tooltip_markup(txt)

        # Visual effects
        txt = _("Visual Effects")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["visual"].set_markup(txt)
        txt = _("Enable transparency, shadows, and other desktop effects.")
        txt = "<span size='small'>%s</span>" % txt
        self.labels["visual"].set_markup(txt)

        txt = _("Compton is a lightweight, standalone composite manager,\n"
                "suitable for use with window managers that do not natively\n"
                "provide compositing functionality. Compton itself is a fork\n"
                "of xcompmgr-dana, which in turn is a fork of xcompmgr.\n"
                "See the compton github page for further information.")
        self.titles["visual"].set_tooltip_markup(txt)
        self.switches["visual"].set_tooltip_markup(txt)
        self.labels["visual"].set_tooltip_markup(txt)

        # Firewall
        txt = _("Uncomplicated Firewall")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["firewall"].set_markup(txt)
        txt = _("Control the incoming and outgoing network traffic.")
        txt = "<span size='small'>%s</span>" % txt
        self.labels["firewall"].set_markup(txt)

        txt = _("Ufw stands for Uncomplicated Firewall, and is a program for\n"
                "managing a netfilter firewall. It provides a command line\n"
                "interface and aims to be uncomplicated and easy to use.")
        self.titles["firewall"].set_tooltip_markup(txt)
        self.switches["firewall"].set_tooltip_markup(txt)
        self.labels["firewall"].set_tooltip_markup(txt)

        # Proprietary packages (third_party)
        txt = _("Proprietary Software")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["third_party"].set_markup(txt)
        txt = _("Software to play Flash videos, MP3 audio, and other media.")
        txt = "<span size='small'>%s</span>" % txt
        self.labels["third_party"].set_markup(txt)

        # txt = _("")
        #self.titles["third_party"].set_tooltip_markup(txt)
        #self.switches["third_party"].set_tooltip_markup(txt)
        #self.labels["third_party"].set_tooltip_markup(txt)

        # Sort listbox items
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
                logging.debug(_("Detected bluetooth device. Enabling by default..."))
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

        info = Gtk.MessageDialog(transient_for=None,
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
        self.translate_ui()
        self.show_all()
        self.hide_features()
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
