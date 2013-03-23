#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  location.py
#  
#  Copyright 2013 Cinnarch
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
#  
#  Cinnarch Team:
#   Alex Filgueira (faidoc) <alexfilgueira.cinnarch.com>
#   Raúl Granados (pollitux) <raulgranados.cinnarch.com>
#   Gustau Castells (karasu) <karasu.cinnarch.com>
#   Kirill Omelchenko (omelcheck) <omelchek.cinnarch.com>
#   Marc Miralles (arcnexus) <arcnexus.cinnarch.com>
#   Alex Skinner (skinner) <skinner.cinnarch.com>

from gi.repository import Gtk, GLib

# Import functions
import config
import os
import log
import show_message as show
import log
import xml.etree.ElementTree as etree

_next_page = "check"
_prev_page = "language"

class Location(Gtk.Box):
    def __init__(self, params):
        self.title = params['title']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        self.settings = params['settings']

        super().__init__()

        self.ui = Gtk.Builder()

        self.ui.add_from_file(os.path.join(self.ui_dir, "location.ui"))

        self.ui.connect_signals(self)

        self.treeview = self.ui.get_object("treeview_countries")
        self.label_choose_country = self.ui.get_object("label_choose_country")
        self.label_help = self.ui.get_object("label_help")

        self.treeview_items = 0
        
        self.create_toolview()
        
        self.load_locales()
        
        super().add(self.ui.get_object("location"))

    def translate_ui(self):
        txt = _("Select your location")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.title.set_markup(txt)
        
        txt = _("The selected location will be used to help select the system locale.\n" \
            "Normally this should be the country where you live.\n" \
            "This is a shortlist of locations based on the language you selected.")
        self.label_help.set_markup(txt)
        
        txt = _("Country, territory or area:")
        txt = "<span weight='bold'>%s</span>" % txt
        self.label_choose_country.set_markup(txt)
        
    def create_toolview(self):
        render = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn("", render, text=0)
        liststore = Gtk.ListStore(str)
        self.treeview.append_column(col)
        self.treeview.set_model(liststore)
        self.treeview.set_headers_visible(False)
        
    def select_first_treeview_item(self):
        model = self.treeview.get_model()
        treeiter = model.get_iter(0)
        self.treeview.set_cursor(0)
        path = model.get_path(treeiter)
        GLib.idle_add(self.scroll_to_cell, self.treeview, path)

    def scroll_to_cell(self, treeview, path):
        treeview.scroll_to_cell(path)
        return False

    def hide_all(self):
        names = [ "location_box", "label_help", "label_choose_country", \
                     "box1", "eventbox1", "eventbox2", "scrolledwindow1", \
                     "treeview_countries" ]
        for name in names:
            control = self.ui.get_object(name)
            if control != None:
                control.hide()

    def prepare(self, direction):
        self.hide_all()
        self.fill_treeview()
        
        if self.treeview_items == 1:
            # If we have only one option, don't bother our beloved user
            self.store_values()
            if direction == 'forwards':
                GLib.idle_add(self.forward_button.clicked)
            else:
                GLib.idle_add(self.backwards_button.clicked)
        else:
            self.select_first_treeview_item()
            self.translate_ui()       
        
        # If I don't do this, check page is not shown well when skipping this page (location)
        # If I do this, we can see location page for a second (it's ugly)
        self.show_all()
        
    def load_locales(self):
        data_dir = self.settings.get("DATA_DIR")  
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

    def fill_treeview(self):
        lang_code = self.settings.get("language_code")
        areas = []
        for locale_name in self.locales:
            if lang_code in locale_name:
                areas.append(self.locales[locale_name])
        liststore = self.treeview.get_model()
        liststore.clear()
        
        # FIXME: What do we have to do when can't find any country?
        # Right now we put them all!
        # I've observed this with Esperanto and Asturianu at least.
        if len(areas) == 0:
            for locale_name in self.locales:
                areas.append(self.locales[locale_name])

        self.treeview_items = len(areas)
        
        for area in areas:
            liststore.append([area])
            

    def store_values(self):
        selected = self.treeview.get_selection()
        if selected:
            (ls, iter) = selected.get_selected()
            if iter:
                country = ls.get_value(iter, 0)
                lang_code = self.settings.get("language_code")
                for mylocale in self.locales:
                    if self.locales[mylocale] == country:
                        self.settings.set("locale", mylocale)
                        try:
                            import locale
                            locale.setlocale(locale.LC_ALL, mylocale)
                            log.debug(_("locale changed to : %s") % mylocale)
                        except (ImportError, locale.Error):
                            log.debug(_("Can't change to locale '%s'") % mylocale)
        return True

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page
