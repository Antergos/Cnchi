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
    
    #print(temp_file.name)
    
    element = {}
    
    # TODO: Add clear nodes
    for event, elem in ET.iterparse(temp_file.name, events=('start', 'end', 'start-ns', 'end-ns')):
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
                element['urls'].append(elem.text)
        if event == "end":
            if elem.tag.endswith("file"):
                metalink_info[element['identity']] = element                
                element.clear()
        #if event == "end":
        #    print("end:",elem)
    
    '''
    root = ET.fromstring(str(metalink))

    for child1 in root.iter(tag + "file"):
        element = {}
        element['filename'] = child1.attrib['name']

        for child2 in child1.iter(tag + "identity"):
            element['identity'] = child2.text

        for child2 in child1.iter(tag + "size"):
            element['size'] = child2.text

        for child2 in child1.iter(tag + "version"):
            element['version'] = child2.text

        for child2 in child1.iter(tag + "description"):
            element['description'] = child2.text

        for child2 in child1.iter(tag + "hash"):
            element[child2.attrib['type']] = child2.text

        element['urls'] = []
        for child2 in child1.iter(tag + "url"):
            element['urls'].append(child2.text)

        metalink_info[element['identity']] = element
    '''

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

    meta4 = '<?xml version="1.0" encoding="utf-8"?>' \
        '<metalink xmlns="urn:ietf:params:xml:ns:metalink">' \
        '<file name="ubuntu-9.04-alternate-amd64.iso">' \
        '<size>732282880</size>' \
        '<publisher name="Ubuntu" url="http://www.ubuntu.com"/>' \
        '<license name="GPL" url="http://www.gnu.org/licenses/gpl.html"/>' \
        '<version>9.04</version>' \
        '<description>Ubuntu CD Image</description>' \
        '<logo>http://www.ubuntu.com/themes/ubuntu07/images/ubuntulogo.png</logo>' \
        '<os>Linux-x64</os>' \
        '<hash type="md5">3b5e9861910463374bb0d4ba9025bbb1</hash>' \
        '<metaurl type="torrent" priority="1">http://releases.ubuntu.com/9.04/ubuntu-9.04-alternate-amd64.iso.torrent</metaurl>' \
        '<url location="jp" priority="1">http://ftp.yz.yamagata-u.ac.jp/pub/linux/ubuntu/releases/9.04/ubuntu-9.04-alternate-amd64.iso</url>' \
        '<url location="de" priority="2">ftp://ftp.rrzn.uni-hannover.de/pub/mirror/linux/ubuntu-releases/9.04/ubuntu-9.04-alternate-amd64.iso</url>' \
        '<url location="gb" priority="2">http://ftp.ticklers.org/releases.ubuntu.org/releases/9.04/ubuntu-9.04-alternate-amd64.iso</url>' \
        '<url location="us" priority="3">http://ubuntu.media.mit.edu/ubuntu-releases/9.04/ubuntu-9.04-alternate-amd64.iso</url>' \
        '</file>' \
        '</metalink>'

    get_info(meta4)
