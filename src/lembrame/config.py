#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  config.py
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


class LembrameConfig(object):
    request_download_endpoint = False
    file_path = False
    decrypted_file_path = False
    folder_file_path = False
    pacman_packages = False

    def __init__(self):
        self.request_download_endpoint = \
            'https://lz6fjo9m5d.execute-api.us-west-2.amazonaws.com/dev/request-download-link'
        self.file_path = "/tmp/export.tar.gz.encrypted"
        self.decrypted_file_path = "/tmp/export.tar.gz"
        self.folder_file_path = "/tmp/export"
        self.pacman_packages = 'pacman_package_list'
