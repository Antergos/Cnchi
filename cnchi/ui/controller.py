#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ui_controller.py
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

""" UI Controller Module """

import json
import logging

from ui.base_widgets import BaseObject, Singleton, WebKit2
from ui.main_window import MainWindow
from ui.html.main_container import MainContainer
from ui.html.pages_helper import PagesHelper


class Controller(BaseObject, metaclass=Singleton):
    """
    UI Controller

    Class Attributes:
        _emit_js_tpl (str): Javascript string used to emit signals in web_view.
        See also `BaseWidget.__doc__`

    """

    _emit_js_tpl = 'window.cnchi._emit(%s)'

    def __init__(self, name='controller', *args, **kwargs):

        super().__init__(name=name, *args, **kwargs)

        main_window = MainWindow()
        main_container = MainContainer()

        main_window.widget.add(self._web_view)
        self._initialize_pages()
        self._connect_signals_to_callbacks()

        for widget in [main_window.widget, self._web_view]:
            widget.show_all()

    def _connect_signals_to_callbacks(self):
        self._main_window.widget.connect('on-js', self.js_log_message_cb)

    def _initialize_pages(self):
        self._pages_helper = PagesHelper()
        self.set_current_page(0)

    def emit_js(self, name, *args):
        """
        Trigger and pass data to a JavaScript event in the web_view.

        Args:
            name (str): The name of the JavaScript event to trigger.
            *args (str): Arguments to pass to the event handler (optional).

        """
        msg = json.dumps([name] + list(args), None, None, None)
        self._web_view.run_javascript(self._emit_js_tpl.format(msg))

    def js_log_message_cb(self, called, msg, *args):
        if not called or 'logger' not in called:
            return

        level = 'debug'

        if '.' in called:
            level = called.split('.')[-1]

        _logger = getattr(self.logger, level)

        _logger(msg, *args)

    def set_current_page(self, identifier):
        page = self._pages_helper.get_page(identifier)

        if page is None:
            raise ValueError('page cannot be None!')

        page.prepare()
        self._web_view.load_uri('cnchi:///')

