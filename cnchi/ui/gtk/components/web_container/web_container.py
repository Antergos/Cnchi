#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  container.py
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
import time

from _cnchi_object import (
    json,
    os
)

# 3rd-party Libs
from _cnchi_object import (
    Gdk,
    Gio,
    Gtk,
    WebKit2
)

# This Application
from ui.base_widgets import (
    CnchiWidget,
    DataObject,
    Singleton,
    bg_thread
)

WebContext = WebKit2.WebContext
WebsiteDataManager = WebKit2.WebsiteDataManager
WebView = WebKit2.WebView


class WebContainer(CnchiWidget, metaclass=Singleton):
    """
    Gtk web container for the React UI.

    Class Attributes:
        Also see `CnchiWidget.__doc__`

    """

    def __init__(self, name='main_container', *args, **kwargs):
        """
        Attributes:
            Also see `CnchiWidget.__doc__`.

        Args:
            name (str): A name for this widget.

        """

        super().__init__(name=name, tpl_engine=None, *args, **kwargs)

        self.cnchi_loaded = False

        if self._web_view is None:
            self._wv_parts = DataObject()

            self._initialize_web_view()
            self._set_background_color_for_web_view()
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
        self._wv_parts.context.register_uri_scheme('cnchi', self.uri_request_cb)
        self._wv_parts.security_manager.register_uri_scheme_as_cors_enabled('cnchi')

    @staticmethod
    def _get_page_name_from_uri(uri):
        if '?' in uri:
            uri = uri.split('?')[0]

        page = 'language'

        if 'cnchi:///' != uri:
            # Uri is in this format: cnchi://page_name.page
            page = uri[8:-5]

        return page

    @staticmethod
    def _get_settings_for_webkit():
        return {
            'enable_developer_extras': True,
            'javascript_can_open_windows_automatically': True,
            'allow_file_access_from_file_urls': True,
            'enable_write_console_messages_to_stdout': True,
            'allow_universal_access_from_file_urls': True
        }

    def _get_website_data_dirs(self):
        return {
            'base-data-directory': self.WK_DATA_DIR,
            'base-cache-directory': self.WK_CACHE_DIR
        }

    def _initialize_web_view(self):
        self._wv_parts.data_mgr = WebsiteDataManager(**self._get_website_data_dirs())
        self._wv_parts.context = WebContext.new_with_website_data_manager(self._wv_parts.data_mgr)

        self._wv_parts.security_manager = self._wv_parts.context.get_security_manager()
        self._wv_parts.security_manager.register_uri_scheme_as_local('cnchi://')
        self._wv_parts.security_manager.register_uri_scheme_as_cors_enabled('cnchi://')

        self._apply_webkit_settings()

        self._web_view = WebView.new_with_context(self._wv_parts.context)

        self._web_view.set_settings(self._wv_parts.settings)

    def _set_background_color_for_web_view(self, color='rgba(56, 58, 65, 0.5)'):
        _color = Gdk.RGBA()
        _color.parse(color)

        self._web_view.set_background_color(_color)
        self._set_up_style_provider()

    def _set_up_style_provider(self):
        style_provider = Gtk.CssProvider()
        bg_color = 'background-color: rgba(56, 58, 65, 0.5);'
        box_shadow = 'box-shadow: 0 1px 1px rgba(0, 0, 0, .04);'
        data = 'window, .main_window {{\n{0}\n{1}\n}}\n'.format(bg_color, box_shadow)

        style_provider.load_from_data(data.encode('utf-8'))

        self._main_window.widget.get_style_context().add_provider(
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    @bg_thread
    def _uri_request_finish_page(self, page, request):
        # page_obj = self._pages_helper.get_page(page)
        # page_obj.prepare()
        # data = page_obj.render_template_as_bytes()
        #
        # request.finish(
        #     Gio.MemoryInputStream.new_from_data(data), -1,
        #     Gio.content_type_guess(None, data)[0]
        # )
        tpl_path = os.path.join(self.UI_DIR, 'react/dist/index.html')
        self._cnchi_ui.current_page = page
        self._uri_request_finish_resource(tpl_path, request)

    @bg_thread
    def _uri_request_finish_resource(self, path, request):
        if path.startswith(self.APP_DIR) and os.path.exists(path):
            request.finish(
                Gio.File.new_for_path(path).read(None), -1,
                Gio.content_type_guess(path, None)[0]
            )

        elif path.startswith(self.APP_DIR):
            raise RuntimeError('Requested path: "{}" does not exist!'.format(path))

        elif os.path.exists(path):
            raise RuntimeError('Requested path: "{}" is not inside Cnchi directory!'.format(path))

    def decide_policy_cb(self, view, decision, decision_type):
        if decision_type == WebKit2.PolicyDecisionType.NAVIGATION_ACTION:
            # grab the requested URI
            uri = decision.get_request().get_uri()
            self.logger.debug(uri)

    def load_changed_cb(self, view, event):
        if WebKit2.LoadEvent.FINISHED != event:
            return

        page_name = self._get_page_name_from_uri(view.get_uri())

        self._controller.emit_js('trigger-event', 'page-loaded', page_name)

        if not self.cnchi_loaded:
            self.cnchi_loaded = True
            self._main_window.widget.set_opacity(1)

        self.logger.debug('load_changed fired! %s', page_name)

    def title_changed_cb(self, widget, event):
        incoming = widget.get_title()
        self.logger.debug('title changed!')

        # Check for "_BR::" prefix to determine if its a message from our JavaScript UI.
        if not incoming or not incoming.startswith('_BR::'):
            return

        try:
            incoming = json.loads(incoming[5:])

            name = incoming.pop(0)
            self.logger.debug('incoming is: %s', incoming)
            args = incoming if not incoming or len(incoming) > 1 else incoming[0]

            if 'do-log-message' == name:
                self._controller.js_log_message_cb(*args)
            else:
                self._main_window.widget.emit(name, args)

        except Exception as err:
            self.logger.exception(err)

    def uri_request_cb(self, request):
        uri = request.get_uri()

        if '?' in uri:
            uri, query = uri.split('?')

        page_name = self._get_page_name_from_uri(uri)

        if uri.count('.') > 1:
            # Uri is in this format: cnchi://page_name.page/path/to/resource.ext
            resource = uri.partition('.page/')[-1]
            resource_path = os.path.join(self.UI_DIR, 'react', 'dist', resource)

            self.logger.debug('Loading app resource: {0}'.format(uri))
            self._uri_request_finish_resource(resource_path, request)

        elif page_name.capitalize() in self.settings.install_options:
            self.logger.debug('Loading app page: {0}'.format(page_name))
            self._uri_request_finish_page(page_name, request)

        else:
            raise Exception('Path is not valid: {0}'.format(uri))
