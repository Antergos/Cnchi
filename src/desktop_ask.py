#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  desktop_ask.py
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

_next_page = "installation_ask"
_prev_page = "check"

class DesktopAsk(Gtk.Box):

    def __init__(self, params):
        self.title = params['title']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        self.settings = params['settings']

        self.desktop_choice = ''
        
        super().__init__()
        self.ui = Gtk.Builder()
        self.ui.add_from_file(os.path.join(self.ui_dir, "desktop_ask.ui"))

        self.ui.connect_signals(self)

        super().add(self.ui.get_object("desktop_ask"))

        # by default, select automatic installation
        #self.next_page = "installation_automatic"

    def prepare(self, direction):
        self.translate_ui()
        self.show_all()

    def translate_ui(self):
        txt = _("Select your Desktop")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.title.set_markup(txt)
        
        # In case we're coming from an installer screen, we change
        # to forward stock button and we activate it
        self.forward_button.set_label("gtk-go-forward")
        self.forward_button.set_sensitive(True)

        radio = self.ui.get_object("gnome_radiobutton")
        radio.set_label(_("Gnome"))

        label = self.ui.get_object("gnome_description")
        txt = _("GNOME 3 is an easy and elegant way to use your computer.")
        txt = '<span weight="light" size="small">%s</span>' % txt
        label.set_markup(txt)
        label.set_line_wrap(True)
        
        radio = self.ui.get_object("cinnamon_radiobutton")
        radio.set_label(_("Cinnamon"))

        label = self.ui.get_object("cinnamon_description")
        txt = _("Traditional layout, advanced features, easy to use, powerful, flexible.")
        txt = '<span weight="light" size="small">%s</span>' % txt
        label.set_markup(txt)
        label.set_line_wrap(True)

        radio = self.ui.get_object("xfce_radiobutton")
        radio.set_label(_("Xfce"))

        label = self.ui.get_object("xfce_description")
        txt = _("Xfce is a lightweight desktop environment for UNIX-like operating systems.")
        txt = '<span weight="light" size="small">%s</span>' % txt
        label.set_markup(txt)
        label.set_line_wrap(True)

        radio = self.ui.get_object("lxde_radiobutton")
        radio.set_label(_("Lxde"))

        label = self.ui.get_object("lxde_description")
        txt = _("Lxde is an extremely fast-performing and energy-saving desktop environment.")
        txt = '<span weight="light" size="small">%s</span>' % txt
        label.set_markup(txt)
        label.set_line_wrap(True)

        radio = self.ui.get_object("openbox_radiobutton")
        radio.set_label(_("Openbox"))

        label = self.ui.get_object("openbox_description")
        txt = _("Openbox is a highly configurable, next generation window manager with extensive standards support.")
        txt = '<span weight="light" size="small">%s</span>' % txt
        label.set_markup(txt)
        label.set_line_wrap(True)

    def store_values(self):
        if self.desktop_choice == "gnome":
            self.settings.set('desktop', 'gnome')
        elif self.desktop_choice == "cinnamon":
            self.settings.set('desktop', 'cinnamon')
        elif self.desktop_choice == "xfce":
            self.settings.set('desktop', 'xfce')
        elif self.desktop_choice == "lxde":
            self.settings.set('desktop', 'lxde')
        elif self.desktop_choice == "openbox":
            self.settings.set('desktop', 'openbox')

        return True

    def get_next_page(self):
        return _next_page

    def get_prev_page(self):
        return _prev_page

    def on_gnome_radiobutton_toggled(self, widget):
        if widget.get_active():
            self.desktop_choice = 'gnome'

    def on_cinnamon_radiobutton_toggled(self, widget):
        if widget.get_active():
            self.desktop_choice = 'cinnamon'

    def on_xfce_radiobutton_toggled(self, widget):
        if widget.get_active():
            self.desktop_choice = 'xfce'

    def on_lxde_radiobutton_toggled(self, widget):
        if widget.get_active():
            self.desktop_choice = 'lxde'

    def on_openbox_radiobutton_toggled(self, widget):
        if widget.get_active():
            self.desktop_choice = 'openbox'
