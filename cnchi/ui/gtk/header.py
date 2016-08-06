#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  header.py
#
#  Copyright © 2016 Antergos
#
#  This file is part of The Antergos Build Server, (AntBS).
#
#  AntBS is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  AntBS is distributed in the hope that it will be useful,
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
#  along with AntBS; If not, see <http://www.gnu.org/licenses/>.

import logging
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .container import Container

TPL_DIR = '/usr/share/cnchi/tpl'
UI_DIR = '/usr/share/cnchi/cnchi/ui'


class HeaderOverlay(Gtk.Headerbar, Container):
    pass


class Header(Gtk.Headerbar, Container):
    def __init__(self, template_dir=TPL_DIR, name='header', parent=None, *args, **kwargs):
        Gtk.Headerbar.__init__(self)
        Container.__init__(template_dir=template_dir, name=name, parent=parent, *args, **kwargs)

        self.overlay = HeaderOverlay()
        self.progressbar = self.ui.get('progressbar')
        self.navigation = self.ui.get('primary_navigation')
        self.forward_button = self.ui.get('forward_button')

        for widget in [self, self.progressbar, self.navigation, self.forward_button]:
            self.overlay.add_overlay(widget)
