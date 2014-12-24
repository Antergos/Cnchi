#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  alongside.py
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

""" Alongside installation module """

from gi.repository import Gtk, Gdk

import sys
import os
import logging
import subprocess
import tempfile

if __name__ == '__main__':
    # Insert the parent directory at the front of the path.
    # This is used only when we want to test this screen
    base_dir = os.path.dirname(__file__) or '.'
    parent_dir = os.path.join(base_dir, '..')
    sys.path.insert(0, parent_dir)

try:
    import parted
except ImportError as err:
    logging.error(_("Can't import parted module: %s"), str(err))

import canonical.misc as misc
import canonical.gtkwidgets as gtkwidgets
import show_message as show
import bootinfo

import parted3.partition_module as pm
import parted3.fs_module as fs
import parted3.used_space as used_space

from installation import process as installation_process
from gtkbasebox import GtkBaseBox

# Leave at least 6.5GB for Antergos when shrinking
MIN_ROOT_SIZE = 6500

def get_partition_size_info(partition_path, human=False):
    """ Gets partition used and available space """

    min_size = "0"
    part_size = "0"

    already_mounted = False

    with open("/proc/mounts") as mounts:
        if partition_path in mounts.read():
            already_mounted = True

    tmp_dir = ""

    try:
        if not already_mounted:
            tmp_dir = tempfile.mkdtemp()
            subprocess.call(["mount", partition_path, tmp_dir])
        if human:
            cmd = ['df', '-h', partition_path]
        else:
            cmd = ['df', partition_path]
        df_out = subprocess.check_output(cmd).decode()
        if not already_mounted:
            subprocess.call(["umount", "-l", tmp_dir])
    except subprocess.CalledProcessError as err:
        logging.error(err)
        return

    if os.path.exists(tmp_dir):
        os.rmdir(tmp_dir)

    if len(df_out) > 0:
        df_out = df_out.split('\n')
        df_out = df_out[1].split()
        if human:
            part_size = df_out[1]
            min_size = df_out[2]
        else:
            part_size = float(df_out[1])
            min_size = float(df_out[2])

    return (min_size, part_size)

