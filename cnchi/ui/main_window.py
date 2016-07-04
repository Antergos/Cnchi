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

from .base_widgets import (
    Gtk,
    Gdk,
    GLib,
    GObject,
    BaseWidget,
    Singleton
)


class MainWindow(BaseWidget, metaclass=Singleton):
    """
    Cnchi Main Window

    Class Attributes:
        Also see `BaseWidget.__doc__`

    """

    def __init__(self, name='main_window', *args, **kwargs):
        super().__init__(name=name, *args, **kwargs)

        self._state = {}

        # Default window size
        self._main_window_width = 1120
        self._main_window_height = 721

        self._create_custom_signals()

        self.widget.set_size_request(1120, 721)
        self.widget.set_position(Gtk.WindowPosition.CENTER)
        self.widget.set_decorated(False)

    def connect_signals(self):
        self.widget.connect('delete-event', self.delete_event_cb)
        self.widget.connect('window-state-event', self.window_state_event_cb)

    def _create_custom_signals(self):
        GObject.signal_new('on-js', self.widget, GObject.SignalFlags.RUN_LAST,
                           None, (GObject.TYPE_STRING, GObject.TYPE_PYOBJECT,))

    def delete_event_cb(self, *args):
        self.widget.emit('__close_app', *args)

    def toggle_maximize(self):
        if self.widget.is_maximized():
            self.widget.unmaximize()
            self._controller.emit_js('window-unmaximized')
        else:
            self.widget.maximize()
            self._controller.emit_js('window-maximized')

    def toggle_fullscreen(self):
        if self._state.get("fullscreen", False):
            self.widget.unfullscreen()
            self._controller.emit_js('window-unfullscreen')
        else:
            self.widget.fullscreen()
            self._controller.emit_js('window-fullscreen')

    def window_state_event_cb(self, window, event, *args):
        self._state["maximized"] = event.new_window_state & Gdk.WindowState.MAXIMIZED
        self._state["fullscreen"] = event.new_window_state & Gdk.WindowState.FULLSCREEN

