#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  updater.py
#  
#  Copyright 2013 Antergos
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import urllib.request
import urllib.error
from urllib.request import urlopen

import json
import hashlib
import os
import info

import logging

#_url_prefix = "https://raw.github.com/Antergos/Cnchi/stable/"
_url_prefix = "https://raw.github.com/Antergos/Cnchi/master/"

_src_dir = os.path.dirname(__file__) or '.'
_base_dir = os.path.join(_src_dir, "..")

class Updater():
    def __init__(self, force_update):
        self.web_version = ""
        self.web_files = []
        
        response = ""
        try: 
            update_info_url = _url_prefix + "update.info"
            request = urlopen(update_info_url)
            response = request.read().decode('utf-8')
            
        except urllib.HTTPError as e:
            logging.exception('Unable to get latest version info - HTTPError = %s' % e.reason)
        except urllib.URLError as e:
            logging.exception('Unable to get latest version info - URLError = %s' % e.reason)
        except httplib.HTTPException as e:
            logging.exception('Unable to get latest version info - HTTPException')
        except Exception as e:
            import traceback
            logging.exception('Unable to get latest version info - Exception = %s' % traceback.format_exc())

        if len(response) > 0:
            updateInfo = json.loads(response)

            self.web_version = updateInfo['version']
            self.web_files = updateInfo['files']
        
            logging.info("Cnchi Internet version: %s" % self.web_version)
            
            self.force = force_update
            
    def is_web_version_newer(self):
        if self.force:
             return True
             
        #version is always: x.y.z
        cur_ver = info.cnchi_VERSION.split(".")
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

    # This will update all files only if necessary (or forced)
    def update(self):
        if self.is_web_version_newer():
            logging.info("New version found. Updating installer...")
            num_files = len(self.web_files)
            i = 1
            for f in self.web_files:
                name = f['name']
                md5 = f['md5']
                print("Downloading %s (%d/%d)" % (name, i, num_files))
                if self.download(name, md5) is False:
                    # download has failed
                    logging.error("Download of %s has failed" % name)
                    return False
                i = i + 1
            # replace old files with the new ones
            self.replace_old_with_new_versions()                
            return True
        else:
            return False
                
    def get_md5(self, text):
        md5 = hashlib.md5()
        md5.update(text)
        return md5.hexdigest()

    def download(self, name, md5):
        url = _url_prefix + name
        response = ""
        try: 
            request = urlopen(url)
            txt = request.read()
            #.decode('utf-8')
        except urllib.error.HTTPError as e:
            logging.exception('Unable to get %s - HTTPError = %s' % (name, e.reason))
            return False
        except urllib.error.URLError as e:
            logging.exception('Unable to get %s - URLError = %s' % (name, e.reason))
            return False
        except httplib.error.HTTPException as e:
            logging.exception('Unable to get %s - HTTPException' % name)
            return False
        except Exception as e:
            import traceback
            logging.exception('Unable to get %s - Exception = %s' % (name, traceback.format_exc()))
            return False

        web_md5 = self.get_md5(txt)
        
        if web_md5 != md5:
            logging.error("Checksum error in %s. Download aborted" % name)
            return False
        
        new_name = os.path.join(_base_dir, name + "." + self.web_version.replace(".", "_"))
        
        with open(new_name, "wb") as f:
            f.write(txt)

        return True

    def replace_old_with_new_versions(self):
        logging.info("Replacing version %s with version %s..." % (info.cnchi_VERSION, self.web_version))
        for f in self.web_files:
            name = f['name']
            old_name = os.path.join(_base_dir, name + "." + info.cnchi_VERSION.replace(".", "_"))
            new_name = os.path.join(_base_dir, name + "." + self.web_version.replace(".", "_"))
            cur_name = os.path.join(_base_dir, name)
            
            if os.path.exists(name):
                os.rename(name, old_name)
            
            if os.path.exists(new_name):
                os.rename(new_name, cur_name)
