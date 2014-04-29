#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  location.py
#
#  Copyright 2013 Antergos
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

from gi.repository import Gtk, GLib

# Import functions
import config
import os
import logging
import show_message as show
import xml.etree.ElementTree as etree

from gtkbasebox import GtkBaseBox

class Location(GtkBaseBox):
    def __init__(self, params):

        self.next_page = "timezone"
        self.prev_page = "check"

        super().__init__(params, "location")

        self.ui.connect_signals(self)

        self.listbox = self.ui.get_object("listbox")
        self.listbox.connect("row-selected", self.on_listbox_row_selected)
        self.listbox.set_selection_mode(Gtk.SelectionMode.BROWSE)

        self.label_choose_country = self.ui.get_object("label_choose_country")
        self.label_help = self.ui.get_object("label_help")

        self.listbox_items = 0

        self.load_locales()

        self.selected_country = ""

        self.add(self.ui.get_object("location"))

    def translate_ui(self):
        txt = _("The location you select will be used to help determine the system locale.\n" \
            "This should normally be the country in which you reside.\n" \
            "Here is a shortlist of locations based on the language you selected.")
        self.label_help.set_markup(txt)

        txt = _("Country, territory or area:")
        txt = "<span weight='bold'>%s</span>" % txt
        self.label_choose_country.set_markup(txt)

        self.header.set_subtitle(_("Select your location"))

    def select_first_listbox_item(self):
        listbox_row = self.listbox.get_children()[0]
        self.listbox.select_row(listbox_row)

    def hide_all(self):
        names = [ "location_box", "label_help", "label_choose_country", \
                     "box1", "eventbox1", "eventbox2", "scrolledwindow1", \
                     "listbox_countries" ]

        for name in names:
            control = self.ui.get_object(name)
            if control != None:
                control.hide()

    def prepare(self, direction):
        self.hide_all()
        self.fill_listbox()

        if self.listbox_items == 1:
            # If we have only one option, don't bother our beloved user
            self.store_values()
            if direction == 'forwards':
                GLib.idle_add(self.forward_button.clicked)
            else:
                GLib.idle_add(self.backwards_button.clicked)

            while Gtk.events_pending():
                Gtk.main_iteration()
        else:
            self.select_first_listbox_item()
            self.translate_ui()
            self.show_all()

        # Enable forward button
        # If timezone does not work, forward button is disabled. If user doesn't choose timezone and
        # goes back to this screen, forward button will still be disabled.
        self.forward_button.set_sensitive(True)
            

    def load_locales(self):
        data_dir = self.settings.get('data')
        xml_path = os.path.join(data_dir, "locales.xml")

        self.locales = {}

        tree = etree.parse(xml_path)
        root = tree.getroot()
        for child in root.iter("language"):
            for item in child:
                if item.tag == 'language_name':
                    language_name = item.text
                elif item.tag == 'locale_name':
                    locale_name = item.text
            self.locales[locale_name] = language_name

        xml_path = os.path.join(data_dir, "iso3366-1.xml")

        countries = {}

        tree = etree.parse(xml_path)
        root = tree.getroot()
        for child in root:
            code = child.attrib['value']
            name = child.text
            countries[code] = name

        for locale_name in self.locales:
            language_name = self.locales[locale_name]
            for country_code in countries:
                if country_code in language_name:
                    self.locales[locale_name] = self.locales[locale_name] + ", " + countries[country_code]

    def fill_listbox(self):
        lang_code = self.settings.get("language_code")
        areas = []
        for locale_name in self.locales:
            if lang_code in locale_name:
                areas.append(self.locales[locale_name])

        # FIXME: What do we have to do when can't find any country?
        # Right now we put them all!
        # I've observed this with Esperanto and Asturianu at least.
        if len(areas) == 0:
            for locale_name in self.locales:
                areas.append(self.locales[locale_name])

        self.listbox_items = len(areas)

        areas.sort()

        # Delete listbox previous contents (if any)
        for listbox_row in self.listbox.get_children():
            listbox_row.destroy()

        for area in areas:
            box = Gtk.VBox()
            label = Gtk.Label()
            label.set_markup(area)
            label.set_alignment(0, 0.5)
            box.add(label)
            self.listbox.add(box)
            #self.select_default_row(current_language)

        self.selected_country = areas[0]

    def on_listbox_row_selected(self, listbox, listbox_row):
        if listbox_row is not None:
            vbox = listbox_row.get_children()[0]
            label = vbox.get_children()[0]
            self.selected_country = label.get_text()

    def store_values(self):
        country = self.selected_country
        lang_code = self.settings.get("language_code")
        for mylocale in self.locales:
            if self.locales[mylocale] == country:
                self.settings.set("locale", mylocale)
                try:
                    import locale
                    locale.setlocale(locale.LC_ALL, mylocale)
                    logging.info(_("locale changed to : %s") % mylocale)
                except (ImportError, locale.Error):
                    logging.warning(_("Can't change to locale '%s'") % mylocale)

        return True

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message): return message

if __name__ == '__main__':
    from test_screen import _,run
    run('Location')
