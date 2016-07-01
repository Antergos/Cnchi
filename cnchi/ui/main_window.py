#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# main_window.py
#
# Copyright © 2013-2016 Antergos
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


""" Main Cnchi Window """

import logging
import multiprocessing
import os
import sys

import gi

from ui.base_widgets import BaseWidget

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib


class MainWindow(Gtk.ApplicationWindow, BaseWidget):
    """
    Cnchi Main Window

    Class Attributes:
        Also see `BaseWidget.__doc__`

    """

    def __init__(self, application=None, _name='main_window', *args, **kwargs):
        ignore = self._get_gtk_ignore_kwargs(**kwargs)
        super().__init__(application=application, _name=_name, ignore=ignore, *args, **kwargs)

        self._state = {}

        # Default window size
        self._main_window_width = 1120
        self._main_window_height = 721

    def _connect_signals(self):
        self.connect('delete-event', self.delete_event_cb)
        self.connect('window-state-event', self.window_state_event_cb)

    def delete_event_cb(self, *args):
        self._controller.emit('__close_app', *args)

    def toggle_maximize(self):
        if self.is_maximized():
            self.unmaximize()
            self._controller.emit_js('window-unmaximized')
        else:
            self.maximize()
            self._controller.emit_js('window-maximized')

    def toggle_fullscreen(self):
        if self._state.get("fullscreen", False):
            self.unfullscreen()
            self._controller.emit_js('window-unfullscreen')
        else:
            self.fullscreen()
            self._controller.emit_js('window-fullscreen')

    def window_state_event_cb(self, window, event, *args):
        self._state["maximized"] = event.new_window_state & Gdk.WindowState.MAXIMIZED
        self._state["fullscreen"] = event.new_window_state & Gdk.WindowState.FULLSCREEN

