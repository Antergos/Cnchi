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
import os

DEVICES = []

class Hardware(object):
    """ This is an abstract class. You need to use this as base """
    def __init__(self):
        pass
    
    def get_packages(self):
        raise NotImplementedError("get_packages is not implemented!")
    
    def postinstall(self):
        raise NotImplementedError("postinstall is not implemented!")

    #def check_device(self, device):
    #    """ Device is (VendorID, ProductID) """
    #    raise NotImplementedError("check_device is not implemented")
    def check_device(self, device):
        """ Device is (VendorID, ProductID) """
        if device in DEVICES:
            return True
        return False

class HardwareInstall(object):
    """ This class checks user's hardware """
    def __init__(self):
        self.imports = []
        
        dirs = os.listdir('.')

        # This is unsafe, but we don't care if somebody wants
        # Cnchi to run code arbitrarily.
        for filename in dirs:
            if ".py" in filename and "__init__" not in filename and "hardware" not in filename:
                filename = filename[:-3]
                try:
                    package = filename
                    name = filename.capitalize()
                    # from package import name
                    if package is not 'hardware' and package is not '__init__':
                        print(package)
                        class_name = getattr(__import__(package, fromlist=[name]), "CLASS_NAME")
                        #print("from",package, "import", name)
                        #self.imports.append(getattr(__import__(package, fromlist=[name]), name))
                except ImportError:
                    print("Error importing %s from %s" % (name, package))
                        
    def run(self):
        pci_devices = []
        usb_devices = []
        
        lines = subprocess.check_output(["lspci", "-n"]).decode().split("\n")
        for line in lines:
            if len(line) > 0:
                pci_devices.append(line.split()[2])

        lines = subprocess.check_output(["lsusb"]).decode().split("\n")
        for line in lines:
            if len(line) > 0:
                usb_devices.append(line.split()[5])
        
        for imp in self.imports:
            for pci_device in pci_devices:
                print(imp.check_device(pci_device))
            for usb_device in usb_devices:
                print(imp.check_device(usb_device))

if __name__ == '__main__':
    hardware_install = HardwareInstall()
    hardware_install.run()
