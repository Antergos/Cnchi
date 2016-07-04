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
import json
import logging

from ui.base_widgets import BaseWidget, DataObject, Singleton, Gio, Gtk, WebKit2

from .pages import *


class MainContainer(BaseWidget, metaclass=Singleton):
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
            self._connect_signals_to_callbacks()

    def _apply_webkit_settings(self):
        self._wv_parts.settings = WebKit2.Settings()
        all_settings = self._get_settings_for_webkit()

        for setting_name, value in all_settings.items():
            setting_name = 'set_{}'.format(setting_name)
            set_setting = getattr(self._wv_parts.settings, setting_name)

            set_setting(value)

    def _connect_signals_to_callbacks(self):
        # register signals
        # self._web_view.connect('decide-policy', self.decide_policy_cb)
        self._web_view.connect('load-changed', self.load_changed_cb)
        self._web_view.connect('notify::title', self.title_changed_cb)

        # register custom uri scheme cnchi://
        self._wv_parts.context.register_uri_scheme('cnchi', self.uri_resource_cb)
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

    def decide_policy_cb(self, view, decision, decision_type):
        if decision_type == WebKit2.PolicyDecisionType.NAVIGATION_ACTION:
            # grab the requested URI
            uri = decision.get_request().get_uri()
            logging.debug(uri)

    def load_changed_cb(self, view, event):
        self.logger.debug('load_changed fired!')

    def title_changed_cb(self, view, event):
        incoming = view.get_title()

        # check for "_BR::" prefix to determine we're crossing the python/JS bridge
        if not incoming or not incoming.startswith('_BR::'):
            return

        try:
            incoming = json.loads(incoming[5:])

            name = incoming.setdefault('name', '')
            args = incoming.setdefault('args', [])

            # emit our python/js bridge signal
            self._main_window.emit('on-js', name, args)

        except Exception as err:
            logging.exception(err)

    def uri_resource_cb(self, request):
        path = request.get_uri()

        if '?' in path:
            path, query = path.split('?')

        page = path.replace('cnchi://', '') if 'cnchi:///' != path else 'language'

        if '.' in path:
            self.logger.debug('Loading app resource: {0}'.format(path))
            path = page

            if path.startswith(self.APP_DIR) and os.path.exists(path):
                request.finish(
                    Gio.File.new_for_path(path).read(None), -1,
                    Gio.content_type_guess(path, None)[0]
                )

        elif page in self._pages_helper.page_names:
            self.logger.debug('Loading app page: {0}'.format(page))
            page_obj = self._pages_helper.get_page(page)
            data = page_obj.render_template_as_bytes()

            request.finish(
                Gio.MemoryInputStream.new_from_data(data), -1,
                Gio.content_type_guess(None, data)[0]
            )

        else:
            raise Exception('App resource path not found: {0}'.format(path))
