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


# Standard Lib
from _cnchi_object import (
    json,
    os
)

# 3rd-party Libs
from _cnchi_object import (
    Gdk,
    Gio,
    GLib,
    GObject,
    Gtk,
    WebKit2
)

# This application
from _cnchi_object import (
    CnchiObject,
    bg_thread,
    DataObject,
    NonSharedData,
    SharedData,
    Singleton
)


class CnchiWidget(CnchiObject):
    """
    Base class for UI classes that have a corresponding toolkit-specific widget instance which is
    accessible via the class's `widget` attribute.

    Class Attributes:
        widget (NonSharedData):   Descriptor that provides access to the toolkit-specific widget
                                  instance for this object.

        See Also `CnchiObject.__doc__`

    """

    widget = NonSharedData('widget')

    def __init__(self, name='base_widget', *args, **kwargs):
        """
        Attributes:
            See Also `CnchiObject.__doc__`

        """

        super().__init__(name=name, *args, **kwargs)

        self._maybe_load_widget()

    def _get_template_path(self):
        if 'gtkbuilder' == self.tpl_engine:
            template = os.path.join(self.TPL_DIR, '{}.ui'.format(self.name))
        else:
            self.logger.debug('Unknown template engine "%s".'.format(self.tpl_engine))
            template = None

        return template

    def _maybe_load_widget(self):
        if not self.tpl_engine:
            return

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

    def get_ancestor_window(self):
        """ Returns first ancestor that is a Gtk Window """
        return self.widget.get_ancestor(Gtk.Window)


class Page(CnchiWidget):
    """
    Base class for pages.

    Class Attributes:
        Also see `CnchiWidget.__doc__`

    """

    def __init__(self, name='page', tpl_engine=None, *args, **kwargs):
        """
        Attributes:
            Also see `CnchiWidget.__doc__`.

        Args:
            name (str): A name for this widget.

        """

        super().__init__(name=name, tpl_engine=tpl_engine, *args, **kwargs)

        self._props = []

    def prepare(self):
        """ This must be implemented by subclasses """
        raise NotImplementedError

    def store_values(self):
        """ This must be implemented by subclasses """
        raise NotImplementedError
