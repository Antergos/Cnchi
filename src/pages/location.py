#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  location.py
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

""" Location screen """

# Import functions
import os
import logging
import sys
import locale
import re

import defusedxml.cElementTree as elementTree

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from pages.gtkbasebox import GtkBaseBox
from logging_utils import ContextFilter

import geoip

class Location(GtkBaseBox):
    """ Location page """
    def __init__(self, params, prev_page="check", next_page="timezone"):
        super().__init__(self, params, "location", prev_page, next_page)

        self.listbox = self.gui.get_object("location-listbox")
        self.listbox.set_name("location-listbox")
        self.listbox.connect("row-selected", self.on_listbox_row_selected)
        self.listbox.set_selection_mode(Gtk.SelectionMode.BROWSE)

        self.label_choose_country = self.gui.get_object("label_choose_country")
        self.label_choose_country.set_name("location-label-choose-country")
        self.label_help = self.gui.get_object("label_help")
        self.label_help.set_name("location-label-help")

        self.locales = {}
        self.load_locales()

        self.geoip_country = None
        self.selected_country = ""

        self.show_all_locations = False

        button = self.gui.get_object("show_all_locations_checkbutton")
        button.set_name("location-checkbutton-show-all-locations")
        button.connect("toggled", self.all_locations_toggled, "")

        self.scrolledwindow = self.gui.get_object("scrolledwindow1")

    def all_locations_toggled(self, button, _name):
        """ Force to show all locations """
        self.show_all_locations = button.get_active()
        self.fill_listbox()
        if not self.show_all_locations:
            self.select_detected_country()

    def translate_ui(self):
        """ Translates all ui elements """
        par1 = _("The location you select will be used to help determine the "
                 "system locale. It should normally be the country in which "
                 "you reside.")
        par2 = _("Please, note that your system language will be "
                 "determined from this selection.")
        par3 = _("Here is a shortlist of locations based on the language you "
                 "selected for this installer (click on show all locations "
                 "to show them all).")
        txt = "{0}\n\n<b>{1}</b>\n\n{2}".format(par1, par2, par3)
        self.label_help.set_markup(txt)
        self.label_help.set_name("location-label-help")

        txt = _("Country, territory or area:")
        txt = "<span weight='bold'>{0}</span>".format(txt)
        self.label_choose_country.set_markup(txt)

        check = self.gui.get_object('show_all_locations_checkbutton')
        txt = _("Show all locations")
        check.set_label(txt)

        self.header.set_subtitle(_("Select your location"))

    def select_first_listbox_item(self):
        """ Sets first listbox item as selected """
        listbox_row = self.listbox.get_children()[0]
        self.listbox.select_row(listbox_row)

    def select_detected_country(self):
        """ Selects listbox item that matches detected country using GeoIP database """
        if not self.geoip_country:
            logging.debug("Getting your country using GeoIP database")
            self.geoip_country = geoip.GeoIP().get_country()
        if self.geoip_country:
            names = self.geoip_country.names
            #logging.debug(names)
            for listbox_row in self.listbox.get_children():
                label = listbox_row.get_children()[0]
                if label is not None:
                    label = label.get_text()
                    for name in names.values():
                        if name in label:
                            self.selected_country = label
                            self.listbox.select_row(listbox_row)
                            return
            self.select_first_listbox_item()
        else:
            self.select_first_listbox_item()

    def hide_all(self):
        """ Hide all widgets """
        names = [
            "location_box", "label_help", "label_choose_country", "box1",
            "eventbox1", "eventbox2", "scrolledwindow1", "listbox_countries"]

        for name in names:
            control = self.gui.get_object(name)
            if control is not None:
                control.hide()

    def prepare(self, direction):
        """ Prepare dialog for showing """
        self.hide_all()

        self.fill_listbox()
        self.select_detected_country()
        self.translate_ui()
        self.forward_button.set_sensitive(True)

        self.show_all()

        self.settings.set('install_id', self.get_and_save_install_id())

    def load_locales(self):
        """ Load all locales from locales.xml """
        data_dir = self.settings.get('data')
        xml_path = os.path.join(data_dir, "locale", "locales.xml")

        self.locales = {}

        try:
            tree = elementTree.parse(xml_path)
        except FileNotFoundError as file_error:
            logging.error(file_error)
            sys.exit(1)

        root = tree.getroot()
        locale_name = ""
        language_name = ""
        for child in root.iter("language"):
            for item in child:
                if item.tag == 'language_name':
                    language_name = item.text
                elif item.tag == 'locale_name':
                    locale_name = item.text
            if locale_name and language_name:
                self.locales[locale_name] = language_name

        xml_path = os.path.join(data_dir, "locale", "iso3366-1.xml")

        countries = {}

        try:
            tree = elementTree.parse(xml_path)
        except FileNotFoundError as file_error:
            logging.error(file_error)
            sys.exit(1)

        root = tree.getroot()
        for child in root:
            code = child.attrib['value']
            name = child.text
            countries[code] = name

        for locale_name in self.locales:
            language_name = self.locales[locale_name]
            for country_code in countries:
                if country_code in language_name:
                    self.locales[locale_name] = self.locales[locale_name] + \
                        ", " + countries[country_code]

    def get_areas(self):
        """ Get all territories where a certain language is spoken """
        areas = []

        if not self.show_all_locations:
            lang_code = self.settings.get("language_code")
            for locale_name in self.locales:
                if lang_code in locale_name:
                    areas.append(self.locales[locale_name])
            if not areas:
                # When we don't find any country we put all language codes.
                # This happens with Esperanto and Asturianu at least.
                for locale_name in self.locales:
                    areas.append(self.locales[locale_name])
        else:
            # Put all language codes (forced by the checkbox)
            for locale_name in self.locales:
                areas.append(self.locales[locale_name])

        areas.sort()

        return areas

    def fill_listbox(self):
        """ Fills listbox with all territories (areas) """
        areas = self.get_areas()

        for listbox_row in self.listbox.get_children():
            listbox_row.destroy()

        for area in areas:
            label = Gtk.Label.new()
            label.set_markup(area)
            label.show_all()
            self.listbox.add(label)

        self.selected_country = areas[0]

    def on_listbox_row_selected(self, _listbox, listbox_row):
        """ A territory (area) has been selected """
        if listbox_row is not None:
            label = listbox_row.get_children()[0]
            if label is not None:
                self.selected_country = label.get_text()

    def set_locale(self, mylocale):
        """ Sets system locale """
        self.settings.set("locale", mylocale)

        # LANG=en_US.UTF-8
        locale_vars = [
            locale.LC_CTYPE,
            locale.LC_NUMERIC,
            locale.LC_TIME,
            locale.LC_COLLATE,
            locale.LC_MONETARY,
            locale.LC_MESSAGES]

        try:
            locale.setlocale(locale.LC_ALL, mylocale)
        except locale.Error as err:
            logging.debug('Unable to set locale for all categories at once.')
            try:
                for var in locale_vars:
                    locale.setlocale(var, mylocale)
                logging.debug("Locale changed to : %s", mylocale)
            except locale.Error as err:
                logging.warning(
                    "Cannot change to locale '%s': %s", mylocale, err)
                if mylocale.endswith(".UTF-8"):
                    # Try without the .UTF-8 trailing
                    mylocale = mylocale[:-len(".UTF-8")]
                    try:
                        for var in locale_vars:
                            locale.setlocale(var, mylocale)
                        logging.debug("Locale changed to : %s", mylocale)
                        self.settings.set("locale", mylocale)
                    except locale.Error as err:
                        logging.warning(
                            "Cannot change to locale '%s': %s",
                            mylocale,
                            err)
                else:
                    logging.warning("Cannot change to locale '%s'", mylocale)

    def store_values(self):
        """ Store user choices """
        location = self.selected_country
        logging.debug("Selected location: %s", location)
        self.settings.set('location', location)
        for mylocale in self.locales:
            if self.locales[mylocale] == location:
                self.set_locale(mylocale)
        if ',' in location:
            country_name = location.split(',')[1].strip()
            match = re.search(r'\(\w+\)', location)
            if match:
                country_code = match.group()[1:-1].lower()
            else:
                logging.error(
                    _("Can't get country code from %s location"),
                    location)
                country_code = 'us'
        else:
            country_name = 'USA'
            country_code = 'us'
        logging.debug("Selected country name: %s", country_name)
        logging.debug("Selected country code: %s", country_code)
        self.settings.set('country_name', country_name)
        self.settings.set('country_code', country_code)
        return True

    @staticmethod
    def get_and_save_install_id():
        """ Obtains and saves an installation ID for future reference """
        context_filter = ContextFilter()
        return context_filter.get_and_save_install_id(is_location_screen=True)


# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message
