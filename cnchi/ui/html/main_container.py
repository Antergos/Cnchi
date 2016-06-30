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

from ui.base_widgets import Box, gi

from .pages import *

gi.require_version('WebKit2', '4.0')
from gi.repository import WebKit2


class MainContainer(Box):
    """
    Main entry-point for HTML Pages UI.

    Class Attributes:
        all_pages (list):            List of initialized pages for the UI.
        web_view  (WebKit2.WebView): Object that renders the app's HTML UI.
        Also see `Box.__doc__`

    """

    PAGES_DIR = None
    all_pages = None
    page_names = None
    web_view = None

    def __init__(self, name='main_container', controller=None,  *args, **kwargs):
        """
        Attributes:
            Also see `Box.__doc__`.

        Args:
            name (str): A name for this widget.

        """

        super().__init__(name=name, *args, **kwargs)

        if self.PAGES_DIR is None:
            self.PAGES_DIR = os.path.join(self.UI_DIR, 'html/pages')

        if self.all_pages is None:
            self.all_pages = dict()
            self.page_names = []

            self.page_names.extend(self._get_page_names())

        if self.controller is None:
            self.controller = controller

        if self.web_view is None:
            self._initialize_web_view()

    def _get_page_by_index(self, index):
        if index > len(self.page_names):
            raise IndexError

        name = self.page_names[index]

        return self._get_page_by_name(name)

    def _get_page_by_name(self, name):
        if name not in self.all_pages:
            self._load_page(name)

        return self.all_pages[name]

    def _get_page_names(self):
        return [n.rstrip('.py') for n in os.listdir(self.PAGES_DIR) if not n.startswith('_')]

    @staticmethod
    def _get_settings_for_webkit():
        return {
            'enable_developer_extras': True,
            'javascript_can_open_windows_automatically': True,
            'allow_file_access_from_file_urls': True,
            'enable_write_console_messages_to_stdout': True,
        }

    def _get_webkit_settings(self):
        webkit_settings = WebKit2.Settings()
        all_settings = self._get_settings_for_webkit()

        for setting_name, value in all_settings.items():
            setting_name = 'set_{}'.format(setting_name)
            set_setting = getattr(webkit_settings, setting_name)

            set_setting(value)

        return webkit_settings

    def _initialize_web_view(self):
        context = WebKit2.WebContext.get_default()
        security_manager = context.get_security_manager()
        webkit_settings = self._get_webkit_settings()
        self.web_view = WebKit2.WebView.new_with_settings(webkit_settings)

        # register signals
        self.web_view.connect('decide-policy', self.controller.decide_policy_cb)
        self.web_view.connect('load-changed', self.controller.load_changed_cb)
        self.web_view.connect('notify::title', self.controller.title_changed_cb)

        # register custom uri scheme cnchi://
        context.register_uri_scheme('cnchi', self.controller.uri_resource_cb)
        security_manager.register_uri_scheme_as_cors_enabled('cnchi')

    def _load_page(self, name):
        page_class_name = '{}Page'.format(name.capitalize())
        page_class = __dict__[page_class_name]
        self.all_pages[page_class_name] = page_class(name=name, web_view=self.web_view)

    def get_page(self, page):
        """ Get a page by name or by index """
        if isinstance(page, int):
            _page = self._get_page_by_index(page)
        elif isinstance(page, str):
            _page = self._get_page_by_name(page)
        else:
            raise ValueError(
                '"page" to load must be of type(int) or type(str), %s given.', type(page)
            )

        return _page
