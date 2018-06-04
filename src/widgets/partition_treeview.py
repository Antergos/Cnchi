#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# partition_treeview.py
#
# Copyright © 2013-2018 Antergos
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# advanced.py
#
# Copyright © 2013-2018 Antergos
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

import logging

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject


class PartitionTreeview(Gtk.TreeView):

    COL_PATH = 0
    COL_FS = 1
    COL_MOUNT_POINT = 2
    COL_LABEL = 3
    COL_FORMAT_ACTIVE = 4
    COL_FORMAT_VISIBLE = 5
    COL_SIZE = 6
    COL_USED = 7
    COL_PARTITION_PATH = 8
    COL_FLAGS = 9
    COL_PARTITION_TYPE = 10
    COL_FORMAT_SENSITIVE = 11
    COL_SSD_ACTIVE = 12
    COL_SSD_VISIBLE = 13
    COL_SSD_SENSITIVE = 14
    COL_ENCRYPTED = 15

    def __init__(self):
        Gtk.TreeView.__init__(self)

        self.store = None







GObject.type_register(PartitionTreeview)
