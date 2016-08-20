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

# Standard Lib
from _base_object import (
    os
)

# 3rd-party Libs
# from _base_object import ()

# This application
from ui.base_widgets import (
    bg_thread,
    BaseWidget,
    SharedData,
    Singleton,
)

from .pages import ALL_PAGES


class PagesHelper(BaseWidget, metaclass=Singleton):
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

    def __init__(self, name='pages_helper', *args, **kwargs):
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

            self.page_names = self.get_page_names()

        self.logger.debug([self.PAGES_DIR, self.page_names])

    def _find_page_directories(self):
        if not self._page_dirs:
            excluded = ['__', '.', '00']
            _dirs = os.listdir(os.path.join(self.UI_DIR, 'html/pages'))
            _dirs.sort()
            _page_dirs = [
                d for d in _dirs
                if '_' in d and not [x for x in excluded if x in d]
            ]
            self._page_dirs.extend(_page_dirs)

    def _get_page_index(self, name):
        # res = [n[1:2] for n in self._page_dirs if name in n]
        res = self.page_names.index(name)
        return '' if not res else str(res + 1)

    def _get_page_object_by_index(self, index):
        if index > len(self.page_names):
            raise IndexError

        name = self.page_names[index]

        return self._get_page_object_by_name(name)

    def _get_page_object_by_name(self, name):
        if name not in self.all_pages:
            index = self._get_page_index(name).zfill(2)
            self._load_page(name, index)

        return self.all_pages[name]

    def _load_page(self, name, index):
        page_class = getattr(ALL_PAGES, name)
        self.all_pages[name] = page_class(name=name, index=index)

    def get_page(self, identifier):
        page = None

        try:
            page = self.get_page_object(identifier)
        except Exception as err:
            self.logger.exception(err)

        return page

    def get_page_directory_name(self, name):
        res = [d for d in self._page_dirs if name in d]

        return '' if not res else res[0]

    def get_page_names(self):
        return [n[4:].replace('_', ' ') for n in self._page_dirs]

    def get_page_object(self, page_identifier):
        """ Get a page object by name or by index """

        if isinstance(page_identifier, int):
            _page = self._get_page_object_by_index(page_identifier)
        elif isinstance(page_identifier, str):
            _page = self._get_page_object_by_name(page_identifier)
        else:
            raise ValueError(
                '"page_identifier" must be of type(int) or type(str), %s given.', type(page_identifier)
            )

        return _page
