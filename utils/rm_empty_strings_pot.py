#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  poodle.py
#
#  Copyright © 2015 Antergos
#
#  This file is part of Antergos Package Assistant, (Poodle).
#
#  Poodle is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  Poodle is distributed in the hope that it will be useful,
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

import re
import info

version_string = '"Project-Id-Version: CNCHI ' + info.CNCHI_VERSION + '\\\\n"'
first = True


def handle_match(match):
    global first
    if first:
        first = False
        return match.group(0)

    return ''


if __name__ == '__main__':
    with open('/tmp/cnchi_py.pot', 'r') as pot_file:
        contents = pot_file.read()
        cleaned = re.sub(r'msgid ""\nmsgstr ""', handle_match, contents)
        cleaned = re.sub(r'"Project-Id-Version: PACKAGE VERSION\\\\n"', version_string, cleaned)
    with open('/tmp/cnchi_py.pot', 'w') as cleaned_file:
        cleaned_file.write(cleaned)
