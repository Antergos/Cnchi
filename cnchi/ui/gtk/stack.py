#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  stack.py
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
from gi.repository import Gtk

from ui.container import Container

# TODO : EVERYTHING!

class Stack(Gtk.Stack, Container):
    """ Base class for our page stacks """

    def __init__(self, template_dir='', name='', parent=None, *args, **kwargs):
        Gtk.Stack.__init__(self)
        Container.__init__(self, template_dir=template_dir, name=name, parent=parent, *args, **kwargs)
