#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# controller.py
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

""" GTK UI Controller """

from _cnchi_object import (
    CnchiObject,
    Singleton,
)

from ui.gtk.components import MainWindow


class GTKController(CnchiObject, metaclass=Singleton):
    """
    GTK Controller

    Class Attributes:
        See also `CnchiObject.__doc__`
    """

    def __init__(self, name='controller', *args, **kwargs):
        super().__init__(name=name, *args, **kwargs)

        self.current_page = None
        self.page_names = [p for p in self.settings.install_options]

        MainWindow()

    def set_current_page(self, page):
        page.prepare()

