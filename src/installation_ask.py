#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  installation_ask.py
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

import subprocess
import os

import config

_prev_page = "check"

class InstallationAsk(Gtk.Box):

    def __init__(self, params):
        self.title = params['title']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        self.settings = params['settings']
        
        super().__init__()
        self.ui = Gtk.Builder()
        self.ui.add_from_file(os.path.join(self.ui_dir, "installation_ask.ui"))

        partitioner_dir = os.path.join(self.settings.get("DATA_DIR"), "partitioner/")

        image = self.ui.get_object("automatic_image")
        image.set_from_file(partitioner_dir + "automatic.png")

        image = self.ui.get_object("easy_image")
        image.set_from_file(partitioner_dir + "easy.png")

        image = self.ui.get_object("advanced_image")
        image.set_from_file(partitioner_dir + "advanced.png")

        self.ui.connect_signals(self)

        super().add(self.ui.get_object("installation_ask"))

        # by default, select automatic installation
        self.next_page = "installation_automatic"

    def prepare(self, direction):
        self.translate_ui()
        self.show_all()

    def translate_ui(self):
        txt = _("Your preferred installation type")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.title.set_markup(txt)
        
        # In case we're coming from an installer screen, we change
        # to forward stock button and we activate it
        self.forward_button.set_label("gtk-go-forward")
        self.forward_button.set_sensitive(True)

        radio = self.ui.get_object("automatic_radiobutton")
        radio.set_label(_("Erase disk and install Cinnarch (automatic)"))

        label = self.ui.get_object("automatic_description")
        txt = _("Warning: This will delete all programs, documents, photos, music and any other files on your disk")
        txt = '<span weight="light" size="small">%s</span>' % txt
        label.set_markup(txt)
        label.set_line_wrap(True)
        
        radio = self.ui.get_object("easy_radiobutton")
        radio.set_label(_("Choose where to install Cinnarch (easy)"))

        label = self.ui.get_object("easy_description")
        txt = _("You will have to choose where to install Cinnarch. You will be only asked for the mount points of your root and swap devices.")
        txt = '<span weight="light" size="small">%s</span>' % txt
        label.set_markup(txt)
        label.set_line_wrap(True)

        radio = self.ui.get_object("advanced_radiobutton")
        radio.set_label(_("Manage your partitions and choose where to install Cinnarch (advanced)"))

        label = self.ui.get_object("advanced_description")
        txt = _("You will be able to create/delete partitions, choose where to install Cinnarch and also choose additional mount points.")
        txt = '<span weight="light" size="small">%s</span>' % txt
        label.set_markup(txt)
        label.set_line_wrap(True)

    def store_values(self):
        if self.next_page == "installation_automatic":
            self.settings.set('partition_mode', 'automatic')
        elif self.next_page == "installation_easy":
            self.settings.set('partition_mode', 'easy')
        else:
            self.settings.set('partition_mode', 'advanced')
        return True

    def get_next_page(self):
        return self.next_page

    def get_prev_page(self):
        return _prev_page

    def on_automatic_radiobutton_toggled(self, widget):
        if widget.get_active():
            self.next_page = "installation_automatic"

    def on_easy_radiobutton_toggled(self, widget):
        if widget.get_active():
            self.next_page = "installation_easy"

    def on_advanced_radiobutton_toggled(self, widget):
        if widget.get_active():
            self.next_page = "installation_advanced"
