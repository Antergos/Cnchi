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
from misc.run_cmd import call

from ._base_module import CnchiModule


class KeymapModule(CnchiModule):
    """
    Utility class for handling keymap selection and application.

    Attributes:
        name (str): a name for this object.
    """

    def __init__(self, name='_keymap', *args, **kwargs):
        super().__init__(name=name, *args, *kwargs)

        self.keyboard_layout = self.keyboard_variant = self.kbd_names = None

        self.base_xml_path = os.path.join(self.TOP_DIR, 'data', 'base.xml')

    @staticmethod
    def _reset():
        data = {'code': None, 'description': None}
        return data, data

    def initialize(self):
        self.kbd_names = keyboard_names.KeyboardNames(self.base_xml_path)
        country_code = self.settings.country_code
        description = self.kbd_names.get_layout_description(country_code)

        self.keyboard_layout, self.keyboard_variant = self._reset()
        self.keyboard_layout['code'] = country_code

        if description:
            self.keyboard_layout['description'] = description
            # specific variant cases
            country_name = self.settings.country_name
            language_name = self.settings.language_name

            # if country_name == "Spain" and language_name == "Catalan":
            #     self.keyboard_variant['code'] = "cat"
            #     variant_desc = self.kbd_names.get_variant_description(
            #         country_code,
            #         "cat")
            #     self.keyboard_variant['description'] = variant_desc
            # elif country_name == "Canada" and language_name == "English":
            #     self.keyboard_variant['code'] = "eng"
            #     variant_desc = self.kbd_names.get_variant_description(
            #         country_code,
            #         "eng")
            #     self.keyboard_variant['description'] = variant_desc

            # Immediately set new keymap
            # (this way entry widget will work as it should)

    def get_keyboard_layouts_list(self):
        layouts = self.kbd_names.get_layouts()
        self.logger.debug(layouts)
        return [
            {
                'id': layout_name,
                'name': str(layouts[layout_name]),
                'variants': [
                    {
                        'id': layouts[layout_name].variants[variant].name,
                        'name': str(layouts[layout_name].variants[variant])
                    }
                    for variant in layouts[layout_name].variants
                ]
             }
            for layout_name in layouts
        ]

    def set_keymap(self, layout, variant=None):
        self.settings.keyboard_layout = layout
        self.settings.keyboard_variant = variant

        # setxkbmap sets the keyboard layout for the current X session only
        cmd = ['setxkbmap', '-layout', layout]

        if variant:
            cmd.extend(['-variant', variant])
            txt = 'Set keyboard to "{0}" ({1}), variant "{2}" ({3})'
            txt = txt.format('', layout, '', variant)
        else:
            txt = 'Set keyboard to "{0}" ({1})'.format('', layout)

        try:
            call(cmd)
            self.logger.debug(txt)
        except (OSError, subprocess.CalledProcessError) as setxkbmap_error:
            self.logger.warning(setxkbmap_error)


# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

if __name__ == '__main__':
    from test_screen import _, run

    run('Keymap')
