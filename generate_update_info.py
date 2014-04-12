#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  generate_update_info.py
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

""" This script generates an update.info file used to update Cnchi """

import os
import hashlib
import src.info as info

def get_md5(file_name):
    """ Gets md5 hash from a file """
    md5_hash = hashlib.md5()
    with open(file_name, "rb") as myfile:
        for line in myfile:
            md5_hash.update(line)
    return md5_hash.hexdigest()

def get_files(path):
    """ Returns all files from a directory """
    all_files = []
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        # Do not parse hidden files
        if filename[0] != ".":
            if os.path.isfile(file_path):
                print(file_path)
                all_files.append(file_path)
            elif os.path.isdir(file_path) and filename != "." and filename != "..":
                all_files.extend(get_files(file_path))
    return all_files

def create_update_info():
    """ Creates update.info file """

    myfiles = get_files("/usr/share/cnchi")

    txt = '{"version":"%s","files":[\n' % info.CNCHI_VERSION

    for filename in myfiles:
        md5 = get_md5(filename)
        txt += '{"name":"%s","md5":"%s"},\n' % (filename, md5)

    # remove last comma and close
    txt = txt[:-3]
    txt += '}]}\n'

    with open("update.info", "w") as update_info:
        update_info.write(txt)

if __name__ == '__main__':
    create_update_info()
