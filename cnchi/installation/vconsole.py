#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  vconsole.py
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

import logging
import os

# The keyboard layout for Great Britain is "uk" in the cli and
# "gb" (not uk) in X, just to make things more complicated.
# Also "ca" (Canada) works as "us"
match = {
    "ca": "us",
    "gb": "uk",
    "latam": "la-latin1"
}

class VConsole(object):
    """ Keyboard configuration in console
        https://wiki.archlinux.org/index.php/Keyboard_configuration_in_console """

    def __init__(self, keyboard_layout):
        self.keyboard_layout = keyboard_layout

    def get_keymap(self):
        # Get keyboard layout - console keymap equivalence. If it does
        # not exist it will use the keyboard layout as default value
        return match.get(self.keyboard_layout, self.keyboard_layout)

    def save(self, dest_dir="/install"):
        """ Stores console configuration in vconsole.conf """

        vconsole = self.get_keymap()

        # Write vconsole.conf
        vconsole_path = os.path.join(dest_dir, "etc/vconsole.conf")
        with open(vconsole_path, 'w') as vconsole_file:
            vconsole_file.write("# File modified by Cnchi\n\n")
            vconsole_file.write("KEYMAP={0}\n".format(vconsole))
        logging.debug("Set vconsole to %s", vconsole)

if __name__ == '__main__':
    vc = VConsole("es")
    print(vc.get_keymap())
