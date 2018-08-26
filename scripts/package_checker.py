#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# package_checker.py
#
# Copyright © 2013-2018 Antergos
#
# This file is part of Cnchi.
#
# Cnchi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Cnchi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cnchi; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

""" Checks that all packages in packages.xml exist in the repositories. """

import os
import subprocess
import sys

XML_URL = "https://raw.githubusercontent.com/Antergos/Cnchi/master/data/packages.xml"
XML_FILE = "packages.xml"

def get_pkg_names():
    """ Get pkg names from packages.xml """
    if os.path.exists(XML_FILE):
        os.remove(XML_FILE)

    cmd = ["curl", "-O", XML_URL, "--silent"]
    try:
        subprocess.call(cmd)
    except subprocess.CalledProcessError as err:
        print(err)

    if not os.path.exists(XML_FILE):
        print("Could not download xml file!")
        sys.exit(1)

    with open(XML_FILE, 'r') as myfile:
        lines = myfile.readlines()

    begins = len("<pkgname>")
    ends = len("</pkgname>")
    names = []
    for line in lines:
        line = line.strip()
        if not "<!--" in line and not "-->" in line and "<pkgname>" in line:
            names.append(line[begins:-ends])

    return sorted(list(set(names)))

def check_names(pkgs):
    """ Checks if package exists calling pacman """
    not_found = []
    for pkg_name in pkgs:
        cmd = ["pacman", "-Ss", pkg_name]
        try:
            output = subprocess.check_output(cmd).decode()
        except subprocess.CalledProcessError:
            output = ""

        if pkg_name in output:
            print("{}...OK!".format(pkg_name))
        else:
            not_found.append(pkg_name)
            print("{}...NOT FOUND!".format(pkg_name))

    if not_found:
        print("These packages were not found:")
        print(" ".join(not_found))

if __name__ == '__main__':
    check_names(get_pkg_names())
