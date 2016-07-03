#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  main_container.py
#
#  Copyright © 2016 Antergos
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
import logging

from ui.base_widgets import BaseWidget, SharedData

from .pages import *


class Pages(BaseWidget):
    """
    Manages the UI's pages.

    Class Attributes:
        all_pages  (dict): Dict of initialized page objects for the UI.
        page_names (list): List of all page names that are available.
        Also see `BaseObject.__doc__`

    """

    PAGES_DIR = SharedData('PAGES_DIR')
    all_pages = SharedData('all_pages')
    page_names = SharedData('page_names')

    def __init__(self, name='pages', *args, **kwargs):
        """
        Attributes:
            Also see `BaseWidget.__doc__`.

        Args:
            name (str): A name for this widget.

        """

        super().__init__(name=name, *args, **kwargs)

        if self.PAGES_DIR is None:
            self.PAGES_DIR = os.path.join(self.UI_DIR, 'html/pages')

        if self.all_pages is None:
            self.all_pages = dict()

            self._find_page_directories()

            self.page_names = self._get_page_names()

    def _find_page_directories(self):
        if not self._page_dirs:
            self._page_dirs.extend(os.listdir(os.path.join(self.UI_DIR, 'html/pages')))

    def _get_page_names(self):
        return [n.split('-', 1)[1] for n in self._page_dirs if '_' not in n]

    def _get_page_object_by_index(self, index):
        if index > len(self.page_names):
            raise IndexError

        name = self.page_names[index]

        return self._get_page_object_by_name(name)

    def _get_page_object_by_name(self, name):
        if name not in self.all_pages:
            self._load_page(name)

        return self.all_pages[name]

    def _load_page(self, name):
        page_class_name = '{}Page'.format(name.capitalize())
        page_class = __dict__[page_class_name]
        self.all_pages[page_class_name] = page_class(name=name, web_view=self._web_view)

    def get_page_directory_name(self, name=None):
        name = name if name is not None else self.name

        res = [d for d in self._page_dirs if '-{}'.format(name) in d]

        return '' if not res else res[0]

    def get_page_object(self, page_identifier):
        """ Get a page_identifier object by name or by index """
        if isinstance(page_identifier, int):
            _page = self._get_page_object_by_index(page_identifier)
        elif isinstance(page_identifier, str):
            _page = self._get_page_object_by_name(page_identifier)
        else:
            raise ValueError(
                '"page_identifier" must be of type(int) or type(str), %s given.', type(page_identifier)
            )

        return _page
