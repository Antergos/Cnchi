#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gtkbasebox.py
#
#  Copyright © 2013-2018 Antergos
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

""" Cnchi's base class for screens """

import os
import logging

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class GtkBaseBox(Gtk.Box):
    """ Base class for our screens """

    def __init__(self, child, params, name, prev_page, next_page):
        self.backwards_button = params['backwards_button']
        self.callback_queue = params['callback_queue']
        self.no_tryit = params['no_tryit']
        self.forward_button = params['forward_button']
        self.header = params['header']
        self.main_progressbar = params['main_progressbar']
        self.settings = params['settings']
        self.gui_dir = params['gui_dir']
        self.main_window = params['main_window']
        self.prev_page = prev_page
        self.next_page = next_page

        Gtk.Box.__init__(self)

        self.set_name(name)
        self.name = name

        logging.debug("Loading '%s' screen", name)

        self.gui = Gtk.Builder()
        self.gui_file = os.path.join(self.gui_dir, "{}.ui".format(name))
        self.gui.add_from_file(self.gui_file)

        # Connect UI signals
        self.gui.connect_signals(child)

        child.add(self.gui.get_object(name))

    def get_prev_page(self):
        """ Returns previous screen """
        return self.prev_page

    def get_next_page(self):
        """ Returns next screen """
        return self.next_page

    def translate_ui(self):
        """ This must be implemented by childen """
        raise NotImplementedError

    def prepare(self, direction):
        """ This must be implemented by childen """
        raise NotImplementedError

    def store_values(self):
        """ This must be implemented by childen """
        raise NotImplementedError

    def get_name(self):
        """ Return screen name """
        return self.name

    def get_ancestor_window(self):
        """ Returns first ancestor that is a Gtk Window """
        return self.get_ancestor(Gtk.Window)

    def get_toplevel_window(self):
        """ Returns top level window """
        top = self.main_window
        if isinstance(top, Gtk.Window):
            return top
        else:
            return None

    def get_main_window(self):
        """ Returns top level window (main window) """
        if isinstance(self.main_window, Gtk.Window):
            return self.main_window
        else:
            return None
