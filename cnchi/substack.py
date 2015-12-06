#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# keymap.py
#
# Copyright © 2013-2015 Antergos
#
# This file is part of Cnchi.
#
# Cnchi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Cnchi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# The following additional terms are in effect as per Section 7 of the license:
#
# The preservation of all legal notices and author attributions in
# the material or in the Appropriate Legal Notices displayed
# by works containing it is required.
#
# You should have received a copy of the GNU General Public License
# along with Cnchi; If not, see <http://www.gnu.org/licenses/>.

""" Substack class used for page groups """

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class SubStack(Gtk.Stack):
    def __init__(self, params=None, title=None, name=None, prev_page=None, next_page=None):
        super().__init__()

        self.backwards_button = params['backwards_button']
        self.callback_queue = params['callback_queue']
        self.disable_tryit = params['disable_tryit']
        self.forward_button = params['forward_button']
        self.header = params['header']
        self.main_progressbar = params['main_progressbar']
        self.settings = params['settings']
        self.testing = params['testing']
        self.ui_dir = params['ui_dir']
        self.process_list = params['process_list']
        self.main_window = params['main_window']
        self.prev_page = prev_page
        self.next_page = next_page
        self.title = title
        self.name = name
        self.in_group = False

    def get_prev_page(self):
        """ Returns previous screen """
        return self.prev_page

    def get_next_page(self):
        """ Returns next screen """
        return self.next_page

    def translate_ui(self):
        """ This must be implemented by childen """
        pass

    def prepare(self, direction):
        """ This must be implemented by childen """
        pass

    def store_values(self):
        """ This must be implemented by childen """
        pass

    def get_name(self):
        """ Return screen name """
        return self.name

    def get_toplevel(self):
        """ Returns top level window """
        top = self.main_window
        if isinstance(top, Gtk.Window):
            return top
        else:
            return None