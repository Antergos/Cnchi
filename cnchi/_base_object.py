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
from gi.repository import GLib, Gio, Gtk, WebKit2

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

    _cnchi_app = None
    _controller = None
    _main_container = None
    _main_window = None
    _pages_data = None
    _web_view = None
    log_wrap = '-'
    settings = SharedData('settings', from_dict=settings)

    def __init__(self, name='base_widget', parent=None, tpl_engine='builder', *args, **kwargs):
        """
        Attributes:
            widget     (Gtk.Widget):  This object's GTK Widget.
            name       (str):         A name for this object (all objects must have unique name).
            parent     (mixed):       This object's parent object (if applicable).
            ui         (Gtk.Builder): This objects's GTK Builder instance (if applicable).
            template   (str):         Abs path to this object's template file.
            tpl_engine (str):         Name of this object's primary template engine.

        """

        super().__init__()

        self.name, self.parent, self.tpl_engine = (name, parent, tpl_engine)

        self.template = self.ui = None

        if self.settings is None:
            self.settings =

        if self._pages_data is None:
            self._pages_data = dict()

        for component in ['main_window', 'controller', 'cnchi_app']:
            attrib_name = '_{}'.format(component)
            attrib = getattr(self, attrib_name)

            if attrib is None and name == attrib_name:
                setattr(self, attrib_name, self)


        logging.debug("Loading '%s' %s", _name, self.__class__.__name__)
        # self.load_template()

        if all([self.ui, self.template, self.name]):
            main_box = self.ui.get_object(_name)

            if main_box:
                log_wrap = self.log_wrap * 25
                logging.debug("%s %s %s", log_wrap, self.name, log_wrap)
                self.pack_start(main_box, True, True, 0)

    @staticmethod
    def _get_gtk_ignore_kwargs(**kwargs):
        return [kw for kw in kwargs if kw.startswith('_')]

    def load_template(self):
        if 'gtkbuilder' == self.tpl_engine:
            self.template = os.path.join(self.BUILDER_DIR, '{}.ui'.format(self.name))
        elif 'jinja' == self.tpl_engine:
            self.template = os.path.join(self.JINJA_DIR, '{}.html'.format(self.name))
        else:
            logging.error('Unknown template engine "%s".'.format(self.tpl_engine))
            return

        if os.path.exists(self.template):
            logging.debug("Loading %s template and connecting its signals", self.template)

            if 'gtkbuilder' == self.tpl_engine:
                self.ui = Gtk.Builder().new_from_file(self.template)
                # Connect UI signals
                self.ui.connect_signals(self)

            elif 'jinja' == self.tpl_engine:
                pass
        else:
            logging.warning("Cannot find %s template!", self.template)
            self.template = False

    def get_ancestor_window(self):
        """ Returns first ancestor that is a Gtk Window """
        return self.get_ancestor(Gtk.Window)






class Stack(BaseWidget, Gtk.Stack):
    """
    Base class for page stacks (not used for HTML UI).

    Class Attributes:
        See `Container.__doc__`

    """

    def __init__(self, name='', _parent=None, tpl_engine='gtkbuilder', *args, **kwargs):
        """
        Attributes:
            Also see `Container.__doc__`.

        Args:
            name (str): A name for this widget.

        """

        super().__init__(name=name, _parent=_parent, tpl_engine=tpl_engine, *args, **kwargs)


class Page(BaseWidget, Gtk.Box):
    """
    Base class for pages.

    Class Attributes:
        _page_data (NonSharedData): Data storage for `Page` objects.
        Also see `Box.__doc__`

    """

    def __init__(self, _name='page', _parent=None, _tpl_engine='gtkbuilder', *args, **kwargs):
        """
        Attributes:
            Also see `Box.__doc__`.

        Args:
            name (str): A name for this widget.

        """

        ignore = self._get_gtk_ignore_kwargs(**kwargs)
        super().__init__(orientation=HORIZONTAL, spacing=0, ignore=ignore, _name=_name,
                         _parent=_parent, _tpl_engine=_tpl_engine, *args, **kwargs)

        if self._page_data is None:
            self._page_data = NonSharedData('_page_data')

    def prepare(self, direction):
        """ This must be implemented by subclasses """
        raise NotImplementedError

    def store_values(self):
        """ This must be implemented by subclasses """
        raise NotImplementedError
