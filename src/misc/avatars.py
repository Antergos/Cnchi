#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# avatars.py
#
# Copyright © 2013-2018 Antergos
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

import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message


class Avatars(Gtk.Dialog):
    """ Avatar chooser dialog """        
    AVATARS = ['bob', 'jarry', 'jonathan', 'mike', 'suzanne', 'tom']
    AVATAR_WIDTH = 64
    AVATAR_HEIGHT = 64

    def __init__(self, data_path, parent=None):
        Gtk.Dialog.__init__(self)
        if parent:
            self.set_transient_for(parent)
        self.set_modal(True)
        self.set_decorated(False)
        self.set_title(_("Choose your avatar"))

        self.set_border_width(3)
        self.set_default_size(-1, -1)
        self.set_resizable(False)

        self.add_button(Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY)

        self.selected_avatar = None

        self.list_store = Gtk.ListStore(str, GdkPixbuf.Pixbuf)
        self.avatars_path = os.path.join(data_path, 'images/avatars')
        
        iconview = Gtk.IconView()
        iconview.set_model(self.list_store)
        iconview.set_item_width(60)
        iconview.set_text_column(0)
        iconview.set_pixbuf_column(1)
        #iconview.set_tooltip_column(2)
        iconview.set_activate_on_single_click(True)
        iconview.connect("item-activated", self.avatar_selected)
        
        area = self.get_content_area()
        area.add(iconview)

        image = Gtk.Image()

        for avatar in Avatars.AVATARS:
            path = os.path.join(self.avatars_path, avatar + '.png')
            image.set_from_file(path)
            pixbuf = image.get_pixbuf()
            new_pixbuf = pixbuf.scale_simple(
                Avatars.AVATAR_WIDTH,
                Avatars.AVATAR_HEIGHT,
                GdkPixbuf.InterpType.BILINEAR)
            self.list_store.append([avatar, new_pixbuf])
        self.show_all()
    
    def avatar_selected(self, _iconview, treepath):
        self.selected_avatar = self.list_store[treepath][0]

def test_module():
    data_path = "/usr/share/cnchi/data"
    window = Avatars(0, 0, data_path)
    window.show_all()
    Gtk.main()

if __name__ == "__main__":
    test_module()
