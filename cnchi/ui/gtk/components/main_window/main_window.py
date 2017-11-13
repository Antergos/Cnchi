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

# 3rd-party Libs
from ui import (
    Gdk,
    GObject
)

# This application
from ui.base_widgets import (
    CnchiWidget,
    Singleton
)


class MainWindow(CnchiWidget, metaclass=Singleton):
    """
    Cnchi Main Window

    Class Attributes:
        Also see `CnchiWidget.__doc__`
    """

    def __init__(self, name='main_window', *args, **kwargs):
        super().__init__(name=name, *args, **kwargs)

        self._state = {'fullscreen': False}
        self.is_dragging = False
        self._button_press_hook_id = None

        # Default window size
        self._main_window_width = 1120
        self._main_window_height = 721

        self.create_custom_signal('window-dragging-start')
        self.create_custom_signal('window-dragging-stop')

        self._apply_window_settings()
        self._connect_signals()

    def _apply_window_settings(self):
        visual = self._main_window.widget.get_screen().get_rgba_visual()

        if visual:
            self.widget.set_visual(visual)
        else:
            self.logger.error('Unable to set transparent background!')

        self.widget.set_size_request(1120, 721)
        self.widget.set_decorated(False)
        # self.widget.set_interactive_debugging(True)
        self.widget.set_app_paintable(True)

    def _connect_signals(self):
        # self.widget.connect('delete-event', self.delete_event_cb)
        self.connect('window-state-event', self.window_state_event_cb)
        self.connect('window-dragging-start', self.window_dragging_cb)
        self.connect('window-dragging-stop', self.window_dragging_cb)

        # signal_id = GObject.signal_lookup('button-press-event', WebKit2.WebView)
        # self._button_press_hook_id = GObject.signal_add_emission_hook(
        #    signal_id, 0, self.button_press_event_cb, None
        # )

    def button_press_event_cb(self, ihint, param_values, data):
        self.logger.debug([ihint, param_values, data])

    def connect(self, signal_name, callback):
        self.widget.connect(signal_name, callback)

    def create_custom_signal(self, signal_name):
        GObject.signal_new(
            signal_name,
            self.widget,
            GObject.SignalFlags.RUN_LAST,
            None,
            (GObject.TYPE_PYOBJECT,)
        )

    def delete_event_cb(self, *args):
        self.widget.emit('__close_app', *args)

    def emit(self, signal_name, callback):
        self.widget.emit(signal_name, callback)

    def toggle_maximize(self):
        if self.widget.is_maximized():
            self.widget.unmaximize()
            self._controller.trigger_js_event('window-unmaximized')
        else:
            self.widget.maximize()
            self._controller.trigger_js_event('window-maximized')

    def toggle_fullscreen(self):
        if self._state.get('fullscreen', False):
            self.widget.unfullscreen()
            self._controller.trigger_js_event('window-unfullscreen')
        else:
            self.widget.fullscreen()
            self._controller.trigger_js_event('window-fullscreen')

    def window_dragging_cb(self, window, event, *args):
        pass

    def window_state_event_cb(self, window, event, *args):
        self._state['maximized'] = event.new_window_state & Gdk.WindowState.MAXIMIZED
        self._state['fullscreen'] = event.new_window_state & Gdk.WindowState.FULLSCREEN

