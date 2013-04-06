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

from show_message import warning

# Useful vars for gettext (translations)
APP="cnchi"
DIR = "/usr/share/locale"

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

        data_dir = self.settings.get("DATA_DIR")
        welcome_dir = os.path.join(data_dir, "welcome")
        
        self.label = {}
        self.label['welcome'] = self.ui.get_object("welcome_label")
        self.label['info'] = self.ui.get_object("infowelcome_label")
        
        self.button = {}
        self.button['tryit'] = self.ui.get_object("tryit_button")
        self.button['cli'] = self.ui.get_object("cli_button")
        self.button['graph'] = self.ui.get_object("graph_button")
        
        self.image = {}
        self.image['tryit'] = self.ui.get_object("tryit_image")
        self.image['cli'] = self.ui.get_object("cli_image")
        self.image['graph'] = self.ui.get_object("graph_image")
        
        self.filename = {}
        self.filename['tryit'] = os.path.join(welcome_dir, "tryit-icon.png")
        self.filename['cli'] = os.path.join(welcome_dir, "cliinstaller-icon.png")
        self.filename['graph'] = os.path.join(welcome_dir, "installer-icon.png")
        
        for key in self.image:
            self.image[key].set_from_file(self.filename[key])
        
        self.translate_ui()

        super().add(self.ui.get_object("welcome"))

    def translate_ui(self):
        #label = self.ui.get_object("infowelcome_label")
        txt = _("You can try Cinnarch without modifying your hard drive, just click on 'Try it'.\n" \
        "If you want to install the system to your PC, use one of the two installer options.")
        txt = '<span weight="bold">%s</span>' % txt
        self.label['info'].set_markup(txt)

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
        try:
            subprocess.Popen(["cinnarch-setup"])
        except:
            warning(_("Can't load the CLI installer"))
        finally:
            self.remove_temp_files()
        #Gtk.main_quit()
		
    def on_graph_button_clicked(self, widget, data=None):
        self.forward_button.emit("clicked")

    def store_values(self):
        self.forward_button.show()
        return True

    def prepare(self, direction):
        self.translate_ui()
        self.show_all()
        self.forward_button.hide()

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page
