#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  LanguagePage.py
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

# Standard Lib
from _base_object import (
    json,
    locale,
    os
)

# This Application
import misc.i18n as i18n
from ..ReactPage import ReactPage


class LanguagePage(ReactPage):
    """
    The first page shown when the app starts. It facilitates language selection (translations).

    Class Attributes:
        Also see `ReactPage.__doc__`

    """

    def __init__(self, name='language', index=0, *args, **kwargs):
        """
        Attributes:
            Also see `ReactPage.__doc__`.

        Args:
            name (str): A name for this widget.

        """

        super().__init__(name=name, index=index, *args, **kwargs)


        self.languages = []
        self.signals.extend(['language-selected'])

        self._initialize_page_state()
        self.set_languages_list()
        self._create_and_connect_signals()
        self.logger.debug(self._pages_state)

    def _get_default_state(self):
        state = super()._get_default_state()
        state.update({
            'languages': self.languages,
            'signals': self.signals,
            'selectedLanguage': self.selected_language
        })

        return state

    def _get_prop_names(self):
        prop_names = super()._get_prop_names()
        prop_names.extend(['languages', 'selectedLanguage'])
        return prop_names



    def prepare(self):
        """ Prepare to become the current (visible) page. """
        self._main_window.toggle_maximize()

    def store_values(self):
        super().store_values()
        self._pages_state.selected_language = self.selected_language
