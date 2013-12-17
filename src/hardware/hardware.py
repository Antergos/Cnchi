#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  hardware.py
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

""" Hardware related packages installation """

import subprocess

class Hardware(object):
    """ This is an abstract class. You need to use this as base """
    def __init__(self):
        pass
    
    def get_packages(self):
        raise NotImplementedError("get_packages is not implemented!")
    
    def postinstall(self):
        raise NotImplementedError("postinstall is not implemented!")

    def check_device(self, device):
        """ Device is (VendorID, ProductID) """
        raise NotImplementedError("check_device is not implemented")

class HardwareInstall(object):
    """ This class checks user's hardware """
    def __init__(self):
        pass
    
    def get_all(self):
        pass
    
    def run(self):
        # pci
        lines = subprocess.check_call(["lspci", "-n"])
        for line in lines:
            pci = line[2]
            print(pci)

if __name__ == '__main__':
    hardware_install = HardwareInstall()
    hardware_install.run()
