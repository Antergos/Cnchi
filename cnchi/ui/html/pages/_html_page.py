#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  _html_page.py
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

from ui.base_widgets import Page, Gtk


class HTMLPage(Page):
    """
    Base class for HTML UI pages.

    Class Attributes:
        web_view (Gtk.WebKitWebView): Object that renders the app's HTML UI.
        Also see `Page.__doc__`

    """

    def __init__(self, name='', web_view=None, *args, **kwargs):
        """
        Attributes:
            Also see `Page.__doc__`.

        Args:
            name (str):                   A name for this widget.
            web_view (Gtk.WebKitWebView): Object that renders the app's HTML UI.

        """

        super().__init__(name=name, *args, **kwargs)

        if web_view is not None and self.web_view is None:
            self.web_view = web_view

    def prepare(self, direction):
        """ This must be implemented by subclasses """
        raise NotImplementedError

    def store_values(self):
        """ This must be implemented by subclasses """
        raise NotImplementedError