#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# updater.py
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

""" Update Module """

from ._base_module import CnchiModule
from _cnchi_object import GLib
from installation.pacman.pac import Pac


class UpdateModule(CnchiModule):

    def __init__(self, name='_update', *args, **kwargs):
        super().__init__(name=name, *args, **kwargs)

        self.repo_version = ''
        self.pacman = None

    def _initialize_alpm(self, force_refresh=True):
        self.pacman = Pac()

        if force_refresh:
            self.pacman.refresh()

    def do_update_check(self, force_refresh=True):
        result = True
        restart = False

        if self.is_repo_version_newer(force_refresh):
            # Signal the UI to inform it that we are going to update Cnchi.
            yield '--update-available'

            result = self.pacman.install(['cnchi']) > -1
            restart = result

        self.settings.cnchi_is_updated = result
        yield dict(result=result, restart=restart)

    @staticmethod
    def is_remote_version_newer(remote_version, local_version):
        """
        If `remote_version` is newer than `local_version` returns True else False

        Notes:
            We are not currently using this method. It is being retained because it
            could be useful in the future.

        """

        if not remote_version:
            return False

        # Version is always: x.y.z
        local_ver = local_version.split(".")
        remote_ver = remote_version.split(".")

        local = [int(local_ver[0]), int(local_ver[1]), int(local_ver[2])]
        remote = [int(remote_ver[0]), int(remote_ver[1]), int(remote_ver[2])]

        if remote[0] > local[0]:
            return True

        if remote[0] == local[0] and remote[1] > local[1]:
            return True

        if remote[0] == local[0] and remote[1] == local[1] and remote[2] > local[2]:
            return True

        return False

    def is_repo_version_newer(self, force_refresh=True):
        if self.pacman is None:
            self._initialize_alpm(force_refresh)

        pkg_objs = self.pacman.get_packages_with_available_update()

        return [p for p in pkg_objs if p and 'cnchi' == p.name]

