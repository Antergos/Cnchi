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
        logging.exception('Unable to get latest version info - HTTPError = %s' % err.reason)
    except urllib.error.URLError as err:
        logging.exception('Unable to get latest version info - URLError = %s' % err.reason)
    except httplib.HTTPException as err:
        logging.exception('Unable to get latest version info - HTTPException')
    except Exception as err:
        import traceback
        logging.exception('Unable to get latest version info - Exception = %s' % traceback.format_exc())
    finally:
        return request

class Updater():
    def __init__(self, force_update):
        self.web_version = ""
        self.web_files = []

        # Download update.info (contains info of all Cnchi's files)
        update_info_url = _url_prefix + "update.info"
        request = urlopen(update_info_url)
        
        if request is not None:
            response = request.read().decode('utf-8')
            if len(response) > 0:
                updateInfo = json.loads(response)
                self.web_version = updateInfo['version']
                self.web_files = updateInfo['files']
                logging.info(_("Cnchi Internet version: %s"), self.web_version)
                self.force = force_update

    def is_web_version_newer(self):
        if self.force:
             return True

        # Version is always: x.y.z
        cur_ver = info.CNCHI_VERSION.split(".")
        web_ver = self.web_version.split(".")

        cur = [int(cur_ver[0]),int(cur_ver[1]),int(cur_ver[2])]
        web = [int(web_ver[0]),int(web_ver[1]),int(web_ver[2])]

        if web[0] > cur[0]:
            return True

        if web[0] == cur[0] and web[1] > cur[1]:
            return True

        if web[0] == cur[0] and web[1] == cur[1] and web[2] > cur[2]:
            return True

        return False

    def update(self):
        ''' Check if a new version is available and
            update all files only if necessary (or forced) '''
        if self.is_web_version_newer():
            logging.info(_("New version found. Updating installer..."))
            num_files = len(self.web_files)
            i = 1
            for fil in self.web_files:
                name = fil['name']
                md5 = fil['md5']
                print("Downloading %s (%d/%d)" % (name, i, num_files))
                if self.download(name, md5) is False:
                    # download has failed
                    logging.error(_("Download of %s has failed, update will stop"), name)
                    return False
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
        url = _url_prefix + name
        request = urlopen(url)

        if request is not None:
            txt = request.read()
            
            if self.get_md5(txt) != md5:
                logging.error(_("Checksum error in %s. Download aborted"), name)
                return False
            
            new_name = os.path.join(
                _base_dir,
                name + "." + self.web_version.replace(".", "_"))
            
            with open(new_name, "wb") as f:
                f.write(txt)
            return True
        return False

    def replace_old_with_new_versions(self):
        """ Deletes old files and renames the new ones """
        logging.info(_("Replacing version %s with version %s..."), info.CNCHI_VERSION, self.web_version)
        for f in self.web_files:
            name = f['name']
            old_name = os.path.join(_base_dir, name + "." + info.CNCHI_VERSION.replace(".", "_"))
            new_name = os.path.join(_base_dir, name + "." + self.web_version.replace(".", "_"))
            cur_name = os.path.join(_base_dir, name)

            if os.path.exists(name):
                # Remove old file
                os.remove(name)

            if os.path.exists(new_name):
                # Rename new download file (removes trailing version in filename)
                os.rename(new_name, cur_name)
