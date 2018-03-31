#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  lembrame.py
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


import requests
import os
import logging

from lembrame.config import LembrameConfig


def _(x): return x


class Lembrame:
    """ Lembrame main class """

    download_link = False

    def __init__(self, settings):
        self.settings = settings
        self.config = LembrameConfig
        self.credentials = self.settings.get('lembrame_credentials')

    def download_file(self):
        """ Download new Cnchi version from github """
        if self.request_download_link():
            logging.debug("We ", self.credentials.user_id)
            req = requests.get(self.download_link, stream=True)
            if req.status_code == requests.codes.ok:
                with open(self.config.file_path, 'wb') as encrypted_file:
                    for data in req.iter_content(1024):
                        if not data:
                            break
                        encrypted_file.write(data)
                return True
            else:
                logging.debug("Downloading the Lembrame encrypted file failed")
                return False
        else:
            return False

    def request_download_link(self):
        payload = {'uid': self.credentials.user_id}

        logging.debug("Requesting download link for uid: %s", self.credentials.user_id)

        req = requests.post(self.config.request_download_endpoint, json=payload)
        if req.status_code == requests.codes.ok:
            self.download_link = req.json()['data']
            logging.debug("API responded with a download link: %s", self.download_link)
            return True
        else:
            logging.debug("Requesting for download link to Lembrame failed")
            return False

