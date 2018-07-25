#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# action.py
#
# Copyright © 2013-2018 Antergos
#
# This file is part of Cnchi.
#
# Cnchi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Cnchi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cnchi; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

""" Store actions on devices for the user to confirm """

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

class Action():
    """ Store actions on devices for the user to confirm """

    def __init__(self, action_type, path_or_info, relabel=False,
                 fs_format=False, mount_point="", encrypt=False):
        """ Init fields """

        # action_type can be "create", "modify" , "delete", "info"
        self.action_type = action_type
        self.path = path_or_info
        self.relabel = relabel
        self.format = fs_format
        self.mount_point = mount_point
        self.encrypt = encrypt
        self.info_txt = path_or_info

    def __str__(self):
        txt = ""
        if self.action_type == "delete":
            txt = _("Device {0} will be deleted!").format(self.path)
        elif self.action_type == "info":
            txt = self.info_txt
        else:
            if self.action_type == "create":
                txt = _("Device {0} will be created").format(self.path)
                txt += ", "
            elif self.action_type == "modify":
                if self.relabel or self.format or self.encrypt:
                    txt = _("Device {0} will be modified").format(self.path)
                else:
                    txt = _("Device {0} will be ").format(self.path)
                txt += ", "
            if self.relabel:
                txt += _("relabeled") + ", "
            else:
                txt += _("not relabeled") + ", "
            if self.format:
                txt += _("formatted") + ", "
            else:
                txt += _("not formatted") + ", "
            if self.mount_point:
                txt += _("mounted as {0}").format(self.mount_point)
                txt += " "
            else:
                txt += _("not mounted")
                txt += " "
            if self.encrypt:
                txt += _("and encrypted.")
            else:
                txt += _("and not encrypted.")
        return txt
