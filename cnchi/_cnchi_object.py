#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  base_widget.py
#
#  Copyright © 2016 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
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
#  along with Cnchi; If not, see <http://www.gnu.org/licenses/>.

# Standard Lib
import gettext
import json
import locale
import logging
import os
import strictyaml as yaml
import sys
import time
from collections import OrderedDict
from random import choice
from string import ascii_uppercase

# 3rd-party Libs

# This application
from _data import (
    DataObject,
    NonSharedData,
    SharedData
)

from misc.extra import bg_thread


class CnchiObject:
    """
    Base class for all of Cnchi's classes.

    Class Attributes:
        TOP_DIR     (str): Absolute path to the application's top-most directory.
        APP_DIR     (str): Abs path to the app's source files (derived from TOP_DIR).
        UI_DIR      (str): Abs path to the app's UI directory (derived from APP_DIR).
        PAGES_DIR   (str): Abs path to the app UI's pages (derived from UI_DIR).

        _cnchi_app       (CnchiObject):     The application instance.
        _controller      (CnchiObject):     The app's ui controller instance.
        _main_container  (CnchiObject):     The app's main ui container instance.
        _main_window     (CnchiWidget):     The app's main window instance.
        _pages_data      (SharedData):      Descriptor that provides access to the app ui
                                            pages' data (storage for `Page.store_values()`)
        _web_view        (CnchiWidget):     The app ui's web view object.

        all_signals      (set):             Names of custom signals.
        logger           (logging.Handler): The app's log handler.
        settings         (SharedData):      Descriptor that provides access to the app's settings.
    """

    TOP_DIR = '/usr/share/cnchi'
    APP_DIR = os.path.join(TOP_DIR, 'cnchi')
    UI_DIR = os.path.join(APP_DIR, 'ui')
    PAGES_DIR = os.path.join(UI_DIR, 'react/app/pages')

    _cnchi_app = SharedData('_cnchi_app')
    _cnchi_ui = SharedData('_cnchi_ui')
    _controller = SharedData('_controller')
    _main_container = SharedData('_main_container')
    _main_window = SharedData('_main_window')
    _pages_helper = SharedData('_pages_helper')
    _web_view = SharedData('_web_view')

    all_signals = SharedData('all_signals')
    logger = None
    log_wrap = '-'
    settings = SharedData('settings', from_dict={})
    state = SharedData('state')

    def __init__(self, name='cnchi_base', parent=None, logger=None, *args, **kwargs):
        """
        Attributes:
            name       (str):         A name for this object (all objects must have unique name).
            parent     (mixed):       This object's parent object (if applicable).
            ui         (Gtk.Builder): This objects's GTK Builder instance (if applicable).
            template   (str):         Abs path to this object's template file.
            tpl_engine (str):         Name of this object's primary template engine.
            widget     (Gtk.Widget):  This object's UI Toolkit Widget (GTK or Qt).
        """

        super().__init__()

        self.name, self.parent = name, parent

        self.template = self.ui = None

        if self.all_signals is None:
            self.all_signals = set()

        self._maybe_register_main_component(name)

        if self.logger is None:
            CnchiObject.logger = logger

        self.logger.debug("Loading '%s' %s", name, self.__class__.__name__)

    def _maybe_register_main_component(self, name):
        components = [
            'main_window',
            'cnchi_ui',
            'cnchi_app',
            'pages_helper',
            'controller',
        ]

        if name not in components:
            return

        attrib = getattr(self, f'_{name}')

        if attrib is None:
            setattr(self, f'_{name}', self)


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)

        return cls._instance

