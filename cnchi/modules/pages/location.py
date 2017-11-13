#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  location.py
#
#  Copyright © 2016 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  The following additional terms are in effect as per Section 7 of the license:
#
#  The preservation of all legal notices and author attributions in
#  the material or in the Appropriate Legal Notices displayed
#  by works containing it is required.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; If not, see <http://www.gnu.org/licenses/>.

import locale
import logging
import os
import re
import sys

import xml.etree.ElementTree as eTree

from modules._base_module import CnchiModule
from _cnchi_object import Gtk


class LocationModule(CnchiModule):
    """
    Utility module for the location page.

    Class Attributes:
        See Also `CnchiModule.__doc__`

    """

    def __init__(self, name='_location', *args, **kwargs):
        """
        Attributes:
            name (str): A name for this object (all objects must have unique name).
            See Also: `CnchiModule.__doc__`

        """

        super().__init__(name=name, *args, **kwargs)

        self.locales = {}
        self.locales_by_country = {}

        self.load_locales()

    def _load_locale_codes_and_language_names(self):
        xml_path = os.path.join(self.TOP_DIR, 'data', 'locale', 'locales.xml')

        try:
            tree = eTree.parse(xml_path)
        except FileNotFoundError as file_error:
            # TODO: Should be bubbling up a fatal error instead of calling sys.exit() here.
            self.logger.exception(file_error)
            sys.exit(1)

        root = tree.getroot()
        locale_name = ''
        language_name = ''
        for child in root.iter('language'):
            for item in child:
                language_name = item.text if 'language_name' == item.tag else language_name
                locale_name = item.text if 'locale_name' == item.tag else locale_name

            if locale_name and language_name:
                self.locales[locale_name] = language_name

    def _load_country_codes(self):
        xml_path = os.path.join(self.TOP_DIR, 'data', 'locale', 'iso3366-1.xml')

        try:
            tree = eTree.parse(xml_path)
        except FileNotFoundError as file_error:
            # TODO: Should be bubbling up a fatal error instead of calling sys.exit() here.
            self.logger.exception(file_error)
            sys.exit(1)

        root = tree.getroot()
        countries = {child.attrib['value']: child.text for child in root}
        locales = {
            l_name: dict(
                language=self.locales[l_name],
                country=countries[c_code],
                c_code=c_code,
                locale=l_name[:-6]
            )
            for c_code in countries
            for l_name in self.locales
            if '(' + c_code + ')' in self.locales[l_name]
        }

        by_country = {v['c_code']: [] for k, v in locales.items()}
        _ = [
            by_country[ldict['c_code']].append(ldict)
            for lname, ldict in locales.items()
        ]

        self.locales = locales
        self.locales_by_country = by_country

    def get_location_collection_items(self):
        areas = self.get_areas()
        country = self.settings.timezone_country
        top_items = []

        def _not_top_item(item):
            if country and [l for l in item if country == l['c_code']]:
                top_items.append(item)
                return False
            return True

        items = [a for a in areas if _not_top_item(a)]

        if top_items:
            items = top_items.extend(items)

        return items

    def get_areas(self):
        lang_code = self.settings.language_code
        show_all_locations = self.state.show_all_locations
        all_areas = self.locales_by_country
        self.logger.debug(all_areas)
        areas = [
            all_areas[c_code]
            for c_code in all_areas
            if show_all_locations or lang_code in [cdict['locale'] for cdict in all_areas[c_code]]
        ]

        if not areas:
            # When we don't find any country we put all language codes.
            areas = [all_areas[c_code] for c_code in all_areas]

        areas = sorted(areas, key=lambda l: l[0]['country'])

        return areas

    def load_locales(self):
        self._load_locale_codes_and_language_names()
        self._load_country_codes()



