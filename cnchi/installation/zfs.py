# -*- coding: utf-8; Mode: Python; indent-tabs-mode: nil; tab-width: 4 -*-
#
#  zfs.py
#
# Copyright © 2013-2016 Antergos
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

""" ZFS installation screen """

import subprocess
import os
import logging
import math
import random
import shutil
import string
import time

import parted

import misc.extra as misc
from misc.extra import InstallError
from misc.run_cmd import call

import show_message as show
from installation import action
from installation import install
from installation import wrapper

import parted3.fs_module as fs

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from gtkbasebox import GtkBaseBox

COL_USE_ACTIVE = 0
COL_USE_VISIBLE = 1
COL_USE_SENSITIVE = 2
COL_DISK = 3
COL_SIZE = 4
COL_DEVICE_NAME = 5
COL_DISK_ID = 6

DEST_DIR = "/install"

# Partition sizes are in MiB
MAX_ROOT_SIZE = 30000

# KDE (with all features) needs 8 GB for its files
# (including pacman cache xz files).
MIN_ROOT_SIZE = 8000


def is_int(num):
    """ Checks if num is an integer """
    try:
        int(num)
        return True
    except ValueError:
        return False


def random_generator(size=4, chars=string.ascii_lowercase + string.digits):
    """ Generates a random string to be used as pool name """
    return ''.join(random.choice(chars) for x in range(size))


