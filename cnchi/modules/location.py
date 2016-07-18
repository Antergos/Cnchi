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

from ._base_module import BaseModule
from _base_object import Gtk


class LocationModule(BaseModule):
    """
    Utility module for the location page.

    Class Attributes:
        See Also `BaseModule.__doc__`

    """

    def __init__(self, name='_location', *args, **kwargs):
        """
        Attributes:
            name (str): A name for this object (all objects must have unique name).
            See Also: `BaseModule.__doc__`

        """

        super().__init__(name=name, *args, **kwargs)

        self.locales = {}

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
            locale_name: '{0}, {1}'.format(self.locales[locale_name], countries[country_code])
            for country_code in countries
            for locale_name in self.locales
            if country_code in self.locales[locale_name]
        }

        self.locales = locales

    def load_locales(self):
        self._load_locale_codes_and_language_names()
        self._load_country_codes()



