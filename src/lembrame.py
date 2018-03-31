#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  lembrame.py
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


class LembrameCredentials(object):
    user_id = False
    upload_code = False

    def __init__(self, user_id, upload_code):
        self.user_id = user_id
        self.upload_code = upload_code


class LembrameDialog(Gtk.Dialog):
    """ Asks user for lembrame credentials """

    def __init__(self, transient_for, ui_dir):
        Gtk.Dialog.__init__(self)

        self.set_transient_for(transient_for)
        self.ui_dir = ui_dir
        self.set_default_size(300, 150)

        self.ui = Gtk.Builder()
        self.ui_file = os.path.join(self.ui_dir, "lembrame.ui")
        self.ui.add_from_file(self.ui_file)

        self.translate_ui()

        self.add_button(Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY)

        dialog_grid = self.ui.get_object("LembrameDialogGrid")
        content_area = self.get_content_area()
        content_area.add(dialog_grid)

    def translate_ui(self):
        self.set_title(_("Cnchi - Lembrame credentials"))

        # label = self.ui.get_object("http_proxy_label")
        # label.set_text(_("HTTP proxy server:"))
        # label = self.ui.get_object("https_proxy_label")
        # label.set_text(_("HTTPS proxy server:"))
        # label = self.ui.get_object("ftp_proxy_label")
        # label.set_text(_("FTP proxy server:"))
        # label = self.ui.get_object("socks_proxy_label")
        # label.set_text(_("SOCKS host server:"))
        # label = self.ui.get_object("use_same_proxy_label")
        # label.set_text(_("Use this proxy server for all protocols"))
        #
        # port_names = [
        #     "http_proxy_port_label", "https_proxy_port_label",
        #     "https_proxy_port_label", "ftp_proxy_port_label",
        #     "socks_proxy_port_label"]
        # for name in port_names:
        #     label = self.ui.get_object(name)
        #     label.set_text(_("Port:"))

    def get_credentials(self):
        user_id = self.ui.get_object("userid_entry")
        upload_code = self.ui.get_object("uploadcode_entry")

        return LembrameCredentials(user_id.get_text(), upload_code.get_text())
