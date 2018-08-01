#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# download_hash.py
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


""" Module to check downloaded packages hash """

import hashlib
import logging
import os

def check_hash(path, element, queue_event=None):
    """ Checks file hash (sha256 or md5) """
    # Note: path must exist!

    identity = element['identity']
    filename = element['filename']

    sha256 = get_element_hash(element, 'sha256')
    md5 = get_element_hash(element, 'md5')

    # Check sha256 if available
    if sha256:
        if sha256 != get_file_hash(path, 'sha256'):
            logging.warning("SHA256 hash of file %s does not match!", filename)
            return False
        logging.debug("SHA256 hash of %s is OK.", path)
        return True

    logging.warning(
        "Element %s (%s) has no SHA256 hash info in its metalink", identity, filename)

    # sha256 not available let's check md5
    if md5:
        if md5 != get_file_hash(path, 'md5'):
            logging.warning("MD5 hash of file %s does not match!", filename)
            return False
        logging.debug("MD5 hash of %s is OK.", path)
        return True

    logging.warning(
        "Element %s (%s) has no MD5 hash info in its metalink", identity, filename)

    logging.debug(
        'Checksum unavailable for package: %s (%s)', identity, filename)
    if queue_event:
        queue_event('cache_pkgs_md5_check_failed', identity)
    return True

def get_file_hash(path, hash_type):
    """ Gets md5 or sha256 hash from a file """

    if not os.path.exists(path):
        return None

    if hash_type == 'md5':
        myhash = hashlib.md5()
    else:
        myhash = hashlib.sha256()

    with open(path, 'rb') as myfile:
        for line in myfile:
            myhash.update(line)

    return myhash.hexdigest()

def get_element_hash(element, hash_type):
    """ Get hash from one metalink element """
    hash_value = None
    hashes = element.get('hash', None)
    if hashes:
        hash_value = hashes.get(hash_type, None)
    return hash_value
