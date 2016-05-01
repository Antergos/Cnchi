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

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from ui.container import Container


class Page(Container, Gtk.Box):
    """ Base class for our pages """

    def __init__(self, template_dir='', name='', parent=None, *args, **kwargs):
        super().__init__(template_dir=template_dir, name=name, parent=parent, *args, **kwargs)

    def translate_ui(self):
        """ This must be implemented by childen """
        raise NotImplementedError

    def prepare(self, direction):
        """ This must be implemented by childen """
        raise NotImplementedError

    def store_values(self):
        """ This must be implemented by childen """
        raise NotImplementedError