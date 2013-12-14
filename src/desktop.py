#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  desktop.py
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

""" Desktop screen """

from gi.repository import Gtk, GLib
import os
import logging
import desktop_environments as desktops

_next_page = "features"
_prev_page = "check"

class DesktopAsk(Gtk.Box):
    """ Class to show the Desktop screen """
    def __init__(self, params):
        self.header = params['header']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        self.settings = params['settings']

        super().__init__()

        self.ui = Gtk.Builder()
        self.ui.add_from_file(os.path.join(self.ui_dir, "desktop.ui"))

        self.desktops_dir = os.path.join(self.settings.get('data'), "desktops/")

        self.desktop_info = self.ui.get_object("desktop_info")
        self.treeview_desktop = self.ui.get_object("treeview_desktop")

        self.ui.connect_signals(self)

        self.desktop_choice = 'gnome'

        self.enabled_desktops = self.settings.get("desktops")

        self.set_desktop_list()

        super().add(self.ui.get_object("desktop"))

    def translate_ui(self, desktop):
        """ Translates all ui elements """
        image = self.ui.get_object("image_desktop")
        label = self.ui.get_object("desktop_info")
        
        txt = "<span weight='bold'>%s</span>\n" % desktops.NAMES[desktop]
        txt += desktops.DESCRIPTIONS[desktop]
            
        label.set_markup(txt)

        image.set_from_file(self.desktops_dir + desktop + ".png")

        txt = _("Choose Your Desktop")
        self.header.set_subtitle(txt)


    def prepare(self, direction):
        """ Prepare screen """
        self.translate_ui(self.desktop_choice)
        self.show_all()

    def set_desktop_list(self):
        """ Set desktop list in the TreeView """
        render = Gtk.CellRendererText()
        col_desktops = Gtk.TreeViewColumn(_("Desktops"), render, text=0)
        liststore_desktop = Gtk.ListStore(str)
        self.treeview_desktop.append_column(col_desktops)
        self.treeview_desktop.set_model(liststore_desktop)

        names = []
        for desktop in self.enabled_desktops:
            names.append(desktops.NAMES[desktop])

        names.sort()

        for name in names:
            liststore_desktop.append([name])

        self.select_default_row(self.treeview_desktop, 'Gnome')

    def set_desktop(self, desktop):
        """ Show desktop info """
        for key in desktops.NAMES.keys():
            if desktops.NAMES[key] == desktop:
                self.desktop_choice = key
                self.translate_ui(self.desktop_choice)
                return

    def on_treeview_desktop_cursor_changed(self, treeview):
        selected = treeview.get_selection()
        if selected:
            (selection, iterator) = selected.get_selected()
            if iterator:
                desktop = selection.get_value(iterator, 0)
                self.set_desktop(desktop)

    def store_values(self):
        """ Store desktop """
        self.settings.set('desktop', self.desktop_choice)
        logging.info(_("Cnchi will install Antergos with the '%s' desktop"), self.desktop_choice)
        return True

    def select_default_row(self, treeview, desktop):
        """ Select default treeview row """
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
        """ Scrolls treeview to show the desired cell """
        treeview.scroll_to_cell(path)
        return False

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page
