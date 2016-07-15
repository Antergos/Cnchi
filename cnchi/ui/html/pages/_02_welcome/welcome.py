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


# Standard Lib
from _base_object import (
    json
)
from misc.extra import has_connection
from modules.update import UpdateModule
from ui.html.pages.html_page import HTMLPage, bg_thread


class WelcomePage(HTMLPage):
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

        self.signals.extend(['try-it-selected', 'install-it-selected', 'update-check',
                             '--update-available', 'restart', 'connection-check'])

        self._create_and_connect_signals()

    def _get_default_template_vars(self):
        signals = json.dumps(self.signals)
        return {'page_name': self.name, 'signals': signals}

    @bg_thread
    def connection_check_cb(self, *args):
        self._controller.trigger_js_event('connection-check-result', has_connection())

    def install_it_selected_cb(self, *args):
        self.go_to_next_page()

    def prepare(self):
        """ Prepare to become the current (visible) page. """
        pass

    def restart_cb(self, *args):
        self._controller.do_restart()

    def store_values(self):
        super().store_values()
        self._main_window.toggle_maximize()

    def try_it_selected_cb(self, *args):
        self._controller.exit_app()

    @bg_thread
    def update_check_cb(self, *args):
        updater = UpdateModule()

        for response in updater.do_update_check():
            self.logger.debug(response)
            if isinstance(response, str) and response.startswith('--'):
                self._controller.trigger_js_event(response)

            elif isinstance(response, dict):
                self._controller.trigger_js_event('update-check-result', response)
