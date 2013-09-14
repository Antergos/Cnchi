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
#  
#  Antergos Team:
#   Alex Filgueira (faidoc) <alexfilgueira.antergos.com>
#   Raúl Granados (pollitux) <raulgranados.antergos.com>
#   Gustau Castells (karasu) <karasu.antergos.com>
#   Kirill Omelchenko (omelcheck) <omelchek.antergos.com>
#   Marc Miralles (arcnexus) <arcnexus.antergos.com>
#   Alex Skinner (skinner) <skinner.antergos.com>

from gi.repository import Gtk, GObject

import subprocess
import os
import gtkwidgets
import logging

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
        
        self.features = [ "bluetooth", "cups", "office", "visual", "firewall", "third_party" ]
        
        self.labels = {}
        self.titles = {}
        self.switches = {}
        
        for feature in self.features:
            object_name = "label_" + feature
            self.labels[feature] = self.ui.get_object(object_name)

            object_name = "label_title_" + feature
            self.titles[feature] = self.ui.get_object(object_name)

            object_name = "switch_" + feature
            self.switches[feature] = self.ui.get_object(object_name)

        super().add(self.ui.get_object("features"))

    def translate_ui(self):
        txt = _("Feature selection")
        txt = '<span weight="bold" size="large">%s</span>' % txt
        self.title.set_markup(txt)

        # Bluetooth
        txt = _("Bluetooth support")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["bluetooth"].set_markup(txt)

        txt = _("Without Bluetooth support you can't use Bluetooth devices")
        self.labels["bluetooth"].set_markup(txt)

        # Printing support
        txt = _("Printing support (cups)")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["cups"].set_markup(txt)
        
        txt = _("This includes printer drivers and manage tools")
        self.labels["cups"].set_markup(txt)

        # LibreOffice
        txt = _("LibreOffice")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["office"].set_markup(txt)
        
        txt = _("Office suite (word processor, spreadsheet, ...)")
        self.labels["office"].set_markup(txt)

        # Visual effects
        txt = _("Visual effects")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["visual"].set_markup(txt)
        
        txt = _("Visual effects such as transparencies, shadows, etc.")
        self.labels["visual"].set_markup(txt)

        # Firewall
        txt = _("Firewall")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["firewall"].set_markup(txt)

        txt = _("Activates your firewall (closes all ports by default)")
        self.labels["firewall"].set_markup(txt)

        # Propietary packages (third_party)
        txt = _("Propietary packages")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.titles["third_party"].set_markup(txt)
        
        txt = _("Third-party software to play Flash, MP3 and other media")
        self.labels["third_party"].set_markup(txt)

    def store_values(self):
        # Enable forward button
        self.forward_button.set_sensitive(True)
        
        # Get switches' values and store them
        for feature in self.features:
            isactive = self.switches[feature].get_active()
            self.settings.set("feature_" + feature, isactive)
            if isactive:
                logging.debug("Selected '%s' feature to install" % feature)

        return True

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page

    def prepare(self, direction):
        self.translate_ui()
        self.show_all()

