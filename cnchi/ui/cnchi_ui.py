#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# controller.py
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

""" UI Controller """

import importlib

from _base_object import (
    BaseObject,
    Singleton,
    sys
)


class CnchiUI(BaseObject, metaclass=Singleton):
    """
    UI Controller

    Class Attributes:
        See also `BaseObject.__doc__`

    """

    modules = []

    def __init__(self, name='cnchi_ui', *args, **kwargs):
        super().__init__(name=name, *args, **kwargs)

        self.pages = []
        self._initialize_controller()
        self._controller.initialize_pages_list()
        self._create_and_connect_signals()

    def _create_and_connect_signals(self):
        self._main_window.create_custom_signal('do-page-navigation-request')
        self._main_window.connect('do-page-navigation-request', self.page_navigation_request_cb)

    def _get_page_by_index(self, index):
        raise NotImplementedError

    def _get_page_by_name(self, name):
        page = None

        if name not in self._controller.page_names:
            self.logger.error('Unknown page requested: %s', name)
            return page

        matches = [p for p in self.pages if name == p.name]

        if matches:
            page = matches[0]
        else:
            index = self._controller.page_names.index(name)
            page = self._controller.Page(name=name, index=index)

        return page

    def _initialize_controller(self):
        ui_module_name = self.settings.ui.module
        ui_module_settings = getattr(self.settings.ui, ui_module_name)
        controller_path = '.{}.{}'.format(ui_module_name, ui_module_settings.controller_path)
        controller_name = '{}Controller'.format(ui_module_name.capitalize())

        controller_module = importlib.import_module(controller_path, 'ui')
        controller = getattr(controller_module, controller_name)

        controller()

    def do_restart(self):
        pass

    def page_navigation_request_cb(self, widget, *args):
        if not args or not args[0]:
            self.logger.error('No page identifier was included in request!')

        if isinstance(args[0], int):
            page = self._get_page_by_index(args[0])
        elif isinstance(args[0], str):
            page = self._get_page_by_name(args[0])
        else:
            self.logger.error('Page identifier must be one of types [int, str]!')

    def exit_app(self):
        sys.exit(0)
