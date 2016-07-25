#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# keymap.py
#
# Copyright © 2013-2016 Antergos
#
# This file is part of Cnchi.
#
# Cnchi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Cnchi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# The following additional terms are in effect as per Section 7 of the license:
#
# The preservation of all legal notices and author attributions in
# the material or in the Appropriate Legal Notices displayed
# by works containing it is required.
#
# You should have received a copy of the GNU General Public License
# along with Cnchi; If not, see <http://www.gnu.org/licenses/>.

import os
import subprocess

import misc.keyboard_names as keyboard_names

from ._base_module import BaseModule


class Keymap(BaseModule):
    """ Keymap screen """

    def __init__(self, name='_keymap', *args, **kwargs):

        super().__init__(name=name, *args, *kwargs)

        self.prepared = False
        self.keyboard_layout = {'code': None, 'description': None}
        self.keyboard_variant = {'code': None, 'description': None}

        base_xml_path = os.path.join(self.TOP_DIR, 'data', 'base.xml')
        self.kbd_names = keyboard_names.KeyboardNames(base_xml_path)

    def clear(self):
        """ Clears treeview model """
        self.keyboard_layout = {'code': None, 'description': None}
        self.keyboard_variant = {'code': None, 'description': None}

    def prepare(self, direction):
        """ Prepare screen """

        if self.keyboard_layout['code'] is None:
            country_code = self.settings.country_code
            self.clear()

            self.get_keyboard_layouts_list()

            self.keyboard_layout['code'] = country_code
            description = self.kbd_names.get_layout_description(country_code)
            if description:
                self.keyboard_layout['description'] = description

                # specific variant cases
                country_name = self.settings.get("country_name")
                language_name = self.settings.get("language_name")
                # language_code = self.settings.get("language_code")
                if country_name == "Spain" and language_name == "Catalan":
                    self.keyboard_variant['code'] = "cat"
                    variant_desc = self.kbd_names.get_variant_description(
                        country_code,
                        "cat")
                    self.keyboard_variant['description'] = variant_desc
                elif country_name == "Canada" and language_name == "English":
                    self.keyboard_variant['code'] = "eng"
                    variant_desc = self.kbd_names.get_variant_description(
                        country_code,
                        "eng")
                    self.keyboard_variant['description'] = variant_desc

                self.select_in_treeview(
                    self.keymap_treeview,
                    self.keyboard_layout['description'],
                    self.keyboard_variant['description'])

                # Immediately set new keymap
                # (this way entry widget will work as it should)
                self.set_keymap()
            else:
                logging.debug(
                    _("Can't match a keymap for country code '%s'"),
                    country_code)
                self.keyboard_layout = {'code': None, 'description': None}
                self.keyboard_variant = {'code': None, 'description': None}

        self.prepare_called = True
        self.show_all()

    def get_keyboard_layouts_list(self):
        layouts = self.kbd_names.get_layouts()
        layouts_list = [
            {str(layouts[layout_name]): [str(v) for v in layouts[layout_name].variants]}
            for layout_name in layouts
        ]

    def select_in_treeview(self, treeview, value0, value1=None):
        """ Simulates the selection of a value in the treeview """

        tree_model = treeview.get_model()
        tree_iter = tree_model.get_iter(0)
        found = False
        path = None

        while tree_iter and not found:
            if tree_model[tree_iter][0] == value0:
                path = tree_model.get_path(tree_iter)
                treeview.expand_row(path, False)
                found = True
            else:
                tree_iter = tree_model.iter_next(tree_iter)

        if not found:
            logging.warning("Cannot find value '%s' in treeview", value0)
            return

        if value1 and tree_iter and tree_model.iter_has_child(tree_iter):
            found = False
            tree_iter = tree_model.get_iter(path)
            child_iter = tree_model.iter_children(tree_iter)
            while child_iter and not found:
                if str(tree_model[child_iter][0]) == str(value1):
                    path = tree_model.get_path(child_iter)
                    found = True
                else:
                    child_iter = tree_model.iter_next(child_iter)
            if not found:
                logging.warning("Cannot find value '%s' in treeview", value1)

        if path:
            treeview.set_cursor(path)
            # Simulate row activation
            self.on_keymap_row_activated(self.keymap_treeview, tree_iter, path)
            GLib.idle_add(self.scroll_to_cell, treeview, path)

    @staticmethod
    def scroll_to_cell(treeview, path):
        """ Move scroll in treeview """
        treeview.scroll_to_cell(path)
        return False

    @staticmethod
    def get_selected_in_treeview(treeview):
        """ Gets selected value in treeview """
        layout = None
        variant = None
        tree_model = treeview.get_model()
        selected = treeview.get_selection()
        if selected:
            (ls, iterator) = selected.get_selected()
            if iterator:
                layout = ls.get_value(iterator, 0)
                iter_parent = tree_model.iter_parent(iterator)
                if iter_parent:
                    # A variant was selected
                    variant = layout
                    layout = tree_model[iter_parent][0]

        if not layout:
            # Set English as default keyboard layout if none selected
            logging.warning("Setting English (US) keyboard layout as none was selected")
            layout = "English (US)"
        return layout, variant

    def on_keymap_row_activated(self, treeview, iterator, path):
        """ Set selected keymap """
        self.forward_button.set_sensitive(True)
        self.store_values()
        self.set_keyboard_widget_keymap()


    def store_values(self):
        """ Store selected values """

        self.keyboard_layout = {'code': None, 'description': None}
        self.keyboard_variant = {'code': None, 'description': None}

        # Read selected value from treeview
        (layout_description, variant_description) = self.get_selected_in_treeview(self.keymap_treeview)

        if not layout_description:
            logging.debug("Layout description not selected")
            return False

        layout_name = self.kbd_names.get_layout_name_by_description(layout_description)

        if not layout_name:
            logging.warning("Unknown layout description: %s", layout_description)
            return False

        self.keyboard_layout['code'] = layout_name
        self.keyboard_layout['description'] = layout_description

        if variant_description:
            variant_name = self.kbd_names.get_variant_name_by_description(variant_description)
            if variant_name:
                self.keyboard_variant['code'] = variant_name
                self.keyboard_variant['description'] = variant_description
            else:
                logging.warning("Unknown variant description: %s", variant_description)

        if self.prepare_called:
            self.set_keymap()

        return True

    def set_keymap(self):
        """ Uses selected keymap """
        if self.keyboard_layout['code']:
            self.settings.set("keyboard_layout", self.keyboard_layout['code'])
            self.settings.set("keyboard_variant", self.keyboard_variant['code'])

            # setxkbmap sets the keyboard layout for the current X session only
            cmd = ['setxkbmap', '-layout', self.keyboard_layout['code']]

            if self.keyboard_variant['code']:
                cmd.extend(["-variant", self.keyboard_variant['code']])
                txt = _("Set keyboard to '{0}' ({1}), variant '{2}' ({3})")
                txt = txt.format(
                    self.keyboard_layout['description'],
                    self.keyboard_layout['code'],
                    self.keyboard_variant['description'],
                    self.keyboard_variant['code'])
            else:
                txt = _("Set keyboard to '{0}' ({1})").format(
                    self.keyboard_layout['description'],
                    self.keyboard_layout['code'])

            try:
                subprocess.check_call(cmd)
                logging.debug(txt)
            except (OSError, subprocess.CalledProcessError) as setxkbmap_error:
                logging.warning(setxkbmap_error)

    def set_keyboard_widget_keymap(self):
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
