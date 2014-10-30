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

import logging
import xml.etree.ElementTree as ET

def get_info(metalink):
    """ Reads metalink xml and stores it in a dict """

    metalink_info = {}
    TAG = "{urn:ietf:params:xml:ns:metalink}"
    root = ET.fromstring(str(metalink))

    for child1 in root.iter(TAG + "file"):
        element = {}
        element['filename'] = child1.attrib['name']

        for child2 in child1.iter(TAG + "identity"):
            element['identity'] = child2.text

        for child2 in child1.iter(TAG + "size"):
            element['size'] = child2.text

        for child2 in child1.iter(TAG + "version"):
            element['version'] = child2.text

        for child2 in child1.iter(TAG + "description"):
            element['description'] = child2.text

        for child2 in child1.iter(TAG + "hash"):
            element[child2.attrib['type']] = child2.text

        element['urls'] = []
        for child2 in child1.iter(TAG + "url"):
            element['urls'].append(child2.text)

        metalink_info[element['identity']] = element

    return metalink_info

def create(package_name, pacman_conf_file):
    """ Creates a metalink to download package_name and its dependencies """
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
        logging.error(_("Unable to create download queue for package %s"), package_name)
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
