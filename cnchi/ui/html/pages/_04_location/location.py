#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  location.py
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
    os,
    json
)

from ui.html.pages.html_page import HTMLPage
from modules.location import LocationModule


class LocationPage(HTMLPage):
    """
    The first page shown when the app starts.

    Class Attributes:
        Also see `HTMLPage.__doc__`

    """

    def __init__(self, name='location', *args, **kwargs):
        """
        Attributes:
            Also see `HTMLPage.__doc__`.

        Args:
            name (str): A name for this widget.

        """

        super().__init__(name=name, *args, **kwargs)

        self._module = None
        self.locations = None
        self.locations_items = []
        self.signals.extend(['show-all-locations'])
        self.tabs.extend([
            (_('Location'), True),
            (_('Keyboard Layout'), False),
            (_('Timezone'), False)
        ])

        self._create_and_connect_signals()
        self._initialize_page_data()

    def _get_default_template_vars(self):
        signals = json.dumps(self.signals)
        tpl_vars = super()._get_default_template_vars()
        tpl_vars.update({'signals': signals, 'tabs': self.tabs, 'locations': self.locations_items})
        self.logger.debug(tpl_vars)

        return tpl_vars

    def _get_initial_page_data(self):
        return {
            'show_all_locations': False
        }

    def prepare(self):
        """ Prepare to become the current (visible) page. """
        self._module = LocationModule()
        self.locations = info = self._module.get_location_collection_items()
        self.logger.debug(self.locations)
        self.logger.debug(info)
        self.locations_items = info

    def store_values(self):
        """ This must be implemented by subclasses """
        raise NotImplementedError

    def show_all_locations_cb(self, *args):
        self.logger.debug("SHOW ALL LOCATIONS ********************+")
