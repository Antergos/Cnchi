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

        self.keyboard_test_entry = self.ui.get_object("keyboard_test_entry")
        self.keyboard_widget = self.ui.get_object("keyboard_widget")

        self.keyboard_layout = { 'code': None, 'description': None }
        self.keyboard_variant  = { 'code': None, 'description': None }

        base_xml_path = os.path.join(self.settings.get('data'), "base.xml")
        self.kbd_names = keyboard_names.KeyboardNames(base_xml_path)

        self.keymap_treeview = self.ui.get_object("keymap_treeview")
        tree_store = Gtk.TreeStore(str)
        self.keymap_treeview.set_model(tree_store)

    def clear(self):
        logging.warning("*clear*")
        # Clear layout treeview model
        tree_store = self.keymap_treeview.get_model()
        if tree_store:
            tree_store.clear()

        self.keyboard_layout = { 'code': None, 'description': None }
        self.keyboard_variant  = { 'code': None, 'description': None }

    def translate_ui(self):
        """ Translates all ui elements """
        logging.warning("*translate_ui*")
        self.header.set_subtitle(_("Select Your Keyboard Layout"))

        lbl = self.ui.get_object("label_layouts")
        lbl.set_markup(_("Keyboard Layouts"))

        lbl = self.ui.get_object("label_variants")
        lbl.set_markup(_("Keyboard Variants"))

    def prepare(self, direction):
        logging.warning("*prepare*")
        self.translate_ui()

        country_code =  self.settings.get("country_code")

        if country_code != self.keyboard_layout['code']:
            self.clear()

            self.fill_layout_treeview()
            self.forward_button.set_sensitive(False)

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
            else:
                logging.debug(_("Can't match a keymap for country code '%s'"), country_code)
                self.keyboard_layout['description'] = None
                self.keyboard_variant['code'] = None
                self.keyboard_variant['description'] = None

        self.prepare_called = True
        self.show_all()



#parent_iter = treestore.append(None, ["parent row"])
#treestore.append(parent_iter, ["child row"])

    def fill_layout_treeview(self):
        logging.warning("*fill_layout_treeview*")
        tree_store = self.keymap_treeview.get_model()
        layouts = self.kbd_names.get_layouts()
        for layout_name in layouts:
            (name, short_description, description, language_names) = layouts[layout_name]
            parent_iter = tree_store.append(None, [description])

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
        logging.warning("*select_value_in_treeview*")
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
        logging.warning("*fill_variant_treeview*")

        selected = self.layout_treeview.get_selection()

        if selected:
            (ls, iterator) = selected.get_selected()
            if iterator:
                # Store layout selected
                layout_description = ls.get_value(iterator, 0)
                logging.warning("** %s **", layout_description)
                self.keyboard_layout['description'] = layout_description

                layout_name = self.kbd_names.get_layout_name_by_description(layout_description)
                self.keyboard_layout['code'] = layout_name

                sorted_variant_descriptions = []

                if self.kbd_names.has_variants(layout_name):
                    sorted_variant_descriptions = self.kbd_names.get_variant_descriptions(layout_name)
                    sorted_variant_descriptions = misc.sort_list(
                        sorted_variant_descriptions,
                        self.settings.get("locale"))
                else:
                    logging.debug(
                        _("Keyboard layout '%s' has no variants"),
                        self.keyboard_layout['description'])

                # Block signal
                self.variant_treeview.handler_block_by_func(self.on_keyboardvariant_cursor_changed)

                # Clear our model
                liststore = self.variant_treeview.get_model()
                liststore.clear()

                # Add keyboard variants (if any, sorted)
                for description in sorted_variant_descriptions:
                    liststore.append([description])

                self.variant_treeview.set_cursor(0)
                # Unblock signal
                self.variant_treeview.handler_unblock_by_func(self.on_keyboardvariant_cursor_changed)


    def on_keyboardlayout_cursor_changed(self, widget):
        logging.warning("*on_keyboardlayout_cursor_changed*")
        self.fill_variant_treeview()
        self.forward_button.set_sensitive(True)

    def on_keyboardvariant_cursor_changed(self, widget):
        logging.warning("*on_keyboardvariant_cursor_changed*")
        self.store_values()
        self.set_keyboard_widget()

    def store_values(self):
        logging.warning("*store_values*")
        if self.keyboard_layout['description'] is None:
            # We have not previously stored our layout
            return

        self.keyboard_variant  = { 'code': None, 'description': None }

        selected = self.variant_treeview.get_selection()
        if selected:
            (ls, iterator) = selected.get_selected()
            if iterator:
                variant_description = ls.get_value(iterator, 0)
                self.keyboard_variant['description'] = variant_description
                self.keyboard_variant['code'] = self.kbd_names.get_variant_name_by_description(variant_description)

        # This fixes issue 75: Won't pick/load the keyboard layout after selecting one (sticks to qwerty)
        if not self.testing and self.prepare_called:
            self.settings.set("keyboard_layout", self.keyboard_layout['code'])
            self.settings.set("keyboard_variant", self.keyboard_variant['code'])

            if self.keyboard_variant['code'] is None:
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
            self.set_keymap()

        return True

    def set_keymap(self):
        logging.warning("*set_keymap*")
        if self.keyboard_layout['code']:
            cmd = ['setxkbmap', '-layout', self.keyboard_layout['code']]

            if self.keyboard_variant['code']:
                cmd.extend(["-variant", self.keyboard_variant['code']])

            try:
                subprocess.check_call(cmd)
            except subprocess.CalledProcessError as process_error:
                logging.warning(process_error)

    def set_keyboard_widget(self):
        logging.warning("*set_keyboard_widget*")
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
