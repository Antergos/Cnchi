#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  process.py
#
#  Copyright © 2013-2015 Antergos
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

""" Installation thread module. """

import multiprocessing

from installation import Installation
from installation import Format

class Process(multiprocessing.Process):
    """ Format and Installation process thread class """

    def __init__(self, settings, callback_queue, mount_devices, fs_devices,  alternate_package_list="", ssd=None, blvm=False):

        """ Initialize installation class """
        multiprocessing.Process.__init__(self)

        self.alternate_package_list = alternate_package_list
        self.callback_queue = callback_queue
        self.settings = settings
        self.method = self.settings.get('partition_mode')

        # This flag tells us if there is a lvm partition (from advanced install)
        # If it's true we'll have to add the 'lvm2' hook to mkinitcpio
        self.blvm = blvm

        if ssd is not None:
            self.ssd = ssd
        else:
            self.ssd = {}

        self.mount_devices = mount_devices
        self.fs_devices = fs_devices

        self.running = True
        self.error = False

        # Initialize some vars that are correctly initialized elsewhere
        self.auto_device = ""
        self.packages = []
        self.pacman = None
        self.vbox = "False"


    def run(self):
        """ Calls run_installation and takes care of exceptions """

        self.run_format()
        self.run_installation()

    def run_format(self):
        pass

    def run_installation(self):

        self.installation = Installation()
  def __init__(self, settings, callback_queue, mount_devices,
                 fs_devices, alternate_package_list="", ssd=None, blvm=False):
        (self, settings, callback_queue, mount_devices,
                     fs_devices, alternate_package_list="", ssd=None, blvm=False):
