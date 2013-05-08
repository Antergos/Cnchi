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
#  
#  Antergos Team:
#   Alex Filgueira (faidoc) <alexfilgueira.antergos.com>
#   Raúl Granados (pollitux) <raulgranados.antergos.com>
#   Gustau Castells (karasu) <karasu.antergos.com>
#   Kirill Omelchenko (omelcheck) <omelchek.antergos.com>
#   Marc Miralles (arcnexus) <arcnexus.antergos.com>
#   Alex Skinner (skinner) <skinner.antergos.com>

import urllib.request
import urllib.error
from urllib.request import urlopen

import json
import hashlib

import info

url_prefix = "https://raw.github.com/Antergos/Cnchi/alongside/"
#url_prefix = "https://raw.github.com/Antergos/Cnchi/master/"

class Updater():
    def __init__(self, force_update=False):
        self.web_version = ""
        self.web_files = []
        
        response = ""
        try: 
            update_info_url = url_prefix + "update.info"
            request = urlopen(update_info_url)
            response = request.read().decode('utf-8')
                    
        except urllib.HTTPError as e:
            print('Unable to get latest version info - HTTPError = %s' % e.reason)
        except urllib.URLError as e:
            print ('Unable to get latest version info - URLError = %s' % e.reason)
        except httplib.HTTPException as e:
            print ('Unable to get latest version info - HTTPException')
        except Exception as e:
            import traceback
            print ('Unable to get latest version info - Exception = %s' % traceback.format_exc())

        if len(response) > 0:
            updateInfo = json.loads(response)

            self.web_version = updateInfo['version']
            self.web_files = updateInfo['files']
        
        print("web version: %s" % self.web_version)
        
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

    # This will update all files only if necessary
    def update(self):
        if self.is_web_version_newer():
            print("New version found. Updating installer...")
            for f in self.web_files:
                name = f['name']
                md5 = f['md5']
                self.download(name, md5)
                
    def get_md5(self, text):
        md5 = hashlib.md5()
        md5.update(text)
        return md5.hexdigest()

    def download(self, name, md5):
        url = url_prefix + name
        response = ""
        try: 
            request = urlopen(url)
            txt = request.read()
            #.decode('utf-8')
        except urllib.error.HTTPError as e:
            print('Unable to get %s - HTTPError = %s' % (name, e.reason))
        except urllib.error.URLError as e:
            print ('Unable to get %s - URLError = %s' % (name, e.reason))
        except httplib.error.HTTPException as e:
            print ('Unable to get %s - HTTPException' % name)
        except Exception as e:
            import traceback
            print ('Unable to get %s - Exception = %s' % (name, traceback.format_exc()))

        web_md5 = self.get_md5(txt)
        
        if web_md5 != md5:
            print("Checksum error in %s. Download aborted" % name)
            return
        
        print("checksum of %s is ok" % name)


if __name__ == '__main__':
    # to test updater, let's pretend we have a lower version
    updater = Updater(force_update=True)
    updater.update()
            
