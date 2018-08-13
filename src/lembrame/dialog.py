#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  dialog.py
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

""" Lembrame credentials GUI module """

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os

from lembrame.credentials import LembrameCredentials


def _(msg):
    return msg


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
        """ Translate GUI widgets """
        self.set_title(_("Cnchi - Lembrame credentials"))

        label = self.ui.get_object("lembrame_label")
        label.set_text(_("You will need to write your UserID and your upload code\n"
                         "which you should generate first with the Lembrame tool\n"
                         "before beginning a new installation."))
        label = self.ui.get_object("userid_label")
        label.set_text(_("Your UserID:"))
        label = self.ui.get_object("uploadcode_label")
        label.set_text(_("Your upload code:"))

    def get_credentials(self):
        """ Load credentials from UI and return them as a class """
        user_id = self.ui.get_object("userid_entry")
        upload_code = self.ui.get_object("uploadcode_entry")

        return LembrameCredentials(user_id.get_text(), upload_code.get_text())
