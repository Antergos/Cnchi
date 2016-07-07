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

import json
import hashlib
import os
import logging
import shutil

import requests

import misc.extra as misc
from info import CNCHI_VERSION
from _base_object import BaseObject
from installation.pacman.pac import Pac

_update_info_url = "https://raw.github.com/Antergos/Cnchi/master/update.info"
_master_zip_url = "https://github.com/Antergos/Cnchi/archive/master.zip"
_update_info = "/usr/share/cnchi/update.info"

_src_dir = os.path.dirname(__file__) or '.'
_base_dir = os.path.join(_src_dir, "..")



class Updater(BaseObject):

    def __init__(self, name='update', *args, **kwargs):
        super().__init__(name=name, *args, **kwargs)

        self.update_available = False
        self.repo_version = ''
        self.pacman = Pac()
        self.alpm = self.pacman.get_handle()

        self.pacman.refresh()
        self._compare_versions()

    def _compare_versions(self):



    def is_remote_version_newer(self):
        """ Returns true if the Internet version of Cnchi is
            newer than the local one """

        if not self.remote_version:
            return False

        # Version is always: x.y.z
        local_ver = self.local_version.split(".")
        remote_ver = self.remote_version.split(".")

        local = [int(local_ver[0]), int(local_ver[1]), int(local_ver[2])]
        remote = [int(remote_ver[0]), int(remote_ver[1]), int(remote_ver[2])]

        if remote[0] > local[0]:
            return True

        if remote[0] == local[0] and remote[1] > local[1]:
            return True

        if remote[0] == local[0] and remote[1] == local[1] and remote[2] > local[2]:
            return True

        return False

    def should_update_local_file(self, remote_name, remote_md5):
        """ Checks if remote file is different from the local one
            (just compares md5)"""
        for local_file in self.local_files:
            if (local_file['name'] == remote_name and
                    local_file['md5'] != remote_md5 and
                    '__' not in local_file['name']):
                return True
        return False

    def update(self):
        """ Check if a new version is available and
            update all files only if necessary (or forced) """
        update_cnchi = False

        if self.is_remote_version_newer():
            logging.info("New version found. Updating installer...")
            update_cnchi = True
        elif self.force:
            logging.info("No new version found. Updating anyways...")
            update_cnchi = True

        if update_cnchi:
            logging.debug("Downloading Cnchi %s...", self.remote_version)
            zip_path = "/tmp/cnchi-{0}.zip".format(self.remote_version)
            res = self.download_master_zip(zip_path)
            if not res:
                logging.error("Error downloading new version.")
                return False

            # master.zip file is downloaded, we must unzip it
            logging.debug("Uncompressing new version...")
            try:
                self.unzip_and_copy(zip_path)
            except Exception as ex:
                template = "Cannot update Cnchi. An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                logging.error(message)
                return False

        return update_cnchi

    @staticmethod
    def download_master_zip(zip_path):
        """ Download new Cnchi version from github """
        req = requests.get(_master_zip_url, stream=True)
        if req.status_code == requests.codes.ok:
            with open(zip_path, 'wb') as zip_file:
                for data in req.iter_content(1024):
                    if not data:
                        break
                    zip_file.write(data)
            return True
        else:
            return False

    def unzip_and_copy(self, zip_path):
        """ Unzip (decompress) a zip file using zipfile standard module
            and copy cnchi's files to their destinations """
        import zipfile

        dst_dir = "/tmp"

        # First check all md5 signatures
        all_md5_ok = True
        with zipfile.ZipFile(zip_path) as zip_file:
            # Check md5 sums
            for member in zip_file.infolist():
                zip_file.extract(member, dst_dir)
                full_path = os.path.join(dst_dir, member.filename)
                dst_full_path = os.path.join(
                    "/usr/share/cnchi",
                    full_path.split("/tmp/Cnchi-master/")[1])
                if os.path.isfile(dst_full_path):
                    if dst_full_path in self.md5s:
                        if ("update.info" not in dst_full_path and
                                self.md5s[dst_full_path] != get_md5_from_file(full_path)):
                            logging.warning(
                                _("Wrong md5 (%s). Bad download or wrong file, "
                                  "Cnchi won't update itself"),
                                member.filename)
                            all_md5_ok = False
                            break
                    else:
                        logging.warning(
                            _("File %s is not in md5 signatures list"),
                            member.filename)

            if all_md5_ok:
                # All md5 sums where ok. Let's copy all files
                for member in zip_file.infolist():
                    full_path = os.path.join(dst_dir, member.filename)
                    dst_full_path = os.path.join(
                        "/usr/share/cnchi",
                        full_path.split("/tmp/Cnchi-master/")[1])
                    if os.path.isfile(dst_full_path):
                        try:
                            with misc.raised_privileges():
                                logging.debug(
                                    _("Copying %s to %s..."),
                                    full_path,
                                    dst_full_path)
                                shutil.copyfile(full_path, dst_full_path)
                        except FileNotFoundError as file_error:
                            logging.error(
                                _("Can't copy %s to %s"),
                                full_path,
                                dst_full_path)
                            logging.error(file_error)
