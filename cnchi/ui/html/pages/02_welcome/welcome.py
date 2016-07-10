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
import json

from ui.base_widgets import Singleton
from ui.html.pages._html_page import HTMLPage
from updater import do_update_check
from misc.extra import has_connection


class WelcomePage(HTMLPage, metaclass=Singleton):
    """
    This page provides the user with a choice: (Try It or Install It).

    Class Attributes:
        Also see `HTMLPage.__doc__`

    """

    def __init__(self, name='welcome', *args, **kwargs):
        """
        Attributes:
            Also see `HTMLPage.__doc__`.

        Args:
            name (str): A name for this widget.

        """

        super().__init__(name=name, *args, **kwargs)

        self.signals.extend(['tryit-selected', 'installit-selected', 'do-update-check',
                             'update-available', 'update-result-ready', 'do-restart',
                             'do-connection-check', 'connection-check-result-ready'])

        self._create_signals()
        self._connect_signals()

    def _connect_signals(self):
        super()._connect_signals()
        self._main_window.connect('tryit-selected', self.try_it_selected_cb)
        self._main_window.connect('installit-selected', self.go_to_next_page)
        self._main_window.connect('do-update-check', self.do_update_check_cb)
        self._main_window.connect('do-restart', self._controller.do_restart)
        self._main_window.connect('do-connection-check', self.do_has_connection_check_cb)

    def _get_default_template_vars(self):
        signals = json.dumps(self.signals)
        return {'page_name': self.name, 'signals': signals}

    def do_has_connection_check_cb(self, *args):
        self._controller.run_in_new_thread(
            has_connection,
            self._controller.trigger_js_event,
            'connection-check-result-ready'
        )

    def do_update_check_cb(self, *args):
        do_update_check()

    def try_it_selected_cb(self, *args):
        self._controller.exit_app()

    def prepare(self):
        """ Prepare to become the current (visible) page. """
        pass

    def store_values(self):
        super().store_values()
        self._main_window.toggle_maximize()
