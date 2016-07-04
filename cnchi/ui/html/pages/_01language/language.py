#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  welcome.py
#
#  Copyright © 2016 Antergos
#
#  This file is part of The Antergos Build Server, (AntBS).
#
#  AntBS is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  AntBS is distributed in the hope that it will be useful,
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
#  along with AntBS; If not, see <http://www.gnu.org/licenses/>.

import os
import locale
import gettext

from ui.base_widgets import Singleton
from ui.html.pages._html_page import HTMLPage
import misc.i18n as i18n


class LanguagePage(HTMLPage, metaclass=Singleton):
    """
    The first page shown when the app starts. It facilitates language selection (translations).

    Class Attributes:
        Also see `HTMLPage.__doc__`

    """

    def __init__(self, name='language', *args, **kwargs):
        """
        Attributes:
            Also see `HTMLPage.__doc__`.

        Args:
            name (str): A name for this widget.

        """

        super().__init__(name=name, *args, **kwargs)

        self.current_locale = locale.getdefaultlocale()[0]
        self.language_list = os.path.join(
            self.settings.data,
            'locale',
            'languagelist.txt.gz'
        )
        self.set_languages_list()

    def get_lang(self):
        return os.environ["LANG"].split(".")[0]

    def get_locale(self):
        default_locale = locale.getdefaultlocale()
        if len(default_locale) > 1:
            return default_locale[0] + "." + default_locale[1]
        else:
            return default_locale[0]

    def langcode_to_lang(self, display_map):
        # Special cases in which we need the complete current_locale string
        if self.current_locale not in ('pt_BR', 'zh_CN', 'zh_TW'):
            self.current_locale = self.current_locale.split("_")[0]

        for lang, lang_code in display_map.items():
            if lang_code[1] == self.current_locale:
                return lang

    def set_language(self, locale_code):
        if not locale_code:
            locale_code, encoding = locale.getdefaultlocale()

        # os.environ["LANG"] = locale_code
        #
        # try:
        #     lang = gettext.translation(APP_NAME, LOCALE_DIR, [locale_code])
        #     lang.install()
        #     self.translate_ui()
        # except IOError:
        #     logging.warning(
        #         "Can't find translation file for the %s language",
        #         locale_code)

    def set_languages_list(self):
        """ Load languages list """
        sorted_choices = display_map = None

        try:
            (current_language,
             sorted_choices,
             display_map) = i18n.get_languages(self.language_list)
        except FileNotFoundError as file_error:
            self.logger.exception(file_error)

        current_language = self.langcode_to_lang(display_map)

        for lang in sorted_choices:
            box = Gtk.VBox()
            label = Gtk.Label()
            label.set_markup(lang)
            box.add(label)
            self.listbox.add(box)
            if current_language == lang:
                self.select_default_row(current_language)


    def prepare(self):
        """ Prepare to become the current (visible) page. """
        self._main_window.toggle_maximize()

    def store_values(self):
        """ This must be implemented by subclasses """
        raise NotImplementedError
