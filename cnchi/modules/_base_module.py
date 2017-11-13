#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  _base_module.py
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

from _cnchi_object import (
    CnchiObject,
    bg_thread,
    locale,
    os
)


class BaseModuleMeta(type):
    """
    Metaclass which ensures all class instance methods
    are run in a background thread.
    """

    def __new__(cls, name, bases, namespace, **kwargs):
        for key in namespace:
            if '__' in key:
                continue

            if callable(namespace[key]):
                namespace[key] = bg_thread(namespace[key])

        return type.__new__(cls, name, bases, namespace)


class CnchiModule(CnchiObject, metaclass=BaseModuleMeta):
    """
    Base class for all of Cnchi's modules. Modules house logic that is not directly
    related to rendering the UI. Modules' methods are run in background threads
    so that they do not block the UI.

    Class Attributes:
        See Also: `CnchiObject.__doc__`

    """

    def __init__(self, name='base_module', page_name='', *args, **kwargs):
        """
        Attributes:
            name (str): A name for this object (all objects must have unique name).
            See Also: `CnchiObject.__doc__`

        """
        super().__init__(name=name, *args, **kwargs)

        self.page_name = page_name

    def prepare(self):
        raise NotImplementedError

