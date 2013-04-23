#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  desktop.py
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

from gi.repository import Gtk, GLib
import config
import os

_next_page = "installation_ask"
_prev_page = "check"

class DesktopAsk(Gtk.Box):

    def __init__(self, params):
        self.title = params['title']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        self.settings = params['settings']

        super().__init__()

        self.ui = Gtk.Builder()
        self.ui.add_from_file(os.path.join(self.ui_dir, "desktop.ui"))

        self.desktops_dir = os.path.join(self.settings.get("DATA_DIR"), "desktops/")

        self.desktop_info = self.ui.get_object("desktop_info")
        self.treeview_desktop = self.ui.get_object("treeview_desktop")

        self.ui.connect_signals(self)

        self.desktop_choice = 'gnome'

        self.set_desktop_list()

        super().add(self.ui.get_object("desktop"))

    def translate_ui(self, desktop):
        image = self.ui.get_object("image_desktop")     

        label = self.ui.get_object("desktop_info")
        if desktop == 'gnome':
            txt = _("<span weight='bold'>GNOME</span>\n" \
            "Gnome 3 is an easy and elegant way to use your \n" \
            "computer. It is designed to put you in control \n" \
            "and bring freedom to everybody. GNOME 3 is \n" \
            "developed by the GNOME community, a diverse, \n" \
            "international group of contributors that is \n" \
            "supported by an independent, non-profit foundation.")

        elif desktop == 'xfce':
            txt = _("<span weight='bold'>XFCE</span>\n" \
            "Xfce is a lightweight desktop environment \n" \
            "for UNIX-like operating systems. It aims to \n" \
            "be fast and low on system resources, while \n" \
            "still being visually appealing and user friendly.")

        elif desktop == 'lxde':
            txt = _("<span weight='bold'>LXDE</span>\n" \
            "Extremely fast-performing and energy-saving desktop \n" \
            "environment. Maintained by an international community \n" \
            "of developers, it comes with a beautiful interface, \n" \
            "multi-language support, standard keyboard short cuts \n" \
            "and additional features like tabbed file browsing.")

        elif desktop == 'openbox':
            txt = _("<span weight='bold'>OPENBOX</span>\n" \
            "Openbox is a highly configurable, next generation \n" \
            "window manager with extensive standards support.\n" \
            "The *box visual style is well known for its \n" \
            "minimalistic appearance.")
            
        label.set_markup(txt)
        image.set_from_file(self.desktops_dir + desktop + ".png")

        txt = _("Select your desktop")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.title.set_markup(txt)
            
    def prepare(self, direction):
        self.translate_ui(self.desktop_choice)
        self.show_all()


    def set_desktop_list(self):
        liststore_desktop = Gtk.ListStore(str)

        render = Gtk.CellRendererText()
        col_desktops = Gtk.TreeViewColumn(_("Desktops"), render, text=0)
        self.treeview_desktop.set_model(liststore_desktop)
        self.treeview_desktop.append_column(col_desktops)

        liststore_desktop.append(['Gnome'])
        liststore_desktop.append(['Xfce'])
        liststore_desktop.append(['Lxde'])
        liststore_desktop.append(['Openbox'])

        self.select_default_row(self.treeview_desktop, 'Gnome')

    def set_desktop(self, desktop):

        if desktop == 'Gnome':
            self.desktop_choice = 'gnome'
        elif desktop == 'Xfce':
            self.desktop_choice = 'xfce'
        elif desktop == 'Lxde':
            self.desktop_choice = 'lxde'
        elif desktop == 'Openbox':
            self.desktop_choice = 'openbox'

        self.translate_ui(self.desktop_choice)
                
    def on_treeview_desktop_cursor_changed(self, treeview):
        selected = treeview.get_selection()
        if selected:
            (ls, iter) = selected.get_selected()
            if iter:
                desktop = ls.get_value(iter, 0)
                self.set_desktop(desktop)
        
    def store_values(self):
        selected = self.treeview_desktop.get_selection()

        (ls, iter) = selected.get_selected()
        desktop = ls.get_value(iter,0)

        self.settings.set('desktop', desktop)

        return True

    def select_default_row(self, treeview, desktop):   
        model = treeview.get_model()
        iterator = model.iter_children(None)
        while iterator is not None:
            if model.get_value(iterator, 0) == desktop:
                path = model.get_path(iterator)
                treeview.get_selection().select_path(path)
                GLib.idle_add(self.scroll_to_cell, treeview, path)
                break
            iterator = model.iter_next(iterator)


    def scroll_to_cell(self, treeview, path):
        treeview.scroll_to_cell(path)
        return False


    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page
