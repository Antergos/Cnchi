#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# controller.py
#
# Copyright © 2013-2016 Antergos
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

""" UI Controller """

from _base_object import (
    BaseObject,
    Singleton,
    sys
)

# This Application
from ui.react.app.core.controller import ReactController


class Controller(BaseObject, metaclass=Singleton):
    """
    UI Controller

    Class Attributes:
        _emit_js_tpl (str): Javascript string used to emit signals in web_view.
        See also `BaseObject.__doc__`

    """

    _emit_js_tpl = 'window.{0} = {1}; window.cnchi.js_bridge_handler("{0}");'

    def __init__(self, name='ui_controller', *args, **kwargs):

        super().__init__(name=name, *args, **kwargs)

        # TODO: Implement external config file for all initial settings including which UI to use.
        ReactController()

    def do_restart(self):
        pass

    def exit_app(self):
        sys.exit(0)
