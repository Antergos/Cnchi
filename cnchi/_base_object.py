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
from random import choice
from string import ascii_uppercase

# 3rd-party Libs
import gi

# Once 3.22 is released we will be able to do this:
# gi.require_versions({'Gtk': '3.0', 'WebKit2': '4.0'})
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import (
    Gdk,
    Gio,
    GLib,
    GObject,
    Gtk,
    WebKit2
)

# This application
from _data import (
    DataObject,
    NonSharedData,
    SharedData
)

from misc.extra import bg_thread


TE = 'gtkbuilder'
BO = 'base_object'


class BaseObject:
    """
    Base class for all of Cnchi's classes.

    Class Attributes:
        TOP_DIR      (str): Absolute path to the application's top-most directory.
        APP_DIR      (str): Abs path to the app's source files (derived from TOP_DIR).
        UI_DIR       (str): Abs path to the app's UI source files (derived from APP_DIR).
        PAGES_DIR    (str): Abs path to the app's UI's pages (derived from UI_DIR).
        TPL_DIR      (str): Abs path to the app's UI templates (derived from UI_DIR).
        BUILDER_DIR  (str): Abs path to the app's GtkBuilder templates (derived from TPL_DIR).
        WK_CACHE_DIR (str): Abs path to the app's webkit cache directory.
        WK_DATA_DIR  (str): Abs path to the app's webkit data directory.

        _cnchi_app       (BaseObject):      The application object.
        _controller      (BaseObject):      The app's ui controller object.
        _main_container  (BaseObject):      The app's main ui container object.
        _main_window     (BaseWidget):      The app's main window object.
        _pages_data      (SharedData):      Descriptor that provides access to the app's ui
                                            pages' data (storage for `Page.store_values()`)
        _web_view        (BaseWidget):      The app's ui web view object.

        _allowed_signals (list):            List of signals allowed over the python/js bridge.
        logger           (logging.Handler): The app's log handler.
        settings         (SharedData):      Descriptor that provides access to the app's
                                            Settings object.
        widget           (NonSharedData):   Descriptor that provides access to the `Gtk.Widget`
                                            for this object.

    """

    TOP_DIR = '/usr/share/cnchi'
    APP_DIR = os.path.join(TOP_DIR, 'cnchi')
    UI_DIR = os.path.join(APP_DIR, 'ui')
    PAGES_DIR = os.path.join(UI_DIR, 'react/app/pages')
    TPL_DIR = os.path.join(UI_DIR, 'tpl')
    BUILDER_DIR = os.path.join(TPL_DIR, 'gtkbuilder')
    WK_CACHE_DIR = '/var/cache/cnchi'
    WK_DATA_DIR = '/var/tmp/cnchi'

    _cnchi_app = SharedData('_cnchi_app')
    _cnchi_controller = SharedData('_cnchi_controller')
    _main_container = SharedData('_main_container')
    _main_window = SharedData('_main_window')
    _pages_helper = SharedData('_pages_helper')
    _pages_state = SharedData('_pages_state')
    _react_controller = SharedData('_react_controller')
    _web_view = SharedData('_web_view')

    _allowed_signals = SharedData('_allowed_signals')
    logger = None
    log_wrap = '-'
    settings = SharedData('settings', from_dict={})
    widget = NonSharedData('widget')

    def __init__(self, name=BO, parent=None, tpl_engine=TE, logger=None, *args, **kwargs):
        """
        Attributes:
            name       (str):         A name for this object (all objects must have unique name).
            parent     (mixed):       This object's parent object (if applicable).
            ui         (Gtk.Builder): This objects's GTK Builder instance (if applicable).
            template   (str):         Abs path to this object's template file.
            tpl_engine (str):         Name of this object's primary template engine.
            widget     (Gtk.Widget):  This object's GTK Widget.

        """

        super().__init__()

        self.name, self.parent, self.tpl_engine = (name, parent, tpl_engine)

        self.template = self.ui = None

        if self._allowed_signals is None:
            self._allowed_signals = []

        self._check_for_main_components(name)

        if self.logger is None:
            BaseObject.logger = logger

        self.logger.debug("Loading '%s' %s", name, self.__class__.__name__)

    def _check_for_main_components(self, name):
        components = [
            'main_window', 'cnchi_controller', 'cnchi_app', 'pages_helper', 'react_controller'
        ]

        if name not in components:
            return

        attrib_name = '_{}'.format(name)
        attrib = getattr(self, attrib_name)

        if attrib is None:
            setattr(self, attrib_name, self)

    @staticmethod
    def toggle_bool(value):
        """
        Given a `bool`, returns the opposite `bool` value.
        Given a `str` value representing a bool, returns the opposite bool value as a `str`.

        Args:
            value (str|bool): Value to toggle.

        Examples:
            >>> bool_string_helper('False')
            'True'
            >>> bool_string_helper(True)
            False

        Raises:
            ValueError: If value is not of type(bool|str) or if str value not in ['True', 'False'].

        """

        if isinstance(value, str) and value in ['True', 'False']:
            return 'True' if 'False' == value else 'False'
        elif isinstance(value, bool):
            return False if value else True
        else:
            raise ValueError(
                'value must be of type(bool|str["True", "False"]). {0} given.'.format(type(value))
            )


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)

        return cls._instance

