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
import logging

DEVICES = []

CLASS_NAME = ""

def chroot(cmd, dest_dir, stdin=None, stdout=None):
    """ Runs command inside the chroot """
    run = [ 'chroot', dest_dir ]

    for element in cmd:
        run.append(element)

    try:
        proc = subprocess.Popen(run,
                                stdin=stdin,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        out = proc.communicate()[0]
        logging.debug(out.decode())
    except OSError as err:
        logging.exception(_("Error running command: %s"), err.strerror)

class Hardware(object):
    """ This is an abstract class. You need to use this as base """
    def __init__(self):
        pass

    def get_packages(self):
        """ Returns all necessary packages to install """
        raise NotImplementedError("get_packages is not implemented!")

    def post_install(self, dest_dir):
        """ Runs post install commands """
        raise NotImplementedError("postinstall is not implemented!")

    def check_device(self, device):
        """ Device is (VendorID, ProductID) """
        raise NotImplementedError("check_device is not implemented")

class HardwareInstall(object):
    """ This class checks user's hardware """
    def __init__(self):
        self.all_objects = []
        self.objects_found = []

        dirs = os.listdir('/usr/share/cnchi/src/hardware')

        # This is unsafe, but we don't care if somebody wants
        # Cnchi to run code arbitrarily.
        for filename in dirs:
            if filename.endswith(".py") and "__init__" not in filename and "hardware" not in filename:
                filename = filename[:-len(".py")]
                try:
                    package = "hardware." + filename
                    name = filename.capitalize()
                    # from package import name
                    class_name = getattr(__import__(package, fromlist=[name]), "CLASS_NAME")
                    self.all_objects.append(getattr(__import__(package, fromlist=[class_name]), class_name))
                except ImportError as err:
                    logging.exception("Error importing %s from %s : %s" % (name, package, err))
                except Exception as err:
                    logging.exception("Unexpected error importing %s: %s " % (package, err))

        # Detect devices
        devices = []

        # Get PCI devices
        lines = subprocess.check_output(["lspci", "-n"]).decode().split("\n")
        for line in lines:
            if len(line) > 0:
                dev = line.split()[2].split(":")
                devices.append(("0x" + dev[0], "0x" + dev[1]))

        # Get USB devices
        lines = subprocess.check_output(["lsusb"]).decode().split("\n")
        for line in lines:
            if len(line) > 0:
                dev = line.split()[5].split(":")
                devices.append(("0x" + dev[0], "0x" + dev[1]))

        # Enable this for testing
        devices.append(('0x80ee', '0xcafe'))

        # Find objects that support the found devices
        for obj in self.all_objects:
            for device in devices:
                if obj.check_device(self=obj, device=device):
                    #print(device, "detected", obj, "supports it")
                    self.objects_found.append(obj)

    def get_packages(self):
        """ Get pacman package list for all detected devices """
        packages = []
        for obj in self.objects_found:
            packages.extend(obj.get_packages(obj))
        return packages

    def post_install(self, dest_dir):
        """ Run post install commands for all detected devices """
        for obj in self.objects_found:
            obj.post_install(obj, dest_dir)
