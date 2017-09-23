#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# webview.py
#
# Copyright © 2013-2017 Antergos
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

""" Web View """

import logging

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, GLib, WebKit2


class BrowserWindow(Gtk.Window):
    def __init__(self, title, width=800, height=600):
        Gtk.Window.__init__(self)

        self.set_size_request(width, height)

        self.set_resizable(False)
        scrolled_window = Gtk.ScrolledWindow()
        self.add(scrolled_window)

        self.connect('delete-event', self.on_destroy)

        # https://lazka.github.io/pgi-docs/WebKit2-4.0/classes/Settings.html
        settings = WebKit2.Settings().new()
        self.webview = WebKit2.WebView().new_with_settings(settings)

        self.webview.connect('decide-policy', self.decide_policy_cb)
        self.webview.connect('load_changed', self.load_changed_cb)

        scrolled_window.add(self.webview)

    def on_destroy(self, event, data):
        self.destroy()

    def decide_policy_cb(self, decision, type, data):
        # Allows all (security flaw, but we do not care when installing)
        return True

    def load_changed_cb(self, webview, load_event):
        if load_event == WebKit2.LoadEvent.FINISHED:
            self.show_all()

    def load_url(self, url):
        GLib.idle_add(self.webview.load_uri, url)
