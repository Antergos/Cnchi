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

        self.treeview = self.ui.get_object("treeview1")
        self.label1 = self.ui.get_object("label1")
        self.label2 = self.ui.get_object("label2")
        self.label3 = self.ui.get_object("label3")

        self.create_toolview()
        
        self.load_locales()

        super().add(self.ui.get_object("location"))

    def translate_ui(self):
        txt = _("Select your location")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.title.set_markup(txt)
        
        txt = _("The selected location will be used to help select the system locale. Normally this should be the country where you live")
        self.label1.set_markup(txt)
        
        txt = _("This is a shortlist of locations based on the language you selected.")
        self.label2.set_markup(txt)
        
        txt = _("Country, territory or area:")
        self.label3.set_markup(txt)

    def create_toolview(self):
        render = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn("", render, text=0)
        liststore = Gtk.ListStore(str)
        self.treeview.append_column(col)
        self.treeview.set_model(liststore)

    def prepare(self):
        self.translate_ui()
        self.fill_treeview()
        self.translate_ui()
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
            #print("self.locales[%s]=%s" % (locale_name.encode('utf-8'), language_name.encode('utf-8')))
            
        xml_path = os.path.join(data_dir, "iso3366-1.xml")
        
        countries = {}
        
        tree = etree.parse(xml_path)
        root = tree.getroot()
        for child in root:
            code = child.attrib['value']
            #print (child.text.encode('utf-8'))
            name = child.text
            countries[code] = name
            #print("countries[%s] = %s" % (code, name.encode('utf-8')))
            
        for locale_name in self.locales:
            language_name = self.locales[locale_name]
            for country_code in countries:
                if country_code in language_name:
                    self.locales[locale_name] = self.locales[locale_name] + ", " + countries[country_code]
                    #print("self.locales[%s]=%s" % (locale_name, self.locales[locale_name].encode('utf-8')))

    def fill_treeview(self):
        lang_code = self.settings.get("language_code")
        areas = []
        for locale_name in self.locales:
            if lang_code in locale_name:
                areas.append(self.locales[locale_name])
        liststore = self.treeview.get_model()
        liststore.clear()
        for area in areas:
            liststore.append([area])

    def store_values(self):
        selected = self.treeview.get_selection()
        if selected:
            (ls, iter) = selected.get_selected()
            if iter:
                country = ls.get_value(iter, 0)
                lang_code = self.settings.get("language_code")
                for locale in self.locales:
                    if self.locales[locale] == country:
                        self.settings.set("locale", locale)
                        #print("Setting locale to %s" % locale)
        return True

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page
