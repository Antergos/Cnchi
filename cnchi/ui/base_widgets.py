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

from _base_object import (
    Gdk,
    Gio,
    GLib,
    GObject,
    Gtk,
    WebKit2,
    BaseObject,
    DataObject,
    bg_thread
)

from _settings import NonSharedData, SharedData, settings

VERTICAL = Gtk.Orientation.VERTICAL
HORIZONTAL = Gtk.Orientation.HORIZONTAL


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)

        return cls._instance


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
            raise NotImplementedError
        else:
            self.logger.error('Unknown template engine "%s".'.format(self.tpl_engine))
            template = None

        return template

    def _maybe_load_widget(self):
        template_path = self._get_template_path()

        if not template_path or not os.path.exists(template_path):
            self.logger.debug("Cannot find %s template!", self.template)
            return

        if template_path and os.path.exists(template_path):
            path_parts = template_path.rsplit('/', 2)
            self.template = '{0}/{1}'.format(path_parts[-2], path_parts[-1])

            self.logger.debug("Loading %s template and connecting its signals", self.template)

            if 'gtkbuilder' == self.tpl_engine:
                self.ui = Gtk.Builder().new_from_file(template_path)

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

    def __init__(self, name='page', *args, **kwargs):
        """
        Attributes:
            Also see `BaseWidget.__doc__`.

        Args:
            name (str): A name for this widget.

        """

        super().__init__(name=name, *args, **kwargs)

    def _get_template_path(self):
        if 'gtkbuilder' == self.tpl_engine:
            template_path = os.path.join(self.BUILDER_DIR, '{}.ui'.format(self.name))

        elif 'jinja' == self.tpl_engine:
            page_dir = self._pages_helper.get_page_directory_name(self.name)
            template_path = os.path.join(self.PAGES_DIR, '{0}/{1}.html'.format(page_dir, self.name))
            self.logger.debug([self.name, page_dir, template_path])
        else:
            self.logger.error('Unknown template engine "%s".'.format(self.tpl_engine))
            template_path = None

        return template_path

    def prepare(self):
        """ This must be implemented by subclasses """
        raise NotImplementedError

    def store_values(self):
        """ This must be implemented by subclasses """
        raise NotImplementedError
