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

#update_nfo_url = "https://raw.github.com/Antergos/Cnchi/master/update.info"
update_nfo_url = "https://raw.github.com/Antergos/Cnchi/alongside/update.info"

class Updater():
    def __init__(self):
        self.web_version = ""
        self.web_files = []
        
        response = ""
        try: 
            request = urlopen(update_nfo_url)
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
            
    def is_web_version_newer(self):
        return True

    # This will update all files only if necessary
    def update(self):
        if self.is_web_version_newer():
            for f in self.web_files:
                name = f['name']
                md5 = f['md5']
                self.download(name, md5)
                
    def download(self, name, md5):
        pass


if __name__ == '__main__':
    updater = Updater()
    updater.update()
            
