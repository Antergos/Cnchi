# -*- coding: utf-8; Mode: Python; indent-tabs-mode: nil; tab-width: 4 -*-
#
#  zfs.py
#
#  Copyright © 2013-2015 Antergos
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import subprocess
import os
import logging

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

try:
    from gtkbasebox import GtkBaseBox
except ImportError:
    import sys
    sys.path.append('/usr/share/cnchi/cnchi')
    from gtkbasebox import GtkBaseBox

import parted
import misc.misc as misc

from installation import wrapper

COL_USE_ACTIVE = 0
COL_USE_VISIBLE = 1
COL_USE_SENSITIVE = 2
COL_DISK = 3
COL_SIZE = 4
COL_DEVICE_NAME = 5
COL_WWN = 6


class InstallationZFS(GtkBaseBox):
    def __init__(self, params, prev_page="installation_ask", next_page="summary"):
        super().__init__(self, params, "zfs", prev_page, next_page)

        self.page = self.ui.get_object('zfs')

        self.disks = None
        self.diskdic = {}

        self.device_list = self.ui.get_object('treeview')
        self.device_list_store = self.ui.get_object('liststore')
        self.prepare_device_list()
        self.device_list.set_hexpand(True)

        self.zfs_options = {
            "force_4k": False,
            "pool_name": "",
            "encrypt_swap": False,
            "encrypt_disk": False,
            "encrypt_password": "",
            "scheme": "GPT",
            "pool_type": "None",
            "swap_size": 0,
            "pool_name": "",
            "use_pool_name": False,
            "device_paths": []
        }

        self.UEFI = True

        if not os.path.exists("/sys/firmware/efi"):
            # If no UEFI, use MBR by default
            self.UEFI = False
            self.zfs_options["scheme"] = "MBR"

        '''
        liststore
        pool_type_label
        pool_type_combo
        partition_scheme_label
        partition_scheme_combo
        scrolledwindow
        treeview
        password_check_lbl
        password_check_entry
        encrypt_swap_btn
        password_entry
        password_lbl
        encrypt_disk_btn
        swap_size_lbl
        swap_size_entry
        pool_name_btn
        pool_name_entry
        force_4k_btn
        '''

    def on_use_device_toggled(self, widget, path):
        self.device_list_store[path][COL_USE_ACTIVE] = not self.device_list_store[path][COL_USE_ACTIVE]

    def prepare_device_list(self):
        """ Create columns for our treeview """

        # Use check | Disk (sda) | Size(GB) | Name (device name)

        use_toggle = Gtk.CellRendererToggle()
        use_toggle.connect("toggled", self.on_use_device_toggled)

        col = Gtk.TreeViewColumn(
            _("Use"),
            use_toggle,
            active=COL_USE_ACTIVE,
            visible=COL_USE_VISIBLE,
            sensitive=COL_USE_SENSITIVE)

        self.device_list.append_column(col)

        render_text = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn(_("Disk"), render_text, text=COL_DISK)
        self.device_list.append_column(col)

        render_text_right = Gtk.CellRendererText()
        render_text_right.set_property("xalign", 1)
        col = Gtk.TreeViewColumn(_("Size (GB)"), render_text_right, text=COL_SIZE)
        self.device_list.append_column(col)

        col = Gtk.TreeViewColumn(_("Device"), render_text, text=COL_DEVICE_NAME)
        self.device_list.append_column(col)

        col = Gtk.TreeViewColumn(_("WWN"), render_text, text=COL_WWN)
        self.device_list.append_column(col)

    def read_wwns(self):
        # lsblk -do NAME,WWN
        pass

    def fill_device_list(self):
        """ Fill the partition list with all the data. """

        # We will store our data model in 'device_list_store'
        if self.device_list_store is not None:
            self.device_list_store.clear()

        self.device_list_store = Gtk.TreeStore(bool, bool, bool, str, int, str, str)

        with misc.raised_privileges():
            devices = parted.getAllDevices()

        for dev in devices:
            print(dev)
            # avoid cdrom and any raid, lvm volumes or encryptfs
            if not dev.path.startswith("/dev/sr") and not dev.path.startswith("/dev/mapper"):
                size_in_gigabytes = int((dev.length * dev.sectorSize) / 1000000000)
                # Use check | Disk (sda) | Size(GB) | Name (device name)
                if dev.path.startswith("/dev/"):
                    path = dev.path[len("/dev/"):]
                else:
                    path = dev.path
                row = [False, True, True, path, size_in_gigabytes, dev.model, ""]
                self.device_list_store.append(None, row)

        self.device_list.set_model(self.device_list_store)

    def translate_ui(self):
        # Disable objects
        entries = [
            'pool_name_entry', 'password_entry', 'password_check_entry',
            'password_lbl', 'password_check_lbl']
        for name in entries:
            entry = self.ui.get_object(name)
            entry.set_sensitive(False)

        '''
        liststore
        scrolledwindow
        treeview
        '''

        lbl = self.ui.get_object('pool_type_label')
        lbl.set_markup(_("Pool type"))

        pool_types = {
            0: "None",
            1: "Stripe",
            2: "Mirror",
            3: "RAID-Z",
            4: "RAID-Z2"
        }

        combo = self.ui.get_object('pool_type_combo')
        combo.remove_all()
        active_index = 0
        for index in pool_types:
            combo.append_text(pool_types[index])
            if self.zfs_options["pool_type"] == pool_types[index]:
                active_index = index
        combo.set_active(active_index)

        lbl = self.ui.get_object('partition_scheme_label')
        lbl.set_markup(_("Partition scheme"))

        schemes = {
            0: "GPT",
            1: "MBR"
        }

        combo = self.ui.get_object('partition_scheme_combo')
        combo.remove_all()
        active_index = 0
        for index in schemes:
            combo.append_text(schemes[index])
            if self.zfs_options["scheme"] == schemes[index]:
                active_index = index
        combo.set_active(active_index)

        lbl = self.ui.get_object('password_check_lbl')
        lbl.set_markup(_("Validate password"))

        lbl = self.ui.get_object('password_lbl')
        lbl.set_markup(_("Password"))

        lbl = self.ui.get_object('swap_size_lbl')
        lbl.set_markup(_("Swap size"))

        btn = self.ui.get_object('encrypt_swap_btn')
        btn.set_label(_("Encrypt swap"))

        btn = self.ui.get_object('encrypt_disk_btn')
        btn.set_label(_("Encrypt disk"))

        btn = self.ui.get_object('pool_name_btn')
        btn.set_label(_("Pool name"))

        btn = self.ui.get_object('force_4k_btn')
        btn.set_label(_("Force ZFS 4k block size"))

    def on_encrypt_swap_btn_toggled(self, widget):
        self.encrypt_swap = not self.encrypt_swap

    def on_encrypt_disk_btn_toggled(self, widget):
        names = [
            'password_entry', 'password_check_entry',
            'password_lbl', 'password_check_lbl']

        for name in names:
            obj = self.ui.get_object(name)
            status = not obj.get_sensitive()
            obj.set_sensitive(status)
        self.zfs_options["encrypt_disk"] = status

    def on_pool_name_btn_toggled(self, widget):
        obj = self.ui.get_object('pool_name_entry')
        status = not obj.get_sensitive()
        obj.set_sensitive(status)
        self.zfs_options["use_pool_name"] = status

    def on_force_4k_btn_toggled(self, widget):
        self.zfs_options["force_4k"] = not self.zfs_options["force_4k"]

    def on_partition_scheme_combo_changed(self, widget):
        tree_iter = widget.get_active_iter()
        if tree_iter != None:
            model = widget.get_model()
            self.zfs_options["scheme"] = model[tree_iter][0]

    def on_pool_type_combo_changed(self, widget):
        tree_iter = widget.get_active_iter()
        if tree_iter != None:
            model = widget.get_model()
            self.zfs_options["pool_type"] = model[tree_iter][0]

    def prepare(self, direction):
        self.translate_ui()
        self.fill_device_list()
        self.show_all()

    def store_values():
        """ Store all vars """
        '''
        liststore
        pool_type_label
        pool_type_combo
        partition_scheme_label
        partition_scheme_combo
        scrolledwindow
        treeview
        password_check_lbl
        password_check_entry
        encrypt_swap_btn
        password_entry
        password_lbl
        encrypt_disk_btn
        swap_size_lbl
        swap_size_entry
        pool_name_btn
        pool_name_entry
        force_4k_btn
        '''

        # Get device paths
        device_paths = []
        for row in self.device_list_store:
            if row[COL_USE_ACTIVE]:
                device_paths.append("/dev/{0}".format(row[COL_DISK]))
        self.zfs_options["device_paths"] = device_paths

        # Get swap size
        txt = self.ui.get_object("swap_size_entry").get_text()
        self.zfs_options["swap_size"] = int(txt)

        # Get pool name
        txt = self.ui.get_object("pool_name_entry").get_text()
        self.zfs_options["pool_name"] = txt

        # Get password
        txt = self.ui.get_object("password_lbl").get_text()
        self.zfs_options["encrypt_password"] = txt

        # self.set_bootloader()

        return True

    def init_device(self, device, scheme="GPT"):
        if scheme == "GPT":
            # Clean partition table to avoid issues!
            wrapper.sgdisk("zap-all", device)

            # Clear all magic strings/signatures - mdadm, lvm, partition tables etc.
            wrapper.dd("/dev/zero", device, bs=512, count=2048)
            wrapper.wipefs(device)

            # Create fresh GPT
            wrapper.sgdisk("clear", device)

            # Inform the kernel of the partition change. Needed if the hard disk had a MBR partition table.
            try:
                subprocess.check_call(["partprobe", device])
            except subprocess.CalledProcessError as err:
                txt = "Error informing the kernel of the partition change. Command {0} failed: {1}".format(err.cmd, err.output)
                logging.error(txt)
                txt = _("Error informing the kernel of the partition change. Command {0} failed: {1}").format(err.cmd, err.output)
                raise InstallError(txt)
        else:
            # DOS MBR partition table
            # Start at sector 1 for 4k drive compatibility and correct alignment
            # Clean partitiontable to avoid issues!
            wrapper.dd("/dev/zero", device, bs=512, count=2048)
            wrapper.wipefs(device)

            # Create DOS MBR
            wrapper.parted_mktable(device, "msdos")

    def create_zfs_pool(self):
        # lsblk -do NAME,WWN
        pass

    def run_format(self):
        # https://wiki.archlinux.org/index.php/Installing_Arch_Linux_on_ZFS
        # https://wiki.archlinux.org/index.php/ZFS#GRUB-compatible_pool_creation

        device_paths = self.zfs_options["device_paths"]
        logging.debug("Configuring ZFS in %s", ",".join(device_paths))

        if self.scheme == "GPT":
            device = device_paths[0]

            self.init_device(device, "GPT")

            part_num = 1

            if not self.UEFI:
                # Create BIOS Boot Partition
                # GPT GUID: 21686148-6449-6E6F-744E-656564454649
                # This partition is not required if the system is UEFI based,
                # as there is no such embedding of the second-stage code in that case
                wrapper.sgdisk_new(device, part_num, "BIOS_BOOT", 2, "EF02")
                part_num += 1
                wrapper.sgdisk_new(device, part_num, "ANTERGOS_BOOT", 512, "8300")
                part_num += 1
            else:
                # UEFI
                if self.bootloader == "grub":
                    # Create EFI System Partition (ESP)
                    # GPT GUID: C12A7328-F81F-11D2-BA4B-00A0C93EC93B
                    wrapper.sgdisk_new(device, part_num, "UEFI_SYSTEM", 200, "EF00")
                    part_num += 1
                    wrapper.sgdisk_new(device, part_num, "ANTERGOS_BOOT", 512, "8300")
                    part_num += 1
                else:
                    # systemd-boot, refind
                    wrapper.sgdisk_new(device, part_num, "ANTERGOS_BOOT", 512, "EF00")
                    part_num += 1

            wrapper.sgdisk_new(device, part_num, "ANTERGOS_ZFS", 0, "BF00")

            # Now init all other devices that will form part of the pool
            for device in device_paths[1:]:
                self.init_device(device, "GPT")
                wrapper.sgdisk_new(device, 1, "ANTERGOS_ZFS", 0, "BF00")
        else:
            # MBR
            device = device_paths[0]

            self.init_device(device, "MBR")

            # Create boot partition (all sizes are in MiB)
            # if start is -1 wrapper.parted_mkpart assumes that our partition starts at 1 (first partition in disk)
            start = -1
            end = 512
            wrapper.parted_mkpart(device, "primary", start, end)

            # Set boot partition as bootable
            wrapper.parted_set(device, "1", "boot", "on")

            start = end
            end = "-1s"
            wrapper.parted_mkpart(device, "primary", start, end)

            # Now init all other devices that will form part of the pool
            for device in device_paths[1:]:
                self.init_device(device, "MBR")
                wrapper.parted_mkpart(device, "primary", -1, "-1s")

        # Wait until /dev initialized correct devices
        subprocess.check_call(["udevadm", "settle"])

        self.create_zfs_pool()

    def run_install(self, packages, metalinks):
        """ Start installation process """
        pass


# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

if __name__ == '__main__':
    from test_screen import _, run
    run('zfs')
