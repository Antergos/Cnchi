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

from ui.base_widgets import BaseWidget, DataObject, Gtk, WebKit2

from .pages import *


class MainContainer(BaseWidget):
    """
    Main entry-point for HTML Pages UI.

    Class Attributes:
        Also see `BaseWidget.__doc__`

    """

    def __init__(self, name='main_container', *args, **kwargs):
        """
        Attributes:
            Also see `BaseWidget.__doc__`.

        Args:
            name (str): A name for this widget.

        """

        super().__init__(name=name, *args, **kwargs)

        if self._web_view is None:
            self._wv_parts = DataObject()

            self._initialize_web_view()
            self.widget.add(self._web_view)

        self.widget.show_all()

    def _apply_webkit_settings(self):
        self._wv_parts.settings = WebKit2.Settings()
        all_settings = self._get_settings_for_webkit()

        for setting_name, value in all_settings.items():
            setting_name = 'set_{}'.format(setting_name)
            set_setting = getattr(self._wv_parts.settings, setting_name)

            set_setting(value)

    def _connect_signals_to_callbacks(self):
        # register signals
        self._web_view.connect('decide-policy', self._controller.decide_policy_cb)
        self._web_view.connect('load-changed', self._controller.load_changed_cb)
        self._web_view.connect('notify::title', self._controller.title_changed_cb)

        # register custom uri scheme cnchi://
        self._wv_parts.context.register_uri_scheme('cnchi', self._controller.uri_resource_cb)
        self._wv_parts.security_manager.register_uri_scheme_as_cors_enabled('cnchi')

    @staticmethod
    def _get_settings_for_webkit():
        return {
            'enable_developer_extras': True,
            'javascript_can_open_windows_automatically': True,
            'allow_file_access_from_file_urls': True,
            'enable_write_console_messages_to_stdout': True,
        }

    def _initialize_web_view(self):
        self._wv_parts.content_mgr = WebKit2.UserContentManager()
        self._wv_parts.context = WebKit2.WebContext.get_default()
        self._wv_parts.security_manager = self._wv_parts.context.get_security_manager()

        self._apply_webkit_settings()

        self._web_view = WebKit2.WebView.new_with_user_content_manager(self._wv_parts.content_mgr)

        self._web_view.set_settings(self._wv_parts.settings)
        self._web_view.show_all()
