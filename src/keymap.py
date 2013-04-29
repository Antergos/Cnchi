#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  keymap.py
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

from gi.repository import Gtk, GLib

# Import functions
import config
import os
import keyboard_names
import log
import show_message as show

_next_page = "user_info"
_prev_page = "timezone"

class Keymap(Gtk.Box):

    def __init__(self, params):
        self.title = params['title']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        self.settings = params['settings']

        super().__init__()

        self.ui = Gtk.Builder()

        self.ui.add_from_file(os.path.join(self.ui_dir, "keymap.ui"))

        self.ui.connect_signals(self)

        self.layout_treeview = self.ui.get_object("keyboardlayout")
        self.variant_treeview = self.ui.get_object("keyboardvariant")

        self.create_toolviews()

        self.filename = self.settings.get("DATA_DIR") + "kbdnames.gz"

        super().add(self.ui.get_object("keymap"))

    def translate_ui(self):
        txt = _("Select your keyboard layout")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.title.set_markup(txt)
        
        # TODO: Also change layouts and variants text column

    def create_toolviews(self):
        render = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn(_("Layouts"),render,text=0)
        liststore = Gtk.ListStore(str)
        self.layout_treeview.append_column(col)
        self.layout_treeview.set_model(liststore)

        render = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn(_("Variants"),render,text=0)
        liststore = Gtk.ListStore(str)
        self.variant_treeview.append_column(col)
        self.variant_treeview.set_model(liststore)

    def prepare(self, direction):
        self.translate_ui()
        self.fill_layout_treeview()
        self.fill_variant_treeview()
        self.forward_button.set_sensitive(False)
        self.translate_ui()

        # select treeview with selected country in previous screen.
        selected_country = self.settings.get("timezone_human_country")

        selected_country = self.fix_countries(selected_country)

        found = self.select_value_in_treeview(self.layout_treeview, selected_country)

        if found == False:
            self.select_value_in_treeview(self.layout_treeview, "USA")

        log.debug(_("keyboard_layout is %s") % selected_country)

        self.show_all()

    def fix_countries(self, country):
        # Don't know how to fix this.
        # There are some countries that do not
        # match. Convert them here manually
        # More countries should be added here

        if country == "United States":
            country = "USA"
        elif country == "Russian Federation":
            country = "Russia"

        return country


    def fill_layout_treeview(self):
        lang = self.settings.get("language_code")

        if not keyboard_names.has_language(lang):
            lang = "C"

        kbd_names = keyboard_names.KeyboardNames(self.filename)
        kbd_names._load(lang)

        sorted_layouts = []

        # misc.utf8(self.city_entry.get_text())

        for layout in kbd_names._layout_by_human:
            sorted_layouts.append(layout)

        # FIXME: Doesn't sort well accents, must use utf8
        sorted_layouts.sort()

        liststore = self.layout_treeview.get_model()

        liststore.clear()

        for layout in sorted_layouts:
            liststore.append([layout])

    def select_value_in_treeview(self, treeview, value):
        model = treeview.get_model()
        treeiter = model.get_iter(0)

        index = 0

        found = False

        while treeiter != None:
            if model[treeiter][0] == value:
                treeview.set_cursor(index)
                path = model.get_path(treeiter)
                GLib.idle_add(self.scroll_to_cell, treeview, path)
                treeiter = None
                found = True
            else:
                index = index + 1
                treeiter = model.iter_next(treeiter)

        return found

    def scroll_to_cell(self, treeview, path):
        treeview.scroll_to_cell(path)
        return False

    def fill_variant_treeview(self):
        selected = self.layout_treeview.get_selection()

        if selected:
            (ls, iter) = selected.get_selected()
            if iter:

                keyboard_layout = ls.get_value(iter, 0)

                # store layout selected
                self.keyboard_layout = keyboard_layout

                lang = self.settings.get("language_code")

                if not keyboard_names.has_language(lang):
                    lang = "C"

                kbd_names = keyboard_names.KeyboardNames(self.filename)
                kbd_names._load(lang)

                country_code = kbd_names._layout_by_human[keyboard_layout]
                self.keyboard_layout = country_code

                variants = kbd_names._variant_by_human

                sorted_variants = []

                for variant in variants[country_code]:
                    sorted_variants.append(variant)

                # FIXME: Doesn't sort well accents, must use utf8
                sorted_variants.sort()

                liststore = self.variant_treeview.get_model()

                liststore.clear()

                for variant in sorted_variants:
                    liststore.append([variant])

                #selection = self.variant_treeview.get_selection()
                self.variant_treeview.set_cursor(0)

        else:
            liststore = self.variant_treeview.get_model()
            liststore.clear()

    def on_keyboardlayout_cursor_changed(self, widget):
        self.fill_variant_treeview()
        self.forward_button.set_sensitive(True)

    def store_values(self):
        # we've previously stored our layout, now store our variant
        selected = self.variant_treeview.get_selection()

        keyboard_variant = ""

        if selected:
            (ls, iter) = selected.get_selected()
            if iter:
                keyboard_variant = ls.get_value(iter, 0)

        self.settings.set("keyboard_layout", self.keyboard_layout)
        self.settings.set("keyboard_variant", keyboard_variant)
        
        return True

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page
