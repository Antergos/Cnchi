#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  base_module.py
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

from _base_object import BaseObject

TE = 'gtkbuilder'
BM = 'base_module'


class BaseModule(BaseObject):
    """
    Base class for all of Cnchi's modules. Modules house logic that is not directly
    related to rendering the UI. Modules' methods are always called from a background thread
    so that they do not block the UI.

    Class Attributes:
        See Also `BaseObject.__doc__`

    """

    def __init__(self, name=BM, *args, **kwargs):
        """
        Attributes:
            name (str): A name for this object (all objects must have unique name).
            See Also: `BaseObject.__doc__`

        """

        super().__init__(name=name, *args, **kwargs)

