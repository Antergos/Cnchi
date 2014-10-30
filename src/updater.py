#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  updater.py
#
#  Copyright © 2013,2014 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import urllib.request
import urllib.error

import json
import hashlib
import os
import info

import logging

_url_prefix = "https://raw.github.com/Antergos/Cnchi/master/"

_src_dir = os.path.dirname(__file__) or '.'
_base_dir = os.path.join(_src_dir, "..")

def urlopen(url):
    request = None
    try:
        request = urllib.request.urlopen(url)
    except urllib.error.HTTPError as err:
        logging.exception('Unable to get %s - HTTPError = %s', url, err.reason)
    except urllib.error.URLError as err:
        logging.exception('Unable to get %s - URLError = %s', url, err.reason)
    except httplib.HTTPException as err:
        logging.exception('Unable to get %s - HTTPException', url)
    except Exception as err:
        import traceback
        logging.exception('Unable to get %s - Exception = %s', url, traceback.format_exc())
    finally:
        return request

class Updater():
    def __init__(self, force_update):
        self.remote_version = ""
        self.remote_files = []
        
        # Get local info (local update.info)
        with open("/usr/share/cnchi/update.info", "r") as local_update_info:
            response = local_update_info.read()
            if len(response) > 0:
                updateInfo = json.loads(response)
                self.local_files = updateInfo['files']

        # Download update.info (contains info of all Cnchi's files)
        update_info_url = _url_prefix + "update.info"
        request = urlopen(update_info_url)
        
        if request is not None:
            response = request.read().decode('utf-8')
            if len(response) > 0:
                updateInfo = json.loads(response)
                self.remote_version = updateInfo['version']
                self.remote_files = updateInfo['files']
                logging.info(_("Cnchi Internet version: %s"), self.remote_version)
                self.force = force_update

    def is_remote_version_newer(self):
        """ Returns true if the Internet version of Cnchi is newer than the local one """
        if self.force:
             return True

        # Version is always: x.y.z
        local_ver = info.CNCHI_VERSION.split(".")
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
        """ Checks if remote file is different from the local one (just compares md5)"""
        for local_file in self.local_files:
            if local_file['name'] == remote_name and local_file['md5'] != remote_md5:
                return True
        return False

    def update(self):
        ''' Check if a new version is available and
            update all files only if necessary (or forced) '''
        if self.is_remote_version_newer():
            logging.info(_("New version found. Updating installer..."))
            num_files = len(self.remote_files)
            i = 1
            for remote_file in self.remote_files:
                name = remote_file['name']
                md5 = remote_file['md5']
                if self.should_update_local_file(name, md5):
                    print("Downloading %s (%d/%d)" % (name, i, num_files))
                    if self.download(name, md5) is False:
                        # download has failed
                        logging.error(_("Download of %s has failed, update will stop"), name)
                        return False
                else:
                    print("Skipping %s as has not changed" % name)
                i += 1
            # replace old files with the new ones
            self.replace_old_with_new_versions()
            return True
        else:
            return False

    def get_md5(self, text):
        """ Gets md5 hash from str """
        md5 = hashlib.md5()
        md5.update(text)
        return md5.hexdigest()

    def download(self, name, md5):
        """ Download a file """
        prefix = "/usr/share/cnchi/"
        if name.startswith(prefix):
            url = _url_prefix + name[len(prefix):]
        else:
            url = _url_prefix + name

        request = urlopen(url)

        if request is not None:
            txt = request.read()
            
            if "update.info" not in name and self.get_md5(txt) != md5:
                logging.error(_("Checksum error in %s. Download aborted"), name)
                return False
            
            new_name = os.path.join(
                _base_dir,
                name + "." + self.remote_version.replace(".", "_"))
            
            with open(new_name, "wb") as f:
                f.write(txt)
            return True
        return False

    def replace_old_with_new_versions(self):
        """ Deletes old files and renames the new ones """
        logging.info(_("Replacing version %s with version %s..."), info.CNCHI_VERSION, self.remote_version)
        for f in self.remote_files:
            name = f['name']
            old_name = os.path.join(_base_dir, name + "." + info.CNCHI_VERSION.replace(".", "_"))
            new_name = os.path.join(_base_dir, name + "." + self.remote_version.replace(".", "_"))
            local_name = os.path.join(_base_dir, name)

            # Check that there is a new remote file before deleting the local one
            if os.path.exists(new_name) and os.path.exists(name):
                # Remove old file
                os.remove(name)
                # Rename new download file (removes trailing version in filename)
                os.rename(new_name, local_name)
