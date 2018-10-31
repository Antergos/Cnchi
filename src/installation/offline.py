#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# offline.py
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

""" Offline installation process module. """

import os

class Offline():
    """ Class to perform an offline installation """

    def __init__(self):
        """ Initialize class """
        pass
    
    def run(self):
        """ Perform the installation
            System is already formatted and mounted at this point """

        #self.copy_livecd()

        # cp -ax / /install
        # dirName: The next directory it found.
        # subdirList: A list of sub-directories in the current directory.
        # fileList: A list of files in the current directory.

        ##for dirName, subdirList, fileList in os.walk('/'):
        ##    #print('Found directory: %s' % dirName)
        ##    for fname in fileList:
        ##        #print('\t%s' % fname)



        ##cmd = ["cp", "-ax", "/", "/install"]
        ##call(cmd)
        ##cmd = [
        ##    "cp", "-vaT",
        ##    "/run/archiso/bootmnt/arch/boot/x86_64/vmlinuz",
        ##    "/install/boot/vmlinuz-linux"]
        ##call(cmd)
