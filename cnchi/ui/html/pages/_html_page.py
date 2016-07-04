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

import os
from gettext import gettext

from jinja2 import Environment, FileSystemLoader, PrefixLoader

from ui.base_widgets import SharedData, Page


class HTMLPage(Page):
    """
    Base class for HTML UI pages.

    Class Attributes:
        _tpl (SharedData): Descriptor object that handles access to Jinja2 template environment.
        Also see `Page.__doc__`

    """

    _tpl = SharedData('_tpl')
    _tpl_setup_running = SharedData('_tpl_setup_running')

    def __init__(self, name='HTMLPage', tpl_engine='jinja', *args, **kwargs):
        """
        Attributes:
            _tpl (Environment): The Jinja2 template environment.
            Also see `Page.__doc__`.

        Args:
            name (str): A name for this widget.

        """

        super().__init__(name=name, tpl_engine=tpl_engine, *args, **kwargs)

        if self._tpl is None and self._tpl_setup_running is None:
            self._tpl_setup_running = True
            self._initialize_template_engine()

    def emit_js(self, name, *args):
        """ See `Controller.emit_js.__doc__` """
        self._controller.emit_js(name, *args)

    def _initialize_template_engine(self):
        tpl_map = {
            pdir: FileSystemLoader(os.path.join(self.PAGES_DIR, pdir)) for pdir in self._page_dirs
        }
        tpl_map['base'] = FileSystemLoader(self.PAGES_DIR)
        self._tpl = Environment(loader=PrefixLoader(tpl_map))
        self._tpl.globals['_'] = gettext

    def prepare(self):
        """ This must be implemented by subclasses """
        pass

    def render_template(self, name=None, tpl_vars=None):
        name = name if name is not None else self.template
        tpl_vars = tpl_vars if tpl_vars is not None else dict()
        tpl = self._tpl.get_template(name)
        return tpl.render(tpl_vars)

    def render_template_as_bytes(self, name=None, tpl_vars=None):
        tpl = self.render_template(name=name, tpl_vars=tpl_vars)
        return tpl.encode('UTF-8')

    def store_values(self):
        """ This must be implemented by subclasses """
        raise NotImplementedError
