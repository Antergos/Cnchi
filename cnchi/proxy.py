#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  proxy.py
#
#  Copyright © 2013-2017 Antergos
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

import os
import logging

def _(x): return x

class ProxyDialog(Gtk.Dialog):
    """ Asks user for proxy settings """

    def __init__(self, transient_for, proxies, ui_dir):
        Gtk.Dialog.__init__(self)

        self.set_transient_for(transient_for)
        self.proxies = proxies
        self.ui_dir = ui_dir

        self.ui = Gtk.Builder()
        self.ui_file = os.path.join(self.ui_dir, "proxy.ui")
        self.ui.add_from_file(self.ui_file)

        # Connect UI signals
        self.ui.connect_signals(self)

        self.add_button(Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)

        dialog_grid = self.ui.get_object("ProxyDialogGrid")
        content_area = self.get_content_area()
        content_area.add(dialog_grid)

    def get_proxies(self):
        return self.proxies

    def on_apply_clicked(self, widget, data):
        print("apply", widget)

    def on_cancel_clicked(self, widget, data):
        print("cancel", widget)