class InstallationAlongside(GtkBaseBox):
    """ Performs an automatic installation next to a previous installed OS """
    def __init__(self, params, prev_page="installation_ask", next_page="user_info"):
        super().__init__(self, params, "alongside", prev_page, next_page)

        self.label = self.ui.get_object('label_info')

        oses = {}
        oses = bootinfo.get_os_dict()

        # In InstallationAsk (ask.py) we've already checked that the user has Windows OS installed

        # Delete OSes outside sda
        devices = []
        for device in oses:
            if "sda" not in device:
                devices.append(device)
        for device in devices:
            del oses[device]
        devices = []

        existing_device = None
        new_device = None

        for device in oses:
            if "Windows" in oses[device]:
                existing_device = device
                val = int(device[len("/dev/sdX"):]) + 1
                new_device = device[:len("/dev/sdX")] + str(val)

        if existing_device and new_device:
            print("existing device: ", existing_device)
            print("new device: ", new_device)

            (min_size, part_size) = get_partition_size_info(existing_device)
            max_size = part_size - (MIN_ROOT_SIZE * 1000.0)

            print(max_size)

            self.resize = gtkwidgets.ResizeWidget(part_size, min_size, max_size)

            self.resize.set_part_title("existing", oses[existing_device], existing_device)
            self.resize.set_part_icon_name("existing", "distributor-logo")

            self.resize.set_part_title("new", "Antergos", new_device)
            self.resize.set_part_icon_name("new", "distributor-logo")

            self.resize.set_pref_size(max_size)

            self.main_box = self.ui.get_object("alongside")
            self.main_box.pack_start(self.resize, True, False, 5)

    def translate_ui(self):
        """ Translates all ui elements """
        txt = _("Choose the new size of your installation")
        txt = '<span size="large">%s</span>' % txt
        self.label.set_markup(txt)

        self.header.set_subtitle(_("Antergos Alongside Installation"))

    def prepare(self, direction):
        self.translate_ui()
        self.show_all()
        self.forward_button.set_sensitive(False)

    def store_values(self):
        self.start_installation()
        return True

    def is_room_available(self, row):
        """ Checks that we really can shrink the partition and create a new one
        with the current hard disk layout """
        partition_path = row[COL_DEVICE]
        otherOS = row[COL_DETECTED_OS]
        fs_type = row[COL_FILESYSTEM]

        device_path = row[COL_DEVICE][:len("/dev/sdX")]

        new_size = self.new_size

        logging.debug("partition_path: %s" % partition_path)
        logging.debug("device_path: %s" % device_path)
        logging.debug("new_size: %s" % new_size)

        # Find out how many primary partitions device has, and also
        # if there's already an extended partition

        extended_path = ""
        primary_partitions = []

        for path in self.partitions:
            if device_path in path:
                p = self.partitions[path]
                if p.type == pm.PARTITION_EXTENDED:
                    extended_path = path
                elif p.type == pm.PARTITION_PRIMARY:
                    primary_partitions.append(path)

        primary_partitions.sort()

        logging.debug("extended partition: %s" % extended_path)
        logging.debug("primary partitions: %s" % primary_partitions)

        if len(extended_path) > 0:
            # TODO: Allow shrink a logical partition and create inside two additional partitions (root and swap)
            print("Extended present")

        if len(primary_partitions) > 2:
            # We only allow installing if only 2 partitions are already occupied,
            # otherwise there will be no room for root and swap partitions
            txt = _("There are too many primary partitions, can't create a new one")
            logging.error(txt)
            show.error(self.get_toplevel(), txt)
            return False

        return True

    def start_installation(self):
        """ Alongside method shrinks selected partition
        and creates root and swap partition in the available space """

        row = self.get_selected_row()

        if row is None:
            return

        if self.is_room_available(row) is False:
            return

        partition_path = row[COL_DEVICE]
        otherOS = row[COL_DETECTED_OS]
        fs_type = row[COL_FILESYSTEM]

        device_path = row[COL_DEVICE][:len("/dev/sdX")]

        new_size = self.new_size

        # First, shrink filesystem
        res = fs.resize(partition_path, fs_type, new_size)
        if res:
            txt = _("Filesystem on %s shrunk.") % partition_path
            txt += "\n"
            txt += _("Will recreate partition now on device %s partition %s") % (device_path, partition_path)
            logging.debug(txt)
            # Destroy original partition and create a new resized one
            res = pm.split_partition(device_path, partition_path, new_size)
        else:
            txt = _("Can't shrink %s(%s) filesystem") % (otherOS, fs_type)
            logging.error(txt)
            show.error(self.get_toplevel(), txt)
            return

        # res is either False or a parted.Geometry for the new free space
        if res is None:
            txt = _("Can't shrink %s(%s) partition") % (otherOS, fs_type)
            logging.error(txt)
            show.error(self.get_toplevel(), txt)
            txt = _("*** FILESYSTEM IN UNSAFE STATE ***")
            txt += "\n"
            txt += _("Filesystem shrink succeeded but partition shrink failed.")
            logging.error(txt)
            return

        txt = _("Partition %s shrink complete") % partition_path
        logging.debug(txt)

        devices = pm.get_devices()
        disk = devices[device_path][0]
        mount_devices = {}
        fs_devices = {}

        mem_total = subprocess.check_output(["grep", "MemTotal", "/proc/meminfo"]).decode()
        mem_total = int(mem_total.split()[1])
        mem = mem_total / 1024

        # If geometry gives us at least 7.5GB (MIN_ROOT_SIZE + 1GB) we'll create ROOT and SWAP
        no_swap = False
        if res.getLength('MB') < MIN_ROOT_SIZE + 1:
            if mem < 2048:
                # Less than 2GB RAM and no swap? No way.
                txt = _("Cannot create new swap partition. Not enough free space")
                logging.error(txt)
                show.error(self.get_toplevel(), txt)
                return
            else:
                no_swap = True

        if no_swap:
            npart = pm.create_partition(device_path, 0, res)
            if npart is None:
                txt = _("Cannot create new partition.")
                logging.error(txt)
                show.error(self.get_toplevel(), txt)
                return
            pm.finalize_changes(disk)
            mount_devices["/"] = npart.path
            fs_devices[npart.path] = "ext4"
            fs.create_fs(npart.path, 'ext4', label='ROOT')
        else:
            # We know for a fact we have at least MIN_ROOT_SIZE + 1GB of space,
            # and at least MIN_ROOT_SIZE of those must go to ROOT.

            # Suggested sizes from Anaconda installer
            if mem < 2048:
                swap_part_size = 2 * mem
            elif 2048 <= mem < 8192:
                swap_part_size = mem
            elif 8192 <= mem < 65536:
                swap_part_size = mem / 2
            else:
                swap_part_size = 4096

            # Max swap size is 10% of all available disk size
            max_swap = res.getLength('MB') * 0.1
            if swap_part_size > max_swap:
                swap_part_size = max_swap

            # Create swap partition
            units = 1000000
            sec_size = disk.device.sectorSize
            new_length = int(swap_part_size * units / sec_size)
            new_end_sector = res.start + new_length
            my_geometry = pm.geom_builder(disk, res.start, new_end_sector, swap_part_size)
            logging.debug("create_partition %s", my_geometry)
            swappart = pm.create_partition(disk, 0, my_geometry)
            if swappart is None:
                txt = _("Cannot create new swap partition.")
                logging.error(txt)
                show.error(self.get_toplevel(), txt)
                return

            # Create new partition for /
            new_size_in_mb = res.getLength('MB') - swap_part_size
            start_sector = new_end_sector + 1
            my_geometry = pm.geom_builder(disk, start_sector, res.end, new_size_in_mb)
            logging.debug("create_partition %s", my_geometry)
            npart = pm.create_partition(disk, 0, my_geometry)
            if npart is None:
                txt = _("Cannot create new partition.")
                logging.error(txt)
                show.error(self.get_toplevel(), txt)
                return

            pm.finalize_changes(disk)

            # Mount points
            mount_devices["swap"] = swappart.path
            fs_devices[swappart.path] = "swap"
            fs.create_fs(swappart.path, 'swap', 'SWAP')

            mount_devices["/"] = npart.path
            fs_devices[npart.path] = "ext4"
            fs.create_fs(npart.path, 'ext4', 'ROOT')

        # TODO: User should be able to choose if installing a bootloader or not (and which one)
        self.settings.set('bootloader_install', True)

        if self.settings.get('bootloader_install'):
            self.settings.set('bootloader', "Grub2")
            self.settings.set('bootloader_device', device_path)
            msg = _("Cnchi will install the %s bootloader") % self.settings.get('bootloader')
            logging.info(msg)
        else:
            logging.info(_("Cnchi will not install any bootloader"))

        if not self.testing:
            self.process = installation_process.InstallationProcess(
                self.settings,
                self.callback_queue,
                mount_devices,
                fs_devices,
                None,
                self.alternate_package_list)

            self.process.start()
        else:
            logging.warning(_("Testing mode. Cnchi will not change anything!"))


# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message): return message

if __name__ == '__main__':
    from test_screen import _,run
    run('InstallationAlongside')
