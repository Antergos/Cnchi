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

        super().add(self.ui.get_object("features"))

    def translate_ui(self):
        txt = _("Feature selection")
        txt = '<span weight="bold" size="large">%s</span>' % txt
        self.title.set_markup(txt)

        '''
        self.prepare_enough_space = self.ui.get_object("prepare_enough_space")
        txt = _("has at least 3GB available drive space")
        self.prepare_enough_space.props.label = txt

        self.prepare_power_source = self.ui.get_object("prepare_power_source")
        txt = _("is plugged in to a power source")
        self.prepare_power_source.props.label = txt

        self.prepare_network_connection = self.ui.get_object("prepare_network_connection")
        txt = _("is connected to the Internet")
        self.prepare_network_connection.props.label = txt

        self.prepare_best_results = self.ui.get_object("prepare_best_results")
        txt = _("For best results, please ensure that this computer:")
        txt = '<span weight="bold" size="large">%s</span>' % txt
        self.prepare_best_results.set_markup(txt)

        self.third_party_info = self.ui.get_object("third_party_info")
        txt = _("Antergos uses third-party software to play Flash, MP3 " \
                "and other media. Some of this software is propietary. The " \
                "software is subject to license terms included with its documentation.")
        self.third_party_info.set_label(txt)

        self.third_party_checkbutton = self.ui.get_object("third_party_checkbutton")
        txt = _("Install this third-party software")
        self.third_party_checkbutton.set_label(txt)
        '''

    def store_values(self):
        # Enable forward button
        self.forward_button.set_sensitive(True)
        
        # TODO: store values

        
        return True

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page

    def prepare(self, direction):
        self.translate_ui()
        self.show_all()

