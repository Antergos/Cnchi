#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  base.py
#
#  Copyright © 2013-2016 Antergos
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

""" Base class for Cnchi's UI """

import os
import logging
import inspect
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


TPL_DIRECTORY = '/usr/share/cnchi/ui'


class Widget(Gtk.Widget):
    """
    Base class for all of Cnchi's UI classes. This gives us the utmost control
    over Cnchi's UI code making it easier to extend in the future as needed.

    Attributes:
        name (str): a name for this widget.
        template_dir (str): The absolute path to our glade template directory for this widget.
        ui_dir (str): The absolute path to our ui directory.
        settings (dict): Settings object as class attribute (common to all instances)

    """

    settings = None

    def __init__(self, template_dir='', name='', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.template_dir = template_dir
        self.name = name

        self.ui = self.template = None

        if self.settings is None:
            self.settings = {}

        if self.template_dir:
            self.load_template()

    def load_template(self):
        self.ui = Gtk.Builder()
        self.template = os.path.join(self.template_dir, "{}.ui".format(self.name))
        self.ui.add_from_file(self.template)

        # Connect UI signals
        self.ui.connect_signals(self)

    def get_ancestor_window(self):
        """ Returns first ancestor that is a Gtk Window """
        return self.get_ancestor(Gtk.Window)

    def get_main_window(self):
        """ Returns top level window (main window) """
        if isinstance(self.main_window, Gtk.Window):
            return self.main_window
        else:
            return None


class Container(Widget, Gtk.Container):
    """
      Base class for the main components of Cnchi's UI (pages and page stacks).

    """

    params = None

    def __init__(self, template_dir='', name='', *args, **kwargs):
        super().__init__(template_dir=template_dir, name=name, *args, **kwargs)

        logging.debug("Loading '%s' %s", name, self.__class__.name)

        if self.params is None:
            self.params = {}

        self.backwards_button = params['backwards_button']
        self.callback_queue = params['callback_queue']
        self.disable_tryit = params['disable_tryit']
        self.forward_button = params['forward_button']
        self.header = params['header']
        self.main_progressbar = params['main_progressbar']
        self.settings = params['settings']
        self.ui_dir = params['ui_dir']
        self.process_list = params['process_list']
        self.main_window = params['main_window']
        self.prev = prev
        self.next = next
        self.title = title
        self._parent = _parent

        self.can_show = False
        self.tab_button = None

        self.add(self.ui.get_object(name))

        self.set_name(name)
        self.name = name


class Page(Container, Gtk.Box):
    """ Base class for our pages """

    def __init__(self, params=None, name=None, prev=None, next=None, title=None, _parent=None):
        super().__init__(params, name, prev, next, title, _parent)

    def translate_ui(self):
        """ This must be implemented by childen """
        raise NotImplementedError

    def prepare(self, direction):
        """ This must be implemented by childen """
        raise NotImplementedError

    def store_values(self):
        """ This must be implemented by childen """
        raise NotImplementedError


class Stack(Container, Gtk.Stack):
    """ Base class for our page stacks """

    def __init__(self, params=None, name=None, prev=None, next=None, title=None, _parent=None):
        super().__init__(params, name, prev, next, title, _parent)



