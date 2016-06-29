#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  _settings.py
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

""" Classes and data descriptor objects for the storage and retrieval of shared data/settings. """

from config import settings


class DataObject:
    """
    Generic object used to store data/settings as attributes.

    Attributes:
        from_dict (dict): Initialize object using dict.

    """

    _initialized = False

    def __init__(self, from_dict=None):
        from_dict = from_dict is not None and isinstance(from_dict, dict)

        if from_dict and not self._initialized:
            for key, val in from_dict.items():
                setattr(self, key, val)

            self._initialized = True


class SharedData:
    """
    Data descriptor that facilitates shared data storage/retrieval.

    Attributes:
        name      (str): The name of the bound attribute.
        from_dict (dict): Initial data to store.

    """

    _data = None

    def __init__(self, name, from_dict=None):
        self.name = name

        if self._data is None:
            self._data = DataObject(from_dict)

    def __get__(self, instance, cls):
        return self._data

