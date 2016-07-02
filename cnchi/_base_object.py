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

import logging
import os

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gdk, GLib, Gio, Gtk, WebKit2

from _settings import NonSharedData, SharedData, settings


class BaseObject:
    """
    Base class for all of Cnchi's classes.

    Class Attributes:
        TOP_DIR      (str): Absolute path to the application's top-most directory.
        APP_DIR      (str): Abs path to the app's source files (derived from TOP_DIR).
        UI_DIR       (str): Abs path to the app's UI source files (derived from APP_DIR).
        TPL_DIR      (str): Abs path to the app's UI templates (derived from UI_DIR).
        BUILDER_DIR  (str): Abs path to the app's GtkBuilder templates (derived from TPL_DIR).
        JINJA_DIR    (str): Abs path to the app's Jinja templates (derived from TPL_DIR).

        _cnchi_app      (BaseWidget):      The application object.
        _controller     (BaseWidget):      The app's ui controller object.
        _main_container (BaseWidget):      The app's main ui container object.
        _main_window    (BaseWidget):      The app's main window object.
        _pages_data     (SharedData):      Descriptor that provides access to the app's ui
                                           pages' data (storage for `Page.store_values()`)
        _web_view       (BaseWidget):      The app's ui web view object.

        logger          (logging.Handler): The app's log handler.
        settings        (SharedData):      Descriptor that provides access to the app's
                                           Settings object.
        widget          (NonSharedData):   Descriptor that provides access to the `Gtk.Widget`
                                           for this object.

    """

    TOP_DIR = '/usr/share/cnchi'
    APP_DIR = os.path.join(TOP_DIR, 'cnchi')
    UI_DIR = os.path.join(APP_DIR, 'ui')
    TPL_DIR = os.path.join(UI_DIR, 'tpl')
    BUILDER_DIR = os.path.join(TPL_DIR, 'gtkbuilder')
    JINJA_DIR = os.path.join(TPL_DIR, 'jinja')

    _cnchi_app = SharedData('_cnchi_app')
    _controller = SharedData('_controller')
    _main_container = SharedData('_main_container')
    _main_window = SharedData('_main_window')
    _pages_data = NonSharedData('_pages_data')
    _web_view = SharedData('_web_view')

    logger = None
    log_wrap = '-'
    settings = SharedData('settings', from_dict=settings)
    widget = NonSharedData('widget')

    def __init__(self, name='base_widget', parent=None,
                 tpl_engine='gtkbuilder', logger=None, *args, **kwargs):
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

        for component in ['main_window', 'controller', 'cnchi_app']:
            if name != component:
                continue

            attrib_name = '_{}'.format(component)
            attrib = getattr(self, attrib_name)

            if attrib is None:
                setattr(self, attrib_name, self)

        if self.logger is None:
            logging.debug('setting logger!')
            BaseObject.logger = logger

        self.logger.debug("Loading '%s' %s", name, self.__class__.__name__)

