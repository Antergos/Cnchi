#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  desktop.py
#
#  Copyright © 2013,2014 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

""" Desktop screen """

from gi.repository import Gtk, GLib, GdkPixbuf
import os
import logging
import desktop_environments as desktops

from gtkbasebox import GtkBaseBox

class DesktopAsk(GtkBaseBox):
    """ Class to show the Desktop screen """
    def __init__(self, params, prev_page="keymap", next_page="features"):
        super().__init__(self, params, "desktop", prev_page, next_page)

        data_dir = self.settings.get('data')
        self.desktops_dir = os.path.join(data_dir, "images", "desktops")

        self.desktop_info = self.ui.get_object("desktop_info")
        
        self.desktop_image = None
        self.icon_desktop_image = None

        # Set up list box
        self.listbox = self.ui.get_object("listbox_desktop")
        self.listbox.connect("row-selected", self.on_listbox_row_selected)
        self.listbox.set_selection_mode(Gtk.SelectionMode.BROWSE)

        self.desktop_choice = 'gnome'

        self.enabled_desktops = self.settings.get("desktops")

        self.set_desktop_list()

    def translate_ui(self, desktop):
        """ Translates all ui elements """
        label = self.ui.get_object("desktop_info")
        txt = "<span weight='bold'>%s</span>\n" % desktops.NAMES[desktop]
        description = desktops.DESCRIPTIONS[desktop]
        txt += _(description)
        label.set_markup(txt)

        # This sets the desktop's image
        path = os.path.join(self.desktops_dir, desktop + ".png")
        if self.desktop_image is None:
            self.desktop_image = Gtk.Image.new_from_file(path)
            overlay = self.ui.get_object("image_overlay")
            overlay.add(self.desktop_image)
        else:
            self.desktop_image.set_from_file(path)
            
        # and this sets the icon
        filename = "desktop-environment-" + desktop.lower() + ".svg"
        icon_path = os.path.join(desktops.DESKTOP_ICONS_PATH, "scalable", filename)       
        icon_exists = os.path.exists(icon_path)
        
        if self.icon_desktop_image is None:
            if icon_exists:
                #self.icon_desktop_image = Gtk.Image.new_from_file(icon_path)
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icon_path, 48, 48)
                self.icon_desktop_image = Gtk.Image.new_from_pixbuf(pixbuf)
            else:
                filename = desktop.lower() + ".png"
                icon_path = os.path.join(desktops.DESKTOP_ICONS_PATH, "48x48", filename)
                icon_exists = os.path.exists(icon_path)
                if icon_exists:
                    self.icon_desktop_image = Gtk.Image.new_from_file(icon_path)
                else:
                    self.icon_desktop_image = Gtk.Image.new_from_icon_name("image-missing", Gtk.IconSize.DIALOG)

            overlay = self.ui.get_object("image_overlay")
            overlay.add_overlay(self.icon_desktop_image)
        else:
            if icon_exists:
                #self.icon_desktop_image.set_from_file(icon_path)
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icon_path, 48, 48)
                self.icon_desktop_image.set_from_pixbuf(pixbuf)                
            else:
                filename = desktop.lower() + ".png"
                icon_path = os.path.join(desktops.DESKTOP_ICONS_PATH, "48x48", filename)
                icon_exists = os.path.exists(icon_path)
                if icon_exists:
                    self.icon_desktop_image.set_from_file(icon_path)
                else:
                    self.icon_desktop_image.set_from_icon_name("image-missing", Gtk.IconSize.DIALOG)

        # set header text
        txt = _("Choose Your Desktop")
        self.header.set_subtitle(txt)

    def prepare(self, direction):
        """ Prepare screen """
        self.translate_ui(self.desktop_choice)
        self.show_all()

    def set_desktop_list(self):
        """ Set desktop list in the ListBox """
        desktop_names = []
        for desktop in self.enabled_desktops:
            desktop_names.append(desktops.NAMES[desktop])

        desktop_names.sort()

        for desktop_name in desktop_names:
            box = Gtk.HBox()

            filename = "desktop-environment-" + desktop_name.lower() + ".svg"
            icon_path = os.path.join(desktops.DESKTOP_ICONS_PATH, "scalable", filename)
            if os.path.exists(icon_path):
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icon_path, 24, 24)
                image = Gtk.Image.new_from_pixbuf(pixbuf)
                #image = Gtk.Image.new_from_file(icon_path)
            else:
                filename = desktop_name.lower() + ".png"
                icon_path = os.path.join(desktops.DESKTOP_ICONS_PATH, "24x24", filename)
                if os.path.exists(icon_path):
                    image = Gtk.Image.new_from_file(icon_path)
                else:
                    image = Gtk.Image.new_from_icon_name("image-missing", Gtk.IconSize.LARGE_TOOLBAR)
            box.pack_start(image, False, False, 2)

            label = Gtk.Label()
            label.set_markup(desktop_name)
            box.pack_start(label, False, False, 2)

            self.listbox.add(box)
            # Set Gnome as default
            if desktop_name == desktops.NAMES["gnome"]:
                self.select_default_row(desktop_name)

    def select_default_row(self, desktop_name):
        """ Selects default row
            WARNING: IF LAYOUT IS CHANGED IN desktop.ui THEN THIS SHOULD BE CHANGED ACCORDINGLY. """
        for listbox_row in self.listbox.get_children():
            for vbox in listbox_row.get_children():
                label = vbox.get_children()[1]
                if desktop_name == label.get_text():
                    self.listbox.select_row(listbox_row)
                    return

    def set_desktop(self, desktop):
        """ Show desktop info """
        for key in desktops.NAMES.keys():
            if desktops.NAMES[key] == desktop:
                self.desktop_choice = key
                self.translate_ui(self.desktop_choice)
                return

    def on_listbox_row_selected(self, listbox, listbox_row):
        """ Someone selected a different row of the listbox
            WARNING: IF LAYOUT IS CHANGED IN desktop.ui THEN THIS SHOULD BE CHANGED ACCORDINGLY. """
        if listbox_row is not None:
            for vbox in listbox_row:
                label = vbox.get_children()[1]
                desktop = label.get_text()
                self.set_desktop(desktop)
    
    def store_values(self):
        """ Store desktop """
        self.settings.set('desktop', self.desktop_choice)
        logging.info(_("Cnchi will install Antergos with the '%s' desktop"), self.desktop_choice)
        return True
    
    def scroll_to_cell(self, treeview, path):
        """ Scrolls treeview to show the desired cell """
        treeview.scroll_to_cell(path)
        return False

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message): return message

if __name__ == '__main__':
    from test_screen import _,run
    run('DesktopAsk')
