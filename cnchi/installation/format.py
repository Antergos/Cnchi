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

import crypt
import logging
import multiprocessing
import os
import queue
import shutil
import subprocess
import sys
import time

import parted3.fs_module as fs

from installation import auto_partition
from installation import chroot
from installation import mkinitcpio

from misc.misc import InstallError

def chroot_run(cmd):
    chroot.run(cmd, DEST_DIR)

class Format(object):
    """ Format Class """

    def __init__(self, settings, callback_queue, mount_devices,
                 fs_devices, alternate_package_list="", ssd=None, blvm=False):
        """ Initialize installation class """
        multiprocessing.Process.__init__(self)

        self.alternate_package_list = alternate_package_list

        self.callback_queue = callback_queue
        self.settings = settings
        self.method = self.settings.get('partition_mode')
        msg = _("Installing using the '{0}' method").format(self.method)
        self.queue_event('info', msg)

        # Check desktop selected to load packages needed
        self.desktop = self.settings.get('desktop')

        # This flag tells us if there is a lvm partition (from advanced install)
        # If it's true we'll have to add the 'lvm2' hook to mkinitcpio
        self.blvm = blvm

        if ssd is not None:
            self.ssd = ssd
        else:
            self.ssd = {}

        self.mount_devices = mount_devices

        # Set defaults
        self.desktop_manager = 'lightdm'
        self.network_manager = 'NetworkManager'

        # Packages to be removed
        self.conflicts = []

        self.fs_devices = fs_devices

        self.running = True
        self.error = False

        # Initialize some vars that are correctly initialized elsewhere
        # (pylint complains if we don't do it here)
        self.auto_device = ""
        self.packages = []
        self.pacman = None
        self.vbox = "False"

        # Cnchi will store here info (packages needed, post install actions, ...)
        # for the detected hardware
        self.hardware_install = None

    def queue_fatal_event(self, txt):
        """ Queues the fatal event and exits process """
        self.error = True
        self.running = False
        self.queue_event('error', txt)
        # self.callback_queue.join()
        sys.exit(0)

    def queue_event(self, event_type, event_text=""):
        if self.callback_queue is not None:
            try:
                self.callback_queue.put_nowait((event_type, event_text))
            except queue.Full:
                pass
        else:
            print("{0}: {1}".format(event_type, event_text))

    def wait_for_empty_queue(self, timeout):
        if self.callback_queue is not None:
            tries = 0
            if timeout < 1:
                timeout = 1
            while tries < timeout and not self.callback_queue.empty():
                time.sleep(1)
                tries += 1

    def run(self):
        """ Calls run_installation and takes care of exceptions """

        try:
            self.run_format()
        except subprocess.CalledProcessError as process_error:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
            logging.error(_("Error running command %s"), process_error.cmd)
            logging.error(_("Output: %s"), process_error.output)
            for line in trace:
                logging.error(line)
            self.queue_fatal_event(process_error.output)
        except (InstallError,
                pyalpm.error,
                KeyboardInterrupt,
                TypeError,
                AttributeError,
                OSError,
                IOError) as install_error:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
            logging.error(install_error)
            for line in trace:
                logging.error(line)
            self.queue_fatal_event(install_error)

    @misc.raise_privileges
    def run_format(self):
        """ Run partitioning and formating """

        auto_partition.unmount_all(DEST_DIR)

        # Create and format partitions

        if self.method == 'automatic':
            self.auto_device = self.settings.get('auto_device')

            logging.debug(_("Creating partitions and their filesystems in %s"), self.auto_device)

            # If no key password is given a key file is generated and stored in /boot
            # (see auto_partition.py)

            auto = auto_partition.AutoPartition(dest_dir=DEST_DIR,
                                                auto_device=self.auto_device,
                                                use_luks=self.settings.get("use_luks"),
                                                luks_password=self.settings.get("luks_root_password"),
                                                use_lvm=self.settings.get("use_lvm"),
                                                use_home=self.settings.get("use_home"),
                                                bootloader=self.settings.get("bootloader"),
                                                callback_queue=self.callback_queue)
            auto.run()

            # Get mount_devices and fs_devices
            # (mount_devices will be used when configuring GRUB in modify_grub_default)
            # (fs_devices will be used when configuring the fstab file)
            self.mount_devices = auto.get_mount_devices()
            self.fs_devices = auto.get_fs_devices()
        elif self.method == 'alongside'
        elif self.method == 'advanced':
            self.
