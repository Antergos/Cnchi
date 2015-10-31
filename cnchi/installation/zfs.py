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
from misc.misc import InstallError
import show_message as show
from installation import wrapper
from installation import action

COL_USE_ACTIVE = 0
COL_USE_VISIBLE = 1
COL_USE_SENSITIVE = 2
COL_DISK = 3
COL_SIZE = 4
COL_DEVICE_NAME = 5
COL_DISK_ID = 6


class InstallationZFS(GtkBaseBox):
    def __init__(self, params, prev_page="installation_ask", next_page="summary"):
        super().__init__(self, params, "zfs", prev_page, next_page)

        self.page = self.ui.get_object('zfs')

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
            "pool_name": "",
            "encrypt_swap": False,
            "encrypt_disk": False,
            "encrypt_password": "",
            "scheme": "GPT",
            "pool_type": "None",
            "swap_size": 8192,
            "pool_name": "",
            "use_pool_name": False,
            "device_paths": []
        }

        if os.path.exists("/sys/firmware/efi"):
            # UEFI, use GPT by default
            self.UEFI = True
            self.zfs_options["scheme"] = "GPT"
        else:
            # No UEFI, use MBR by default
            self.UEFI = False
            self.zfs_options["scheme"] = "MBR"


    def on_use_device_toggled(self, widget, path):
        self.device_list_store[path][COL_USE_ACTIVE] = not self.device_list_store[path][COL_USE_ACTIVE]

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
        col = Gtk.TreeViewColumn(_("Size (GB)"), render_text_right, text=COL_SIZE)
        self.device_list.append_column(col)

        col = Gtk.TreeViewColumn(_("Device"), render_text, text=COL_DEVICE_NAME)
        self.device_list.append_column(col)

        col = Gtk.TreeViewColumn(_("Disk ID"), render_text, text=COL_DISK_ID)
        self.device_list.append_column(col)

    def fill_device_list(self):
        """ Fill the partition list with all the data. """

        # We will store our data model in 'device_list_store'
        if self.device_list_store is not None:
            self.device_list_store.clear()

        self.device_list_store = Gtk.TreeStore(bool, bool, bool, str, int, str, str)

        with misc.raised_privileges():
            devices = parted.getAllDevices()

        self.get_ids()

        for dev in devices:
            # Skip cdrom, raid, lvm volumes or encryptfs
            if not dev.path.startswith("/dev/sr") and not dev.path.startswith("/dev/mapper"):
                size_in_gigabytes = int((dev.length * dev.sectorSize) / 1000000000)
                # Use check | Disk (sda) | Size(GB) | Name (device name)
                if dev.path.startswith("/dev/"):
                    path = dev.path[len("/dev/"):]
                else:
                    path = dev.path
                disk_id = self.ids.get(path, "")
                row = [False, True, True, path, size_in_gigabytes, dev.model, disk_id]
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
        lbl.set_markup(_("Swap size (MB)"))

        swap_size = str(self.zfs_options["swap_size"])
        entry = self.ui.get_object("swap_size_entry")
        entry.set_text(swap_size)

        btn = self.ui.get_object('encrypt_swap_btn')
        btn.set_label(_("Encrypt swap"))

        btn = self.ui.get_object('encrypt_disk_btn')
        btn.set_label(_("Encrypt disk"))

        btn = self.ui.get_object('pool_name_btn')
        btn.set_label(_("Pool name"))

        btn = self.ui.get_object('force_4k_btn')
        btn.set_label(_("Force ZFS 4k block size"))

    def on_force_4k_help_btn_clicked(self, widget):
        msg = _("Advanced Format (AF) is a new disk format which natively uses "
        "a 4,096 byte instead of 512 byte sector size. To maintain compatibility "
        "with legacy systems AF disks emulate a sector size of 512 bytes.\n\n"
        "By default, ZFS will automatically detect the sector size of the drive. "
        "This combination will result in poorly aligned disk access which will "
        "greatly degrade the pool performance. If that might be your case, you "
        "can force ZFS to use a sector size of 4096 bytes by selecting this option.")
        show.message(self.get_toplevel(), msg)

    def on_encrypt_swap_btn_toggled(self, widget):
        self.zfs_options["encrypt_swap"] = not self.zfs_options["encrypt_swap"]

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
        self.zfs_options["pool_name"] = txt

        # Get password
        txt = self.ui.get_object("password_lbl").get_text()
        self.zfs_options["encrypt_password"] = txt

        # self.set_bootloader()

        return True

    def init_device(self, device_path, scheme="GPT"):
        if scheme == "GPT":
            # Clean partition table to avoid issues!
            wrapper.sgdisk("zap-all", device_path)

            # Clear all magic strings/signatures - mdadm, lvm, partition tables etc.
            wrapper.dd("/dev/zero", device_path, bs=512, count=2048)
            wrapper.wipefs(device_path)

            # Create fresh GPT
            wrapper.sgdisk("clear", device_path)

            # Inform the kernel of the partition change. Needed if the hard disk had a MBR partition table.
            try:
                subprocess.check_call(["partprobe", device_path])
            except subprocess.CalledProcessError as err:
                txt = "Error informing the kernel of the partition change. Command {0} failed: {1}".format(err.cmd, err.output)
                logging.error(txt)
                txt = _("Error informing the kernel of the partition change. Command {0} failed: {1}").format(err.cmd, err.output)
                raise InstallError(txt)
        else:
            # DOS MBR partition table
            # Start at sector 1 for 4k drive compatibility and correct alignment
            # Clean partitiontable to avoid issues!
            wrapper.dd("/dev/zero", device_path, bs=512, count=2048)
            wrapper.wipefs(device_path)

            # Create DOS MBR
            wrapper.parted_mktable(device_path, "msdos")

    def append_change(self, action_type, device, info=""):
        if action_type == "create":
            info = _("Create {0} on device {1}").format(info, device)
            # action_type, path_or_info, relabel=False, fs_format=False, mount_point="", encrypt=False):
            act = action.Action("info", info, True, True, "", self.zfs_options["encrypt_disk"])
        elif action_type == "delete":
            act = action.Action(action_type, device)
        self.change_list.append(act)

    def get_changes(self):
        """ Grab all changes for confirmation """

        self.change_list = []
        device_paths = self.zfs_options["device_paths"]

        device_path = device_paths[0]

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

            self.append_change("create", device_path, "Antergos ZFS")

            for device_path in device_paths[1:]:
                self.append_change("delete", device_path)
                self.append_change("create", device_path, "Antergos ZFS")
        else:
            # MBR
            self.append_change("delete", device_path)

            self.append_change("create", device_path, "Antergos Boot (512MB)")
            self.append_change("create", device_path, "Antergos ZFS")

            # Now init all other devices that will form part of the pool
            for device_path in device_paths[1:]:
                self.append_change("delete", device_path)
                self.append_change("create", device_path, "Antergos ZFS")

        return self.change_list

    def run_format(self):
        # https://wiki.archlinux.org/index.php/Installing_Arch_Linux_on_ZFS
        # https://wiki.archlinux.org/index.php/ZFS#GRUB-compatible_pool_creation

        device_paths = self.zfs_options["device_paths"]
        logging.debug("Configuring ZFS in %s", ",".join(device_paths))

        device_path = device_paths[0]

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
                wrapper.sgdisk_new(device_path, part_num, "ANTERGOS_BOOT", 512, "8300")
                part_num += 1
            else:
                # UEFI
                if self.bootloader == "grub":
                    # Create EFI System Partition (ESP)
                    # GPT GUID: C12A7328-F81F-11D2-BA4B-00A0C93EC93B
                    wrapper.sgdisk_new(device_path, part_num, "UEFI_SYSTEM", 200, "EF00")
                    part_num += 1
                    wrapper.sgdisk_new(device_path, part_num, "ANTERGOS_BOOT", 512, "8300")
                    part_num += 1
                else:
                    # systemd-boot, refind
                    wrapper.sgdisk_new(device_path, part_num, "ANTERGOS_BOOT", 512, "EF00")
                    part_num += 1

            wrapper.sgdisk_new(device_path, part_num, "ANTERGOS_ZFS", 0, "BF00")

            # Now init all other devices that will form part of the pool
            for device_path in device_paths[1:]:
                self.init_device(device_path, "GPT")
                wrapper.sgdisk_new(device_path, 1, "ANTERGOS_ZFS", 0, "BF00")
        else:
            # MBR
            self.init_device(device_path, "MBR")

            # Create boot partition (all sizes are in MiB)
            # if start is -1 wrapper.parted_mkpart assumes that our partition starts at 1 (first partition in disk)
            start = -1
            end = 512
            wrapper.parted_mkpart(device_path, "primary", start, end)

            # Set boot partition as bootable
            wrapper.parted_set(device_path, "1", "boot", "on")

            start = end
            end = "-1s"
            wrapper.parted_mkpart(device_path, "primary", start, end)

            # Now init all other devices that will form part of the pool
            for device_path in device_paths[1:]:
                self.init_device(device_path, "MBR")
                wrapper.parted_mkpart(device_path, "primary", -1, "-1s")

        # Wait until /dev initialized correct devices
        subprocess.check_call(["udevadm", "settle"])

        self.create_zfs_pool()

    def check_call(self, cmd):
        try:
            logging.debug(" ".join(cmd))
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as err:
            txt = "Error creating a new partition on device {0}. Command {1} has failed: {2}".format(device, err.cmd, err.stderr)
            logging.error(txt)
            txt = _("Error creating a new partition on device {0}. Command {1} has failed: {2}").format(device, err.cmd, err.stderr)
            raise InstallError(txt)

    def create_zfs_pool(self):
        # Create the root zpool
        device_paths = self.zfs_options["device_paths"]
        if len(device_paths) <= 0:
            txt = _("No devices were selected for ZFS")
            raise InstallError(txt)

        device_path = device_paths[0]

        # Make sure the ZFS modules are loaded
        self.check_call(["modprobe", "zfs"])

        # Command: zpool create zroot /dev/disk/by-id/id-to-partition
        device_id = self.ids[device_path]
        cmd = ["zpool", "create"]
        if self.zfs_options["force_4k"]:
            cmd.extend(["-o", "ashift=12"])
        cmd.extend(["antergos", device_id])
        self.check_call(cmd)

        # Set the mount point of the root filesystem
        self.check_call(["zfs", "set", "mountpoint=/", "antergos"])

        # Set the bootfs property on the descendant root filesystem so the
        # boot loader knows where to find the operating system.
        self.check_call(["zpool", "set", "bootfs=antergos", "antergos"])

        # Create swap zvol
        cmd = [
            "zfs", "create", "-V", "8G", "-b", os.sysconf("SC_PAGE_SIZE"),
            "-o", "primarycache=metadata", "-o", "com.sun:auto-snapshot=false",
            "antergos/swap"]
        self.check_call(cmd)

        # Export the pool
        self.check_call(["zpool", "export", "antergos"])

        # Finally, re-import the pool
        self.check_call(["zpool", "import", "-d", "/dev/disk/by-id", "-R", "/install", "antergos"])

        # Create zpool.cache file
        self.check_call(["zpool", "set", "cachefile=/etc/zfs/zpool.cache", "antergos"])

    def get_ids(self):
        """ Get disk and partitions IDs """
        path = "/dev/disk/by-id"
        for entry in os.scandir(path):
            if not entry.name.startswith('.') and entry.is_symlink() and entry.name.startswith("ata"):
                dest_path = os.readlink(entry.path)
                device = dest_path.split("/")[-1]
                self.ids[device] = entry.name

    def run_install(self, packages, metalinks):
        """ Start installation process """
        pass

try:
    _("")
except NameError as err:
    def _(message):
        return message

if __name__ == '__main__':
    # When testing, no _() is available

    from test_screen import _, run
    run('zfs')
