#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  container.py
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
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from ui.base_widget import BaseWidget


class Container(BaseWidget, Gtk.Container):
    """
    Base class for the main components of Cnchi's UI (pages and page stacks).

    Class attributes:
        params (dict):  ['callback_queue', 'disable_tryit', 'top_nav_buttons', 'header',
                  'sub_nav_buttons', 'main_progressbar', 'process_list', 'settings']

    """
    params = None

    def __init__(self, name='', parent=None):
        """
        Attributes:
            name (str): a name for this widget.
        """
        super().__init__(name=name, parent=parent)

        logging.debug("Loading '%s' %s", name, self.__class__.name)

        self.children = []
