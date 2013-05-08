#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  update-info.py
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

import os
import sys
import hashlib

# Insert the src directory at the front of the path.
base_dir = os.path.dirname(__file__) or '.'
src_dir = os.path.join(base_dir, 'src')
sys.path.insert(0, src_dir)

import info

# This script generates an update.nfo file used to update Cnchi

def get_md5(filename):
    md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for line in f:
            md5.update(line)
    return md5.hexdigest()

if __name__ == '__main__':
    files = []
    
    for f in os.listdir(base_dir):
         if os.path.isfile(os.path.join(base_dir, f)) and f[0] != "." :
             files.append(f)

    for f in os.listdir(src_dir):
         if os.path.isfile(os.path.join(src_dir, f)) and f[0] != "." :
             files.append("src/" + f)
        
    txt = '{"version":"%s","files":[\n' % info.cnchi_VERSION
    
    for f in files:
        md5 = get_md5(f)
        txt += '{"name":"%s","md5":"%s"},\n' % (f, md5)
    
    # remove last comma
    txt = txt[:-3]
    txt +='}]}\n'
    
    with open("update.nfo", "w") as f:
        f.write(txt)
