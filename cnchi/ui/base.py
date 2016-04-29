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

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import os
import logging

TPL_DIRECTORY = os.path.normpath()


class Widget(Gtk.Widget):
    """
    Base class for all of Cnchi's UI classes. This will ensure we have the utmost control
    over Cnchi's UI code making it easier to extend in the future as needed.

    Attributes:
        name (str): a name for this widget.
        template_dir (str): The absolute path to our glade template directory for this widget.
        ui_dir (str): The absolute path to our ui directory.
        settings (dict): Settings object as class attribute (common to all instances)

    """

    cn_settings = None

    def __init__(self, template_dir='', name='', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set('template_dir', template_dir)
        self.set('name', name)

        if self.get('settings') is None:
            self.set('settings', {})

    def get(self, attribute=None):
        """
        Getter method that handles prefixing our attributes automatically.

        Args:
            attribute (str): Attribute to get

        Returns:
            (mixed) value of requested attribute.

        """
        if attribute is None:
            msg = '{0}.get() called without an attribute to "get".'
            logging.debug(msg.format(self.__class__.__name__))
            return

        attr = 'cn_{0}'.format(attribute)

        return getattr(self, attr)

    def set(self, attribute=None, value=None):
        """
        Setter method that handles prefixing our attributes automatically.

        Args:
            attribute (str): Attribute name to set
            value (mixed): Attribute value to set

        Returns:
            True if attribute was set successfully.

        """
        if attribute is None or value is None:
            msg = '{0}.set() called without an attribute or value to "set". '
            msg += 'attribute was: {1}. value was: {2}'
            logging.debug(msg.format(self.__class__.__name__, attribute, value))
            return

        attr = 'cn_{0}'.format(attribute)

        return setattr(self, attr, value)


class Container(Widget, Gtk.Container):
    """
      Base class for the main components of Cnchi's UI (pages and page stacks).

    """

    def __init__(self, params=None, name=None, prev=None, next=None, title=None, _parent=None):
        super().__init__()

        logging.debug("Loading '%s' %s", (name, self.__class__.name))

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

        self.ui = Gtk.Builder()
        self.ui_file = os.path.join(self.ui_dir, "{}.ui".format(name))
        self.ui.add_from_file(self.ui_file)

        # Connect UI signals
        self.ui.connect_signals(self)

        self.add(self.ui.get_object(name))

        self.set_name(name)
        self.name = name

    def get_name(self):
        """ Return screen name """
        return self.name

    def get_prev_page(self):
        """ Returns previous screen """
        return self.prev_page

    def get_next_page(self):
        """ Returns next screen """
        return self.next_page

    def get_ancestor_window(self):
        """ Returns first ancestor that is a Gtk Window """
        return self.get_ancestor(Gtk.Window)

    def get_main_window(self):
        """ Returns top level window (main window) """
        if isinstance(self.main_window, Gtk.Window):
            return self.main_window
        else:
            return None

    def setup_tab_button(self, button):
        self.tab_button = Gtk.Button.new_with_label(self.title)

        self.tab_button.connect(
            'clicked',
            self.main_window.on_header_nav_button_clicked,
            {'parent_name': self._parent.name, 'name': self.name}
        )

        self._parent.tab_buttons.append(self.tab_button)


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



