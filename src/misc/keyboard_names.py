#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# keyboard_names.py
#
# Copyright © 2013-2018 Antergos
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

""" Parse base.xml that contains keyboards info """

import logging
import os
from collections import OrderedDict

from gi.repository import GObject


try:
    import xml.etree.cElementTree as eTree
except ImportError as err:
    import xml.etree.ElementTree as eTree


class Model(GObject.GObject):
    """ Represents a keyboard model """

    def __init__(self, name, description, vendor):
        GObject.GObject.__init__(self)
        self.name = name
        self.description = description
        self.vendor = vendor

    def __repr__(self):
        """ Return model description """
        return self.description


class Variant(GObject.GObject):
    """ Keymap variant layout """

    def __init__(self, name, short_description, description, language_list):
        GObject.GObject.__init__(self)
        self.name = name
        self.short_description = short_description
        self.description = description
        self.language_list = language_list

    def __repr__(self):
        """ Return variant description """
        return self.description


class Layout(GObject.GObject):
    """ Keymap layout """

    def __init__(self, name, short_description, description, language_list):
        GObject.GObject.__init__(self)
        self.name = name
        self.short_description = short_description
        self.description = description
        self.language_list = language_list
        self.variants = {}

    def __repr__(self):
        """ Return layout description """
        return self.description

    def add_variant(self, variant):
        """ Add new layout variant """
        self.variants[variant.name] = variant

    def sort_variants(self):
        """ Sort variants """
        self.variants = OrderedDict(
            sorted(self.variants.items(), key=lambda t: str(t[1])))


class KeyboardNames():
    """ Read all keyboard info (models, layouts and variants) """

    def __init__(self, filename):
        self.models = None
        self.layouts = None
        self._filename = filename
        self._load_xml()

    def _clear(self):
        """ Clear all data """
        self.models = {}
        self.layouts = {}

    def _load_models(self, xml_root):
        """ Load keyboard models from xml root node """
        for model_node in xml_root.iter('model'):
            for config_item in model_node.iter('configItem'):
                model = {'name': "", 'description': "", 'vendor': ""}
                for item in config_item:
                    model[item.tag] = item.text
                # Store model
                self.models[model['name']] = Model(
                    model['name'], model['description'], model['vendor'])

    def _load_layout_item(self, layout_item):
        """ Loads a layout item from xml and returns its name """
        layout = {
            'name': "", 'short_description': "", 'description': "", 'language_list': []}

        for item in layout_item:
            if item.tag == "languageList":
                for lang in item:
                    layout['language_list'].append(lang.text)
            else:
                layout[item.tag] = item.text

        self.layouts[layout['name']] = Layout(
            layout['name'], layout['short_description'],
            layout['description'], layout['language_list'])

        return layout['name']

    def _load_variant_item(self, layout_item, layout_name):
        """ Load a layout's variant item """
        for variant_node in layout_item:
            for config_item in variant_node:
                variant = {
                    'name': "", 'short_description': "",
                    'description': "", 'language_list': []}
                for item in config_item:
                    if item.tag == "languageList":
                        for lang in item:
                            variant['language_list'].append(
                                lang.text)
                    else:
                        variant[item.tag] = item.text

                self.layouts[layout_name].add_variant(
                    Variant(
                        variant['name'],
                        variant['short_description'],
                        variant['description'],
                        variant['language_list']))

    def _load_layouts(self, xml_root):
        """ Load keyboard layouts and variants from xml root node """
        for layout_node in xml_root.iter('layout'):
            for layout_item in layout_node:
                if layout_item.tag == "configItem":
                    layout_name = self._load_layout_item(layout_item)
                if layout_item.tag == "variantList":
                    self._load_variant_item(layout_item, layout_name)

    def _load_xml(self):
        """ Load info from xml file """
        if not os.path.exists(self._filename):
            logging.error("Can't find %s file!", self._filename)
            return

        self._clear()

        xml_tree = eTree.parse(self._filename)
        xml_root = xml_tree.getroot()

        self._load_models(xml_root)
        self._load_layouts(xml_root)
        self.sort_layouts()

    def sort_layouts(self):
        """ Sort stored layouts """
        self.layouts = OrderedDict(
            sorted(self.layouts.items(), key=lambda t: str(t[1])))
        for name in self.layouts:
            self.layouts[name].sort_variants()

    def get_layout(self, name):
        """ Get layout by its name """
        if name in self.layouts:
            return self.layouts[name]
        return None

    def get_layouts(self):
        """ Return all layouts """
        return self.layouts

    def get_layout_description(self, name):
        """ Get layout description by its name """
        if name in self.layouts:
            return str(self.layouts[name])
        return None

    def get_layout_by_description(self, description):
        """ Get layout by its description """
        for name in self.layouts:
            if description == str(self.layouts[name]):
                return self.layouts[name]
        return None

    def get_layout_name_by_description(self, description):
        """ Get layout name by its description """
        for name in self.layouts:
            if description == str(self.layouts[name]):
                return name
        return None

    def has_variants(self, name):
        """ Check if layout has variants """
        return bool(self.layouts[name].variants)

    def get_variants(self, name):
        """ Get layout variants """
        return self.layouts[name].variants

    def get_variant_description(self, name, variant_name):
        """ Get variant description by its name (and layout name)"""
        try:
            return str(self.layouts[name].variants[variant_name])
        except KeyError as _key_error:
            return None

    def get_variant_descriptions(self, name):
        """ Get all variant descriptions for layout 'name' """
        descriptions = []
        for variant_name in self.layouts[name].variants:
            description = str(self.layouts[name].variants[variant_name])
            descriptions.append(description)
        return descriptions

    def get_variant_name_by_description(self, description):
        """ Get variant name by its description """
        for layout_name in self.layouts:
            for variant_name in self.layouts[layout_name].variants:
                if description == str(self.layouts[layout_name].variants[variant_name]):
                    return variant_name
        return None


def test():
    """ Test module """
    base_xml_path = "/usr/share/cnchi/data/base.xml"
    kbd_names = KeyboardNames(base_xml_path)

    layouts = kbd_names.get_layouts()
    for name in layouts:
        print(name, layouts[name])
        for variant_name in layouts[name].variants:
            print(layouts[name], "-", layouts[name].variants[variant_name])


if __name__ == '__main__':
    test()
