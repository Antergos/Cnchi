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
from gi.repository import Gtk

from _settings import SharedData, settings


class BaseWidget(Gtk.Widget):
    """
    Base class for all of Cnchi's UI classes. This gives us the utmost control
    over Cnchi's UI code making it easier to extend in the future as needed.

    Class Attributes:
        TOP_DIR      (str): Absolute path to the application's top-most directory.
        APP_DIR      (str): Abs path to the app's source files (derived from TOP_DIR).
        UI_DIR       (str): Abs path to the app's UI source files (derived from APP_DIR).
        TPL_DIR      (str): Abs path to the app's UI templates (derived from UI_DIR).
        BUILDER_DIR  (str): Abs path to the app's GtkBuilder templates (derived from TPL_DIR).
        JINJA_DIR    (str): Abs path to the app's Jinja templates (derived from TPL_DIR).

        main_window (Gtk.MainWindow): The application's main window.
        settings    (SharedData):     Settings object (common to all instances).

    """

    TOP_DIR = '/usr/share/cnchi'
    APP_DIR = os.path.join(TOP_DIR, 'cnchi')
    UI_DIR = os.path.join(APP_DIR, 'ui')
    TPL_DIR = os.path.join(UI_DIR, 'tpl')
    BUILDER_DIR = os.path.join(TPL_DIR, 'gtkbuilder')
    JINJA_DIR = os.path.join(TPL_DIR, 'jinja')

    main_window = None
    settings = SharedData('settings', from_dict=settings)

    def __init__(self, name='', parent=None, tpl_engine='gtkbuilder'):
        """
        Attributes:
            name       (str):         A name for this widget.
            parent     (mixed):       This widget's parent widget (if applicable).
            ui         (Gtk.Builder): This Widget's GTKBuilder instance.
            template   (str):         Abs path to this widget's template file.
            tpl_engine (str):         Name of this widget's primary template engine.

        """

        super().__init__()

        self.name = name
        self.parent = parent
        self.tpl_engine = tpl_engine
        self.template = self.ui = None

        if parent:
            self.set_parent(parent)

        if name:
            self.set_name(name)

        if self.main_window is None and isinstance(self, Gtk.Window):
            self.main_window = self

        logging.debug("Loading '%s' %s", name, self.__class__.name)
        self.load_template()

        if all([self.ui, self.template, self.name]):
            main_box = self.ui.get_object(name)

            if main_box:
                logging.debug(" ------------------------ %s ------------------------", self.name)
                self.pack_start(main_box, True, True, 0)

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
            logging.error("Cannot find %s template!", self.template)

    def get_ancestor_window(self):
        """ Returns first ancestor that is a Gtk Window """
        return self.get_ancestor(Gtk.Window)
