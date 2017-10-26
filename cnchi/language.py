#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  language.py
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


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import gettext
import locale
import os
import logging
import sys

from gtkbasebox import GtkBaseBox

import misc.i18n as i18n

from proxy import ProxyDialog

# Useful vars for gettext (translations)
APP_NAME = "cnchi"
LOCALE_DIR = "/usr/share/locale"


class Language(GtkBaseBox):
    def __init__(self, params, prev_page="welcome", next_page="check"):
        super().__init__(self, params, "language", prev_page, next_page)

        # Set up list box
        self.listbox = self.ui.get_object("listbox")
        self.listbox.connect("row-selected", self.on_listbox_row_selected)
        self.listbox.set_selection_mode(Gtk.SelectionMode.BROWSE)

        data_dir = self.settings.get('data')

        self.current_locale = locale.getdefaultlocale()[0]
        self.language_list = os.path.join(
            data_dir,
            "locale",
            "languagelist.txt.gz")
        self.set_languages_list()

        image1 = self.ui.get_object("image1")
        image1.set_from_file(os.path.join(data_dir, "images/languages.png"))

        label = self.ui.get_object("welcome_label")
        label.set_name("WelcomeMessage")

        self.main_window = params['main_window']

    def get_lang(self):
        return os.environ["LANG"].split(".")[0]

    def get_locale(self):
        default_locale = locale.getdefaultlocale()
        if len(default_locale) > 1:
            return default_locale[0] + "." + default_locale[1]
        else:
            return default_locale[0]

    def on_listbox_row_selected(self, listbox, listbox_row):
        """ Someone selected a different row of the listbox """
        if listbox_row is not None:
            for vbox in listbox_row:
                for label in vbox.get_children():
                    (current_language,
                        sorted_choices,
                        display_map) = i18n.get_languages(self.language_list)
                    lang = label.get_text()
                    lang_code = display_map[lang][1]
                    self.set_language(lang_code)

    def translate_ui(self):
        """ Translates all ui elements """
        txt_bold = _("Notice: The Cnchi Installer is beta software.")
        # FIXME: Can't use an a html tag in the label
        # (as we're running as root)
        txt = _("<span weight='bold'>{0}</span>\n\n"
                "Cnchi is pre-release beta software that is under active "
                "development. It does not yet properly handle RAID, btrfs "
                "subvolumes, or other advanced setups. Please proceed with "
                "caution as data loss is possible!\n\n"
                "If you find any bugs, please report them at "
                "<a href='{1}'>{1}</a>")
        url = "http://bugs.antergos.com"
        txt = txt.format(txt_bold, url)
        label = self.ui.get_object("welcome_label")
        label.set_markup(txt)

        label.set_hexpand(False)
        label.set_line_wrap(True)
        label.set_max_width_chars(50)

        # a11y
        label.set_can_focus(False)

        txt = _("Choose your language")
        self.header.set_subtitle(txt)

    def langcode_to_lang(self, display_map):
        # Special cases in which we need the complete current_locale string
        if self.current_locale not in ('pt_BR', 'zh_CN', 'zh_TW'):
            self.current_locale = self.current_locale.split("_")[0]

        for lang, lang_code in display_map.items():
            if lang_code[1] == self.current_locale:
                return lang

    def set_languages_list(self):
        """ Load languages list """
        try:
            (current_language,
                sorted_choices,
                display_map) = i18n.get_languages(self.language_list)
        except FileNotFoundError as file_error:
            logging.error(file_error)
            sys.exit(1)

        current_language = self.langcode_to_lang(display_map)
        for lang in sorted_choices:
            box = Gtk.VBox()
            label = Gtk.Label()
            label.set_markup(lang)
            box.add(label)
            self.listbox.add(box)
            if current_language == lang:
                self.select_default_row(current_language)

    def set_language(self, locale_code):
        if locale_code is None:
            locale_code, encoding = locale.getdefaultlocale()

        if 'en' == locale_code:
            # Perl expects LANG to be in this format, otherwise it complains which
            # messes up the keyboard widget.
            locale_code = language = 'en_US.UTF-8'
        else:
            language = '{}.UTF-8:en_US.UTF-8'.format(locale_code)

        os.environ['LANG'] = locale_code
        os.environ['LANGUAGE'] = language

        try:
            lang = gettext.translation(APP_NAME, LOCALE_DIR, [locale_code])
            lang.install()
            self.translate_ui()
        except IOError:
            logging.warning(
                "Can't find translation file for the %s language",
                locale_code)

    def select_default_row(self, language):
        for listbox_row in self.listbox.get_children():
            for vbox in listbox_row.get_children():
                label = vbox.get_children()[0]
                if language == label.get_text():
                    self.listbox.select_row(listbox_row)
                    return

    def store_values(self):
        lang = ""
        listbox_row = self.listbox.get_selected_row()
        if listbox_row is not None:
            for vbox in listbox_row:
                for label in vbox.get_children():
                    lang = label.get_text()

        (current_language,
            sorted_choices,
            display_map) = i18n.get_languages(self.language_list)

        if lang:
            self.settings.set("language_name", display_map[lang][0])
            self.settings.set("language_code", display_map[lang][1])
            logging.debug("language_name: %s", display_map[lang][0])
            logging.debug("language_code: %s", display_map[lang][1])

        return True

    def prepare(self, direction):
        self.translate_ui()
        # Enable forward button
        self.forward_button.set_sensitive(True)
        self.show_all()

        # a11y
        self.listbox.set_can_default(True)
        self.main_window.set_default(self.listbox)

    def on_setup_proxy(self, widget, data=None):
        """ Ask for proxy settings """

        dlg = ProxyDialog(
            self.get_main_window(),
            self.settings.get('proxies'),
            self.settings.get('use_same_proxy_for_all_protocols'),
            self.ui_dir)

        response = dlg.run()

        if response == Gtk.ResponseType.APPLY:
            self.settings.set(
                'use_same_proxy_for_all_protocols',
                dlg.get_use_same_proxy_for_all_protocols())
            proxies = dlg.get_proxies()
            if proxies:
                self.settings.set('proxies', proxies)
                logging.debug("Will use these proxy settings: %s", proxies)

        dlg.destroy()


# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

if __name__ == '__main__':
    from test_screen import _, run

    run('Language')
