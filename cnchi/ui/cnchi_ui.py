#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# cnchi_ui.py
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

from _cnchi_object import (
    CnchiObject,
    Singleton,
    sys
)


class CnchiUI(CnchiObject, metaclass=Singleton):
    """
    UI Controller

    Class Attributes:
        See also `CnchiObject.__doc__`

    """

    modules = []

    def __init__(self, name='cnchi_ui', *args, **kwargs):
        super().__init__(name=name, *args, **kwargs)

        self._pages = dict()
        self._initialize_controller()
        self._create_and_connect_signals()

        page = self._get_page_by_name('Language')
        self._controller.set_current_page(page)

    def _create_and_connect_signals(self):
        self._main_window.create_custom_signal('do-page-navigation-request')
        self._main_window.connect('do-page-navigation-request', self.page_navigation_request_cb)
        self.all_signals.add('page-navigation-request')

    def _get_page_by_index(self, index):
        raise NotImplementedError

    def _get_page_by_name(self, name):
        if name not in self._controller.page_names:
            self.logger.error('Unknown page requested: %s', name)
            return

        try:
            return self._pages[name]
        except KeyError:
            self._initialize_page(name)

        return self._pages[name]

    def _initialize_controller(self):
        ui_module_name = self.settings.ui.module
        ui_module_settings = getattr(self.settings.ui, ui_module_name)
        controller_path = '.{}.{}'.format(ui_module_name, ui_module_settings.controller_path)
        controller_name = '{}Controller'.format(ui_module_name.capitalize())

        controller_module = importlib.import_module(controller_path, 'ui')
        controller = getattr(controller_module, controller_name)

        controller()

    def _initialize_page(self, name):
        index = self._controller.page_names.index(name)
        module_path = 'modules.pages.{}'.format(name.lower())
        python_module = importlib.import_module(module_path)
        module_name = '{0}Module'.format(name)
        module = getattr(python_module, module_name)

        self._pages[name] = self._controller.Page(name=name, index=index, module=module())

    def do_restart(self):
        pass

    def page_navigation_request_cb(self, widget, *args):
        if not args or not args[0]:
            self.logger.error('No page identifier was included in request!')

        page = None

        if isinstance(args[0], int):
            page = self._get_page_by_index(args[0])
        elif isinstance(args[0], str):
            page = self._get_page_by_name(args[0])

        if page:
            self._controller.set_current_page(page)
        else:
            self.logger.error('Page identifier must be one of types [int, str]!')

    def exit_app(self):
        sys.exit(0)
