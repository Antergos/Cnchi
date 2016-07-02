#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  base_widget.py
#
#  Copyright © 2016 Antergos
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


import os

from _base_object import Gdk, Gio, GLib, Gtk, BaseObject, WebKit2

from _settings import NonSharedData, SharedData, settings

VERTICAL = Gtk.Orientation.VERTICAL
HORIZONTAL = Gtk.Orientation.HORIZONTAL


class BaseWidget(BaseObject):
    """
    Base class for all of Cnchi's UI classes.

    Class Attributes:
        See Also `BaseObject.__doc__`

    """

    _page_dirs = []

    def __init__(self, name='base_widget', *args, **kwargs):
        """
        Attributes:
            See Also `BaseObject.__doc__`

        """

        super().__init__(name=name, *args, **kwargs)

        self._maybe_load_widget()

    def _get_template_path(self):
        if 'gtkbuilder' == self.tpl_engine:
            template = os.path.join(self.BUILDER_DIR, '{}.ui'.format(self.name))

        elif 'jinja' == self.tpl_engine:
            page_dir = self._get_page_directory_name()
            template = os.path.join(self.JINJA_DIR, '{0}/{1}.html'.format(page_dir, self.name))
        else:
            self.logger.error('Unknown template engine "%s".'.format(self.tpl_engine))
            template = None

        return template

    def _get_page_directory_name(self, name=None):
        name = name if name is not None else self.name

        if not self._page_dirs:
            self._page_dirs.extend(os.listdir(os.path.join(self.UI_DIR, 'html/pages')))

        res = [d for d in self._page_dirs if '-{}'.format(name) in d]

        return '' if not res else res[0]

    def _get_page_names(self):
        return [n.split('-', 1)[1] for n in self._page_dirs if '_' not in n]

    def _maybe_load_widget(self):
        template = self._get_template_path()

        if not template or not os.path.exists(template):
            self.logger.warning("Cannot find %s template!", self.template)
            return

        if template and os.path.exists(template):
            self.template = template

            self.logger.debug("Loading %s template and connecting its signals", self.template)

            if 'gtkbuilder' == self.tpl_engine:
                self.ui = Gtk.Builder().new_from_file(self.template)

                # Connect UI signals
                self.ui.connect_signals(self)

                self.widget = self.ui.get_object(self.name)

            elif 'jinja' == self.tpl_engine:
                pass

    def get_ancestor_window(self):
        """ Returns first ancestor that is a Gtk Window """
        return self.widget.get_ancestor(Gtk.Window)


class Stack(BaseWidget):
    """
    Base class for page stacks (not used for HTML UI).

    Class Attributes:
        See `BaseWidget.__doc__`

    """

    def __init__(self, name='stack', *args, **kwargs):
        """
        Attributes:
            Also see `BaseWidget.__doc__`.

        Args:
            name (str): A name for this widget.

        """

        super().__init__(name=name, *args, **kwargs)


class Page(BaseWidget):
    """
    Base class for pages.

    Class Attributes:
        _page_data (NonSharedData): Data storage for `Page` objects.
        Also see `BaseWidget.__doc__`

    """

    def __init__(self, _name='page', *args, **kwargs):
        """
        Attributes:
            Also see `BaseWidget.__doc__`.

        Args:
            name (str): A name for this widget.

        """

        super().__init__(_name=_name, *args, **kwargs)

    def prepare(self, direction):
        """ This must be implemented by subclasses """
        raise NotImplementedError

    def store_values(self):
        """ This must be implemented by subclasses """
        raise NotImplementedError
