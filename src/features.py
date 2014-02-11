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

from gi.repository import Gtk, GObject

import subprocess
import os
import gtkwidgets
import logging
import misc

_next_page = "installation_ask"
_prev_page = "desktop"

class Features(Gtk.Box):

    def __init__(self, params):

        self.title = params['title']
        self.ui_dir = params['ui_dir']
        self.settings = params['settings']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']

        super().__init__()

        self.ui = Gtk.Builder()

        self.ui.add_from_file(os.path.join(self.ui_dir, "features.ui"))
        self.ui.connect_signals(self)
        
        # Available features (for reference)
        # if you add a feature, remember to add it's setup in installation_process.py
        self.all_features = [ "bluetooth", "cups", "office", "visual", "firewall", "third_party" ]
        
        # Each desktop has its own features
        self.features_by_desktop = {}
        self.features_by_desktop["nox"] = [ "bluetooth", "cups", "firewall" ]
        self.features_by_desktop["gnome"] = [ "bluetooth", "cups", "office", "firewall", "third_party" ]
        self.features_by_desktop["cinnamon"] = [ "bluetooth", "cups", "office", "firewall", "third_party" ]
        self.features_by_desktop["xfce"] = [ "bluetooth", "cups", "office", "firewall", "third_party" ]
        self.features_by_desktop["razor"] = [ "bluetooth", "cups", "office", "firewall", "third_party" ]
        self.features_by_desktop["openbox"] = [ "bluetooth", "cups", "office", "visual", "firewall", "third_party" ]
                
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
        
        # Only show ufw rules info once
        self.ufw_info_already_shown = False
        
        super().add(self.ui.get_object("features"))

    def translate_ui(self):
        desktop = self.settings.get('desktop')
        self.desktops = {
         "nox" : "Base",
         "gnome" : "Gnome",
         "cinnamon" : "Cinnamon",
         "xfce" : "Xfce",
         "lxde" : "Lxde",
         "openbox" : "Openbox",
         "enlightenment" : "Enlightenment (e17)",
         "kde" : "KDE",
         "razor" : "Razor-qt" }

        txt = self.desktops[desktop] + " - " + _("Features")
        txt = '<span weight="bold" size="large">%s</span>' % txt
        self.title.set_markup(txt)

        # Bluetooth
        txt = _("Bluetooth Support")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["bluetooth"].set_markup(txt)
        txt = _("Enables your system to make wireless connections via Bluetooth.")
        self.labels["bluetooth"].set_markup(txt)

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
        txt = _("Open source office suite that supports editing MS Office files.")
        self.labels["office"].set_markup(txt)

        # Visual effects
        txt = _("Visual Effects")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["visual"].set_markup(txt)
        txt = _("Enable 3D acceleration for transparency, shadows, and other desktop effects.")
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
        txt = _("Third-party software to play Flash videos, MP3 audio, and other media.")
        self.labels["third_party"].set_markup(txt)
        
        # Uncomplicated Firewall dialog
        ufw = self.ui.get_object("ufw")
        txt = _("Uncomplicated Firewall will be installed with these rules:")
        txt = "<big>%s</big>" % txt
        ufw.set_markup(txt)
        toallow = misc.get_network()
        txt = "ufw default deny\nufw allow from %s\nufw allow Transmission\nufw allow SSH" % toallow
        txt = "<i>%s</i>" % txt
        ufw.format_secondary_markup(txt)
    
    def hide_features(self):
        for feature in self.all_features:
            if feature not in self.features:
                prefixes = [ "box", "image", "switch", "label_title", "label" ]
                for prefix in prefixes:
                    object_name = prefix + "_" + feature
                    obj = self.ui.get_object(object_name)
                    obj.hide()

    def enable_defaults(self):
        if 'bluetooth' in self.features:
            p1 = subprocess.Popen(["lsusb"], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(["grep", "-i", "bluetooth"],\
                              stdin=p1.stdout, stdout=subprocess.PIPE)
            p1.stdout.close()
            out, err = p2.communicate()
            if out.decode() is not '':
                logging.debug("Detected bluetooth device. Enabling by default...")
                self.switches['bluetooth'].set_active(True)
        if 'firewall' in self.features:
            self.switches['firewall'].set_active(True)
        if 'cups' in self.features:
            self.switches['cups'].set_active(True)

    def store_values(self):
        # Enable forward button
        self.forward_button.set_sensitive(True)
        
        # Get switches' values and store them
        for feature in self.features:
            isactive = self.switches[feature].get_active()
            self.settings.set("feature_" + feature, isactive)
            if isactive:
                logging.debug("Selected '%s' feature to install" % feature)
                
        # Show ufw info message if ufw is selected
        if self.settings.get("feature_firewall") and not self.ufw_info_already_shown:
            ufw = self.ui.get_object("ufw")
            ufw.run()
            ufw.hide()
            self.ufw_info_already_shown = True

        return True

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page

    def prepare(self, direction):
        desktop = self.settings.get('desktop')
        self.features = self.features_by_desktop[desktop]
        self.translate_ui()
        self.show_all()
        self.hide_features()
        if self.defaults:
            self.enable_defaults()
            self.defaults = False

