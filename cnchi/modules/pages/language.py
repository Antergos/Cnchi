#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  language.py
#
#  Copyright © 2013-2016 Antergos
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

from .._base_module import (
    CnchiModule,
    bg_thread,
    locale,
    os
)

# This Application
import misc.i18n as i18n


class LanguageModule(CnchiModule):

    def __init__(self, name='language_module', page_name='language'):
        super().__init__(name=name, page_name=page_name)

        self.languages = []
        self.languages_ready = False
        self.current_locale = locale.getdefaultlocale()[0]
        self.selected_language = self.settings.selected_language
        self.language_list = os.path.join(
            self.TOP_DIR,
            'data',
            'locale',
            'languagelist.txt.gz'
        )

        self._prepare_languages_list()

    def _langcode_to_lang(self, display_map):
        # Special cases in which we need the complete current_locale string
        if self.current_locale not in ('pt_BR', 'zh_CN', 'zh_TW'):
            self.current_locale = self.current_locale.split("_")[0]

        for lang, lang_code in display_map.items():
            if lang_code[1] == self.current_locale:
                return lang

    def _prepare_languages_list(self):
        """ Load languages list """
        sorted_choices = display_map = None

        try:
            (current_language,
             sorted_choices,
             display_map) = i18n.get_languages(self.language_list)
        except FileNotFoundError as file_error:
            self.logger.exception(file_error)

        current_language = self._langcode_to_lang(display_map)

        for lang in sorted_choices:
            if lang == current_language:
                self.settings.selected_language = lang

            self.languages.append(lang)

    @staticmethod
    def get_lang():
        return os.environ["LANG"].split(".")[0]

    def get_languages_cb(self, *args):
        if not self.languages:
            self._prepare_languages_list()

        self._controller.trigger_js_event('get-languages-result', self.languages)

    @staticmethod
    def get_locale():
        default_locale = locale.getdefaultlocale()
        if len(default_locale) > 1:
            return default_locale[0] + "." + default_locale[1]
        else:
            return default_locale[0]

    def language_selected_cb(self, widget, lang):
        self.logger.debug('%s language selected!', lang[0])
        self.selected_language = lang
        # TODO: Apply the selected language if its not English!
        self.can_go_to_next_page = True
        self.go_to_next_page()

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

    def prepare(self):
        pass

