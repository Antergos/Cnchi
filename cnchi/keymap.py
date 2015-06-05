#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  keymap.py
#
#  Copyright © 2013-2015 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

from gi.repository import Gtk, GLib

import os
import logging
import subprocess

import misc.misc as misc
import misc.keyboard_names as keyboard_names
import misc.keyboard_widget as keyboard_widget

from gtkbasebox import GtkBaseBox


class Keymap(GtkBaseBox):
    def __init__(self, params, prev_page="timezone", next_page="desktop"):
        super().__init__(self, params, "keymap", prev_page, next_page)

        self.prepare_called = False

        self.layout_treeview = self.ui.get_object("keyboardlayout")
        self.variant_treeview = self.ui.get_object("keyboardvariant")

        self.keyboard_test_entry = self.ui.get_object("keyboard_test_entry")
        self.keyboard_widget = self.ui.get_object("keyboard_widget")

        self.keyboard_layout = { 'code': None, 'description': None }
        self.keyboard_variant  = { 'code': None, 'description': None }

        base_xml_path = os.path.join(self.settings.get('data'), "base.xml")
        self.kbd_names = keyboard_names.KeyboardNames(base_xml_path)

        self.create_treeviews()

    def translate_ui(self):
        """ Translates all ui elements """
        self.header.set_subtitle(_("Select Your Keyboard Layout"))

        lbl = self.ui.get_object("label_layouts")
        lbl.set_markup(_("Keyboard Layouts"))

        lbl = self.ui.get_object("label_variants")
        lbl.set_markup(_("Keyboard Variants"))

    def create_treeviews(self):
        render = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn(_("Layouts"), render, text=0)
        liststore = Gtk.ListStore(str)
        self.layout_treeview.append_column(col)
        self.layout_treeview.set_model(liststore)

        render = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn(_("Variants"), render, text=0)
        liststore = Gtk.ListStore(str)
        self.variant_treeview.append_column(col)
        self.variant_treeview.set_model(liststore)

    def prepare(self, direction):
        self.translate_ui()

        '''
        <name>us</name> <-- country code
        <shortDescription>en</shortDescription>
        <description>English (US)</description>
        <languageList>
          <iso639Id>eng</iso639Id> <-- language code
        </languageList>
        '''

        if direction == 'forwards':
            self.fill_layout_treeview()
            self.forward_button.set_sensitive(False)

            country_code =  self.settings.get("country_code")
            self.keyboard_layout['code'] = country_code

            layout_description = self.kbd_names.get_layout_description(country_code)
            if layout_description:
                self.keyboard_layout['description'] = layout_description
                self.select_value_in_treeview(self.layout_treeview, layout_description)

                # specific variant cases
                country = self.settings.get("country")
                language_name = self.settings.get("language_name")
                language_code = self.settings.get("language_code")
                if country == "Spain" and language_name == "Catalan":
                    self.keyboard_variant['code'] = "cat"
                    self.keyboard_variant['description'] = self.kbd_names.get_variant_description(country_code, "cat")
                    self.select_value_in_treeview(self.variant_treeview, self.keyboard_variant['description'])
                if country == "Canada" and language_name == "English":
                    self.keyboard_variant['code'] = "eng"
                    self.keyboard_variant['description'] = self.kbd_names.get_variant_description(country_code, "eng")
                    self.select_value_in_treeview(self.variant_treeview, self.keyboard_variant['description'])
        self.prepare_called = True
        self.show_all()

    def fill_layout_treeview(self):
        layouts = self.kbd_names.get_layouts()
        sorted_descriptions = []
        for layout_name in layouts:
            description = self.kbd_names.get_layout_description(layout_name)
            sorted_descriptions.append(description)

        sorted_descriptions = misc.sort_list(sorted_descriptions, self.settings.get("locale"))

        # Block signal
        self.layout_treeview.handler_block_by_func(self.on_keyboardlayout_cursor_changed)

        # Clear our model
        liststore = self.layout_treeview.get_model()
        liststore.clear()

        # Add layouts (sorted)
        for description in sorted_descriptions:
            liststore.append([description])

        # Unblock signal
        self.layout_treeview.handler_unblock_by_func(self.on_keyboardlayout_cursor_changed)

    def select_value_in_treeview(self, treeview, value):
        model = treeview.get_model()
        tree_iter = model.get_iter(0)

        index = 0

        found = False

        while tree_iter is not None and not found:
            if model[tree_iter][0] == value:
                treeview.set_cursor(index)
                path = model.get_path(tree_iter)
                GLib.idle_add(self.scroll_to_cell, treeview, path)
                tree_iter = None
                found = True
            else:
                index += 1
                tree_iter = model.iter_next(tree_iter)

        return found

    @staticmethod
    def scroll_to_cell(treeview, path):
        treeview.scroll_to_cell(path)
        return False

    def fill_variant_treeview(self):
        selected = self.layout_treeview.get_selection()

        if selected:
            (ls, iterator) = selected.get_selected()
            if iterator:
                # Store layout selected
                layout_description = ls.get_value(iterator, 0)
                self.keyboard_layout['description'] = ls.get_value(iterator, 0)

                layout_name = self.kbd_names.get_layout_name_by_description(layout_description)
                self.keyboard_layout['code'] = layout_name

                sorted_variant_descriptions = []

                if self.kbd_names.has_variants(layout_name):
                    sorted_variant_descriptions = self.kbd_names.get_variant_descriptions(layout_name)
                else:
                    logging.debug(
                        _("Keyboard layout '%s' has no variants"),
                        self.keyboard_layout['description'])

                sorted_variant_descriptions = misc.sort_list(
                    sorted_variant_descriptions,
                    self.settings.get("locale"))

                # Block signal
                self.variant_treeview.handler_block_by_func(self.on_keyboardvariant_cursor_changed)

                # Clear our model
                liststore = self.variant_treeview.get_model()
                liststore.clear()

                # Add keyboard variants (sorted)
                for description in sorted_variant_descriptions:
                    liststore.append([description])

                # Unblock signal
                self.variant_treeview.handler_unblock_by_func(self.on_keyboardvariant_cursor_changed)

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
        if self.keyboard_layout['code'] is None or self.keyboard_layout['description'] is None:
            # We have not previously stored our layout
            return

        selected = self.variant_treeview.get_selection()

        self.keyboard_variant['code'] = None
        self.keyboard_variant['description'] = None

        if selected:
            (ls, iterator) = selected.get_selected()
            if iterator:
                variant_description = ls.get_value(iterator, 0)
                self.keyboard_variant['description'] = variant_description
                self.keyboard_variant['code'] = self.kbd_names.get_variant_name_by_description(variant_description)


        self.settings.set("keyboard_layout", self.keyboard_layout['code'])
        self.settings.set("keyboard_variant", self.keyboard_variant['code'])

        if self.keyboard_variant['code'] is None or len(self.keyboard_variant['code']) == 0:
            txt = _("Set keyboard to layout name '{0}' ({1})").format(
                self.keyboard_layout['description'],
                self.keyboard_layout['code'])
        else:
            txt = _("Set keyboard to layout name '{0}' ({1}) and variant name '{2}' ({3})").format(
                self.keyboard_layout['description'],
                self.keyboard_layout['code'],
                self.keyboard_variant['description'],
                self.keyboard_variant['code'])
        logging.debug(txt)

        # This fixes issue 75: Won't pick/load the keyboard layout after selecting one (sticks to qwerty)
        if not self.testing and self.prepare_called:
            self.setkb()

        return True

    def setkb(self):
        if len(self.keyboard_layout['code']) > 0:
            cmd = ['setxkbmap', '-layout', self.keyboard_layout['code']]

            if self.keyboard_variant['code'] and len(self.keyboard_variant['code']) > 0:
                cmd.extend(["-variant", self.keyboard_variant['code']])

            try:
                subprocess.check_call(cmd)
            except subprocess.CalledProcessError as process_error:
                logging.warning(process_error)

            keymap = misc.check_console_keymap(
                self.keyboard_layout['code'],
                self.settings.get('data'))

            logging.debug(_("Will use console keymap '{0}'").format(keymap))

            with misc.raised_privileges():
                cmd = ['localectl', 'set-keymap', '--no-convert', keymap]
                try:
                    subprocess.check_call(cmd)
                except subprocess.CalledProcessError as process_error:
                    logging.warning(process_error)


    def set_keyboard_widget(self):
        """ Pass current keyboard layout to the keyboard widget. """
        self.keyboard_widget.set_layout(self.keyboard_layout['code'])
        self.keyboard_widget.set_variant(self.keyboard_variant['code'])
        self.keyboard_widget.show_all()

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

if __name__ == '__main__':
    from test_screen import _, run

    run('Keymap')
