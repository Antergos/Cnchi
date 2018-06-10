#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# advanced.py
#
# Copyright © 2013-2018 Antergos
#
# This file is part of Cnchi.
#
# Cnchi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Cnchi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# The following additional terms are in effect as per Section 7 of the license:
#
# The preservation of all legal notices and author attributions in
# the material or in the Appropriate Legal Notices displayed
# by works containing it is required.
#
# You should have received a copy of the GNU General Public License
# along with Cnchi; If not, see <http://www.gnu.org/licenses/>.


""" Installation advanced module. Custom partition screen """


import os
import logging
import re

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import parted

import misc.extra as misc
import misc.validation as validation
from misc.gtkwidgets import StateBox
from misc.run_cmd import call

import parted3.partition_module as pm
import parted3.fs_module as fs
import parted3.lvm as lvm
import parted3.used_space as used_space

from installation import install
from installation import action

import show_message as show

from pages.gtkbasebox import GtkBaseBox

from widgets.partition_treeview import PartitionTreeview

# Dialogs
from dialogs.create_partition import CreatePartitionDialog
from dialogs.edit_partition import EditPartitionDialog
from dialogs.create_table import CreateTableDialog


# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message


class InstallationAdvanced(GtkBaseBox):
    """ Installation advanced class. Custom partitioning. """

    def __init__(self, params, prev_page="installation_ask",
                 next_page="user_info"):
        # Call base class
        super().__init__(self, params, "advanced", prev_page, next_page)

        # Init class vars

        self.blvm = False

        self.installation = None
        self.mount_devices = {}
        self.fs_devices = {}

        self.lv_partitions = []
        self.disks_changed = []

        self.check_ok_once = False

        # Store here all LUKS options for each partition (if any)
        # stores tuple (use_luks, vol_name, password)
        # uses partition uid as index
        self.luks_options = {}

        self.first_time_in_fill_partition_treeview = True

        self.orig_label_dic = {}
        self.orig_part_dic = {}

        # stage_opts holds info about newly created partitions
        # (it's like a todo list)
        # format is tuple (is_new, label, mount_point, fs, format)
        # see its usage in listing, creating, and deleting partitions
        # uses partition uid as index
        self.stage_opts = {}

        # What's this?
        self.used_dic = {}

        # Holds partitions that exist now but are going to be deleted
        self.to_be_deleted = []

        # We will store our devices here
        self.disks = None

        # We will store if our device is SSD or not
        self.ssd = {}

        # Initialize some attributes
        self.install_process = None
        self.format_process = None
        self.diskdic = {}

        # Store here ALL partitions from ALL devices
        self.all_partitions = []

        # Init GUI elements

        # Create and edit partition dialogs
        main_window = self.get_main_window()
        self.create_part_dlg = CreatePartitionDialog(
            self.ui_dir, main_window)
        self.edit_part_dlg = EditPartitionDialog(
            self.ui_dir, main_window)

        self.bootloader = "grub2"
        self.bootloader_device = ""
        self.bootloader_entry = self.ui.get_object('bootloader_entry')
        self.bootloader_device_entry = self.ui.get_object(
            'bootloader_device_entry')
        self.bootloader_devices = {}

        # Initialise our partition list tree view
        #<signal name="row-activated" handler="partition_treeview_row_activated" swapped="no"/>
        self.scrolledwindow = self.ui.get_object(
            'partition_treeview_scrolledwindow')
        self.partition_treeview = PartitionTreeview()
        self.partition_treeview.prepare()
        self.scrolledwindow.add(self.partition_treeview)

        # Connect partition treeview's checkbox cells
        self.partition_treeview.connect_format_cell(self.format_cell_toggled)
        self.partition_treeview.connect_ssd_cell(self.ssd_cell_toggled)

        # Connect changing selection in the partition list treeview
        select = self.partition_treeview.get_selection()
        select.connect("changed", self.partition_treeview_selection_changed)

    def ssd_cell_toggled(self, _widget, path):
        """ User confirms selected disk is a ssd disk (or not) """
        disk_path = self.partition_treeview.store[path][PartitionTreeview.COL_PATH]
        self.ssd[disk_path] = self.partition_treeview.store[path][PartitionTreeview.COL_SSD_ACTIVE]

    def format_cell_toggled(self, _widget, path):
        """ Mark a partition to be formatted """
        partition_path = self.partition_treeview.store[path][PartitionTreeview.COL_PATH]
        uid = self.gen_partition_uid(path=partition_path)
        # As it's not a new partition, we set it to False
        self.stage_opts[uid] = (
            False,
            self.partition_treeview.store[path][PartitionTreeview.COL_LABEL],
            self.partition_treeview.store[path][PartitionTreeview.COL_MOUNT_POINT],
            self.partition_treeview.store[path][PartitionTreeview.COL_FS],
            self.partition_treeview.store[path][PartitionTreeview.COL_FORMAT_ACTIVE])

    def gen_partition_uid(self, partition=None, path=None):
        """ Function to generate uid by partition object or path """
        if path and not partition:
            if "free" in path:
                return None
            # Search for partition with path "path"
            for part in self.all_partitions:
                if "/dev/mapper" not in part:
                    for i in part:
                        if part[i].path == path:
                            partition = part[i]
        try:
            dev_path = partition.disk.device.path
        except Exception as _ex:
            dev_path = path

        if partition:
            ends = partition.geometry.end
            starts = partition.geometry.start
        else:
            ends = 'none'
            starts = 'none'

        uid = dev_path + str(starts) + str(ends)
        return uid

    def check_buttons(self, selection):
        """ Activates/deactivates our buttons depending on which is
            selected in the partition treeview """

        model, tree_iter = selection.get_selected()

        path = None
        if tree_iter:
            path = model[tree_iter][PartitionTreeview.COL_PATH]

        if not path:
            return

        button = {
            'undo': self.ui.get_object('partition_button_undo'),
            'new': self.ui.get_object('partition_button_new'),
            'delete': self.ui.get_object('partition_button_delete'),
            'edit': self.ui.get_object('partition_button_edit'),
            'new_label': self.ui.get_object('partition_button_new_label')}

        for key in button:
            button[key].set_sensitive(False)

        if self.stage_opts:
            button['undo'].set_sensitive(True)

        if path == _("free space"):
            button['new'].set_sensitive(True)
        else:
            disks = pm.get_devices()
            if ((path not in disks and 'dev/mapper' not in path) or
                    ('dev/mapper' in path and '-' in path)):
                # A partition is selected
                diskobj = None
                for i in self.all_partitions:
                    if path in i and '/mapper' not in path and '/' in path:
                        diskobj = i[path].disk.device.path
                if (diskobj and
                        model[tree_iter][PartitionTreeview.COL_FS] == 'extended' and
                        self.diskdic[diskobj]['has_logical']):
                    # It's an extended partition and has logical ones in it,
                    # so it can't be edited or deleted until the logical ones
                    # are deleted first.
                    button['delete'].set_sensitive(False)
                    button['edit'].set_sensitive(False)
                else:
                    if '/mapper' in path:
                        button['delete'].set_sensitive(False)
                    else:
                        button['delete'].set_sensitive(True)

                    button['edit'].set_sensitive(True)
            else:
                # A drive (disk) is selected
                button['new_label'].set_sensitive(True)

    def fill_bootloader_device_entry(self):
        """ Get all devices where we can put our bootloader.
            Avoiding partitions """

        self.bootloader_device_entry.remove_all()
        self.bootloader_devices.clear()

        # Just call get_devices once
        if self.disks is None:
            self.disks = pm.get_devices()

        for path in sorted(self.disks):
            (disk, _result) = self.disks[path]
            if disk:
                dev = disk.device
                # Avoid cdrom and any raid, lvm volumes or encryptfs
                if (not dev.path.startswith("/dev/sr") and
                        not dev.path.startswith("/dev/mapper")):
                    size = dev.length * dev.sectorSize
                    size_gbytes = int(parted.formatBytes(size, 'GB'))
                    line = '{0} [{1} GB] ({2})'.format(
                        dev.model,
                        size_gbytes,
                        dev.path)
                    self.bootloader_device_entry.append_text(line)
                    self.bootloader_devices[line] = dev.path

        if not self.select_bootdevice(self.bootloader_device_entry, self.bootloader_device):
            # Automatically select first entry
            misc.select_first_combobox_item(self.bootloader_device_entry)

    @staticmethod
    def select_bootdevice(combobox, value):
        """ Update chosen boot device option """
        model = combobox.get_model()
        combo_iter = model.get_iter_first()
        index = 0
        found = False
        while combo_iter and not found:
            if value.lower() in model[combo_iter][0].lower():
                combobox.set_active_iter(combo_iter)
                combo_iter = None
                found = True
            else:
                index += 1
                combo_iter = model.iter_next(combo_iter)
        return found

    def fill_bootloader_entry(self):
        """ Put the bootloaders for the user to choose """
        self.bootloader_entry.remove_all()

        if os.path.exists('/sys/firmware/efi'):
            self.bootloader_entry.append_text("Grub2")
            self.bootloader_entry.append_text("Systemd-boot")

            # TODO: rEFInd needs more testing
            # self.bootloader_entry.append_text("rEFInd")

            if not misc.select_combobox_value(self.bootloader_entry, self.bootloader):
                # Automatically select first entry
                self.bootloader_entry.set_active(0)
            self.bootloader_entry.show()
        else:
            self.bootloader_entry.hide()
            widget_ids = ["bootloader_label", "bootloader_device_label"]
            for widget_id in widget_ids:
                widget = self.ui.get_object(widget_id)
                widget.hide()

    def bootloader_device_check_toggled(self, checkbox):
        """ Enable / disable bootloader installation """
        status = checkbox.get_active()

        widget_ids = [
            "bootloader_device_entry", "bootloader_entry",
            "bootloader_label", "bootloader_device_label"]

        for widget_id in widget_ids:
            widget = self.ui.get_object(widget_id)
            widget.set_sensitive(status)

    def bootloader_device_entry_changed(self, _widget):
        """ Get new selected bootloader device """
        line = self.bootloader_device_entry.get_active_text()
        if line:
            self.bootloader_device = self.bootloader_devices[line]

    def bootloader_entry_changed(self, _widget):
        """ Get new selected bootloader """
        line = self.bootloader_entry.get_active_text()
        if line:
            self.bootloader = line.lower()
            self.check_mount_points()

    @staticmethod
    def get_size(length, sector_size):
        """ Helper function to get a disk/partition size in human format """
        size = length * sector_size
        size_txt = "{0}b".format(size)

        if size >= 1000000000000:
            size /= 1000000000000
            size_txt = "{0:.0f}T".format(size)
        elif size >= 1000000000:
            size /= 1000000000
            size_txt = "{0:.0f}G".format(size)
        elif size >= 1000000:
            size /= 1000000
            size_txt = "{0:.0f}M".format(size)
        elif size >= 1000:
            size /= 1000
            size_txt = "{0:.0f}K".format(size)

        return size_txt

    def fill_partition_treeview(self):
        """ Fill the partition list with all the data. """

        self.partition_treeview.create_store()

        # Be sure to call get_devices once
        if self.disks is None:
            self.disks = pm.get_devices()

        self.diskdic = {}
        self.diskdic['mounts'] = []

        self.all_partitions = []
        self.lv_partitions = []

        # Put all volumes (lvm) info in our model
        volume_groups = lvm.get_volume_groups()
        if volume_groups:
            for volume_group in volume_groups:
                is_ssd = False
                logical_volumes = lvm.get_logical_volumes(volume_group)
                if not logical_volumes:
                    continue
                row = [
                    volume_group, "", "", "", False, False, "", "", "", "",
                    0, False, is_ssd, False, False, False]
                lvparent = self.partition_treeview.append(None, row)
                for logical_volume in logical_volumes:
                    fmt_enable = True
                    fmt_active = False
                    label = ""
                    mount_point = ""
                    formatable = True
                    # Fixes issue #278
                    partition_path = "/dev/mapper/{0}-{1}".format(
                        volume_group.replace("-", "--"),
                        logical_volume)
                    self.all_partitions.append(partition_path)
                    self.lv_partitions.append(partition_path)

                    uid = self.gen_partition_uid(path=partition_path)

                    if fs.get_type(partition_path):
                        fs_type = fs.get_type(partition_path)
                    elif used_space.is_btrfs(partition_path):
                        # kludge, btrfs not being detected...
                        fs_type = 'btrfs'
                    else:
                        # Say unknown if we can't detect fs type instead
                        # of assumming btrfs
                        fs_type = 'unknown'

                    label = fs.get_label(partition_path)

                    if uid in self.stage_opts:
                        (is_new,
                         label,
                         mount_point,
                         fs_type,
                         fmt_active) = self.stage_opts[uid]

                    if mount_point:
                        self.diskdic['mounts'].append(mount_point)

                    # Do not show swap version, only the 'swap' word
                    if 'swap' in fs_type:
                        fs_type = 'swap'

                    row = [partition_path, fs_type, mount_point, label,
                           fmt_active, formatable, '', '', partition_path,
                           "", 0, fmt_enable, is_ssd, False, False, False]

                    self.partition_treeview.append(lvparent, row)

                    if self.first_time_in_fill_partition_treeview:
                        self.orig_part_dic[partition_path] = uid
                        self.orig_label_dic[partition_path] = label

        # Fill our model with the rest of devices (non LVM)
        for disk_path in sorted(self.disks):
            if '/dev/mapper/arch_' in disk_path:
                # Already added
                continue

            self.diskdic[disk_path] = {}
            self.diskdic[disk_path]['has_logical'] = False
            self.diskdic[disk_path]['has_extended'] = False

            if disk_path not in self.ssd:
                self.ssd[disk_path] = fs.is_ssd(disk_path)

            is_ssd = self.ssd[disk_path]

            (disk, _result) = self.disks[disk_path]

            if disk is None:
                # Disk without a partition table
                row = [disk_path, "", "", "", False, False, "", "", "", "",
                       0, False, is_ssd, False, False, False]
                self.partition_treeview.append(None, row)
            elif '/dev/mapper/' in disk_path:
                # Already added
                continue
            else:
                dev = disk.device

                # Get device size
                size_txt = self.get_size(dev.length, dev.sectorSize)

                # Append the device info to our model
                row = [dev.path, "", "", "", False, False, size_txt, "", "",
                       "", 0, False, is_ssd, True, True, False]
                disk_parent = self.partition_treeview.append(None, row)

                extended_parent = None

                # Create a list of partitions for this device
                # (/dev/sda for example)
                partitions = pm.get_partitions(disk)
                self.all_partitions.append(partitions)
                partition_list = pm.order_partitions(partitions)

                # Append all partitions to our model
                for partition_path in partition_list:
                    # Get partition size
                    partition = partitions[partition_path]
                    size_txt = self.get_size(
                        partition.geometry.length,
                        dev.sectorSize)
                    fmt_active = False
                    label = ""
                    mount_point = ""
                    used = ""
                    formatable = True

                    path = partition.path

                    # Skip lvm, LUKS, cdrom, ...
                    if '/dev/mapper' in path or 'sr0' in path:
                        continue

                    # Get filesystem
                    if partition.fileSystem and partition.fileSystem.type:
                        fs_type = partition.fileSystem.type

                    # Check if its free space before trying to get
                    # the filesystem with blkid.
                    elif 'free' in partition_path:
                        fs_type = _("none")
                    elif fs.get_type(path):
                        fs_type = fs.get_type(path)
                    else:
                        # Unknown filesystem
                        fs_type = '?'

                    # Nothing should be mounted at this point

                    if partition.type == pm.PARTITION_EXTENDED:
                        formatable = False
                        self.diskdic[disk_path]['has_extended'] = True
                    elif partition.type == pm.PARTITION_LOGICAL:
                        formatable = True
                        self.diskdic[disk_path]['has_logical'] = True

                    if partition.type in (pm.PARTITION_FREESPACE, pm.PARTITION_FREESPACE_EXTENDED):
                        # Show 'free space' instead of /dev/sda-1
                        path = _("free space")
                        formatable = False
                    # else:
                    #    # Get partition flags
                    #    flags = pm.get_flags(partition)

                    uid = self.gen_partition_uid(partition=partition)
                    if uid in self.stage_opts:
                        (is_new, label, mount_point, fs_type,
                         fmt_active) = self.stage_opts[uid]
                        fmt_enable = not is_new
                        if mount_point == "/":
                            fmt_enable = False
                    else:
                        fmt_enable = True
                        if _("free space") not in path:
                            if self.first_time_in_fill_partition_treeview:
                                if mount_point:
                                    used = pm.get_used_space(partition)
                                else:
                                    used = used_space.get_used_space(
                                        partition_path, fs_type)
                                    used = used * partition.geometry.length
                                    used = self.get_size(used, dev.sectorSize)
                                self.used_dic[(
                                    disk_path, partition.geometry.start)] = used
                            else:
                                if (disk_path, partition.geometry.start) in self.used_dic:
                                    used = self.used_dic[(
                                        disk_path, partition.geometry.start)]
                                else:
                                    used = '0b'
                            label = fs.get_label(partition_path)

                    if mount_point:
                        self.diskdic['mounts'].append(mount_point)

                    if partition.type == pm.PARTITION_EXTENDED:
                        # Show 'extended' in file system type column
                        fs_type = "extended"

                    if not fs_type:
                        # fs_type is None when it can't be readed
                        fs_type = _("Unknown")
                    elif 'swap' in fs_type:
                        # Do not show swap version, only the 'swap' word
                        fs_type = 'swap'

                    row = [path, fs_type, mount_point, label, fmt_active,
                           formatable, size_txt, used, partition_path, "",
                           partition.type, fmt_enable, False, False, False, False]

                    if partition.type in (pm.PARTITION_LOGICAL, pm.PARTITION_FREESPACE_EXTENDED):
                        # Our parent (in the treeview) will be the extended
                        # partition we're in, not the disk
                        parent = extended_parent
                    else:
                        # Our parent (in the treeview) will be the disk we're in
                        parent = disk_parent

                    tree_iter = self.partition_treeview.append(parent, row)

                    # If we're an extended partition, all the logical partitions
                    # that follow will be shown as children of this one
                    if partition.type == pm.PARTITION_EXTENDED:
                        extended_parent = tree_iter

                    if self.first_time_in_fill_partition_treeview:
                        uid = self.gen_partition_uid(partition=partition)
                        self.orig_part_dic[partition.path] = uid
                        self.orig_label_dic[partition.path] = label

        self.first_time_in_fill_partition_treeview = False

        # Assign our new model to our treeview
        self.partition_treeview.load_model()
        self.partition_treeview.expand_all()

    # ---------------------------------------------------------------------

    def show_partition_edit_error(self, error):
        """ Show partition edit error to user """
        errors = [
            _("Can't use same mount point twice."),
            _("Root partition must be formatted."),
            _("Root partition cannot be NTFS or FAT32"),
            _("Home partition cannot be NTFS or FAT32"),
            _("As no /boot/efi is defined (yet), /boot needs to be fat32."),
            _("/boot/efi needs to be fat32.")]
        main_window = self.get_main_window()
        show.warning(main_window, errors[error])

    def partition_treeview_edit_activated(self, _button):
        """ The user wants to edit a partition """
        selection = self.partition_treeview.get_selection()
        if not selection:
            return

        model, tree_iter = selection.get_selected()
        if tree_iter is None:
            return

        # Get selected row's data
        row = model[tree_iter]

        # Can't edit a partition that uses a LVM filesystem type
        if "lvm2" in row[PartitionTreeview.COL_FS].lower():
            logging.warning(
                "Can't edit a partition with a LVM filesystem type")
            return

        self.edit_part_dlg.prepare()
        self.edit_part_dlg.show_all()

        # Fill partition dialog with correct data
        partition_info = {
            "filesystem": row[PartitionTreeview.COL_FS],
            "mount_point": row[PartitionTreeview.COL_MOUNT_POINT],
            "label": row[PartitionTreeview.COL_LABEL],
            "format_active": row[PartitionTreeview.COL_FORMAT_ACTIVE],
            "format_sensitive": row[PartitionTreeview.COL_FORMAT_SENSITIVE]
        }

        self.edit_part_dlg.set_partition_info(partition_info)

        # Be sure to just call get_devices once
        if self.disks is None:
            self.disks = pm.get_devices()

        uid = self.gen_partition_uid(
            path=row[PartitionTreeview.COL_PARTITION_PATH])

        # Get LUKS info for the encryption properties dialog
        if uid in self.luks_options:
            options = self.luks_options[uid]
        else:
            options = (False, "", "")
        self.edit_part_dlg.luks_options = options

        # Show edit partition dialog
        response = self.edit_part_dlg.run()
        if response == Gtk.ResponseType.OK:
            new_mount = self.edit_part_dlg.get_mount_point()
            new_fs = self.edit_part_dlg.get_filesystem()
            new_format = self.edit_part_dlg.is_format_active()
            new_label = self.edit_part_dlg.get_label()

            if (new_mount in self.diskdic['mounts'] and
                    new_mount != row[PartitionTreeview.COL_MOUNT_POINT]):
                self.show_partition_edit_error(0)
            elif new_mount == "/" and not new_format:
                self.show_partition_edit_error(1)
            elif new_mount == "/" and new_fs in ["fat32", "ntfs"]:
                self.show_partition_edit_error(2)
            elif new_mount == "/home" and new_fs in ["fat32", "ntfs"]:
                self.show_partition_edit_error(3)
            else:
                if row[PartitionTreeview.COL_MOUNT_POINT]:
                    self.diskdic['mounts'].remove(
                        row[PartitionTreeview.COL_MOUNT_POINT])

                if uid in self.stage_opts:
                    is_new = self.stage_opts[uid][0]
                else:
                    is_new = False

                if new_fs == 'swap':
                    new_mount = 'swap'

                is_uefi = os.path.exists('/sys/firmware/efi')
                if is_uefi and new_fs != "fat32":
                    if new_mount == "/boot":
                        # search for /boot/efi
                        boot_efi_exists = False
                        for tmp_uid in self.stage_opts:
                            opt = self.stage_opts[tmp_uid]
                            if opt and opt[2] == '/boot/efi':
                                boot_efi_exists = True
                        # if no /boot/efi is defined, /boot must be fat32 (force it)
                        if not boot_efi_exists:
                            self.show_partition_edit_error(4)
                            new_fs = "fat32"
                    elif new_mount == "/boot/efi":
                        self.show_partition_edit_error(5)
                        new_fs = "fat32"

                self.stage_opts[uid] = (
                    is_new, new_label, new_mount, new_fs, new_format)
                self.luks_options[uid] = self.edit_part_dlg.luks_options

                if new_mount == "/":
                    # Set if we'll be using LUKS in the root partition
                    self.settings.set('use_luks_in_root',
                                      self.edit_part_dlg.luks_options[0])
                    self.settings.set('luks_root_volume',
                                      self.edit_part_dlg.luks_options[1])

        self.edit_part_dlg.hide()

        # Update the partition list treeview
        self.update_view()

    def update_view(self):
        """ Reloads widgets contents """
        self.fill_partition_treeview()
        self.fill_bootloader_device_entry()
        self.fill_bootloader_entry()
        # Check if correct mount points are already defined, so we can
        # proceed with installation
        self.check_mount_points()

    @staticmethod
    def get_disk_path_from_selection(model, tree_iter):
        """ Helper function that returns the disk path where the selected
            partition is in """
        if tree_iter and model:
            row = model[tree_iter]
            # partition_path = row[COL_PARTITION_PATH]

            # Get partition type from the user selection
            part_type = row[PartitionTreeview.COL_PARTITION_TYPE]

            # Get our parent drive
            parent_iter = model.iter_parent(tree_iter)

            if part_type == pm.PARTITION_LOGICAL:
                # If we are a logical partition, our drive won't be our
                # father but our grandfather (we have to skip the extended
                # partition we're in)
                parent_iter = model.iter_parent(parent_iter)

            return model[parent_iter][PartitionTreeview.COL_PATH]
        else:
            return None

    # ---------------------------------------------------------------------

    def partition_treeview_delete_activated(self, _button):
        """ Delete partition """
        selection = self.partition_treeview.get_selection()
        if not selection:
            return

        model, tree_iter = selection.get_selected()

        if tree_iter is None:
            return

        am_new = False

        # Get row data
        row = model[tree_iter]

        mount_point = row[PartitionTreeview.COL_MOUNT_POINT]
        # size_available = row[COL_SIZE]
        partition_path = row[PartitionTreeview.COL_PARTITION_PATH]

        if mount_point in self.diskdic['mounts']:
            self.diskdic['mounts'].remove(mount_point)

        uid = self.gen_partition_uid(path=partition_path)

        if uid in self.stage_opts:
            am_new = self.stage_opts[uid][0]
            del self.stage_opts[uid]

        if uid in self.luks_options:
            del self.luks_options[uid]

        if not am_new:
            for orig_part in self.orig_part_dic:
                if uid == self.orig_part_dic[orig_part]:
                    self.to_be_deleted.append(orig_part)

        disk_path = self.get_disk_path_from_selection(model, tree_iter)
        self.disks_changed.append(disk_path)

        logging.info(
            "You will delete the partition %s from disk %s",
            partition_path,
            disk_path)

        # Be sure to just call get_devices once
        if self.disks is None:
            self.disks = pm.get_devices()

        (disk, _result) = self.disks[disk_path]

        partitions = pm.get_partitions(disk)

        # used_dic ?
        part = partitions[partition_path]
        if (disk.device.path, part.geometry.start) in self.used_dic:
            del self.used_dic[(disk.device.path, part.geometry.start)]

        # Before delete the partition, check if it's already mounted
        if pm.check_mounted(part):
            # We unmount the partition. Should we ask first?
            logging.info("Unmounting %s...", part.path)
            err_msg = "Cannot unmount {0}".format(part.path)
            cmd = ['umount', part.path]
            call(cmd, msg=err_msg)

        # Is it worth to show some warning message here?
        # No, created delete list (self.to_be_deleted) as part of
        # confirmation screen.

        pm.delete_partition(disk, part)

        # Update the partition list treeview
        self.update_view()

    @staticmethod
    def get_mount_point(partition_path):
        """ Get device mount point """
        fs_name = ''
        fs_type = ''
        writable = ''
        with open('/proc/mounts') as my_file:
            for line in my_file:
                line = line.split()
                if line[0] == partition_path:
                    fs_name = line[1]
                    fs_type = line[2]
                    writable = line[3].split(',')[0]
        return fs_name, fs_type, writable

    @staticmethod
    def get_swap_partition(partition_path):
        """ Get active swap partition """

        partition = ''
        with open('/proc/swaps') as my_file:
            for line in my_file:
                line = line.split()
                if line[0] == partition_path:
                    partition = line[0]
        return partition

    # ---------------------------------------------------------------------

    def partition_treeview_new_activated(self, _button):
        """ Add a new partition """
        selection = self.partition_treeview.get_selection()

        if not selection:
            return

        model, tree_iter = selection.get_selected()
        if tree_iter is None:
            return

        # Assume it will be formatted, unless it's extended (see below)
        formatme = True

        # Get necessary row data
        row = model[tree_iter]

        # Get partition type from the user selection
        part_type = row[PartitionTreeview.COL_PARTITION_TYPE]

        # Check that the user has selected a free space row.
        if part_type not in (pm.PARTITION_FREESPACE, pm.PARTITION_FREESPACE_EXTENDED):
            return

        # size_available = row[COL_SIZE]
        partition_path = row[PartitionTreeview.COL_PARTITION_PATH]

        # Get our parent drive
        parent_iter = model.iter_parent(tree_iter)
        parent_part_type = model[parent_iter][PartitionTreeview.COL_PARTITION_TYPE]

        if parent_part_type == pm.PARTITION_EXTENDED:
            # We're creating a partition inside an already created extended
            # partition (a logical one, though). Our drive won't be our
            # father but our grandfather (we have to skip the extended
            # partition we're in)
            parent_iter = model.iter_parent(parent_iter)
            is_primary_or_extended = False
        else:
            is_primary_or_extended = True

        disk_path = model[parent_iter][PartitionTreeview.COL_PATH]
        self.disks_changed.append(disk_path)

        # Be sure to just call get_devices once
        if self.disks is None:
            self.disks = pm.get_devices()

        (disk, _result) = self.disks[disk_path]

        # Added extended, moving extended details up here
        extended = disk.getExtendedPartition()

        if is_primary_or_extended:
            # Get how many primary partitions are already created on disk
            primary_count = disk.primaryPartitionCount
            if primary_count == disk.maxPrimaryPartitionCount:
                msg = _(
                    "Sorry, you already have {0} primary partitions created.")
                msg = msg.format(primary_count)
                show.warning(self.get_main_window(), msg)
                return
            elif primary_count >= (disk.maxPrimaryPartitionCount - 1) and extended:
                msg = _(
                    "Sorry, you already have {0} primary and 1 extended partitions created.")
                msg = msg.format(primary_count)
                show.warning(self.get_main_window(), msg)
                return

        # ------------------------------------------------------------------

        # Get the objects from the dialog
        params = {}
        params['supports_extended'] = disk.supportsFeature(pm.DISK_EXTENDED)
        params['extended_partition'] = extended
        params['is_primary_or_extended'] = is_primary_or_extended

        # Prepare size spin

        dev = disk.device
        partitions = pm.get_partitions(disk)
        partition = partitions[partition_path]

        # +1 as not to leave unusably small space behind
        max_size_mb = int((partition.geometry.length *
                           dev.sectorSize) / 1000000) + 1

        params['max_size_mb'] = max_size_mb

        self.create_part_dlg.prepare(params)
        self.create_part_dlg.show_all()

        # Finally, show the create partition dialog
        response = self.create_part_dlg.run()
        if response == Gtk.ResponseType.OK:
            mylabel = self.create_part_dlg.get_label()

            mymount = self.create_part_dlg.get_mount_point()
            if mymount in self.diskdic['mounts']:
                show.warning(
                    self.get_main_window(),
                    _("Can't use same mount point twice."))
            else:
                if mymount:
                    self.diskdic['mounts'].append(mymount)

                myfs = self.create_part_dlg.get_filesystem()

                if myfs == 'swap':
                    mymount = 'swap'

                # Get selected size
                size = self.create_part_dlg.get_partition_size()

                beg_var = self.create_part_dlg.get_beginning_point()

                start_sector = partition.geometry.start
                end_sector = partition.geometry.end
                geometry = pm.geom_builder(
                    disk,
                    start_sector,
                    end_sector,
                    size,
                    beg_var)

                # User wants to create an extended, logical or primary partition
                if self.create_part_dlg.wants_primary():
                    logging.debug("Creating a primary partition")
                    pm.create_partition(disk, pm.PARTITION_PRIMARY, geometry)
                elif self.create_part_dlg.wants_extended():
                    # Not mounting extended partitions.
                    if mymount:
                        if mymount in self.diskdic['mounts']:
                            self.diskdic['mounts'].remove(mymount)
                        mymount = ''
                    # And no labeling either
                    mylabel = ''
                    myfs = 'extended'
                    formatme = False
                    logging.debug("Creating an extended partition")
                    pm.create_partition(disk, pm.PARTITION_EXTENDED, geometry)
                elif self.create_part_dlg.wants_logical():
                    logical_count = len(list(disk.getLogicalPartitions()))
                    max_logicals = disk.getMaxLogicalPartitions()
                    if logical_count < max_logicals:
                        logging.debug("Creating a logical partition")
                        pm.create_partition(
                            disk, pm.PARTITION_LOGICAL, geometry)

                if (os.path.exists('/sys/firmware/efi') and
                        (mymount == "/boot" or mymount == "/boot/efi")):
                    logging.info(
                        "/boot or /boot/efi need to be fat32 in UEFI systems. Forcing it.")
                    myfs = "fat32"

                # Store new stage partition info in self.stage_opts
                old_parts = []
                for y in self.all_partitions:
                    for z in y:
                        old_parts.append(z)
                partitions = pm.get_partitions(disk)
                for e in partitions:
                    if e not in old_parts:
                        uid = self.gen_partition_uid(partition=partitions[e])
                        self.stage_opts[uid] = (
                            True, mylabel, mymount, myfs, formatme)
                        self.luks_options[uid] = self.edit_part_dlg.luks_options
                        if mymount == "/":
                            # Set if we'll be using LUKS in the root partition
                            # (for process.py to know)
                            self.settings.set(
                                'use_luks_in_root', self.edit_part_dlg.luks_options[0])
                            self.settings.set(
                                'luks_root_volume', self.edit_part_dlg.luks_options[1])

                # Update partition list treeview
                self.update_view()

        self.create_part_dlg.hide()

    # ---------------------------------------------------------------------

    #def edit_partition_luks_settings_clicked(self, widget):
    #    """ User clicks on edit partition luks settings """
    #    self.partition_luks_settings_clicked(widget)

    # ---------------------------------------------------------------------

    def partition_treeview_undo_activated(self, _button):
        """ Undo all user changes """
        # To undo user changes, we simply reload all devices
        self.disks = pm.get_devices()
        self.disks_changed = []

        # Empty stage partitions' options
        self.stage_opts = {}
        self.luks_options = {}

        # Empty to be deleted partitions list
        self.to_be_deleted = []

        # Refresh our partition treeview
        self.update_view()

    def partition_treeview_selection_changed(self, selection):
        """ Selection in treeview changed, call check_buttons to update them """
        self.check_buttons(selection)
        return False

    @staticmethod
    def partition_treeview_button_press_event(_widget, _event):
        """ Called when clicked on the partition list treeview. """
        # Not doing anything here atm (just return false to not stop the
        # chain of events)
        return False

    @staticmethod
    def partition_treeview_key_press_event(_widget, _event):
        """ Called when a key is pressed when the partition list treeview
            has focus. """
        # Not doing anything here atm (just return false to not stop the
        # chain of events)
        return False

    def partition_treeview_row_activated(self, _path, _column, _user_data):
        """ Simulate a click in new or edit if a partition or free space
            is double clicked """
        button_edit = self.ui.get_object('partition_button_edit')
        button_new = self.ui.get_object('partition_button_new')

        if button_edit.get_sensitive():
            self.partition_treeview_edit_activated(None)
        elif button_new.get_sensitive():
            self.partition_treeview_new_activated(None)

        return False

    @staticmethod
    def partition_treeview_popup_menu(_widget):
        """ Show right click popup menu """
        # Not doing anything here (return false to not stop the chain of events)
        return False

    def translate_ui(self):
        """ As the installer language can change anytime the user changes it,
            we have to 'retranslate' all our widgets calling this function """

        self.header.set_subtitle(_("Advanced Installation Mode"))

        txt = _("Use the device below for boot loader installation:")
        txt = "<span weight='bold' size='small'>{0}</span>".format(txt)
        label = self.ui.get_object('bootloader_device_info_label')
        label.set_markup(txt)

        txt = _("Bootloader:")
        label = self.ui.get_object('bootloader_label')
        label.set_markup(txt)

        txt = _("Device:")
        label = self.ui.get_object('bootloader_device_label')
        label.set_markup(txt)

        txt = _("Mount Checklist:")
        txt = "<span weight='bold'>{0}</span>".format(txt)
        label = self.ui.get_object('mnt_chklist')
        label.set_markup(txt)

        part = self.ui.get_object('root_part')
        txt = _("Root")
        part.props.label = txt + " ( / )"

        part = self.ui.get_object('boot_part')
        txt = _("Boot")
        part.props.label = txt + " ( /boot )"

        part = self.ui.get_object('boot_efi_part')
        txt = _("EFI")
        part.props.label = txt + " ( /boot/efi )"

        part = self.ui.get_object('swap_part')
        txt = _("Swap")
        part.props.label = txt

        # txt = _("TODO: Here goes a warning message")
        # txt = "<span weight='bold'>{0}</span>".format(txt)
        # label = self.ui.get_object('part_advanced_warning_message')
        # label.set_markup(txt)

        # Assign labels and images to buttons
        btns = [
            ("partition_button_undo", "edit-undo-symbolic", _("Undo")),
            ("partition_button_new", "list-add-symbolic", _("New")),
            ("partition_button_delete", "list-remove-symbolic", _("Delete")),
            ("partition_button_edit", "system-run-symbolic", _("Edit...")),
            ("partition_button_new_label", "edit-clear-all-symbolic", _("New partition table"))]

        for grp in btns:
            btn_id, icon, lbl = grp
            image = Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.BUTTON)
            btn = self.ui.get_object(btn_id)
            btn.set_always_show_image(True)
            btn.set_image(image)
            btn.set_label(lbl)

    def prepare(self, direction):
        """ Prepare our dialog to show/hide/activate/deactivate
            what's necessary """

        self.translate_ui()
        self.update_view()
        self.show_all()

        self.fill_bootloader_entry()

        # button = self.ui.get_object('create_partition_encryption_settings')
        # button = self.ui.get_object('edit_partition_encryption_settings')

        # label = self.ui.get_object('part_advanced_recalculating_label')
        # label.hide()
        # spinner = self.ui.get_object('partition_recalculating_spinner')
        # spinner.hide()

        button = self.ui.get_object('partition_button_lvm')
        button.hide()

        widget_ids = [
            'partition_button_new',
            'partition_button_delete',
            'partition_button_edit',
            'partition_button_new_label',
            'partition_button_undo']

        for widget_id in widget_ids:
            button = self.ui.get_object(widget_id)
            button.set_sensitive(False)

    def partition_treeview_new_label_activated(self, _button):
        """ Create a new partition table """
        # TODO: We should check first if there's any mounted partition
        # (including swap)

        selection = self.partition_treeview.get_selection()
        if not selection:
            return

        model, tree_iter = selection.get_selected()
        if tree_iter is None:
            return

        disk_path = model[tree_iter][0]

        # Be sure to just call get_devices once
        if self.disks is None:
            self.disks = pm.get_devices()

        # disk_sel, result = self.disks[disk_path]
        main_window = self.get_main_window()
        dialog = CreateTableDialog(self.ui_dir, main_window)
        dialog.show_all()

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            line = dialog.get_table_type()
            if line:
                # by default, use msdos type
                ptype = 'msdos'

                if 'gpt' in line:
                    ptype = 'gpt'

                msg = "Creating a new %s partition table for disk %s"
                logging.info(msg, ptype, disk_path)

                new_disk = pm.make_new_disk(disk_path, ptype)
                self.disks[disk_path] = (new_disk, pm.OK)

                self.update_view()

                is_uefi = os.path.exists('/sys/firmware/efi')

                if ptype == 'gpt' and not is_uefi:
                    # Show warning (https://github.com/Antergos/Cnchi/issues/63)
                    msg = _(
                        "GRUB requires a BIOS Boot Partition in BIOS systems "
                        "to embed its core.img file due to lack of post-MBR "
                        "embed gap in GPT disks.\n\n"
                        "Cnchi will create this BIOS Boot Partition for you.")
                    show.warning(main_window, msg)
                    self.create_bios_gpt_boot_partition(disk_path)

        dialog.hide()

    def create_bios_gpt_boot_partition(self, disk_path):
        """ Create an unformatted partition with no filesystem and with a
            bios_grub flag on. """

        self.disks_changed.append(disk_path)

        # Be sure to just call get_devices once
        if self.disks is None:
            self.disks = pm.get_devices()

        (disk, _result) = self.disks[disk_path]

        partitions = pm.get_partitions(disk)
        partition_list = pm.order_partitions(partitions)
        mypart = None
        for partition_path in partition_list:
            mypart = partitions[partition_path]

        # Get how many primary partitions are already created on disk
        if mypart is None or disk.primaryPartitionCount > 0:
            # BIOS GPT Boot partition must be the first one on the disk
            txt = "Can't create BIOS GPT Boot partition!"
            logging.error(txt)
            show.error(self.get_main_window(), _(txt))
            return

        # max_size_mb = int((p.geometry.length * dev.sectorSize) / 1000000) + 1

        mylabel = ""
        mymount = ""
        myfmt = "bios-gpt-boot"

        # It won't be formated
        formatme = False

        # Size must be 2MiB
        size = 2

        beg_var = True

        start_sector = mypart.geometry.start
        end_sector = mypart.geometry.end
        geometry = pm.geom_builder(disk, start_sector, end_sector, size, beg_var)

        part = pm.create_partition(disk, pm.PARTITION_PRIMARY, geometry)

        res, myerr = pm.set_flag(pm.PED_PARTITION_BIOS_GRUB, part)

        if res:
            txt = "Couldn't create BIOS GPT Boot partition: %s"
            logging.error(txt, myerr)
            txt = _("Couldn't create BIOS GPT Boot partition: {}").format(myerr)
            show.error(self.get_main_window(), txt)
            return

        # Store stage partition info in self.stage_opts

        old_parts = []
        for mydisk in self.all_partitions:
            for partition in mydisk:
                old_parts.append(partition)

        partitions = pm.get_partitions(disk)
        for part in partitions:
            if part not in old_parts:
                uid = self.gen_partition_uid(partition=partitions[part])
                self.stage_opts[uid] = (
                    True, mylabel, mymount, myfmt, formatme)

        # Update partition list treeview
        self.update_view()

    def partition_treeview_lvm_activated(self, button):
        """ Not done """
        pass

    @staticmethod
    def need_swap():
        """ Returns if having a swap partition is advisable """
        with open("/proc/meminfo") as mem_info:
            mem_info_lines = mem_info.readlines()

        mem_total = ""
        for line in mem_info_lines:
            if "MemTotal" in line:
                mem_total = line
                break

        if mem_total:
            mem = float(mem_total.split()[1]) / 1024.0
            mem = int(mem)
        else:
            return True

        if mem < 4096:
            return True
        return False

    def check_mount_points(self):
        """ Check that all necessary mount points are specified.
            At least root (/) partition must be defined and in UEFI systems
            a fat32 partition mounted in /boot (Systemd-boot) or
            /boot/efi (grub2) must be defined too. """

        check_parts = ["/", "/boot", "/boot/efi", "swap"]

        has_part = {}
        for check_part in check_parts:
            has_part[check_part] = False

        # Are we in a EFI system?
        is_uefi = os.path.exists('/sys/firmware/efi')

        # Be sure to just call get_devices once
        if self.disks is None:
            self.disks = pm.get_devices()

        # Get check part labels
        label_names = {
            "/": "root_part",
            "/boot": "boot_part",
            "/boot/efi": "boot_efi_part",
            "swap": "swap_part"}

        part_label = {}
        for check_part in check_parts:
            part_label[check_part] = self.ui.get_object(
                label_names[check_part])
            part_label[check_part].set_state(False)
            part_label[check_part].hide()

        # Root is always necessary
        part_label["/"].show()

        if is_uefi:
            if self.bootloader == "grub2":
                part_label["/boot/efi"].show()
            elif self.bootloader in ["systemd-boot", "refind"]:
                part_label["/boot"].show()
        else:
            # LVM in non UEFI needs a /boot partition
            if self.lv_partitions:
                part_label["/boot"].show()

        if self.need_swap():
            # Low mem systems need a swap partition
            part_label["swap"].show()

        # Check mount points and filesystems
        for part_path in self.stage_opts:
            (_is_new, _lbl, mnt, fsystem, _fmt) = self.stage_opts[part_path]

            if mnt == "/" and fsystem not in ["fat32", "ntfs", "swap"]:
                has_part["/"] = True
                part_label["/"].show()
                part_label["/"].set_state(True)
                if fsystem == "f2fs":
                    # Special case. We need a /boot partition
                    part_label["/boot"].show()

            if mnt == "swap":
                has_part["swap"] = True
                part_label["swap"].show()
                part_label["swap"].set_state(True)

            if is_uefi:
                # /boot or /boot/efi need to be fat32 in UEFI systems
                if "fat" in fsystem:
                    if mnt == "/boot/efi":
                        if self.bootloader == "grub2":
                            # Grub2 in UEFI
                            has_part["/boot/efi"] = True
                            part_label["/boot/efi"].show()
                            part_label["/boot/efi"].set_state(True)
                    elif mnt == "/boot":
                        if self.bootloader in ["systemd-boot", "refind"]:
                            # systemd-boot (Gummiboot) and rEFInd
                            has_part["/boot"] = True
                            part_label["/boot"].show()
                            part_label["/boot"].set_state(True)
            else:
                if mnt == "/boot" and fsystem not in ["f2fs", "swap"]:
                    # /boot in non UEFI systems
                    has_part["/boot"] = True
                    part_label["/boot"].show()
                    part_label["/boot"].set_state(True)

        # In all cases a root partition must be defined
        check_ok = has_part["/"]

        if is_uefi:
            if self.bootloader == "grub2":
                # Grub2 needs a /boot/efi partition in UEFI
                check_ok = check_ok and has_part["/boot/efi"]
            elif self.bootloader in ["systemd-boot", "refind"]:
                # systemd-boot (Gummiboot) needs a /boot partition
                check_ok = check_ok and has_part["/boot"]
        else:
            if self.lv_partitions:
                # LVM in non UEFI needs a boot partition
                check_ok = check_ok and has_part["/boot"]

        self.forward_button.set_sensitive(check_ok)

        if check_ok:
            self.forward_button.set_sensitive(True)
            self.check_ok_once = True
        elif self.check_ok_once:
            self.forward_button.set_name('fwd_btn')
            self.forward_button.set_label('')
            self.check_ok_once = False

    def unmount_partition(self, partition_path):
        """ Unmount partition """
        # Check if there's some mounted partition
        mounted = False
        mount_point, _fs_type, _writable = self.get_mount_point(partition_path)
        # if "swap" in fs_type:
        swap_partition = self.get_swap_partition(partition_path)
        msg = ""
        if swap_partition == partition_path:
            msg = _(
                "{0} is already mounted as swap, to continue it will be unmounted.")
            msg = msg.format(partition_path)
            mounted = True
        elif mount_point:
            msg = _(
                "{0} is already mounted in {1}, to continue it will be unmounted.")
            msg = msg.format(partition_path, mount_point)
            mounted = True

        if "install" in mount_point:
            # If we're recovering from a failed/stopped
            # install, there'll be some mounted directories.
            # Unmount them without asking.
            cmd = ['umount', '-l', partition_path]
            call(cmd)
            logging.debug("%s unmounted", mount_point)
        elif mounted:
            # unmount it!
            show.warning(self.get_main_window(), msg)
            if swap_partition == partition_path:
                cmd = ["swapoff", partition_path]
                with misc.raised_privileges() as __:
                    call(cmd)
                logging.debug("Swap partition %s unmounted", partition_path)
            else:
                cmd = ['umount', partition_path]
                call(cmd)
                logging.debug("%s unmounted", mount_point)
        else:
            logging.warning(
                "%s shows as mounted (busy) but it has no mount point",
                partition_path)

    def get_changes(self):
        """ Grab all changes for confirmation """
        changes = []

        # First, show partitions that will be deleted
        self.to_be_deleted.sort()
        for partition_path in self.to_be_deleted:
            changes.append(action.Action("delete", partition_path))

        # Store values as
        # (path, create?, label?, format?, mount_point, encrypt?)
        if self.lv_partitions:
            for partition_path in self.lv_partitions:
                # Init vars
                relabel = False
                fmt = False
                createme = False
                encrypt = False
                mnt = ''

                uid = self.gen_partition_uid(path=partition_path)
                if uid in self.stage_opts:
                    is_new, lbl, mnt, fsystem, fmt = self.stage_opts[uid]

                    # Advanced method formats root by default
                    # https://github.com/Antergos/Cnchi/issues/8
                    if mnt == "/":
                        fmt = True
                    if is_new:
                        if lbl != "":
                            relabel = True
                        # Avoid extended and bios-gpt-boot partitions getting
                        # fmt flag true on new creation
                        if fsystem not in ["extended", "bios-gpt-boot"]:
                            fmt = True
                        createme = True
                    else:
                        if partition_path in self.orig_label_dic:
                            if self.orig_label_dic[partition_path] == lbl:
                                relabel = False
                            else:
                                relabel = True
                        createme = False

                    if uid in self.luks_options:
                        (use_luks, _vol_name, _password) = self.luks_options[uid]
                        if use_luks:
                            encrypt = True

                    if createme:
                        action_type = "create"
                    else:
                        action_type = "modify"

                    act = action.Action(action_type, partition_path,
                                        relabel, fmt, mnt, encrypt)
                    changes.append(act)
                    logging.debug(str(act))

        if self.disks:
            for disk_path in self.disks:
                (disk, _result) = self.disks[disk_path]
                partitions = pm.get_partitions(disk)
                for partition_path in partitions:
                    # Init vars
                    relabel = False
                    fmt = False
                    createme = False
                    encrypt = False
                    mnt = ''
                    uid = self.gen_partition_uid(path=partition_path)
                    if uid in self.stage_opts:
                        if disk.device.busy or pm.check_mounted(partitions[partition_path]):
                            self.unmount_partition(partition_path)

                        is_new, lbl, mnt, fsystem, fmt = self.stage_opts[uid]

                        # Advanced method formats root by default
                        # https://github.com/Antergos/Cnchi/issues/8
                        if mnt == "/":
                            fmt = True

                        if is_new:
                            if lbl != "":
                                relabel = True
                            # Avoid extended and bios-gpt-boot partitions
                            # getting fmt flag true on new creation
                            if fsystem not in ["extended", "bios-gpt-boot"]:
                                fmt = True
                            createme = True
                        else:
                            if partition_path in self.orig_label_dic:
                                if self.orig_label_dic[partition_path] == lbl:
                                    relabel = False
                                else:
                                    relabel = True
                            createme = False

                        if uid in self.luks_options:
                            use_luks, _vol_name, _password = self.luks_options[uid]
                            if use_luks:
                                encrypt = True

                        if createme:
                            action_type = "create"
                        else:
                            action_type = "modify"

                        act = action.Action(action_type, partition_path,
                                            relabel, fmt, mnt, encrypt)
                        changes.append(act)
                        logging.debug(str(act))

        return changes

    @staticmethod
    def set_cursor(cursor_type):
        """ Sets mouse cursor in root window """
        gdk_screen = Gdk.Screen.get_default()
        if gdk_screen:
            gdk_window = gdk_screen.get_root_window()
            if gdk_window:
                gdk_window.set_cursor(Gdk.Cursor(cursor_type))

    def store_values(self):
        """ The user clicks 'Install now!' """
        self.set_bootloader()
        return True

    def disable_all_widgets(self):
        """ Disable all page widgets """
        self.enable_all_widgets(status=False)

    def enable_all_widgets(self, status=True):
        """ Enables / disables all page widgets """
        widgets = [
            "partition_treeview_scrolledwindow",
            "partition_treeview", "box2",
            "box3", "box4"]
        for name in widgets:
            widget = self.ui.get_object(name)
            widget.set_sensitive(status)
        while Gtk.events_pending():
            Gtk.main_iteration()

    def set_bootloader(self):
        """ Set bootloader setting from the user selection checkbox """
        checkbox = self.ui.get_object("bootloader_device_check")
        if checkbox.get_active() is False:
            self.settings.set('bootloader_install', False)
            logging.info("Cnchi will not install any bootloader")
        else:
            self.settings.set('bootloader_install', True)
            self.settings.set('bootloader_device', self.bootloader_device)

            self.settings.set('bootloader', self.bootloader)
            msg = "Antergos will install the bootloader {0} in device {1}"
            msg = msg.format(self.bootloader, self.bootloader_device)
            logging.info(msg)

    def run_format(self):
        """ Create staged partitions """
        logging.debug("Creating partitions and their filesystems...")

        # Sometimes a swap partition can still be active at this point
        cmd = ["swapon", "--show=NAME", "--noheadings"]
        swaps = call(cmd)
        swaps = swaps.split("\n")
        for name in filter(None, swaps):
            if "/dev/zram" not in name:
                cmd = ["swapoff", name]
                call(cmd)

        # We'll use auto_partition.setup_luks if necessary
        from installation import auto_partition as ap

        partitions = {}
        if self.disks is None:
            # There's nothing we can do
            return

        for disk_path in self.disks:
            (disk, _result) = self.disks[disk_path]
            # Only commit changes to disks we've changed!
            if disk_path in self.disks_changed:
                self.finalize_changes(disk)
            # Now that partitions are created, set fs and label
            partitions.update(pm.get_partitions(disk))

        all_partitions = list(partitions) + self.lv_partitions

        # Checks if a boot partition exists
        noboot = True
        for allopts in self.stage_opts:
            if (self.stage_opts[allopts][2] == '/boot' or
                    self.stage_opts[allopts][2] == '/boot/efi'):
                noboot = False

        for partition_path in all_partitions:
            # Get label, mount point and filesystem of staged partitions
            uid = self.gen_partition_uid(path=partition_path)
            if uid in self.stage_opts:
                _is_new, lbl, mnt, fisy, fmt = self.stage_opts[uid]
                # Do not label or format extended or bios-gpt-boot partitions
                if fisy == "extended" or fisy == "bios-gpt-boot":
                    continue

                if (((mnt == '/' and noboot) or mnt == '/boot') and
                        '/dev/mapper' not in partition_path):
                    partition = partitions[partition_path]
                    if (not pm.get_flag(partition, pm.PED_PARTITION_BOOT) and
                            self.bootloader_device):
                        pm.set_flag(pm.PED_PARTITION_BOOT, partition)
                        logging.debug(
                            "Set BOOT flag to partition %s", partition_path)

                    self.finalize_changes(partition.disk)

                if "/dev/mapper" in partition_path:
                    pvs = lvm.get_lvm_partitions()
                    # Remove "/dev/mapper/"
                    vgname = partition_path.split("/")[-1]
                    # Check that our vgname does not have a --
                    # (- is used to diferenciate between vgname and lvname)
                    if "--" in vgname:
                        match = re.search(r'\w+--\w+', vgname)
                        if match:
                            vgname = match.group()
                        else:
                            # maybe the user has given an invalid name ¿?
                            vgname = ""
                    else:
                        vgname = vgname.split('-')[0]

                    if vgname and (mnt == '/' or mnt == '/boot'):
                        logging.debug("Volume name is %s", vgname)
                        self.blvm = True
                        if noboot or mnt == '/boot':
                            for part_path in pvs[vgname]:
                                flag = pm.get_flag(partitions[part_path], pm.PED_PARTITION_BOOT)
                                if (not flag and self.bootloader_device):
                                    pm.set_flag(pm.PED_PARTITION_BOOT,
                                                partitions[part_path])
                                    logging.debug(
                                        "Set BOOT flag to partition %s", partition_path)
                                self.finalize_changes(
                                    partitions[part_path].disk)

                if uid in self.luks_options:
                    (use_luks, vol_name, password) = self.luks_options[uid]
                    if use_luks and vol_name and password:
                        txt = "Encrypting {0}, assigning volume name {1} and formatting it..."
                        txt = txt.format(partition_path, vol_name)
                        logging.info(txt)

                        with misc.raised_privileges() as __:
                            ap.setup_luks(
                                luks_device=partition_path,
                                luks_name=vol_name,
                                luks_pass=password)
                        self.settings.set("use_luks", True)
                        luks_device = "/dev/mapper/" + vol_name
                        error, msg = fs.create_fs(luks_device, fisy, lbl)
                        if not error:
                            logging.info(msg)
                        else:
                            txt = ("Couldn't format LUKS device '{0}' with "
                                   "label '{1}' as '{2}': {3}")
                            txt = txt.format(luks_device, lbl, fisy, msg)
                            logging.error(txt)
                            txt = _("Couldn't format LUKS device '{0}' with "
                                    "label '{1}' as '{2}': {3}")
                            txt = txt.format(luks_device, lbl, fisy, msg)
                            show.error(self.get_main_window(), txt)

                        # Do not format (already done)
                        fmt = False
                        # Do not relabel (already done)
                        if partition_path in self.orig_label_dic:
                            lbl = self.orig_label_dic[partition_path]
                        if mnt == "/":
                            self.settings.set("luks_root_password", password)
                            self.settings.set(
                                "luks_root_device", partition_path)

                # Only format if they want formatting
                if fmt:
                    # All of fs module takes paths, not partition objs
                    if lbl:
                        txt = "Creating new {0} filesystem in {1} labeled {2}"
                        txt = txt.format(fisy, partition_path, lbl)
                    else:
                        txt = "Creating new {0} filesystem in {1}"
                        txt = txt.format(fisy, partition_path)
                    logging.info(txt)

                    # Create filesystem using mkfs
                    error, msg = fs.create_fs(partition_path, fisy, lbl)
                    if not error:
                        logging.info(msg)
                    else:
                        txt = "Couldn't format partition '{0}' with label '{1}' as '{2}': {3}"
                        txt = txt.format(partition_path, lbl, fisy, msg)
                        logging.error(txt)
                        txt = _("Couldn't format partition '{0}' with label '{1}' as '{2}': {3}")
                        txt = txt.format(partition_path, lbl, fisy, msg)
                        show.error(self.get_main_window(), txt)
                elif (partition_path in self.orig_label_dic and
                      self.orig_label_dic[partition_path] != lbl):
                    try:
                        fs.label_fs(fisy, partition_path, lbl)
                    except Exception as ex:
                        # Catch all exceptions because not being able to label
                        # a partition shouldn't be fatal
                        template = "An exception of type {0} occured. Arguments:\n{1!r}"
                        message = template.format(type(ex).__name__, ex.args)
                        logging.warning(message)

    def finalize_changes(self, disk):
        """ Save changes to disk """
        try:
            pm.finalize_changes(disk)
            logging.info("Saved changes to disk")
        except IOError as io_error:
            msg = "Cannot commit your changes to disk: {0}".format(
                str(io_error))
            logging.error(msg)
            msg = _("Cannot commit your changes to disk: {0}").format(
                str(io_error))
            show.error(self.get_main_window(), msg)

    def run_install(self, packages, metalinks):
        """ Start installation process """

        # Fill fs_devices and mount_devices dicts that are going to be used
        # by the installation
        self.fs_devices = {}
        self.mount_devices = {}
        for disk_path in self.disks:
            (disk, _result) = self.disks[disk_path]
            partitions = pm.get_partitions(disk)
            self.all_partitions.append(partitions)
            partition_list = pm.order_partitions(partitions)
            fs_type = ""
            for ppath in self.lv_partitions:
                uid = self.gen_partition_uid(path=ppath)
                if uid in self.stage_opts:
                    (_is_new, _label, mount_point, fs_type, _fmt_active) = self.stage_opts[uid]
                    self.mount_devices[mount_point] = ppath
                    self.fs_devices[ppath] = fs_type
                if uid in self.luks_options:
                    (use_luks, vol_name, _password) = self.luks_options[uid]
                    if use_luks and vol_name:
                        self.mount_devices[mount_point] = "/dev/mapper/" + vol_name
            for partition_path in partition_list:
                uid = self.gen_partition_uid(
                    partition=partitions[partition_path])
                if uid in self.stage_opts:
                    (_is_new, _label, mount_point, fs_type, _fmt_active) = self.stage_opts[uid]
                    if fs_type == "extended" or fs_type == "bios-gpt-boot":
                        # Do not mount extended or bios-gpt-boot partitions
                        continue
                    self.mount_devices[mount_point] = partition_path
                    self.fs_devices[partition_path] = fs_type

                if uid in self.luks_options:
                    (use_luks, vol_name, _password) = self.luks_options[uid]
                    if use_luks and vol_name:
                        luks_device = "/dev/mapper/" + vol_name
                        self.mount_devices[mount_point] = luks_device
                        del self.fs_devices[partition_path]
                        self.fs_devices[luks_device] = fs_type

        self.installation = install.Installation(
            self.settings,
            self.callback_queue,
            packages,
            metalinks,
            self.mount_devices,
            self.fs_devices,
            self.ssd,
            self.blvm)
        self.installation.start()
