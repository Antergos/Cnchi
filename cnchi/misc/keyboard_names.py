#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
#  Copyright (C) 2012 Canonical Ltd.
#  Written by Colin Watson <cjwatson@ubuntu.com>.
#  Copyright © 2013-2015 Antergos
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
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

""" Parse base.xml """

import logging
import os

from collections import defaultdict

try:
    import xml.etree.cElementTree as eTree
except ImportError as err:
    import xml.etree.ElementTree as eTree

class KeyboardNames():
    def __init__(self, filename):
        self._filename = filename
        self._load_file()

    def _clear(self):
        self.models = {}
        self.layouts = {}
        self.variants = defaultdict(dict)

    def _load_file(self):
        if not os.path.exists(self._filename):
            logging.error(_("Can't find %s"), self._filename)
            return

        self._clear()

        xml_tree = eTree.parse(self._filename)
        xml_root = xml_tree.getroot()

        for model in xml_root.iter('model'):
            for config_item in model.iter('configItem'):
                for item in config_item:
                    if item.tag == "name":
                        model_name = item.text
                    elif item.tag == "description":
                        model_description = item.text
                    elif item.tag == "vendor":
                        model_vendor = item.text
                # Store model
                self.models[model_name] = (model_description, model_vendor)

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
                    self.layouts[layout_name] = (
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
                            self.variants[layout_name][variant_name] = (
                                variant_name,
                                variant_short_description,
                                variant_description,
                                variant_language_list)

    def get_layout(self, name):
        if name in self.layouts:
            return self.layouts[name]
        else:
            return None

    def get_layouts(self):
        return self.layouts

    def get_layout_by_description(self, description):
        for layout_name in self.layouts:
            if description == self.get_layout_description(layout_name):
                return self.layouts[layout_name]
        return None

    def get_layout_name_by_description(self, description):
        layout = self.get_layout_by_description(description)
        if layout:
            return layout[0]
        else:
            return None

    def get_layout_description(self, name):
        if name in self.layouts:
            return self.layouts[name][2]
        else:
            return None

    def has_variants(self, name):
        return bool(self.variants[name])

    def get_variants(self, name):
        return self.variants[name]

    def get_variant_description(self, name, variant_name):
        try:
            return self.variants[name][variant_name][2]
        except KeyError as key_error:
            return None

    def get_variant_descriptions(self, name):
        descriptions = []
        for variant_name in self.variants[name]:
            description = self.get_variant_description(name, variant_name)
            descriptions.append(description)
        return descriptions

    def get_variant_name_by_description(self, description):
        for layout_name in self.variants:
            for variant_name in self.variants[layout_name]:
                if description == self.get_variant_description(layout_name, variant_name):
                    return variant_name
        return None

'''
    """
    layout: layout_code : layout_name
    variant: variant_code : variant_name
    """

    def get_layouts(self, lang):
        self.load(lang)
        return self.layouts

    def get_variants(self, lang, layout_code):
        self.load(lang)
        try:
            return self.variants[layout_code]
        except KeyError:
            return None

    def has_language(self, lang):
        self.load(lang)
        return bool(self.layouts)

    def has_variants(self, lang, layout_code):
        self.load(lang)
        return bool(self.variants[layout_code])

    def has_layout(self, lang, layout_code):
        self.load(lang)
        return layout_code in self.layouts

    def get_layout_code(self, lang, layout_name):
        """ Returns layout code from layout name """
        self.load(lang)
        for code in self.layouts:
            if self.layouts[code] == layout_name:
                return code
        return None

    def get_layout_name(self, lang, code):
        """ Returns layout name from layout code """
        self.load(lang)
        try:
            return self.layouts[code]
        except KeyError:
            return None

    def get_variant_code(self, lang, layout_code, variant_name):
        """ Returns variant code from layout and variant names """
        self.load(lang)
        for variant_code in self.variants[layout_code]:
            if self.variants[layout_code][variant_code] == variant_name:
                return variant_code
        return None

    def get_variant_name(self, lang, layout_code, variant_code):
        """ Returns variant description from variant code """
        self.load(lang)
        try:
            return self.variants[layout_code][variant_code]
        except KeyError:
            return None
'''
