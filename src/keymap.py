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

from gi.repository import Gtk, GLib

# Import functions
import config
import os
import canonical.keyboard_names as keyboard_names
import logging
import show_message as show
import canonical.misc as misc
import subprocess
import keyboard_widget

from gtkbasebox import GtkBaseBox

class Keymap(GtkBaseBox):

    def __init__(self, params):
        self.next_page = "desktop"
        self.prev_page = "timezone"

        self.testing = params['testing']

        self.prepare_called = False

        super().__init__(params, "keymap")

        self.filename = os.path.join(self.settings.get('data'), "kbdnames.gz")

        self.ui.connect_signals(self)

        self.layout_treeview = self.ui.get_object("keyboardlayout")
        self.variant_treeview = self.ui.get_object("keyboardvariant")
        
        self.keyboard_test_entry = self.ui.get_object("keyboard_test_entry")
        self.keyboard_widget = self.ui.get_object("keyboard_widget")

        self.create_toolviews()

        self.add(self.ui.get_object("keymap"))

    def translate_ui(self):
        self.header.set_subtitle(_("Select Your Keyboard Layout"))
        
        lbl = self.ui.get_object("label_layouts")
        lbl.set_markup(_("Keyboard Layouts"))

        lbl = self.ui.get_object("label_variants")
        lbl.set_markup(_("Keyboard Variants"))

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
        
        if direction == 'forwards':
            self.fill_layout_treeview()
            self.forward_button.set_sensitive(False)

            # Select treeview with selected country in previous screen.
            selected_country = self.settings.get("timezone_human_country")
            selected_country = self.fix_countries(selected_country)
            found = self.select_value_in_treeview(self.layout_treeview, selected_country)

            if found == False:
                selected_country = "USA"
                self.select_value_in_treeview(self.layout_treeview, selected_country)

            logging.info(_("keyboard_layout is %s") % selected_country)
        
        self.prepare_called = True

        self.show_all()

    def fix_countries(self, country):
        # FIXME: There are some countries that do not match with 'kbdnames' so we convert them here manually.
        # I'm not sure if there're more countries that should be added here.

        if country == "United States":
            country = "USA"
        elif country == "Russian Federation":
            country = "Russia"

        return country

    def fill_layout_treeview(self):
        lang = self.settings.get("language_code")

        keyboard_names._default_filename = self.filename

        if not keyboard_names.has_language(lang):
            lang = "C"

        kbd_names = keyboard_names.KeyboardNames(self.filename)
        kbd_names._load(lang)

        sorted_layouts = []

        for layout in kbd_names._layout_by_human:
            sorted_layouts.append(layout)

        #sorted_layouts.sort()
        sorted_layouts = misc.sort_list(sorted_layouts, self.settings.get("locale"))

        # Block signal
        self.layout_treeview.handler_block_by_func(self.on_keyboardlayout_cursor_changed)

        # Clear our model
        liststore = self.layout_treeview.get_model()
        liststore.clear()

        # Add layouts (sorted)
        for layout in sorted_layouts:
            liststore.append([layout])
        
        # Unblock signal
        self.layout_treeview.handler_unblock_by_func(self.on_keyboardlayout_cursor_changed)

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
                self.keyboard_layout_human = keyboard_layout

                lang = self.settings.get("language_code")

                if not keyboard_names.has_language(lang):
                    lang = "C"

                kbd_names = keyboard_names.KeyboardNames(self.filename)
                kbd_names._load(lang)

                country_code = kbd_names._layout_by_human[self.keyboard_layout_human]
                self.keyboard_layout = country_code

                variants = kbd_names._variant_by_human

                sorted_variants = []

                for variant in variants[country_code]:
                    sorted_variants.append(variant)

                #sorted_variants.sort()
                sorted_variants = misc.sort_list(sorted_variants, self.settings.get("locale"))
                
                # Block signal
                self.variant_treeview.handler_block_by_func(self.on_keyboardvariant_cursor_changed)

                # Clear our model
                liststore = self.variant_treeview.get_model()
                liststore.clear()

                # Add keyboard variants (sorted)
                for variant in sorted_variants:
                    liststore.append([variant])

                # Unblock signal
                self.variant_treeview.handler_unblock_by_func(self.on_keyboardvariant_cursor_changed)

                #selection = self.variant_treeview.get_selection()
                self.variant_treeview.set_cursor(0)
        else:
            liststore = self.variant_treeview.get_model()
            liststore.clear()

    def on_keyboardlayout_cursor_changed(self, widget):
        self.fill_variant_treeview()
        self.forward_button.set_sensitive(True)

    def on_keyboardvariant_cursor_changed(self, widget):
        self.store_values()
        self.set_keyboard_widget()

    def store_values(self):
        # We've previously stored our layout, now store our variant
        selected = self.variant_treeview.get_selection()

        keyboard_variant_human = "USA"

        if selected:
            (ls, iter) = selected.get_selected()
            if iter:
                keyboard_variant_human = ls.get_value(iter, 0)

        lang = self.settings.get("language_code")

        kbd_names = keyboard_names.KeyboardNames(self.filename)

        if not kbd_names.has_language(lang):
            lang = "C"

        kbd_names._load(lang)
        
        try:
            keyboard_layout_human = self.keyboard_layout_human
        except AttributeError:
            keyboard_layout_human = "USA"
            self.keyboard_layout_human = keyboard_layout_human
        
        country_code = kbd_names._layout_by_human[self.keyboard_layout_human]

        self.keyboard_layout = country_code
        
        self.keyboard_variant = kbd_names._variant_by_human[country_code][keyboard_variant_human]

        self.settings.set("keyboard_layout", self.keyboard_layout)
        self.settings.set("keyboard_variant", self.keyboard_variant)

        # This fixes issue 75: Won't pick/load the keyboard layout after selecting one (sticks to qwerty)
        if not self.testing and self.prepare_called:
            self.setkb()

        return True

    def setkb(self):
        subprocess.check_call(['setxkbmap', '-layout', self.keyboard_layout, "-variant", self.keyboard_variant])

        with misc.raised_privileges():
            subprocess.check_call(['localectl', 'set-keymap', '--no-convert', self.keyboard_layout])

    def set_keyboard_widget(self):
        ''' Pass current keyboard layout to the keyboard widget. '''
        self.keyboard_widget.set_layout(self.keyboard_layout)
        self.keyboard_widget.set_variant(self.keyboard_variant)
        self.keyboard_widget.show_all()

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message): return message

if __name__ == '__main__':
    from test_screen import _,run
    run('Keymap')
