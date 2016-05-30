#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  page.py
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

import gi
import logging

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from ui.container import Container


class Page(Container, Gtk.Box):
    """ Base class for our pages """

    def __init__(self, name='', parent=None):
        """
        Attributes:
            name (str): a name for this widget.
        """
        super().__init__(name=name, parent=parent)

        # FIXME: Is this ok?
        '''
        Specifies whether widget has a GdkWindow of its own.
        Note that all realized widgets have a non-NULL “window” pointer
        (gtk_widget_get_window() never returns a NULL window when a widget is realized),
        but for many of them it’s actually the GdkWindow of one of its parent widgets.
        Widgets that do not create a window for themselves in “realize” must announce
        this by calling this function with has_window = FALSE.
        This function should only be called by widget implementations, and they should call it in their init() function.
        '''
        self.set_has_window(False)

        self.name = name
        self.parent = parent

    def prepare(self, direction):
        """ This must be implemented by childen """
        raise NotImplementedError

    def store_values(self):
        """ This must be implemented by childen """
        raise NotImplementedError
