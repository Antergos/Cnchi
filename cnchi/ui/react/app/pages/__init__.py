#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  __init__.py
#
#  Copyright ©  Antergos
#
#  This file is part of The Antergos Build Server, (AntBS).
#
#  AntBS is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  AntBS is distributed in the hope that it will be useful,
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
#  along with AntBS; If not, see <http://www.gnu.org/licenses/>.

import os
import importlib

__all__ = ['ALL_PAGES']


class AllPages:
    pass

ALL_PAGES = AllPages()
current_dir = os.path.dirname(__file__)

for page_dir in os.listdir(current_dir):
    if '_' in page_dir or not os.path.isdir(os.path.join(current_dir, page_dir)):
        continue

    page_name = '{}Page'.format(page_dir.split('-')[-1])
    import_path = '.react.app.pages.{}.{}'.format(page_dir, page_name)
    page_module = importlib.import_module(import_path, 'ui')

    setattr(ALL_PAGES, page_name, getattr(page_module, page_name))
