# -*- coding: utf-8; Mode: Python; indent-tabs-mode: nil; tab-width: 4 -*-
#
#  zfs.py
#
# Copyright © 2013-2015 Antergos
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

import subprocess
import os
import logging
import math
import shutil

import parted

import misc.extra as misc
from misc.extra import InstallError

import show_message as show
from installation import action
from installation import install
from installation import wrapper

import parted3.fs_module as fs

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

try:
    from gtkbasebox import GtkBaseBox
except ImportError:
    import sys
    sys.path.append('/usr/share/cnchi/cnchi')
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
    try:
        int(num)
        return True
    except ValueError:
        return False


class InstallationZFS(GtkBaseBox):
    def __init__(
            self, params, prev_page="installation_ask", next_page="summary", **kwargs):
        super().__init__(self, params, "zfs", prev_page, next_page, **kwargs)

        self.page = self.ui.get_object('zfs')
        self.title = _('ZFS Setup')

        self.disks = None
        self.diskdic = {}

        self.change_list = []

        self.device_list = self.ui.get_object('treeview')
        self.device_list_store = self.ui.get_object('liststore')
        self.prepare_device_list()
        self.device_list.set_hexpand(True)

        self.ids = {}

        # Set zfs default options
        self.zfs_options = {
            "force_4k": False,
            "encrypt_swap": False,
            "encrypt_disk": False,
            "encrypt_password": "",
            "scheme": "GPT",
            "pool_type": "None",
            "swap_size": 8192,
            "pool_name": "antergos",
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

        self.pool_types_help_shown = []

        self.devices = {}
        self.fs_devices = {}
        self.mount_devices = {}

        if os.path.exists("/sys/firmware/efi"):
            # UEFI, use GPT by default
            self.UEFI = True
            self.zfs_options["scheme"] = "GPT"
        else:
            # No UEFI, use MBR by default
            self.UEFI = False
            self.zfs_options["scheme"] = "MBR"

    def on_use_device_toggled(self, widget, path):
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
        self.header.set_subtitle(_("ZFS Setup"))

        # Encrypt disk checkbox
        btn = self.ui.get_object("encrypt_disk_btn")
        btn.set_active(self.zfs_options["encrypt_disk"])

        # Disable/Enable Encrypt disk options entries
        entries = [
            'password_entry', 'password_check_entry',
            'password_lbl', 'password_check_lbl']
        for name in entries:
            entry = self.ui.get_object(name)
            entry.set_sensitive(self.zfs_options["encrypt_disk"])

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
            if num_drives > 0:
                is_ok = True
            else:
                is_ok = False
                msg = _("You must select at least one drive")

        elif pool_type == "Stripe" or pool_type == "Mirror":
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

        if not is_ok and show_warning:
            show.message(self.get_toplevel(), msg)

        return is_ok

    def show_pool_type_help(self, pool_type):
        pool_types = list(self.pool_types.values())
        msg = ""
        if (pool_type in pool_types and
                pool_type not in self.pool_types_help_shown):
            if pool_type == "Stripe":
                msg = _("When created together, with equal capacity, ZFS "
                        "space-balancing makes a span act like a RAID0 stripe. "
                        "The space is added together. Provided all the devices "
                        "are of the same size, the stripe behavior will "
                        "continue regardless of fullness level. If "
                        "devices/vdevs are not equally sized, then they will "
                        "fill mostly equally until one device/vdev is full.")
            elif pool_type == "Mirror":
                msg = _("A mirror consists of two or more devices, all data "
                        "will be written to all member devices.")
            elif pool_type.startswith("RAID-Z"):
                msg = _("ZFS implements RAID-Z, a variation on standard "
                        "RAID-5. ZFS supports three levels of RAID-Z which "
                        "provide varying levels of redundancy in exchange for "
                        "decreasing levels of usable storage. The types are "
                        "named RAID-Z1 through RAID-Z3 based on the number of "
                        "parity devices in the array and the number of disks "
                        "which can fail while the pool remains operational.")

            self.pool_types_help_shown.append(pool_type)
            if len(msg) > 0:
                show.message(self.get_toplevel(), msg)

    def on_force_4k_help_btn_clicked(self, widget):
        msg = _("Advanced Format (AF) is a new disk format which natively "
                "uses a 4,096 byte instead of 512 byte sector size. To "
                "maintain compatibility with legacy systems AF disks emulate "
                "a sector size of 512 bytes. By default, ZFS will "
                "automatically detect the sector size of the drive. This "
                "combination will result in poorly aligned disk access which "
                "will greatly degrade the pool performance. If that might be "
                "your case, you can force ZFS to use a sector size of 4,096 "
                "bytes by selecting this option.")
        show.message(self.get_toplevel(), msg)

    def on_encrypt_swap_btn_toggled(self, widget):
        self.zfs_options["encrypt_swap"] = not self.zfs_options["encrypt_swap"]

    def on_encrypt_disk_btn_toggled(self, widget):
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
        obj = self.ui.get_object('pool_name_entry')
        status = not obj.get_sensitive()
        obj.set_sensitive(status)
        self.zfs_options["use_pool_name"] = status

    def on_force_4k_btn_toggled(self, widget):
        self.zfs_options["force_4k"] = not self.zfs_options["force_4k"]

    def on_partition_scheme_combo_changed(self, widget):
        tree_iter = widget.get_active_iter()
        if tree_iter is not None:
            model = widget.get_model()
            self.zfs_options["scheme"] = model[tree_iter][0]

    def on_pool_type_combo_changed(self, widget):
        tree_iter = widget.get_active_iter()
        if tree_iter is not None:
            model = widget.get_model()
            self.zfs_options["pool_type"] = model[tree_iter][0]
            self.show_pool_type_help(model[tree_iter][0])
            self.forward_button.set_sensitive(self.check_pool_type())

    def prepare(self, direction):
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
        txt = self.ui.get_object("pool_name_entry").get_text()
        if not txt:
            txt = "antergos"
        self.zfs_options["pool_name"] = txt

        # Get password
        txt = self.ui.get_object("password_lbl").get_text()
        self.zfs_options["encrypt_password"] = txt

        # self.set_bootloader()

        return True

    # -------------------------------------------------------------------------

    def init_device(self, device_path, scheme="GPT"):
        if scheme == "GPT":
            # Clean partition table to avoid issues!
            wrapper.sgdisk("zap-all", device_path)

            # Clear all magic strings/signatures -
            # mdadm, lvm, partition tables etc.
            wrapper.dd("/dev/zero", device_path, bs=512, count=2048)
            wrapper.wipefs(device_path)

            # Create fresh GPT
            wrapper.sgdisk("clear", device_path)

            # Inform the kernel of the partition change.
            # Needed if the hard disk had a MBR partition table.
            self.check_call(["partprobe", device_path])
        else:
            # DOS MBR partition table
            # Start at sector 1 for 4k drive compatibility and correct
            # alignment. Clean partitiontable to avoid issues!
            wrapper.dd("/dev/zero", device_path, bs=512, count=2048)
            wrapper.wipefs(device_path)

            # Create DOS MBR
            wrapper.parted_mktable(device_path, "msdos")

        self.check_call(["sync"])

    def append_change(self, action_type, device, info=""):
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
        """ Grab all changes for confirmation """

        self.change_list = []
        device_paths = self.zfs_options["device_paths"]

        device_path = device_paths[0]

        pool_name = self.zfs_options["pool_name"]

        if self.zfs_options["scheme"] == "GPT":
            self.append_change("delete", device_path)
            if not self.UEFI:
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
            self.append_change("add", device_path,  msg)

        return self.change_list

    def run_format(self):
        # https://wiki.archlinux.org/index.php/Installing_Arch_Linux_on_ZFS
        # https://wiki.archlinux.org/index.php/ZFS#GRUB-compatible_pool_creation

        device_paths = self.zfs_options["device_paths"]
        logging.debug("Configuring ZFS in %s", ",".join(device_paths))

        device_path = device_paths[0]
        solaris_partition_number = -1

        if self.zfs_options["scheme"] == "GPT":
            self.init_device(device_path, "GPT")

            part_num = 1

            if not self.UEFI:
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
                self.fs_devices[devices['boot']] = "ext4"
                part_num += 1
            else:
                # UEFI
                if self.bootloader == "grub":
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
                    self.fs_devices[devices['boot']] = "vfat"
                    self.mount_devices['/boot'] = self.devices['boot']
                    part_num += 1

            wrapper.sgdisk_new(device_path, part_num, "ANTERGOS_ZFS", 0, "BF00")
            solaris_partition_number = part_num

            # Now init all other devices that will form part of the pool
            for device_path in device_paths[1:]:
                self.init_device(device_path, "GPT")
                wrapper.sgdisk_new(device_path, 1, "ANTERGOS_ZFS", 0, "BF00")
        else:
            # MBR
            self.init_device(device_path, "MBR")

            # Create boot partition (all sizes are in MiB)
            # if start is -1 wrapper.parted_mkpart assumes that our partition
            # starts at 1 (first partition in disk)
            start = -1
            end = 512
            part_num = "1"
            wrapper.parted_mkpart(device_path, "primary", start, end)

            # Set boot partition as bootable
            wrapper.parted_set(device_path, part_num, "boot", "on")

            # Format the boot partition as well as any other system partitions.
            # Do not do anything to the Solaris partition nor to the BIOS boot
            # partition. ZFS will manage the first, and the bootloader the
            # second.

            fs.create_fs(device_path + part_num, "ext4", "ANTERGOS_BOOT")
            self.devices['boot'] = "{0}{1}".format(device_path, part_num)
            self.fs_devices[self.devices['boot']] = "ext4"
            self.mount_devices['/boot'] = self.devices['boot']

            # The rest will be solaris type
            start = end
            end = "-1s"
            wrapper.parted_mkpart(device_path, "primary", start, end)
            solaris_partition_number = 2

            # Now init all other devices that will form part of the pool
            for device_path in device_paths[1:]:
                self.init_device(device_path, "MBR")
                wrapper.parted_mkpart(device_path, "primary", -1, "-1s")

        # Wait until /dev initialized correct devices
        self.check_call(["udevadm", "settle"])
        self.check_call(["sync"])

        self.create_zfs_pool(solaris_partition_number)

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

    def check_call(self, cmd):
        try:
            # Convert list and get sure all items are converted to str
            cmd_line = ' '.join(str(x) for x in cmd)
            logging.debug(cmd_line)
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as process_error:
            txt = "Command {0} has failed".format(process_error.cmd)
            logging.error(txt)
            txt = _("Command {0} has failed").format(process_error.cmd)
            raise InstallError(txt)

    def zfs_export_pool(self, pool):
        """ Makes the kernel to flush all pending data to disk, writes data to
            the disk acknowledging that the export was done, and removes all
            knowledge that the storage pool existed in the system """
        try:
            cmd = ["zpool", "export", pool]
            cmd_line = "zpool export {0}".format(pool)
            logging.debug(cmd_line)
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as process_error:
            try:
                cmd = ["zpool", "export", "-f", pool]
                cmd_line = "zpool export -f {0}".format(pool)
                logging.debug(cmd_line)
                subprocess.check_call(cmd)
            except subprocess.CalledProcessError as process_error:
                txt = "Command {0} has failed".format(process_error.cmd)
                logging.error(txt)
                txt = _("Command {0} has failed").format(process_error.cmd)
                raise InstallError(txt)

    def get_home_size(self, pool_name):
        """ Get recommended /home size """
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

    def get_pool_size(self, pool_name):
        """ Gets zfs pool size """
        pool_size = 0
        try:
            cmd_line = "zpool list -H -o size {0}".format(pool_name)
            logging.debug(cmd_line)
            cmd = cmd_line.split()
            pool_size = subprocess.check_output(cmd).decode()
        except subprocess.CalledProcessError as process_error:
            logging.warning("Can't get zfs %s pool size", pool_name)
            pool_size = 0
        finally:
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
        if pool_size and pool_size != 0:
            # pool size will be in M, G, T or P
            pool_size.replace(",", ".", 1)
            try:
                if 'M' in pool_size:
                    pool_size = int(pool_size[:-2]) // 1024
                elif 'G' in pool_size:
                    pool_size = int(pool_size[:-2])
                elif 'T' in pool_size:
                    pool_size = int(pool_size[:-2]) * 1024
                elif 'P' in pool_size:
                    pool_size = int(pool_size[:-2]) * 1024 * 1024
            except ValueError as value_error:
                return swap_size

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
        self.check_call(cmd)

    def create_zfs_pool(self, solaris_partition_number):
        """ Create the root zpool """

        device_paths = self.zfs_options["device_paths"]
        if not device_paths:
            txt = _("No devices were selected for the ZFS pool")
            raise InstallError(txt)

        # Make sure the ZFS modules are loaded
        self.check_call(["modprobe", "zfs"])

        first_disk = True
        devices_ids = []

        for device_path in device_paths:
            device = device_path.split("/")[-1]
            device_id = self.ids.get(device, None)

            if device_id is None:
                txt = "Error while creating ZFS pool: Cannot find device {0}"
                txt = txt.format(device)
                raise InstallError(txt)

            if first_disk:
                # In system disk (first one) use just one partition
                id_path = "/dev/disk/by-id/{0}-part{1}".format(
                    device_id,
                    solaris_partition_number)
                first_disk = False
            else:
                # Use full device for the other disks
                id_path = device_id
                cmd = ["zpool", "labelclear", "-f", id_path]
                self.check_call(cmd)

            devices_ids.append(id_path)

        line = " ".join(devices_ids)
        logging.debug("Cnchi will create a ZFS pool using %s devices", line)

        try:
            os.mkdir(DEST_DIR, mode=0o755)
        except OSError:
            pass

        if self.zfs_options['use_pool_name']:
            pool_name = self.zfs_options["pool_name"]
        else:
            pool_name = "antergos"

        pool_type = self.zfs_options["pool_type"]

        # Command: zpool create zroot /dev/disk/by-id/id-to-partition
        # This will be our / (root) system
        logging.debug("Creating zfs pool %s", pool_name)
        cmd = ["zpool", "create", "-f"]
        if self.zfs_options["force_4k"]:
            cmd.extend(["-o", "ashift=12"])
        cmd.extend(["-m", DEST_DIR, pool_name])
        if pool_type != "None" and pool_type in self.pool_types.values():
            cmd.extend(pool_type)
        cmd.extend(devices_ids)
        self.check_call(cmd)

        # Set the mount point of the root filesystem
        self.check_call(["zfs", "set", "mountpoint=legacy", pool_name])

        if self.settings.get('use_home'):
            home_size = self.get_home_size(pool_name)
            logging.debug("Creating zfs vol 'home' (%dGB)", home_size)
            self.create_zfs_vol(pool_name, "home", home_size)
            cmd = [
                "zfs", "set",
                "mountpoint=/home",
                "{0}/home".format(pool_name)]
            self.check_call(cmd)

        # Create swap zvol
        swap_size = self.get_swap_size(pool_name)
        logging.debug("Creating zfs vol 'swap' (%dGB)", swap_size)
        self.create_zfs_vol(pool_name, "swap", swap_size)

        # Set the bootfs property on the descendant root filesystem so the
        # boot loader knows where to find the operating system.
        cmd = ["zpool", "set", "bootfs={0}".format(pool_name), pool_name]
        self.check_call(cmd)

        # Export the pool
        self.zfs_export_pool(pool_name)

        # Finally, re-import the pool
        cmd = [
            "zpool", "import",
            "-d", "/dev/disk/by-id",
            "-R", DEST_DIR,
            pool_name]
        self.check_call(cmd)

        # Set the mount point of the root filesystem
        cmd = ["zfs", "set", "mountpoint=/", pool_name]
        self.check_call(cmd)

        # Create zpool.cache file
        cmd = ["zpool", "set", "cachefile=/etc/zfs/zpool.cache", pool_name]
        self.check_call(cmd)

        # Copy created cache file to destination
        try:
            dst_dir = os.path.join(DEST_DIR, "etc/zfs")
            os.makedirs(dst_dir, mode=0o755, exist_ok=True)

            src = "/etc/zfs/zpool.cache"
            dst = os.path.join(dst_dir, "zpool.cache")
            shutil.copyfile(src, dst)
        except OSError as copy_error:
            logging.warning(copy_error)

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
