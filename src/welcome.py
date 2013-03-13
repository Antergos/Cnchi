#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  welcome.py
#  
#  Copyright 2013 Cinnarch
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
#  Cinnarch Team:
#   Alex Filgueira (faidoc) <alexfilgueira.cinnarch.com>
#   Raúl Granados (pollitux) <raulgranados.cinnarch.com>
#   Gustau Castells (karasu) <karasu.cinnarch.com>
#   Kirill Omelchenko (omelcheck) <omelchek.cinnarch.com>
#   Marc Miralles (arcnexus) <arcnexus.cinnarch.com>
#   Alex Skinner (skinner) <skinner.cinnarch.com>

from gi.repository import Gtk
import subprocess, sys, os
import gettext
import os
import misc

# Useful vars for gettext (translations)
APP="cnchi"
DIR="po"

# Import functions
import config

_next_page = "language"
_prev_page = None

class Welcome(Gtk.Box):

    def __init__(self, params):
        self.title = params['title']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        self.settings = params['settings']

        super().__init__()

        self.ui = Gtk.Builder()
        self.ui.add_from_file(os.path.join(self.ui_dir, "welcome.ui"))
        self.ui.connect_signals(self)

        self.welcome_label = self.ui.get_object("welcome_label")
        self.infowelcome_label = self.ui.get_object("infowelcome_label")
        self.tryit_button = self.ui.get_object("tryit_button")
        self.cli_button = self.ui.get_object("cli_button")
        self.graph_button = self.ui.get_object("graph_button")

        self.translate_ui()

        super().add(self.ui.get_object("welcome"))

    def translate_ui(self):
        label = self.ui.get_object("infowelcome_label")
        txt = _("You can try Cinnarch without modifying your hard drive, just click on 'Try it'.\n" \
        "If you want to install the system to your PC, use one of the two installer options.")
        txt = '<span weight="bold">%s</span>' % txt
        label.set_markup(txt)

        txt = _("Welcome to Cinnarch!")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.title.set_markup(txt)

    @misc.raise_privileges
    def remove_temp_files(self):
        tmp_files = [".setup-running", ".km-running", "setup-pacman-running", "setup-mkinitcpio-running", ".tz-running", ".setup" ]
        for t in tmp_files:
            p = os.path.join("/tmp", t)
            if os.path.exists(p):
                os.remove(p)
        
    def on_tryit_button_clicked(self, widget, data=None):
        self.remove_temp_files()
        Gtk.main_quit()
        
    def on_cli_button_clicked(self, widget, data=None):
        subprocess.Popen(["cinnarch-setup"])
        self.remove_temp_files()
        Gtk.main_quit()
		
    def on_graph_button_clicked(self, widget, data=None):
        pass

    def store_values(self):      
        return True

    def prepare(self):
        self.translate_ui()
        self.show_all()

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page