class InstallationZFS(GtkBaseBox):
    """ ZFS installation screen class """
    def __init__(
            self, params, prev_page="installation_ask", next_page="summary"):
        super().__init__(self, params, "zfs", prev_page, next_page)

        self.page = self.ui.get_object('zfs')

        self.disks = None
        self.diskdic = {}

        self.change_list = []

        self.device_list = self.ui.get_object('treeview')
        self.device_list_store = self.ui.get_object('liststore')
        self.prepare_device_list()
        self.device_list.set_hexpand(True)

        self.installation = None
        self.ids = {}

        pool_name = "antergos_{0}".format(random_generator())

        # Set zfs default options
        self.zfs_options = {
            "force_4k": False,
            "encrypt_swap": False,
            "encrypt_disk": False,
            "encrypt_password": "",
            "scheme": "GPT",
            "pool_type": "None",
            "swap_size": 8192,
            "pool_name": pool_name,
            "use_pool_name": False,
            "device_paths": []
        }

        self.pool_types = {
            0: "None",
            1: "Stripe",
            2: "Mirror",
            3: "RAID-Z",
            4: "RAID-Z2",
            5: "RAID-Z3"
        }

        self.schemes = {
            0: "GPT",
            1: "MBR"
        }

        self.devices = {}
        self.fs_devices = {}
        self.mount_devices = {}

        if os.path.exists("/sys/firmware/efi"):
            # UEFI, use GPT by default
            self.uefi = True
            self.zfs_options["scheme"] = "GPT"
        else:
            # No UEFI, use MBR by default
            self.uefi = False
            self.zfs_options["scheme"] = "MBR"

    def on_use_device_toggled(self, widget, path):
        """ Use device clicked """
        status = self.device_list_store[path][COL_USE_ACTIVE]
        self.device_list_store[path][COL_USE_ACTIVE] = not status
        self.forward_button.set_sensitive(self.check_pool_type())

    def prepare_device_list(self):
        """ Create columns for our treeview """

        # Use check | Disk (sda) | Size(GB) | Name (device name) | Device ID

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
        col = Gtk.TreeViewColumn(
            _("Size (GB)"),
            render_text_right,
            text=COL_SIZE)
        self.device_list.append_column(col)

        col = Gtk.TreeViewColumn(
            _("Device"),
            render_text,
            text=COL_DEVICE_NAME)
        self.device_list.append_column(col)

        col = Gtk.TreeViewColumn(
            _("Disk ID"),
            render_text,
            text=COL_DISK_ID)
        self.device_list.append_column(col)

    def fill_device_list(self):
        """ Fill the partition list with all the data. """

        # We will store our data model in 'device_list_store'
        if self.device_list_store is not None:
            self.device_list_store.clear()

        self.device_list_store = Gtk.TreeStore(
            bool, bool, bool, str, int, str, str)

        with misc.raised_privileges():
            devices = parted.getAllDevices()

        self.get_ids()

        for dev in devices:
            # Skip cdrom, raid, lvm volumes or encryptfs
            if (not dev.path.startswith("/dev/sr") and
                    not dev.path.startswith("/dev/mapper")):
                size_in_gigabytes = int((dev.length * dev.sectorSize) / 1000000000)
                # Use check | Disk (sda) | Size(GB) | Name (device name)
                if dev.path.startswith("/dev/"):
                    path = dev.path[len("/dev/"):]
                else:
                    path = dev.path
                disk_id = self.ids.get(path, "")
                row = [
                    False,
                    True,
                    True,
                    path,
                    size_in_gigabytes,
                    dev.model,
                    disk_id]
                self.device_list_store.append(None, row)

        self.device_list.set_model(self.device_list_store)

    def translate_ui(self):
        """ Translate widgets """
        self.header.set_subtitle(_("ZFS Setup"))

        # Encrypt disk checkbox
        btn = self.ui.get_object("encrypt_disk_btn")
        # TODO: Finnish LUKS+ZFS
        self.zfs_options["encrypt_disk"] = False
        btn.set_sensitive(False)
        btn.set_active(self.zfs_options["encrypt_disk"])

        # Disable/Enable Encrypt disk options entries
        entries = [
            'password_entry', 'password_check_entry',
            'password_lbl', 'password_check_lbl']
        for name in entries:
            entry = self.ui.get_object(name)
            entry.set_sensitive(self.zfs_options["encrypt_disk"])

        # Encrypt swap
        btn = self.ui.get_object('encrypt_swap_btn')
        # TODO: Finnish LUKS+ZFS
        self.zfs_options["encrypt_swap"] = False
        btn.set_sensitive(False)
        btn.set_active(self.zfs_options["encrypt_swap"])

        # Pool name checkbox
        btn = self.ui.get_object("pool_name_btn")
        btn.set_active(self.zfs_options["use_pool_name"])

        # Disable/Enable Pool name entry
        entry = self.ui.get_object('pool_name_entry')
        entry.set_sensitive(self.zfs_options["use_pool_name"])

        # Set pool type label text
        lbl = self.ui.get_object('pool_type_label')
        lbl.set_markup(_("Pool type"))

        # Fill pool types combobox
        combo = self.ui.get_object('pool_type_combo')
        combo.remove_all()
        active_index = 0
        for index in self.pool_types:
            combo.append_text(self.pool_types[index])
            if self.zfs_options["pool_type"] == self.pool_types[index]:
                active_index = index
        combo.set_active(active_index)

        # Set partition scheme label text
        lbl = self.ui.get_object('partition_scheme_label')
        lbl.set_markup(_("Partition scheme"))

        # Fill partition scheme combobox
        combo = self.ui.get_object('partition_scheme_combo')
        combo.remove_all()
        active_index = 0
        for index in self.schemes:
            combo.append_text(self.schemes[index])
            if self.zfs_options["scheme"] == self.schemes[index]:
                active_index = index
        combo.set_active(active_index)

        # Set all labels
        lbl = self.ui.get_object('password_check_lbl')
        lbl.set_markup(_("Validate password"))

        lbl = self.ui.get_object('password_lbl')
        lbl.set_markup(_("Password"))

        lbl = self.ui.get_object('swap_size_lbl')
        lbl.set_markup(_("Swap size (MB)"))

        # Set button labels
        btn = self.ui.get_object('encrypt_swap_btn')
        btn.set_label(_("Encrypt swap"))

        btn = self.ui.get_object('encrypt_disk_btn')
        btn.set_label(_("Encrypt disk"))

        btn = self.ui.get_object('pool_name_btn')
        btn.set_label(_("Pool name"))

        btn = self.ui.get_object('force_4k_btn')
        btn.set_label(_("Force ZFS 4k block size"))

        # Set swap Size
        swap_size = str(self.zfs_options["swap_size"])
        entry = self.ui.get_object("swap_size_entry")
        entry.set_text(swap_size)

    def check_pool_type(self, show_warning=False):
        """ Check that the user has selected the right number
        of devices for the selected pool type """

        num_drives = 0
        msg = ""
        pool_type = self.zfs_options["pool_type"]

        for row in self.device_list_store:
            if row[COL_USE_ACTIVE]:
                num_drives += 1

        if pool_type == "None":
            if num_drives == 1:
                is_ok = True
            else:
                is_ok = False
                msg = _("You must select one drive")
        elif pool_type in ["Stripe", "Mirror"]:
            if num_drives > 1:
                is_ok = True
            else:
                is_ok = False
                msg = _("For the {0} pool_type, you must select at least two "
                        "drives").format(pool_type)
        elif "RAID" in pool_type:
            min_drives = 3
            min_parity_drives = 1

            if pool_type == "RAID-Z2":
                min_drives = 4
                min_parity_drives = 2
            elif pool_type == "RAID-Z3":
                min_drives = 5
                min_parity_drives = 3

            if num_drives < min_drives:
                is_ok = False
                msg = _("You must select at least {0} drives")
                msg = msg.format(min_drives)
            else:
                num = math.log2(num_drives - min_parity_drives)
                if not is_int(num):
                    msg = _("For the {0} pool type, you must use a 'power of "
                            "two' (2,4,8,...) plus the appropriate number of "
                            "drives for the parity. RAID-Z = 1 disk, RAIDZ-2 "
                            "= 2 disks, and so on.")
                    msg = msg.format(pool_type, min_parity_drives)
                else:
                    is_ok = True

        if not is_ok and show_warning:
            show.message(self.get_main_window(), msg)

        return is_ok

    def on_pool_type_help_btn_clicked(self, widget):
        """ User clicked pool type help button """
        combo = self.ui.get_object('pool_type_combo')
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.show_pool_type_help(model[tree_iter][0])

    def show_pool_type_help(self, pool_type):
        """ Show pool type help to the user """
        msg = ""
        if pool_type == "None":
            msg = _("'None' pool will use ZFS on a single selected disk.")
        elif pool_type == "Stripe":
            msg = _("When created together, with equal capacity, ZFS "
                    "space-balancing makes a span act like a RAID0 stripe. "
                    "The space is added together. Provided all the devices "
                    "are of the same size, the stripe behavior will "
                    "continue regardless of fullness level. If "
                    "devices/vdevs are not equally sized, then they will "
                    "fill mostly equally until one device/vdev is full.")
        elif pool_type == "Mirror":
            msg = _("A mirror consists of two or more devices, all data "
                    "will be written to all member devices. Cnchi will "
                    "try to group devices in groups of two.")
        elif pool_type.startswith("RAID-Z"):
            msg = _("ZFS implements RAID-Z, a variation on standard "
                    "RAID-5. ZFS supports three levels of RAID-Z which "
                    "provide varying levels of redundancy in exchange for "
                    "decreasing levels of usable storage. The types are "
                    "named RAID-Z1 through RAID-Z3 based on the number of "
                    "parity devices in the array and the number of disks "
                    "which can fail while the pool remains operational.")
        if msg:
            show.message(self.get_main_window(), msg)

    def on_force_4k_help_btn_clicked(self, widget):
        """ Show 4k help to the user """
        msg = _("Advanced Format (AF) is a new disk format which natively "
                "uses a 4,096 byte instead of 512 byte sector size. To "
                "maintain compatibility with legacy systems AF disks emulate "
                "a sector size of 512 bytes. By default, ZFS will "
                "automatically detect the sector size of the drive. This "
                "combination will result in poorly aligned disk access which "
                "will greatly degrade the pool performance. If that might be "
                "your case, you can force ZFS to use a sector size of 4,096 "
                "bytes by selecting this option.")
        show.message(self.get_main_window(), msg)

    def on_encrypt_swap_btn_toggled(self, widget):
        """ Swap encrypt button """
        self.zfs_options["encrypt_swap"] = not self.zfs_options["encrypt_swap"]

    def on_encrypt_disk_btn_toggled(self, widget):
        """ Disk encrypt button """
        status = widget.get_active()

        names = [
            'password_entry', 'password_check_entry',
            'password_lbl', 'password_check_lbl']

        for name in names:
            obj = self.ui.get_object(name)
            obj.set_sensitive(status)
        self.zfs_options["encrypt_disk"] = status
        self.settings.set('use_luks', status)

    def on_pool_name_btn_toggled(self, widget):
        """ Use a specific pool name """
        obj = self.ui.get_object('pool_name_entry')
        status = not obj.get_sensitive()
        obj.set_sensitive(status)
        self.zfs_options["use_pool_name"] = status

    def on_force_4k_btn_toggled(self, widget):
        """ Force 4k sector size """
        self.zfs_options["force_4k"] = not self.zfs_options["force_4k"]

    def on_partition_scheme_combo_changed(self, widget):
        """ Select MBR or GPT """
        tree_iter = widget.get_active_iter()
        if tree_iter is not None:
            model = widget.get_model()
            self.zfs_options["scheme"] = model[tree_iter][0]

    def on_pool_type_combo_changed(self, widget):
        """ Choose zfs pool type """
        tree_iter = widget.get_active_iter()
        if tree_iter is not None:
            model = widget.get_model()
            self.zfs_options["pool_type"] = model[tree_iter][0]
            # self.show_pool_type_help(model[tree_iter][0])
            self.forward_button.set_sensitive(self.check_pool_type())

    def prepare(self, direction):
        """ Prepare screen """
        self.zfs_options['encrypt_disk'] = self.settings.get('use_luks')

        self.translate_ui()
        self.fill_device_list()
        self.show_all()
        self.forward_button.set_sensitive(self.check_pool_type())

    def store_values(self):
        """ Store all vars """

        # Get device paths
        device_paths = []
        for row in self.device_list_store:
            if row[COL_USE_ACTIVE]:
                device_paths.append("/dev/{0}".format(row[COL_DISK]))
        self.zfs_options["device_paths"] = device_paths

        # Get swap size
        txt = self.ui.get_object("swap_size_entry").get_text()
        try:
            self.zfs_options["swap_size"] = int(txt)
        except ValueError as verror:
            # Error reading value, set 8GB as default
            self.zfs_options["swap_size"] = 8192

        # Get pool name

        # TODO: The pool name must begin with a letter, and
        # can only contain alphanumeric  characters  as  well  as  underscore
        # ("_"),  dash ("-"), period ("."), colon (":"), and space (" "). The
        # pool names "mirror", "raidz", "spare" and "log"  are  reserved,  as
        # are  names beginning with the pattern "c[0-9]".

        txt = self.ui.get_object("pool_name_entry").get_text()
        if txt:
            self.zfs_options["pool_name"] = txt

        # Bootloader needs to know zpool name
        self.settings.set("zfs_pool_name", self.zfs_options["pool_name"])

        # Get password
        txt = self.ui.get_object("password_lbl").get_text()
        self.zfs_options["encrypt_password"] = txt

        # self.set_bootloader()

        return True

    # ZFS Creation starts here -------------------------------------------------

    def append_change(self, action_type, device, info=""):
        """ Add change for summary screen """
        if action_type == "create":
            info = _("Create {0} on device {1}").format(info, device)
            encrypt = self.zfs_options["encrypt_disk"]
            act = action.Action("info", info, True, True, "", encrypt)
        elif action_type == "add":
            info = _("Add device {0} to {1}").format(device, info)
            encrypt = self.zfs_options["encrypt_disk"]
            act = action.Action("info", info, True, True, "", encrypt)
        elif action_type == "delete":
            act = action.Action(action_type, device)
        self.change_list.append(act)

    def get_changes(self):
        """ Grab all changes for confirmation in summary screen """

        self.change_list = []
        device_paths = self.zfs_options["device_paths"]

        device_path = device_paths[0]

        pool_name = self.zfs_options["pool_name"]

        if self.zfs_options["scheme"] == "GPT":
            self.append_change("delete", device_path)
            if not self.uefi:
                self.append_change("create", device_path, "BIOS boot (2MB)")
                self.append_change("create", device_path, "Antergos Boot (512MB)")
            else:
                # UEFI
                if self.bootloader == "grub":
                    self.append_change("create", device_path, "UEFI System (200MB)")
                    self.append_change("create", device_path, "Antergos Boot (512MB)")
                else:
                    self.append_change("create", device_path, "Antergos Boot (512MB)")
        else:
            # MBR
            self.append_change("delete", device_path)
            self.append_change("create", device_path, "Antergos Boot (512MB)")

        msg = "Antergos ZFS pool ({0})".format(pool_name)
        self.append_change("create", device_path, msg)
        self.append_change("create", device_path, "Antergos ZFS vol (swap)")

        if self.settings.get("use_home"):
            self.append_change("create", device_path, "Antergos ZFS vol (/home)")

        # Now init all other devices that will form part of the pool
        for device_path in device_paths[1:]:
            self.append_change("delete", device_path)
            msg = "Antergos ZFS pool ({0})".format(pool_name)
            self.append_change("add", device_path, msg)

        return self.change_list

    def init_device(self, device_path, scheme="GPT"):
        """ Initialize device """

        logging.debug("Zapping device %s...", device_path)

        offset = 20480

        # Zero out all GPT and MBR data structures
        wrapper.sgdisk("zap-all", device_path)

        # Clear all magic strings/signatures
        # Wipe out first "offset" sectors
        wrapper.dd("/dev/zero", device_path, bs=512, count=offset)

        # Clear the end "offset" sectors of the disk, too.
        try:
            seek = int(call(["blockdev", "--getsz", device_path])) - offset
            wrapper.dd("/dev/zero", device_path, bs=512, count=offset, seek=seek)
        except ValueError as ex:
            logging.warning(ex)

        wrapper.wipefs(device_path)

        if scheme == "GPT":
            # Create fresh GPT table
            wrapper.sgdisk("clear", device_path)

            # Inform the kernel of the partition change.
            # Needed if the hard disk had a MBR partition table.
            call(["partprobe", device_path])
        else:
            # Create fresh MBR table
            wrapper.parted_mklabel(device_path, "msdos")

        """
        if self.zfs_options["encrypt_disk"]:
            from installation import auto_partition as ap
            vol_name = device_path.split("/")[-1]
            ap.setup_luks(
                luks_device=device_path,
                luks_name=vol_name,
                luks_pass=self.zfs_options["encrypt_password"])
            self.settings.set("use_luks", True)
        """

        call(["sync"])

    def run_format(self):
        """ Create partitions and file systems """
        # https://wiki.archlinux.org/index.php/Installing_Arch_Linux_on_ZFS
        # https://wiki.archlinux.org/index.php/ZFS#GRUB-compatible_pool_creation

        device_paths = self.zfs_options["device_paths"]
        logging.debug("Configuring ZFS in %s", ",".join(device_paths))

        # Wipe all disks that will be part of the installation.
        # This cannot be undone!
        self.init_device(device_paths[0], self.zfs_options["scheme"])
        for device_path in device_paths[1:]:
            self.init_device(device_path, "GPT")

        device_path = device_paths[0]
        solaris_partition_number = -1

        self.settings.set('bootloader_device', device_path)

        if self.zfs_options["scheme"] == "GPT":
            part_num = 1

            if not self.uefi:
                # BIOS and GPT
                # Create BIOS Boot Partition
                # GPT GUID: 21686148-6449-6E6F-744E-656564454649
                # This partition is not required if the system is UEFI based,
                # as there is no such embedding of the second-stage code in that case
                wrapper.sgdisk_new(device_path, part_num, "BIOS_BOOT", 2, "EF02")
                part_num += 1

                # Create BOOT partition
                wrapper.sgdisk_new(device_path, part_num, "ANTERGOS_BOOT", 512, "8300")
                fs.create_fs(device_path + str(part_num), "ext4", "ANTERGOS_BOOT")
                self.devices['boot'] = "{0}{1}".format(device_path, part_num)
                self.fs_devices[self.devices['boot']] = "ext4"
                self.mount_devices['/boot'] = self.devices['boot']
                part_num += 1
            else:
                # UEFI and GPT
                if self.bootloader == "grub2":
                    # Create EFI System Partition (ESP)
                    # GPT GUID: C12A7328-F81F-11D2-BA4B-00A0C93EC93B
                    wrapper.sgdisk_new(device_path, part_num, "UEFI_SYSTEM", 200, "EF00")
                    self.devices['efi'] = "{0}{1}".format(device_path, part_num)
                    self.fs_devices[self.devices['efi']] = "vfat"
                    self.mount_devices['/boot/efi'] = self.devices['efi']
                    part_num += 1

                    # Create BOOT partition
                    wrapper.sgdisk_new(device_path, part_num, "ANTERGOS_BOOT", 512, "8300")
                    fs.create_fs(device_path + str(part_num), "ext4", "ANTERGOS_BOOT")
                    self.devices['boot'] = "{0}{1}".format(device_path, part_num)
                    self.fs_devices[self.devices['boot']] = "ext4"
                    self.mount_devices['/boot'] = self.devices['boot']
                    part_num += 1
                else:
                    # systemd-boot, refind
                    # Create BOOT partition
                    wrapper.sgdisk_new(device_path, part_num, "ANTERGOS_BOOT", 512, "EF00")
                    fs.create_fs(device_path + str(part_num), "vfat", "ANTERGOS_BOOT")
                    self.devices['boot'] = "{0}{1}".format(device_path, part_num)
                    self.fs_devices[self.devices['boot']] = "vfat"
                    self.mount_devices['/boot'] = self.devices['boot']
                    part_num += 1

            # The rest of the disk will be of solaris type
            wrapper.sgdisk_new(device_path, part_num, "ANTERGOS_ZFS", 0, "BF00")
            solaris_partition_number = part_num
            self.devices['root'] = "{0}{1}".format(device_path, part_num)
            # self.fs_devices[self.devices['root']] = "zfs"
            self.mount_devices['/'] = self.devices['root']
        else:
            # MBR

            # Create boot partition (all sizes are in MiB)
            # if start is -1 wrapper.parted_mkpart assumes that our partition
            # starts at 1 (first partition in disk)
            start = -1
            end = 512
            part = "1"
            wrapper.parted_mkpart(device_path, "primary", start, end)

            # Set boot partition as bootable
            wrapper.parted_set(device_path, part, "boot", "on")

            # Format the boot partition as well as any other system partitions.
            # Do not do anything to the Solaris partition nor to the BIOS boot
            # partition. ZFS will manage the first, and the bootloader the
            # second.

            if self.uefi:
                fs_boot = "vfat"
            else:
                fs_boot = "ext4"

            fs.create_fs(device_path + part, fs_boot, "ANTERGOS_BOOT")
            self.devices['boot'] = "{0}{1}".format(device_path, part)
            self.fs_devices[self.devices['boot']] = fs_boot
            self.mount_devices['/boot'] = self.devices['boot']

            # The rest of the disk will be of solaris type
            start = end
            wrapper.parted_mkpart(device_path, "primary", start, "-1s")
            solaris_partition_number = 2
            self.devices['root'] = "{0}{1}".format(device_path, 2)
            # self.fs_devices[self.devices['root']] = "zfs"
            self.mount_devices['/'] = self.devices['root']

        # Wait until /dev initialized correct devices
        call(["udevadm", "settle"])
        call(["sync"])

        self.create_zfs(solaris_partition_number)

    def get_ids(self):
        """ Get disk and partitions IDs """
        path = "/dev/disk/by-id"
        for entry in os.scandir(path):
            if (not entry.name.startswith('.') and
                    entry.is_symlink() and
                    entry.name.startswith("ata")):
                dest_path = os.readlink(entry.path)
                device = dest_path.split("/")[-1]
                self.ids[device] = entry.name

    def get_home_size(self, pool_name):
        """ Get recommended /home zvol size in GB """
        pool_size = self.get_pool_size(pool_name)
        home_size = 0
        if pool_size != 0:
            root_needs = pool_size // 5
            if root_needs > MAX_ROOT_SIZE:
                root_needs = MAX_ROOT_SIZE
            elif root_needs < MIN_ROOT_SIZE:
                root_needs = MIN_ROOT_SIZE
            home_size = pool_size - root_needs
        return home_size

    @staticmethod
    def get_pool_size(pool_name):
        """ Gets zfs pool size in GB """
        try:
            cmd_line = "zpool list -H -o size {0}".format(pool_name)
            logging.debug(cmd_line)
            cmd = cmd_line.split()
            output = subprocess.check_output(cmd)
            pool_size = output.decode().strip('\n')
            pool_size = pool_size.replace(',', '.')
            if 'M' in pool_size:
                pool_size = int(pool_size[:-1]) // 1024
            elif 'G' in pool_size:
                pool_size = int(pool_size[:-1])
            elif 'T' in pool_size:
                pool_size = int(pool_size[:-1]) * 1024
            elif 'P' in pool_size:
                pool_size = int(pool_size[:-1]) * 1024 * 1024
        except (subprocess.CalledProcessError, ValueError) as err:
            logging.warning(
                "Can't get zfs %s pool size: %s",
                pool_name,
                err)
            pool_size = 0
        return pool_size

    def get_swap_size(self, pool_name):
        """ Gets recommended swap size in GB """

        cmd = ["grep", "MemTotal", "/proc/meminfo"]
        try:
            mem_total = subprocess.check_output(cmd).decode().split()
            mem_total = int(mem_total[1])
            mem = mem_total / 1024
        except (subprocess.CalledProcessError, ValueError) as mem_error:
            logging.warning("Can't get system memory")
            mem = 4096

        swap_size = 0

        # Suggested sizes from Anaconda installer (these are in MB)
        if mem < 2048:
            swap_size = 2 * mem
        elif 2048 <= mem < 8192:
            swap_size = mem
        elif 8192 <= mem < 65536:
            swap_size = mem // 2
        else:
            swap_size = 4096

        # MB to GB
        swap_size = swap_size // 1024

        # Check pool size and adapt swap size if necessary
        # Swap size should not exceed 10% of all available pool size

        pool_size = self.get_pool_size(pool_name)
        if pool_size > 0:
            # Max swap size is 10% of all available disk size
            max_swap = pool_size * 0.1
            if swap_size > max_swap:
                swap_size = max_swap

        return swap_size

    def create_zfs_vol(self, pool_name, vol_name, size):
        """ Creates zfs vol inside the pool
            size is in GB """

        # Round up
        size = math.ceil(size)
        logging.debug(
            "Creating a zfs vol %s/%s of size %dGB",
            pool_name,
            vol_name,
            size)
        cmd = [
            "zfs", "create",
            "-V", "{0}G".format(size),
            "-b", str(os.sysconf("SC_PAGE_SIZE")),
            "-o", "primarycache=metadata",
            "-o", "checksum=off",
            "-o", "com.sun:auto-snapshot=false",
            "{0}/{1}".format(pool_name, vol_name)]
        call(cmd, fatal=True)

    @staticmethod
    def set_zfs_mountpoint(zvol, mount_point):
        """ Sets mount point of zvol and tries to mount it """
        try:
            cmd = ["zfs", "set", "mountpoint={0}".format(mount_point), zvol]
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
            err_output = err.output.decode().strip("\n")
            logging.warning(err_output)

    @staticmethod
    def get_pool_id(pool_name):
        """ Get zpool id number """
        output = call(["zpool", "import"])
        if not output:
            return None

        name = identifier = state = None
        lines = output.split("\n")
        for line in lines:
            if "pool:" in line:
                name = line.split(": ")[1]
            elif "id:" in line:
                identifier = line.split(": ")[1]
            elif "state:" in line:
                state = line.split(": ")[1]
                if name == pool_name and state == "ONLINE":
                    return identifier
                else:
                    name = identifier = state = None
        return None

    def create_zfs_pool(self, pool_name, pool_type, device_paths):
        """ Create zpool """

        if pool_type not in self.pool_types.values():
            raise InstallError("Unknown pool type: {0}".format(pool_type))

        #for device_path in device_paths:
        #    cmd = ["zpool", "labelclear", device_path]
        #    call(cmd)

        cmd = ["zpool", "create"]

        if self.zfs_options["force_4k"]:
            cmd.extend(["-o", "ashift=12"])

        cmd.extend(["-m", DEST_DIR, pool_name])

        pool_type = pool_type.lower().replace("-", "")

        if pool_type in ["none", "stripe"]:
            # Add first device
            cmd.append(device_paths[0])
        elif pool_type == "mirror":
            if len(device_paths) > 2 and len(device_paths) % 2 == 0:
                # Try to mirror pair of devices
                # (mirrors of two devices each)
                for i,k in zip(device_paths[0::2], device_paths[1::2]):
                    cmd.append(pool_type)
                    cmd.extend([i, k])
            else:
                cmd.append(pool_type)
                cmd.extend(device_paths)
        else:
            cmd.append(pool_type)
            cmd.extend(device_paths)

        # Wait until /dev initialized correct devices
        call(["udevadm", "settle"])
        call(["sync"])

        logging.debug("Creating zfs pool %s of type %s", pool_name, pool_type)
        if call(cmd) == False:
            # Try again, now with -f
            cmd.insert(2, "-f")
            if call(cmd) == False:
                # Wait 10 seconds more and try again (last hope)
                time.sleep(10)
                call(cmd, fatal=True)

        # Wait until /dev initialized correct devices
        call(["udevadm", "settle"])
        call(["sync"])

        if pool_type == "stripe":
            # Add the other devices that were left out
            cmd = ["zpool", "add", pool_name]
            cmd.extend(device_paths[1:])
            call(cmd, fatal=True)

        logging.debug("Pool %s created.", pool_name)

    @staticmethod
    def get_partition_path(device, part_num):
        """ This is awful and prone to fail. We should do some
            type of test here """

        # Remove /dev/
        path = device.replace('/dev/', '')
        partials = [
            'rd/', 'ida/', 'cciss/', 'sx8/', 'mapper/', 'mmcblk', 'md', 'nvme']
        found = [p for p in partials if path.startswith(p)]
        if found:
            return "{0}p{1}".format(device, part_num)
        else:
            return "{0}{1}".format(device, part_num)

    def create_zfs(self, solaris_partition_number):
        """ Setup ZFS system """

        device_paths = self.zfs_options["device_paths"]
        if not device_paths:
            txt = _("No devices were selected for the ZFS pool")
            raise InstallError(txt)

        # Make sure the ZFS modules are loaded
        call(["modprobe", "zfs"])

        # Using by-id (recommended) does not work atm
        # https://github.com/zfsonlinux/zfs/issues/3708

        # Can't use the whole first disk, just the dedicated zfs partition
        device_paths[0] = self.get_partition_path(
            device_paths[0],
            solaris_partition_number)

        line = ", ".join(device_paths)
        logging.debug("Cnchi will create a ZFS pool using %s devices", line)

        # Just in case...
        if os.path.exists("/etc/zfs/zpool.cache"):
            os.remove("/etc/zfs/zpool.cache")

        try:
            os.mkdir(DEST_DIR, mode=0o755)
        except OSError:
            pass

        pool_name = self.zfs_options["pool_name"]
        pool_type = self.zfs_options["pool_type"]

        # Create zpool
        self.create_zfs_pool(pool_name, pool_type, device_paths)

        # Set the mount point of the root filesystem
        self.set_zfs_mountpoint(pool_name, "/")

        # Set the bootfs property on the descendant root filesystem so the
        # boot loader knows where to find the operating system.
        cmd = ["zpool", "set", "bootfs={0}".format(pool_name), pool_name]
        call(cmd, fatal=True)

        # Create zpool.cache file
        cmd = ["zpool", "set", "cachefile=/etc/zfs/zpool.cache", pool_name]
        call(cmd, fatal=True)

        # Create any zfs subvolumes
        if self.settings.get('use_home'):
            # Create home zvol
            home_size = self.get_home_size(pool_name)
            logging.debug("Creating zfs subvolume 'home' (%dGB)", home_size)
            self.create_zfs_vol(pool_name, "home", home_size)
            self.set_zfs_mountpoint("{0}/home".format(pool_name), "/home")

        # Create swap zvol
        swap_size = self.get_swap_size(pool_name)
        logging.debug("Creating zfs subvolume 'swap' (%dGB)", swap_size)
        self.create_zfs_vol(pool_name, "swap", swap_size)

        # Wait until /dev initialized correct devices
        call(["udevadm", "settle"])
        call(["sync"])

        # Export the pool
        # Makes the kernel to flush all pending data to disk, writes data to
        # the disk acknowledging that the export was done, and removes all
        # knowledge that the storage pool existed in the system
        logging.debug("Exporting pool %s...", pool_name)
        cmd = ["zpool", "export", "-f", pool_name]
        call(cmd, fatal=True)

        # Let's get the id of the pool (to import it)
        pool_id = self.get_pool_id(pool_name)

        if not pool_id:
            # Something bad has happened. Will use the pool name instead.
            pool_id = pool_name

        # Save pool id
        self.settings.set("zfs_pool_id", pool_id)

        # Finally, re-import the pool by-id
        logging.debug("Importing pool %s (%s)...", pool_name, pool_id)
        cmd = [
            "zpool", "import",
            "-d", "/dev/disk/by-id",
            "-R", DEST_DIR,
            pool_id]
        call(cmd, fatal=True)

        # Copy created cache file to destination
        try:
            dst_dir = os.path.join(DEST_DIR, "etc/zfs")
            os.makedirs(dst_dir, mode=0o755, exist_ok=True)
            src = "/etc/zfs/zpool.cache"
            dst = os.path.join(dst_dir, "zpool.cache")
            shutil.copyfile(src, dst)
        except OSError as copy_error:
            logging.warning(copy_error)

        # Store hostid
        hostid = call(["hostid"])
        if hostid:
            with open("/install/etc/hostid", "w") as hostid_file:
                hostid_file.write("{0}\n".format(hostid))

    def run_install(self, packages, metalinks):
        """ Start installation process """

        self.installation = install.Installation(
            self.settings,
            self.callback_queue,
            packages,
            metalinks,
            self.mount_devices,
            self.fs_devices)

        self.installation.start()

try:
    _("")
except NameError as err:
    def _(message):
        return message

if __name__ == '__main__':
    # When testing, no _() is available

    from test_screen import _, run
    run('zfs')
