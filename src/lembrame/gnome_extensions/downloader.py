#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  downloader.py
#
#  Copyright © 2013-2017 Antergos
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
import requests
import logging
import zipfile


class GnomeExtensionsDownloader(object):
    extensions = False
    extension_name = False
    extension_info = False
    extension_latest_shell_supported = False
    extension_download_link = False

    def __init__(self, install_user_home, config):
        self.config = config
        self.install_user_home = install_user_home
        self.extension_info_url = self.config.gnome_extensions_url + '/extension-info/?uuid='
        self.tmp_downloads = '/tmp/gshell-extensions/'
        self.extensions_path = self.install_user_home + self.config.gnome_shell_extensions_path

    def run(self, extensions):
        """ Iterate over the list of enabled extensions """
        self.extensions = extensions

        # Create destination folders were we're going to download the extension
        os.makedirs(self.tmp_downloads, exist_ok=True)
        os.makedirs(self.extensions_path, exist_ok=True)

        for self.extension_name in self.extensions:
            self.download_extension()

    def download_extension(self):
        """ Proceed to download the extension """
        # Gather information
        self.extension_info = self.get_extension_info()
        self.extension_latest_shell_supported = self.get_latest_shell_supported()
        self.extension_download_link = self.get_extension_download_link()

        # Download the extension
        if self.extension_download_link and self.extension_name:
            req = requests.get(self.extension_download_link, stream=True)
            if req.status_code == requests.codes.ok:
                with open(self.tmp_downloads + self.extension_name, 'wb') as extension_file:
                    for data in req.iter_content(1024):
                        if not data:
                            break
                        extension_file.write(data)
                self.extract_extension()

                return True
            else:
                logging.debug("Downloading of '%s' gnome shell extension failed.", self.extension_name)
                return False

        logging.debug("We don't have a download link. Something was wrong.")
        return False

    def get_extension_info(self):
        """ Request for the complete information about the current GShell extension """
        req = requests.get(self.extension_info_url + self.extension_name, stream=True)
        if req.status_code == requests.codes.ok:
            logging.debug("We got the info for the gnome extension '%s'", self.extension_name)
            return req.json()
        else:
            logging.debug("Requesting the extension info failed for '%s'", self.extension_name)
            return False

    def get_latest_shell_supported(self):
        """ Get the latest GShell supported version of the current extension """
        latest_supported = max(self.extension_info['shell_version_map'])
        logging.debug("The extension '%s' has '%s' as latest Gnome Shell supported",
                      self.extension_name, latest_supported)
        return latest_supported

    def get_extension_download_link(self):
        """ Based on the latest GShell supported version, ask for the specific information with the download link """
        req_url = self.extension_info_url + \
                  self.extension_name + \
                  "&shell_version=" + \
                  self.extension_latest_shell_supported
        req = requests.get(req_url, stream=True)
        if req.status_code == requests.codes.ok:
            logging.debug("We got the download link for '%s'", self.extension_name)
            return self.config.gnome_extensions_url + req.json()['download_url']
        else:
            logging.debug("Requesting the extension download link failed for '%s'", self.extension_name)
            return False

    def extract_extension(self):
        """ Extract ZIP to the final destination """
        try:
            zip_file = zipfile.ZipFile(self.tmp_downloads + self.extension_name, "r")
            zip_file.extractall(self.extensions_path + self.extension_name)
            zip_file.close()
            return True
        except OSError as err:
            logging.debug("Error trying to extract extension '%s': %s", self.extension_name, str(err))
            return False

