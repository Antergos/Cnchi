#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  widget.py
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

import os
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

TPL_DIRECTORY = '/usr/share/cnchi/tpl'
UI_DIRECTORY = '/usr/share/cnchi/cnchi/ui'


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
    main_window = None

    def __init__(self, template_dir='', name='', ui_dir=UI_DIRECTORY, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.template_dir = template_dir
        self.name = name
        self.ui_dir = ui_dir

        self.ui = self.template = None

        if self.settings is None:
            self.settings = {}

        if self.main_window is None and issubclass(self, Gtk.Window):
            self.main_window = self

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
