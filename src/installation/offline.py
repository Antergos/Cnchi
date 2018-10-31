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

import logging
import os

from misc.events import Events
from misc.run_cmd import call

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message


class Offline():
    """ Class to perform an offline installation """

    DEST_DIR = "/install"

    def __init__(self, callback_queue):
        """ Initialize class """
        self.events = Events(callback_queue)
    
    def copy_root(self):
        """ Copy entire livecd root partition to /install """

        self.events.add('pulse', 'start')
        self.events.add('info', _("Installing files..."))

        for dirpath, _dirnames, filenames in os.walk('/'):
            for filename in filenames:
                src_path = os.path.join(dirpath, filename)
                dst_path = os.path.join(Offline.DEST_DIR, src_path)
                cmd = ['cp', '-ax', src_path, dst_path]
                call(cmd)
                logging.debug("%s file copied to destination", src_path)
                
        self.events.add('pulse', 'stop')

    def copy_kernel(self):
        """ Copies livecd kernel to destination """
        cmd = [
            "cp", "-vaT",
            "/run/archiso/bootmnt/arch/boot/x86_64/vmlinuz",
            "/install/boot/vmlinuz-linux"]
        call(cmd)

    def run(self):
        """ Perform the installation
            System is already formatted and mounted at this point
            https://bbs.archlinux.org/viewtopic.php?pid=1733243#p1733243 """

        logging.debug("Copying LiveCD root partition files...")
        self.copy_root()
        logging.debug("LiveCD root partition files copied.")

        logging.debug("Copying LiveCD kernel...")
        self.copy_kernel()
        logging.debug("LiveCD kernel copied.")
