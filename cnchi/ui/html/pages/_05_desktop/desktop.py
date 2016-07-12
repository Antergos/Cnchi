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

# This Application
from ui.html.pages._html_page import HTMLPage


class DesktopPage(HTMLPage):
    """
    The first page shown when the app starts.

    Class Attributes:
        Also see `HTMLPage.__doc__`

    """

    def __init__(self, name='desktop', *args, **kwargs):
        """
        Attributes:
            Also see `HTMLPage.__doc__`.

        Args:
            name (str): A name for this widget.

        """

        super().__init__(name=name, *args, **kwargs)

        self.signals = []


        self._create_and_connect_signals()


    def _get_default_template_vars(self):
        signals = json.dumps(self.signals)
        return {'page_name': self.name, 'signals': signals, 'tabs_list': self._tabs_list}

    def prepare(self):
        """ Prepare to become the current (visible) page. """
        self._set_active_tab()
        # self._main_window.widget.set_position(Gtk.WindowPosition.CENTER)

    def store_values(self):
        """ This must be implemented by subclasses """
        pass
