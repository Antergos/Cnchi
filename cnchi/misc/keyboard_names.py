#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
#  Copyright (C) 2012 Canonical Ltd.
#  Written by Colin Watson <cjwatson@ubuntu.com>.
#  Copyright © 2013-2015 Antergos
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

""" Parse base.xml """

import logging
import os
from gi.repository import GObject
from collections import OrderedDict

try:
    import xml.etree.cElementTree as eTree
except ImportError as err:
    import xml.etree.ElementTree as eTree


class Model(GObject.GObject):
    def __init__(self, name, description, vendor):
        GObject.GObject.__init__(self)
        self.name = name
        self.description = description
        self.vendor = vendor

    def __repr__(self):
        return self.description


class Variant(GObject.GObject):
    def __init__(self, name, short_description, description, language_list):
        GObject.GObject.__init__(self)
        self.name = name
        self.short_description = short_description
        self.description = description
        self.language_list = language_list

    def __repr__(self):
        return self.description


class Layout(GObject.GObject):
    def __init__(self, name, short_description, description, language_list):
        GObject.GObject.__init__(self)
        self.name = name
        self.short_description = short_description
        self.description = description
        self.language_list = language_list
        self.variants = {}

    def __repr__(self):
        return self.description

    def add_variant(self, variant):
        self.variants[variant.name] = variant

    def sort_variants(self):
        self.variants = OrderedDict(sorted(self.variants.items(), key=lambda t: str(t[1])))


class KeyboardNames(object):
    def __init__(self, filename):
        self.layouts = None
        self._filename = filename
        self._load_file()

    def _clear(self):
        self.models = {}
        self.layouts = {}

    def _load_file(self):
        if not os.path.exists(self._filename):
            logging.error("Can't find %s file!", self._filename)
            return

        self._clear()

        xml_tree = eTree.parse(self._filename)
        xml_root = xml_tree.getroot()

        for model in xml_root.iter('model'):
            for config_item in model.iter('configItem'):
                model_name = ""
                model_description = ""
                model_vendor = ""
                for item in config_item:
                    if item.tag == "name":
                        model_name = item.text
                    elif item.tag == "description":
                        model_description = item.text
                    elif item.tag == "vendor":
                        model_vendor = item.text
                # Store model
                self.models[model_name] = Model(
                    model_name,
                    model_description,
                    model_vendor)

        for layout in xml_root.iter('layout'):
            for layout_item in layout:
                layout_language_list = []
                if layout_item.tag == "configItem":
                    for item in layout_item:
                        if item.tag == "name":
                            layout_name = item.text
                        elif item.tag == "shortDescription":
                            layout_short_description = item.text
                        elif item.tag == "description":
                            layout_description = item.text
                        elif item.tag == "languageList":
                            for lang in item:
                                layout_language_list.append(lang.text)
                    self.layouts[layout_name] = Layout(
                        layout_name,
                        layout_short_description,
                        layout_description,
                        layout_language_list)

                if layout_item.tag == "variantList":
                    for variant in layout_item:
                        variant_language_list = []
                        for config_item in variant:
                            for item in config_item:
                                if item.tag == "name":
                                    variant_name = item.text
                                elif item.tag == "shortDescription":
                                    variant_short_description = item.text
                                elif item.tag == "description":
                                    variant_description = item.text
                                elif item.tag == "languageList":
                                    for lang in item:
                                        variant_language_list.append(lang.text)

                            self.layouts[layout_name].add_variant(
                                Variant(
                                    variant_name,
                                    variant_short_description,
                                    variant_description,
                                    variant_language_list))

        self.sort_layouts()

    def sort_layouts(self):
        self.layouts = OrderedDict(sorted(self.layouts.items(), key=lambda t: str(t[1])))
        for name in self.layouts:
            self.layouts[name].sort_variants()

    def get_layout(self, name):
        if name in self.layouts:
            return self.layouts[name]
        else:
            return None

    def get_layouts(self):
        return self.layouts

    def get_layout_description(self, name):
        if name in self.layouts:
            return str(self.layouts[name])
        else:
            return None

    def get_layout_by_description(self, description):
        for name in self.layouts:
            if description == str(self.layouts[name]):
                return self.layouts[name]
        return None

    def get_layout_name_by_description(self, description):
        for name in self.layouts:
            if description == str(self.layouts[name]):
                return name
        return None

    def has_variants(self, name):
        return bool(self.layouts[name].variants)

    def get_variants(self, name):
        return self.layouts[name].variants

    def get_variant_description(self, name, variant_name):
        try:
            return str(self.layouts[name].variants[variant_name])
        except KeyError as key_error:
            return None

    def get_variant_descriptions(self, name):
        descriptions = []
        for variant_name in self.layouts[name].variants:
            description = str(self.layouts[name].variants[variant_name])
            descriptions.append(description)
        return descriptions

    def get_variant_name_by_description(self, description):
        for layout_name in self.layouts:
            for variant_name in self.layouts[layout_name].variants:
                if description == str(self.layouts[layout_name].variants[variant_name]):
                    return variant_name
        return None


if __name__ == '__main__':
    base_xml_path = "/usr/share/cnchi/data/base.xml"
    kbd_names = KeyboardNames(base_xml_path)

    layouts = kbd_names.get_layouts()
    for name in layouts:
        print(name, layouts[name])
        for variant_name in layouts[name].variants:
            print(layouts[name], "-", layouts[name].variants[variant_name])
