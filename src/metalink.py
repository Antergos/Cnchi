#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  metalink.py
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

""" Operations with metalinks """

import logging
import tempfile
import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

_PM2ML = True
try:
    import pm2ml
except ImportError:
    _PM2ML = False

#import memory_profiler as profiler

#@profiler.profile
def get_info(metalink):
    """ Reads metalink xml and stores it in a dict """

    metalink_info = {}

    tag = "{urn:ietf:params:xml:ns:metalink}"

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(str(metalink).encode('UTF-8'))
    temp_file.close()
    
    element = {}

    for event, elem in ET.iterparse(temp_file.name, events=('start', 'end')):
        if event == "start":
            if elem.tag.endswith("file"):
                element['filename'] = elem.attrib['name']
            elif elem.tag.endswith("identity"):
                element['identity'] = elem.text
            elif elem.tag.endswith("size"):
                element['size'] = elem.text
            elif elem.tag.endswith("version"):
                element['version'] = elem.text
            elif elem.tag.endswith("description"):
                element['description'] = elem.text
            elif elem.tag.endswith("hash"):
                element['hash'] = elem.text
            elif elem.tag.endswith("url"):
                try:
                    element['urls'].append(elem.text)
                except KeyError as err:
                    element['urls'] = [elem.text]
        if event == "end":
            if elem.tag.endswith("file"):
                # Crop to 5 urls max for file
                element['urls'] = element['urls'][:5]
                metalink_info[element['identity']] = element.copy()
                element.clear()
                elem.clear()

    if os.path.exists(temp_file.name):
        os.remove(temp_file.name)

    return metalink_info

#@profiler.profile
def create(package_name, pacman_conf_file):
    """ Creates a metalink to download package_name and its dependencies """

    if _PM2ML is False:
        return None

    args = ["-c", pacman_conf_file, "--noconfirm", "--all-deps", "--needed"]

    if package_name is "databases":
        args += ["--refresh"]

    #if self.use_aria2:
    #    args += "-r -p http -l 50".split()

    if package_name is not "databases":
        args += [package_name]

    try:
        pargs, conf, download_queue, not_found, missing_deps = pm2ml.build_download_queue(args)
    except Exception as err:
        msg = _("Unable to create download queue for package %s") % package_name
        logging.error(msg)
        logging.exception(err)
        return None

    if not_found:
        msg = _("Can't find these packages: ")
        for not_found in sorted(not_found):
            msg = msg + not_found + " "
        logging.warning(msg)

    if missing_deps:
        msg = _("Warning! Can't resolve these dependencies: ")
        for missing in sorted(missing_deps):
            msg = msg + missing + " "
        logging.warning(msg)

    metalink = pm2ml.download_queue_to_metalink(
        download_queue,
        output_dir=pargs.output_dir,
        set_preference=pargs.preference
    )
    
    return metalink

''' Test case '''
if __name__ == '__main__':
    import gettext
    _ = gettext.gettext

    with open("/usr/share/cnchi/test/gnome-sudoku.meta4") as meta4:
        print(get_info(meta4.read()))
