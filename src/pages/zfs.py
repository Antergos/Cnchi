# -*- coding: utf-8; Mode: Python; indent-tabs-mode: nil; tab-width: 4 -*-
#
#  zfs.py
#
# Copyright © 2013-2018 Antergos
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

import os
import logging
import math

from pages.gtkbasebox import GtkBaseBox

import misc.extra as misc
from misc.extra import random_generator

import show_message as show
from installation import action
from installation import install
from installation import wrapper

import parted3.fs_module as fs

from widgets.zfs_treeview import ZFSTreeview
import zfs_manager as zfs

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message


DEST_DIR = "/install"


def is_int(num):
    """ Checks if num is an integer """
    return isinstance(num, int)


class InstallationZFS(GtkBaseBox):
    """ ZFS installation screen class """

    POOL_TYPES = {0: "None", 1: "Stripe", 2: "Mirror", 3: "RAID-Z", 4: "RAID-Z2", 5: "RAID-Z3"}

    SCHEMES = {0: "GPT", 1: "MBR"}

    def __init__(
            self, params, prev_page="installation_ask", next_page="summary"):
        super().__init__(self, params, "zfs", prev_page, next_page)

        self.page = self.ui.get_object('zfs')

        self.disks = None
        self.diskdic = {}

        self.change_list = []

        self.zfs_treeview = ZFSTreeview(self.ui)
        self.zfs_treeview.connect_use_device(self.use_device_toggled)

        self.installation = None

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

        # Set grub2 bootloader as default
        self.bootloader = "grub2"
        self.bootloader_entry = self.ui.get_object('bootloader_entry')

    def use_device_toggled(self, _widget, _path):
        """ Use device clicked """
        self.forward_button.set_sensitive(self.check_pool_type())

    def fill_bootloader_entry(self):
        """ Put the bootloaders for the user to choose """
        self.bootloader_entry.remove_all()

        if self.uefi:
            self.bootloader_entry.append_text("Grub2")

            # TODO: These two need more testing
            # self.bootloader_entry.append_text("Systemd-boot")
            # self.bootloader_entry.append_text("rEFInd")

            if not misc.select_combobox_value(self.bootloader_entry, self.bootloader):
                # Automatically select first entry
                self.bootloader_entry.set_active(0)
            self.bootloader_entry.show()
        else:
            self.bootloader_entry.hide()
            widget = self.ui.get_object("bootloader_label")
            if widget:
                widget.hide()

    def on_bootloader_entry_changed(self, _widget):
        """ Get new selected bootloader """
        line = self.bootloader_entry.get_active_text()
        if line is not None:
            self.bootloader = line.lower()

    def fill_text_combobox(self, object_name, text, zfs_option):
        """ Fill combobox """
        combo = self.ui.get_object(object_name)
        combo.remove_all()
        active_index = 0
        for index in text:
            combo.append_text(text[index])
            if self.zfs_options[zfs_option] == text[index]:
                active_index = index
        combo.set_active(active_index)

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

        # Fill pool types and partition scheme combobox
        self.fill_text_combobox('pool_type_combo', InstallationZFS.POOL_TYPES, 'pool_type')
        self.fill_text_combobox('partition_scheme_combo', InstallationZFS.SCHEMES, 'scheme')

        # Set text labels
        labels = {
            'pool_type_label': _("Pool type"),
            'partition_scheme_label': _("Partition scheme"),
            'password_check_lbl': _("Validate password"),
            'password_lbl': _("Password"),
            'swap_size_lbl': _("Swap size (MB)")}
        for key, value in labels.items():
            lbl = self.ui.get_object(key)
            lbl.set_markup(value)

        # Set button labels
        labels = {
            'encrypt_swap_btn': _("Encrypt swap"),
            'encrypt_disk_btn': _("Encrypt disk"),
            'pool_name_btn': _("Pool name"),
            'force_4k_btn': _("Force ZFS 4k block size")}
        for key, value in labels.items():
            btn = self.ui.get_object(key)
            btn.set_label(value)

        # Set swap Size
        swap_size = str(self.zfs_options["swap_size"])
        entry = self.ui.get_object("swap_size_entry")
        entry.set_text(swap_size)

    def check_pool_type(self, show_warning=False):
        """ Check that the user has selected the right number
        of devices for the selected pool type """

        num_drives = self.zfs_treeview.get_num_drives()

        pool_type = self.zfs_options["pool_type"]

        msg = ""

        if pool_type == "None":
            is_ok = num_drives == 1
            if not is_ok:
                msg = _("You must select one drive")

        elif pool_type in ["Stripe", "Mirror"]:
            is_ok = num_drives > 1
            if not is_ok:
                msg = _("For the {0} pool_type, you must select at least two "
                        "drives").format(pool_type)

        elif "RAID" in pool_type:
            pool_types = {
                'RAID-Z': {'min_drives': 3, 'min_parity_drives': 1},
                'RAID-Z2': {'min_drives': 4, 'min_parity_drives': 2},
                'RAID-Z3': {'min_drives': 5, 'min_parity_drives': 3}
            }

            min_drives = pool_types[pool_type]['min_drives']
            min_parity_drives = pool_types[pool_type]['min_parity_drives']

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
                    is_ok = False
                else:
                    is_ok = True
        else:
            # If we get here, something is wrong.
            msg = _('An unknown error occurred while processing chosen ZFS options.')
            is_ok = False

        if not is_ok and show_warning:
            show.message(self.get_main_window(), msg)

        return is_ok

    def on_pool_type_help_btn_clicked(self, _widget):
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

    def on_force_4k_help_btn_clicked(self, _widget):
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

    def on_encrypt_swap_btn_toggled(self, _widget):
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

    def on_pool_name_btn_toggled(self, _widget):
        """ Use a specific pool name """
        obj = self.ui.get_object('pool_name_entry')
        status = not obj.get_sensitive()
        obj.set_sensitive(status)
        self.zfs_options["use_pool_name"] = status

    def on_force_4k_btn_toggled(self, _widget):
        """ Force 4k sector size """
        self.zfs_options["force_4k"] = not self.zfs_options["force_4k"]

    def partition_scheme_changed(self, widget):
        """ User changes scheme to MBR or GPT """
        tree_iter = widget.get_active_iter()
        if tree_iter:
            model = widget.get_model()
            self.zfs_options["scheme"] = model[tree_iter][0]

    def pool_type_combo_changed(self, widget):
        """ Choose zfs pool type """
        tree_iter = widget.get_active_iter()
        if tree_iter:
            model = widget.get_model()
            self.zfs_options["pool_type"] = model[tree_iter][0]
            self.forward_button.set_sensitive(self.check_pool_type())

    def prepare(self, direction):
        """ Prepare screen """
        self.zfs_options['encrypt_disk'] = self.settings.get('use_luks')

        self.translate_ui()
        self.zfs_treeview.fill_device_list()
        self.show_all()
        self.fill_bootloader_entry()
        self.forward_button.set_sensitive(self.check_pool_type())

    def store_values(self):
        """ Store all vars """

        # Get device paths
        self.zfs_options["device_paths"] = self.zfs_treeview.get_device_paths()

        # Get swap size
        txt = self.ui.get_object("swap_size_entry").get_text()
        try:
            self.zfs_options["swap_size"] = int(txt)
        except ValueError as _verror:
            # Error reading value, set 8GB as default
            self.zfs_options["swap_size"] = 8192

        # Get pool name
        txt = self.ui.get_object("pool_name_entry").get_text()
        if txt:
            self.zfs_options["pool_name"] = txt

        # Bootloader needs to know that we're using zfs and zpool's name
        self.settings.set("zfs", True)
        self.settings.set("zfs_pool_name", self.zfs_options["pool_name"])

        # Get password
        txt = self.ui.get_object("password_lbl").get_text()
        self.zfs_options["encrypt_password"] = txt

        return True

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
                self.append_change("create", device_path,
                                   "Antergos Boot (512MB)")
            else:
                # UEFI
                if self.bootloader == "grub2":
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

    # ZFS Creation starts here -------------------------------------------------

    # BIOS/MBR (Grub)
    # 1 Solaris (bf00)

    # BIOS/GPT (Grub)
    # 1 2M BIOS boot partition (ef02)
    # 2 Solaris (bf00)

    # UEFI/GPT (rEFInd / systemd-boot)
    # 1 512M EFI boot partition (ef00) (/boot) (vfat)
    # 2 Solaris (bf00)

    # UEFI/GPT (Grub)
    # 1 512M EFI boot partition (ef00) (/boot/efi) (vfat)
    # 2 512M boot partition (/boot) (ext4)
    # 3 Solaris (bf00)

    def gpt_boot_partition(self, device_path, part_num, ptype='8300', as_efi=False):
        """ Create and format BOOT or EFI partitions (512MB) in /boot or in /boot/efi """
        if ptype == 'EF00':
            # EFI (/boot or /boot/efi) always uses vfat
            filesystem = 'vfat'
        else:
            # "Normal" /boot uses ext4
            # (in this case, an EFI partition will be mounted in /boot/efi later)
            filesystem = 'ext4'

        if as_efi:
            # An EFI partition in /boot/efi (a ext4 /boot partition will be created later)
            label = 'EFI'
            tag = 'efi'
            mpoint = '/boot/efi'
            ptype = 'EF00'
        else:
            # Boot partition (either ext4 or vfat, depending on partition type above)
            label = 'ANTERGOS_BOOT'
            tag = 'boot'
            mpoint = '/boot'

        wrapper.sgdisk_new(device_path, part_num, label, 512, ptype)
        self.devices[tag] = zfs.get_partition_path(device_path, part_num)
        self.fs_devices[self.devices[tag]] = filesystem
        self.mount_devices[mpoint] = self.devices[tag]
        fs.create_fs(self.devices[tag], filesystem, label)

    def run_format_bios_gpt(self, device_path):
        """ Create partitions and filesystems in a BIOS system using a GPT partition table"""
        # Create BIOS Boot Partition
        # GPT GUID: 21686148-6449-6E6F-744E-656564454649
        # This partition is not required if the system is UEFI based,
        # as there is no such embedding of the second-stage code in that case
        part_num = 1
        wrapper.sgdisk_new(device_path, part_num, 'BIOS_BOOT', 2, 'EF02')
        part_num += 1
        # Create Boot Partition /boot (ext4)
        self.gpt_boot_partition(device_path, part_num, ptype='8300', as_efi=False)
        part_num += 1
        return part_num

    def run_format_uefi_gpt(self, device_path):
        """ Create partitions and filesystems in an UEFI system using a GPT partition table"""
        part_num = 1
        # Partition type (EFI is EF00)
        ptype = 'EF00'
        if self.bootloader == 'grub2':
            # First, create an EFI partition /boot/efi (vfat)
            self.gpt_boot_partition(device_path, part_num, ptype='EF00', as_efi=True)
            part_num += 1
            ptype = '8300'

        # Create boot partition (ext4) /boot
        self.gpt_boot_partition(device_path, part_num, ptype)
        part_num += 1

        return part_num

    def run_format_mbr(self, device_path):
        """ Create partitions and filesystems using a MBR partition table"""
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
            fs_boot = 'vfat'
        else:
            fs_boot = 'ext4'

        # Get partition full path
        self.devices['boot'] = zfs.get_partition_path(device_path, 1)
        self.fs_devices[self.devices['boot']] = fs_boot
        self.mount_devices['/boot'] = self.devices['boot']
        fs.create_fs(self.devices['boot'], fs_boot, "ANTERGOS_BOOT")

        # The rest of the disk will be of solaris type
        start = end
        wrapper.parted_mkpart(device_path, "primary", start, "-1s")
        solaris_partition_number = 2

        return solaris_partition_number

    def run_format(self):
        """ Create partitions and file systems """
        # https://wiki.archlinux.org/index.php/Installing_Arch_Linux_on_ZFS
        # https://wiki.archlinux.org/index.php/ZFS#GRUB-compatible_pool_creation

        device_paths = self.zfs_options['device_paths']
        logging.debug("Configuring ZFS in %s", ",".join(device_paths))

        # Read all preexisting zfs pools. If there's an antergos one, delete it.
        zfs.destroy_pools()

        # Wipe all disks that will be part of the installation.
        # This cannot be undone!
        zfs.init_device(device_paths[0], self.zfs_options['scheme'])
        for device_path in device_paths[1:]:
            zfs.init_device(device_path, 'GPT')

        device_path = device_paths[0]
        solaris_partition_number = -1

        self.settings.set('bootloader_device', device_path)

        if self.zfs_options['scheme'] == 'GPT':
            if not self.uefi:
                part_num = self.run_format_bios_gpt(device_path)
            else:
                part_num = self.run_format_uefi_gpt(device_path)

            # The rest of the disk will be of solaris type
            wrapper.sgdisk_new(device_path, part_num, 'ANTERGOS_ZFS', 0, 'BF00')
            solaris_partition_number = part_num
        else:
            # MBR
            solaris_partition_number = self.run_format_mbr(device_path)
            part_num = 2

        # Get partition full path
        self.devices['root'] = zfs.get_partition_path(device_path, part_num)
        # self.fs_devices[self.devices['root']] = "zfs"
        self.mount_devices['/'] = self.devices['root']

        zfs.settle()

        use_home = self.settings.get('use_home')
        pool_id = zfs.setup(
            solaris_partition_number, self.zfs_options, use_home)

        # Save pool id
        self.settings.set("zfs_pool_id", pool_id)

        # Store swap info
        pool_name = self.zfs_options['pool_name']
        swap_path = "/dev/zvol/{0}/swap".format(pool_name)
        self.devices['swap'] = swap_path
        self.fs_devices[swap_path] = 'swap'
        self.mount_devices['swap'] = swap_path

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
