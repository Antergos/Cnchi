#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  installation_advanced.py
#
#  Copyright 2013 Antergos
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

""" Installation advanced module. Custom partition screen """

from gi.repository import Gtk, Gdk
import subprocess
import os
import sys
import logging

if __name__ == '__main__':
    # Insert the parent directory at the front of the path.
    # This is used only when we want to test this screen
    base_dir = os.path.dirname(__file__) or '.'
    parent_dir = os.path.join(base_dir, '..')
    sys.path.insert(0, parent_dir)

import canonical.gtkwidgets as gtkwidgets

import parted3.partition_module as pm
import parted3.fs_module as fs
import parted3.lvm as lvm
import parted3.used_space as used_space

from installation import process as installation_process
import show_message as show

#_next_page = "timezone"
_next_page = "user_info"
_prev_page = "installation_ask"

class InstallationAdvanced(Gtk.Box):
    """ Installation advanced class. Custom partitioning. """
    def __init__(self, params):
        """ Store class parameters """
        self.blvm = False
        self.header = params['header']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        self.callback_queue = params['callback_queue']
        self.settings = params['settings']
        self.alternate_package_list = params['alternate_package_list']
        self.testing = params['testing']

        self.lv_partitions = []
        self.disks_changed = []

        self.my_first_time = True

        self.orig_label_dic = {}
        self.orig_part_dic = {}

        # stage_opts holds info about newly created partitions
        # format is tuple (label, mountpoint, fs(text), Format)
        # see its usage in listing, creating, and deleting partitions
        self.stage_opts = {}
        self.used_dic = {}

        # hold deleted partitions that exist now
        self.to_be_deleted = []

        # Call base class
        super().__init__()

        # Get UI items
        self.ui = Gtk.Builder()
        self.ui_dir = self.settings.get('ui')
        ui_file = os.path.join(self.ui_dir, "advanced.ui")
        self.ui.add_from_file(ui_file)

        # Connect UI signals
        self.ui.connect_signals(self)

        # Load create and edit partition dialogs
        self.create_partition_dialog = self.ui.get_object('create_partition_dialog')
        self.edit_partition_dialog = self.ui.get_object('edit_partition_dialog')

        # Initialize our create partition dialog filesystems' combo.
        use_combo = self.ui.get_object('partition_use_combo')
        use_combo.remove_all()
        for fs_name in sorted(fs.NAMES):
            use_combo.append_text(fs_name)
        use_combo.set_wrap_width(2)

        # Initialize our edit partition dialog filesystems' combo.
        use_combo = self.ui.get_object('partition_use_combo2')
        use_combo.remove_all()
        for fs_name in sorted(fs.NAMES):
            use_combo.append_text(fs_name)
        use_combo.set_wrap_width(2)

        # Initialize partition_types_combo
        combo = self.ui.get_object('partition_types_combo')
        combo.remove_all()
        combo.append_text("msdos (aka MBR)")
        combo.append_text("GUID Partition Table (GPT)")

        # Automatically select first entry
        self.select_first_combobox_item(combo)

        # Initialize our create and edit partition dialog mount points' combo.
        mount_combos = []
        mount_combos.append(self.ui.get_object('partition_mount_combo'))
        mount_combos.append(self.ui.get_object('partition_mount_combo2'))

        #if os.path.exists('/sys/firmware/efi'):
        #    mount_points = fs.COMMON_MOUNT_POINTS_EFI
        #else:
        #    mount_points = fs.COMMON_MOUNT_POINTS
        
        mount_points = fs.COMMON_MOUNT_POINTS
        
        for combo in mount_combos:
            combo.remove_all()
            for mp in mount_points:
                combo.append_text(mp)

        # We will store our devices here
        self.disks = None

        # We will store if our device is SSD or not
        self.ssd = {}

        self.grub_device_entry = self.ui.get_object('grub_device_entry')
        self.grub_devices = dict()
        self.grub_device = {}
        
        ## Disable boot device selection in uefi systems
        #if os.path.exists('/sys/firmware/efi'):
        #    self.grub_device_entry.set_sensitive(False)

        # Initialise our partition list treeview
        self.partition_list = self.ui.get_object('partition_list_treeview')
        self.partition_list_store = None
        self.prepare_partition_list()

        # Get encryption (LUKS) options dialog
        self.luks_dialog = self.ui.get_object('luks_dialog')

        # Connect changing selection in the partition list treeview
        select = self.partition_list.get_selection()
        select.connect("changed", self.on_partition_list_treeview_selection_changed)

        self.show_changes_grid = None

        # Add ourselves to the parent class
        super().add(self.ui.get_object("installation_advanced"))

        # Initialize some attributes
        self.process = None
        self.diskdic = {}
        self.all_partitions = []

    def gen_partition_uid(self, p=None, path=None):
        """ Function to generate uid by partition object or path """
        if path and not p:
            if "free" in path:
                return None
            for zz in self.all_partitions:
                if "/dev/mapper" not in zz:
                    for yy in zz:
                        if zz[yy].path == path:
                            p = zz[yy]
        try:
            dev = p.disk.device.path
        except:
            dev = path
        if p:
            ends = p.geometry.end
            starts = p.geometry.start
        else:
            ends = 'none'
            starts = 'none'
        uid = dev + str(starts) + str(ends)
        return uid

    def check_buttons(self, selection):
        """ Activates/deactivates our buttons depending on which is selected in the
            partition treeview """

        if self.stage_opts:
            button = self.ui.get_object('partition_button_undo')
            button.set_sensitive(True)

        button_new = self.ui.get_object('partition_button_new')
        button_new.set_sensitive(False)

        button_delete = self.ui.get_object('partition_button_delete')
        button_delete.set_sensitive(False)

        button_edit = self.ui.get_object('partition_button_edit')
        button_edit.set_sensitive(False)

        button_new_label = self.ui.get_object('partition_button_new_label')
        button_new_label.set_sensitive(False)

        model, tree_iter = selection.get_selected()
        diskobj = None
        if tree_iter is not None:
            path = model[tree_iter][0]
            if path == _("free space"):
                button_new.set_sensitive(True)
            else:
                disks = pm.get_devices()
                if (path not in disks and 'dev/mapper' not in path) or ('dev/mapper' in path and '-' in path):
                    # A partition is selected
                    for i in self.all_partitions:
                        if path in i and '/mapper' not in path and '/' in path:
                            diskobj = i[path].disk.device.path
                    if diskobj and model[tree_iter][1] == 'extended' and \
                     self.diskdic[diskobj]['has_logical']:
                        button_delete.set_sensitive(False)
                        button_edit.set_sensitive(False)
                    else:
                        button_delete.set_sensitive(True)
                        if '/mapper' in path:
                            button_delete.set_sensitive(False)
                        button_edit.set_sensitive(True)
                else:
                    # A drive (disk) is selected
                    button_new_label.set_sensitive(True)

    def fill_grub_device_entry(self):
        """ Get all devices where we can put our Grub boot code
            Not using partitions (but we'll have to) """
        self.grub_device_entry.remove_all()
        self.grub_devices.clear()

        # Just call get_devices once
        if self.disks is None:
            self.disks = pm.get_devices()

        for path in sorted(self.disks):
            (disk, result) = self.disks[path]
            if disk is not None:
                dev = disk.device
                # Avoid cdrom and any raid, lvm volumes or encryptfs
                if not dev.path.startswith("/dev/sr") and \
                   not dev.path.startswith("/dev/mapper"):
                    # Hard drives measure themselves assuming kilo=1000, mega=1mil, etc
                    size_in_gigabytes = int((dev.length * dev.sectorSize) / 1000000000)
                    line = '{0} [{1} GB] ({2})'.format(dev.model, size_in_gigabytes, dev.path)
                    self.grub_device_entry.append_text(line)
                    self.grub_devices[line] = dev.path
                    ## Add disk partitions
                    #partitions = pm.get_partitions(disk)
                    #partition_list = pm.order_partitions(partitions)
                    #for partition_path in partition_list:
                    #    if not "free" in partition_path:
                    #        warning_txt = _("It's not recommended to install grub in a partition")
                    #        line = '   {0} ({1})'.format(partition_path, warning_txt)
                    #        self.grub_device_entry.append_text(line)
                    #        self.grub_devices[line] = partition_path

        # Automatically select first entry
        self.select_first_combobox_item(self.grub_device_entry)

    def on_grub_device_check_toggled(self, checkbox):
        combo = self.ui.get_object("grub_device_entry")
        combo.set_sensitive(checkbox.get_active())

    def select_first_combobox_item(self, combobox):
        """ Automatically select first entry """
        tree_model = combobox.get_model()
        tree_iter = tree_model.get_iter_first()
        combobox.set_active_iter(tree_iter)

    def on_grub_device_entry_changed(self, widget):
        """ Get new selected GRUB device """
        line = self.grub_device_entry.get_active_text()
        if line is not None:
            self.grub_device = self.grub_devices[line]

    def prepare_partition_list(self):
        """ Create columns for our treeview """
        render_text = Gtk.CellRendererText()

        col = Gtk.TreeViewColumn(_("Device"), render_text, text=0)
        self.partition_list.append_column(col)

        col = Gtk.TreeViewColumn(_("Type"), render_text, text=1)
        self.partition_list.append_column(col)

        col = Gtk.TreeViewColumn(_("Mount point"), render_text, text=2)
        self.partition_list.append_column(col)

        col = Gtk.TreeViewColumn(_("Label"), render_text, text=3)
        self.partition_list.append_column(col)

        format_toggle = Gtk.CellRendererToggle()
        format_toggle.connect("toggled", self.on_format_cell_toggled)

        col = Gtk.TreeViewColumn(_("Format"), format_toggle, active=4, visible=5, sensitive=11)
        self.partition_list.append_column(col)

        col = Gtk.TreeViewColumn(_("Size"), render_text, text=6)
        self.partition_list.append_column(col)

        col = Gtk.TreeViewColumn(_("Used"), render_text, text=7)
        self.partition_list.append_column(col)

        col = Gtk.TreeViewColumn(_("Flags"), render_text, text=9)
        self.partition_list.append_column(col)

        ssd_toggle = Gtk.CellRendererToggle()
        ssd_toggle.connect("toggled", self.on_ssd_cell_toggled)

        col = Gtk.TreeViewColumn(_("SSD"), ssd_toggle, active=12, visible=13, sensitive=14)
        self.partition_list.append_column(col)

    def get_size(self, length, sector_size):
        """ Helper function to get a disk/partition size in human format """
        size = length * sector_size
        size_txt = "%db" % size

        if size >= 1000000000:
            size /= 1000000000
            size_txt = "%dG" % size
        elif size >= 1000000:
            size /= 1000000
            size_txt = "%dM" % size
        elif size >= 1000:
            size /= 1000
            size_txt = "%dK" % size

        return size_txt

    def fill_partition_list(self):
        """ Fill the partition list with all the data. """
        self.diskdic = {}
        self.all_partitions = []
        # We will store our data model in 'partition_list_store'
        if self.partition_list_store is not None:
            self.partition_list_store.clear()

        # Treeview columns:
        # disc path or partition path or "free space",
        # fs_type
        # label
        # part_name
        # formatable_active
        # formatable_visible
        # size
        # used
        # partition_path
        # flags
        # formatable_selectable (sensitive)
        # ssd_active
        # ssd_visible
        # ssd_selectable (sensitive)

        self.partition_list_store = \
            Gtk.TreeStore(str, str, str, str, bool, bool, str, str, str,
                          str, int, bool, bool, bool, bool)

        # Be sure to call get_devices once
        if self.disks == None:
            self.disks = pm.get_devices()
        self.lv_partitions = []
        self.diskdic['mounts'] = []
        vgs = lvm.get_volume_groups()
        if vgs:
            for vg in vgs:
                is_ssd = False
                lvs = lvm.get_logical_volumes(vg)
                if not lvs:
                    continue
                row = [vg, "", "", "", False, False, "", "", "", "", 0, False, False, False, False]
                lvparent = self.partition_list_store.append(None, row)
                for lv in lvs:
                    fmt_enable = True
                    fmt_active = False
                    label = ""
                    fs_type = ""
                    mount_point = ""
                    used = ""
                    flags = ""
                    formatable = True
                    partition_path = "/dev/mapper/%s-%s" % (vg, lv)
                    self.all_partitions.append(partition_path)
                    self.lv_partitions.append(partition_path)
                    uid = self.gen_partition_uid(path=partition_path)
                    if fs.get_type(partition_path):
                        fs_type = fs.get_type(partition_path)
                    elif used_space.is_btrfs(partition_path):
                        # kludge, btrfs not being detected...
                        fs_type = 'btrfs'
                    else:
                        # Say unknown if we can't detect fs type instead of assumming btrfs
                        fs_type = 'unknown'

                    if uid in self.stage_opts:
                        (is_new, label, mount_point, fs_type, fmt_active) = self.stage_opts[uid]

                    info = fs.get_info(partition_path)
                    if 'LABEL' in info:
                        label = info['LABEL']

                    if mount_point:
                        self.diskdic['mounts'].append(mount_point)

                    # Do not show swap version, only the 'swap' word
                    if 'swap' in fs_type:
                        fs_type = 'swap'

                    row = [partition_path, fs_type, mount_point, label, fmt_active,
                           formatable, '', '', partition_path,
                           "", 0, fmt_enable, False, False, False]
                    self.partition_list_store.append(lvparent, row)
                    if self.my_first_time:
                        self.orig_part_dic[partition_path] = self.gen_partition_uid(path=partition_path)
                        self.orig_label_dic[partition_path] = label

        # Here we fill our model
        for disk_path in sorted(self.disks):
            if '/dev/mapper/arch_' in disk_path:
                continue

            self.diskdic[disk_path] = {}
            self.diskdic[disk_path]['has_logical'] = False
            self.diskdic[disk_path]['has_extended'] = False

            if disk_path not in self.ssd:
                self.ssd[disk_path] = fs.is_ssd(disk_path)

            is_ssd = self.ssd[disk_path]

            (disk, result) = self.disks[disk_path]

            if disk is None:
                # Maybe disk without a partition table?
                row = [disk_path, "", "", "", False, False, "", "", "",
                    "", 0, False, is_ssd, False, False]
                self.partition_list_store.append(None, row)
            else:
                dev = disk.device

                # Get device size
                size_txt = self.get_size(dev.length, dev.sectorSize)

                row = [dev.path, "", "", "", False, False, size_txt, "",
                    "", "", 0, False, is_ssd, True, True]
                if '/dev/mapper/' in disk_path:
                    continue
                disk_parent = self.partition_list_store.append(None, row)
                parent = disk_parent

                # Create a list of partitions for this device (/dev/sda for example)
                partitions = pm.get_partitions(disk)
                self.all_partitions.append(partitions)
                partition_list = pm.order_partitions(partitions)

                for partition_path in partition_list:
                    # Get partition size
                    p = partitions[partition_path]
                    size_txt = self.get_size(p.geometry.length, dev.sectorSize)
                    fmt_enable = False
                    fmt_active = False
                    label = ""
                    fs_type = ""
                    mount_point = ""
                    used = ""
                    flags = ""
                    formatable = True

                    path = p.path

                    # Skip lvm, LUKS, ...
                    if '/dev/mapper' in path:
                        continue

                    # Get filesystem
                    if p.fileSystem and p.fileSystem.type:
                        fs_type = p.fileSystem.type
                    # Check if its free space before trying to get the filesystem with blkid.
                    elif 'free' in partition_path:
                        fs_type = _("none")
                    elif fs.get_type(path):
                        fs_type = fs.get_type(path)
                    else:
                        # Unknown filesystem
                        fs_type = '?'

                    # Nothing should be mounted at this point

                    if p.type == pm.PARTITION_EXTENDED:
                        formatable = False
                        self.diskdic[disk_path]['has_extended'] = True
                    elif p.type == pm.PARTITION_LOGICAL:
                        formatable = True
                        self.diskdic[disk_path]['has_logical'] = True

                    if p.type in (pm.PARTITION_FREESPACE,
                                  pm.PARTITION_FREESPACE_EXTENDED):
                        # Show 'free space' instead of /dev/sda-1
                        path = _("free space")
                        formatable = False
                    else:
                        # Get partition flags
                        flags = pm.get_flags(p)

                    uid = self.gen_partition_uid(p=p)
                    if uid in self.stage_opts:
                        (is_new, label, mount_point, fs_type, fmt_active) = self.stage_opts[uid]
                        fmt_enable = not is_new
                        if mount_point == "/":
                            fmt_enable = False
                    else:
                        fmt_enable = True
                        if _("free space") not in path:
                            if self.my_first_time:
                                if mount_point:
                                    used = pm.get_used_space(p)
                                else:
                                    used = used_space.get_used_space(partition_path, fs_type) * p.geometry.length
                                    used = self.get_size(used, dev.sectorSize)
                                self.used_dic[(disk_path, p.geometry.start)] = used
                            else:
                                if (disk_path, p.geometry.start) in self.used_dic:
                                    used = self.used_dic[(disk_path, p.geometry.start)]
                                else:
                                    used = '0b'
                            info = fs.get_info(partition_path)
                            if 'LABEL' in info:
                                label = info['LABEL']

                    if mount_point:
                        self.diskdic['mounts'].append(mount_point)

                    if p.type == pm.PARTITION_EXTENDED:
                        # Show 'extended' in file system type column
                        fs_type = 'extended'

                    # Do not show swap version, only the 'swap' word
                    if 'swap' in fs_type:
                        fs_type = 'swap'

                    row = [path, fs_type, mount_point, label, fmt_active,
                           formatable, size_txt, used, partition_path,
                           "", p.type, fmt_enable, False, False, False]

                    if p.type in (pm.PARTITION_LOGICAL,
                                  pm.PARTITION_FREESPACE_EXTENDED):
                        parent = myparent
                    else:
                        parent = disk_parent

                    tree_iter = self.partition_list_store.append(parent, row)

                    # If we're an extended partition, all the logical
                    # partitions that follow will be shown as children
                    # of this one
                    if p.type == pm.PARTITION_EXTENDED:
                        myparent = tree_iter

                    if self.my_first_time:
                        self.orig_part_dic[p.path] = self.gen_partition_uid(p)
                        self.orig_label_dic[p.path] = label

        self.my_first_time = False

        # Assign our new model to our treeview
        self.partition_list.set_model(self.partition_list_store)
        self.partition_list.expand_all()

        # Check if correct mount points are already defined,
        # so we can proceed with installation
        self.check_mount_points()

    def on_format_cell_toggled(self, widget, path):
        """ Mark a partition to be formatted """
        # selected_path = Gtk.TreePath(path)
        self.partition_list_store[path][4] = not self.partition_list_store[path][4]
        amnew = False
        partition_path = self.partition_list_store[path][0]
        uid = self.gen_partition_uid(path=partition_path)
        self.stage_opts[uid] = \
            (amnew,
             self.partition_list_store[path][3],
             self.partition_list_store[path][2],
             self.partition_list_store[path][1],
             self.partition_list_store[path][4])

    def on_ssd_cell_toggled(self, widget, path):
        """ Mark disk as ssd """
        # ssd cell
        self.partition_list_store[path][12] = not self.partition_list_store[path][12]
        disk_path = self.partition_list_store[path][0]
        self.ssd[disk_path] = self.partition_list_store[path][12]

    def on_partition_list_edit_activate(self, button):
        """ The user wants to edit a partition """
        selection = self.partition_list.get_selection()

        if not selection:
            return

        model, tree_iter = selection.get_selected()

        if tree_iter is None:
            return

        # Get necessary row data
        row = model[tree_iter]

        fs = row[1]
        mount_point = row[2]
        label = row[3]
        fmt = row[4]
        partition_path = row[8]
        fmtable = row[11]

        # Can't edit an partition with LVM filesystem type
        if "lvm2" in fs.lower():
            logging.warning(_("Can't edit a partition with LVM filesystem type"))
            return

        # Set fs in dialog combobox
        use_combo = self.ui.get_object('partition_use_combo2')
        use_combo_model = use_combo.get_model()
        use_combo_iter = use_combo_model.get_iter_first()

        while use_combo_iter is not None:
            use_combo_row = use_combo_model[use_combo_iter]
            if use_combo_row[0] and use_combo_row[0] in fs:
                use_combo.set_active_iter(use_combo_iter)
                use_combo_iter = None
            else:
                use_combo_iter = use_combo_model.iter_next(use_combo_iter)

        # Set mount point in dialog combobox
        mount_combo_entry = self.ui.get_object('combobox-entry2')
        mount_combo_entry.set_text(mount_point)

        # Set label entry
        label_entry = self.ui.get_object('partition_label_entry2')
        label_entry.set_text(label)

        # Must format?
        format_check = self.ui.get_object('partition_format_check')
        format_check.set_active(fmt)
        format_check.set_sensitive(fmtable)

        # Be sure to just call get_devices once
        if self.disks is None:
            self.disks = pm.get_devices()

        # Get disk_path and disk
        disk_path = self.get_disk_path_from_selection(model, tree_iter)
        try:
            (disk, result) = self.disks[disk_path]
        except:
            disk = None

        # Show edit partition dialog
        response = self.edit_partition_dialog.run()

        if response == Gtk.ResponseType.OK:
            mylabel = label_entry.get_text()
            mymount = mount_combo_entry.get_text().strip()

            if mymount in self.diskdic['mounts'] and mymount != mount_point:
                show.warning(_('Cannot use the same mount point twice.'))
            elif mymount == "/" and not format_check.get_active():
                show.warning(_('Root partition must be formatted.'))
            else:
                if mount_point:
                    self.diskdic['mounts'].remove(mount_point)

                myfmt = use_combo.get_active_text()
                uid = self.gen_partition_uid(path=partition_path)
                fmtop = format_check.get_active()

                if uid in self.stage_opts:
                    is_new = self.stage_opts[uid][0]
                    #fmtop = self.stage_opts[uid][4]
                else:
                    is_new = False
                    #fmtop = False

                if myfmt == 'swap':
                    mymount = 'swap'

                self.stage_opts[uid] = (is_new, mylabel, mymount, myfmt, fmtop)

        self.edit_partition_dialog.hide()

        # Update the partition list treeview
        self.fill_partition_list()
        self.fill_grub_device_entry()

    def get_disk_path_from_selection(self, model, tree_iter):
        """ This returns the disk path where the selected partition is in """
        if tree_iter is not None and model is not None:
            row = model[tree_iter]
            partition_path = row[8]

            # Get partition type from the user selection
            part_type = row[10]

            # Get our parent drive
            parent_iter = model.iter_parent(tree_iter)

            if part_type == pm.PARTITION_LOGICAL:
                # If we are a logical partition, our drive won't be our father
                # but our grandpa (we have to skip the extended partition we're in)
                parent_iter = model.iter_parent(parent_iter)

            return model[parent_iter][0]
        else:
            return None

    def on_partition_list_delete_activate(self, button):
        """ Delete partition """
        selection = self.partition_list.get_selection()
        if not selection:
            return

        model, tree_iter = selection.get_selected()

        if tree_iter is None:
            return
        am_new = False
        # Get row data
        row = model[tree_iter]
        mount_point = row[2]
        size_available = row[6]
        partition_path = row[8]
        if mount_point in self.diskdic['mounts']:
            self.diskdic['mounts'].remove(mount_point)
        if self.gen_partition_uid(path=partition_path) in self.stage_opts:
            am_new = self.stage_opts[self.gen_partition_uid(path=partition_path)][0]
            del(self.stage_opts[self.gen_partition_uid(path=partition_path)])
        if not am_new:
            for e in self.orig_part_dic:
                if self.orig_part_dic[e] == self.gen_partition_uid(path=partition_path):
                    self.to_be_deleted.append(e)
        disk_path = self.get_disk_path_from_selection(model, tree_iter)
        self.disks_changed.append(disk_path)

        logging.info(_("You will delete the partition %s from disk %s"), partition_path, disk_path)

        # Be sure to just call get_devices once
        if self.disks is None:
            self.disks = pm.get_devices()

        (disk, result) = self.disks[disk_path]

        partitions = pm.get_partitions(disk)

        part = partitions[partition_path]
        if (disk.device.path, part.geometry.start) in self.used_dic:
            del self.used_dic[(disk.device.path, part.geometry.start)]

        # Before delete the partition, check if it's already mounted
        if pm.check_mounted(part):
            # We unmount the partition. Should we ask first?
            logging.info(_("Unmounting %s..."), part.path)
            subp = subprocess.Popen(['umount', part.path], stdout=subprocess.PIPE)

        # Is it worth to show some warning message here?
        # No, created delete list as part of confirmation screen.
        pm.delete_partition(disk, part)

        # Update the partition list treeview
        self.fill_partition_list()
        self.fill_grub_device_entry()

    def get_mount_point(self, partition_path):
        """ Get device mount point """
        fsname = ''
        fstype = ''
        writable = ''
        with open('/proc/mounts') as fp:
            for line in fp:
                line = line.split()
                if line[0] == partition_path:
                    fsname = line[1]
                    fstype = line[2]
                    writable = line[3].split(',')[0]
        return fsname, fstype, writable

    def get_swap_partition(self, partition_path):
        """ Get active swap partition """

        partition = ''
        with open('/proc/swaps') as fp:
            for line in fp:
                line = line.split()
                if line[0] == partition_path:
                    partition = line[0]
        return partition

    def on_partition_list_new_activate(self, button):
        """ Add a new partition """
        selection = self.partition_list.get_selection()

        if not selection:
            return

        # Assume it will be formatted, unless it's extended
        formatme = True
        model, tree_iter = selection.get_selected()

        if tree_iter is None:
            return

        # Get necessary row data
        row = model[tree_iter]

        # Get partition type from the user selection
        part_type = row[10]

        # Check that the user has selected a free space row.
        if part_type not in (pm.PARTITION_FREESPACE, pm.PARTITION_FREESPACE_EXTENDED):
            return

        size_available = row[6]
        partition_path = row[8]

        # Get our parent drive
        parent_iter = model.iter_parent(tree_iter)

        parent_part_type = model[parent_iter][10]

        if parent_part_type == pm.PARTITION_EXTENDED:
            # We're creating a partition inside an already created extended
            # partition. Our drive won't be our father but our grandpa
            # (we have to skip the extended partition we're in)
            parent_iter = model.iter_parent(parent_iter)
            isbase = False
        else:
            isbase = True

        disk_path = model[parent_iter][0]
        self.disks_changed.append(disk_path)
        # Be sure to just call get_devices once
        if self.disks is None:
            self.disks = pm.get_devices()

        (disk, result) = self.disks[disk_path]
        dev = disk.device

        partitions = pm.get_partitions(disk)
        p = partitions[partition_path]

        # Added extended, moving extended details up here

        # Get the objects from the dialog
        extended = disk.getExtendedPartition()
        supports_extended = disk.supportsFeature(pm.DISK_EXTENDED)
        primary_radio = self.ui.get_object('partition_create_type_primary')
        logical_radio = self.ui.get_object('partition_create_type_logical')
        extended_radio = self.ui.get_object('partition_create_type_extended')

        primary_radio.set_active(True)
        logical_radio.set_active(False)
        extended_radio.set_active(False)

        logical_radio.set_visible(True)
        primary_radio.set_visible(True)
        extended_radio.set_visible(True)

        if not supports_extended:
            extended_radio.set_visible(False)

        if isbase and extended:
            logical_radio.set_visible(False)
            extended_radio.set_visible(False)
        elif isbase and not extended:
            logical_radio.set_visible(False)
        elif not isbase:
            logical_radio.set_active(True)
            primary_radio.set_visible(False)
            extended_radio.set_visible(False)

        # Get how many primary partitions are already created on disk
        primary_count = disk.primaryPartitionCount
        if primary_count >= disk.maxPrimaryPartitionCount:
            # No room left for another primary partition
            primary_radio.set_sensitive(False)

        beginning_radio = self.ui.get_object('partition_create_place_beginning')
        end_radio = self.ui.get_object('partition_create_place_end')
        beginning_radio.set_active(True)
        end_radio.set_active(False)

        # Prepare size spin
        # +1 as not to leave unusably small space behind
        max_size_mb = int((p.geometry.length * dev.sectorSize) / 1000000) + 1

        size_spin = self.ui.get_object('partition_size_spinbutton')
        size_spin.set_digits(0)
        # value, lower, upper, step_incr, page_incr, page_size
        adjustment = Gtk.Adjustment(max_size_mb, 1, max_size_mb, 1, 10, 0)
        size_spin.set_adjustment(adjustment)
        size_spin.set_value(max_size_mb)

        # label
        label_entry = self.ui.get_object('partition_label_entry')
        label_entry.set_text("")

        # use
        use_combo = self.ui.get_object('partition_use_combo')
        use_combo.set_active(3)

        # mount combo entry
        mount_combo_entry = self.ui.get_object('combobox-entry')
        mount_combo_entry.set_text("")

        # Finally, show the create partition dialog

        response = self.create_partition_dialog.run()
        if response == Gtk.ResponseType.OK:
            mylabel = label_entry.get_text()
            mymount = mount_combo_entry.get_text().strip()
            if mymount in self.diskdic['mounts']:
                show.warning(_('Cannot use the same mount point twice...'))
            else:
                if mymount:
                    self.diskdic['mounts'].append(mymount)
                myfmt = use_combo.get_active_text()
                if myfmt is None:
                    myfmt = ""
                if myfmt == 'swap':
                    mymount = 'swap'
                # Get selected size
                size = int(size_spin.get_value())

                beg_var = beginning_radio.get_active()

                start_sector = p.geometry.start
                end_sector = p.geometry.end
                geometry = pm.geom_builder(disk, start_sector,
                                           end_sector, size, beg_var)

                # User wants to create an extended, logical or primary partition
                if primary_radio.get_active():
                    logging.debug(_("Creating a primary partition"))
                    pm.create_partition(disk, pm.PARTITION_PRIMARY, geometry)
                elif extended_radio.get_active():
                    # No mounting extended partitions.
                    if mymount:
                        self.diskdic['mounts'].remove(mymount)
                        mymount = ''
                    # No labeling either..
                    mylabel = ''
                    myfmt = 'extended'
                    formatme = False
                    logging.debug(_("Creating an extended partition"))
                    pm.create_partition(disk, pm.PARTITION_EXTENDED, geometry)
                elif logical_radio.get_active():
                    logical_count = len(list(disk.getLogicalPartitions()))
                    max_logicals = disk.getMaxLogicalPartitions()
                    if logical_count < max_logicals:
                        logging.debug(_("Creating a logical partition"))
                        # Which geometry should we use here?
                        pm.create_partition(disk, pm.PARTITION_LOGICAL, geometry)

                # Store stage partition info in self.stage_opts
                old_parts = []
                for y in self.all_partitions:
                    for z in y:
                        old_parts.append(z)
                partitions = pm.get_partitions(disk)
                for e in partitions:
                    if e not in old_parts:
                        uid = self.gen_partition_uid(p=partitions[e])
                        self.stage_opts[uid] = (True, mylabel, mymount, myfmt, formatme)
                # Update partition list treeview
                self.fill_partition_list()
                self.fill_grub_device_entry()

        self.create_partition_dialog.hide()

    def on_partition_encryption_settings_clicked(self, widget):
        # TODO: Load previous user choices (if any)
        # show LUKS encryption options dialog
        # save user choices
        """ Show LUKS encryption options dialog """
        response = self.luks_dialog.run()
        if response == Gtk.ResponseType.OK:
            pass

    def on_switch_use_luks_activate(self, widget):
        enable_luks_dialog_options(widget.get_activate())

    def enable_luks_dialog_options(self, status):
        w_sensitive = ['label_luks_vol_name', 'label_luks_password',
                       'label_luks_password_confirm', 'entry_luks_vol_name',
                       'entry_luks_password', 'entry_luks_password_confirm']
        w_hide = ['image_luks_password_confirm', 'label_luks_password_status']

        for w in w_sensitive:
            w.set_sensitive(status)

        if status is False:
            for w in w_hide:
                w.hide()

    def on_partition_create_type_extended_toggled(self, widget):
        partition = {}
        partition['use_label'] = self.ui.get_object('partition_use_label')
        partition['use_combo'] = self.ui.get_object('partition_use_combo')
        partition['mount_label'] = self.ui.get_object('partition_mount_label')
        partition['mount_combo'] = self.ui.get_object('partition_mount_combo')
        partition['label_label'] = self.ui.get_object('partition_label_label')
        partition['label_entry'] = self.ui.get_object('partition_label_entry')

        sensitive = True

        if widget.get_active():
            sensitive = False

        for w in partition:
            partition[w].set_sensitive(sensitive)

    def on_partition_use_combo_changed(self, selection):
        fs_selected = selection.get_active_text()
        p_mount_combo = self.ui.get_object('partition_mount_combo')
        p_mount_label = self.ui.get_object('partition_mount_label')
        if fs_selected == 'swap':
            p_mount_combo.hide()
            p_mount_label.hide()
        else:
            p_mount_combo.show()
            p_mount_label.show()

    def on_partition_use_combo2_changed(self, selection):
        fs_selected = selection.get_active_text()
        p_mount_combo = self.ui.get_object('partition_mount_combo2')
        p_mount_label = self.ui.get_object('partition_mount_label2')
        if fs_selected == 'swap':
            p_mount_combo.hide()
            p_mount_label.hide()
        else:
            p_mount_combo.show()
            p_mount_label.show()

    def on_partition_list_undo_activate(self, button):
        """ Undo all user changes """
        # To undo user changes, we simply reload all devices
        self.disks = pm.get_devices()
        self.disks_changed = []

        # Empty stage partitions' options
        self.stage_opts = {}

        # Empty to be deleted partitions list
        self.to_be_deleted = []

        # Refresh our partition treeview
        self.fill_partition_list()
        self.fill_grub_device_entry()

    def on_partition_list_treeview_selection_changed(self, selection):
        """ Selection changed, call check_buttons to update them """
        self.check_buttons(selection)
        return False

    def on_partition_list_treeview_button_press_event(self, widget, event):
        """ Called when clicked on the partition list treeview
            Inherited from Ubiquity. Not doing anything here (return false to not stop the chain of events) """
        return False

    def on_partition_list_treeview_key_press_event(self, widget, event):
        """ Called when a key is pressed when the partition list treeview has focus
            Inherited from Ubiquity. Not doing anything here (return false to not stop the chain of events) """
        return False

    def on_partition_list_treeview_row_activated(self, path, column, user_data):
        button_edit = self.ui.get_object('partition_button_edit')
        button_new = self.ui.get_object('partition_button_new')

        if button_edit.get_sensitive():
            self.on_partition_list_edit_activate(None)
        elif button_new.get_sensitive():
            self.on_partition_list_new_activate(None)

        return False

    def on_partition_list_treeview_popup_menu(self, widget):
        """ Inherited from Ubiquity. Not doing anything here (return false to not stop the chain of events) """
        return False

    def translate_ui(self):
        """ As the installer language can change anytime the user changes it, we have
            to 'retranslate' all our widgets calling this function """

        self.header.set_subtitle(_("Advanced Installation Mode"))

        #txt = _("Advanced Installation Mode")
        #txt = "<span weight='bold' size='large'>%s</span>" % txt
        #self.title.set_markup(txt)

        txt = _("Use the device below for boot loader installation:")
        txt = "<span weight='bold' size='small'>%s</span>" % txt
        label = self.ui.get_object('grub_device_label')
        label.set_markup(txt)

        txt = _("Mount Checklist:")
        txt = "<span weight='bold'>%s</span>" % txt
        label = self.ui.get_object('mnt_chklist')
        label.set_markup(txt)

        part = self.ui.get_object('root_part')
        txt = _("Root ( / )")
        part.props.label = txt

        part = self.ui.get_object('boot_part')
        txt = _("Boot ( /boot )")
        part.props.label = txt

        part = self.ui.get_object('boot_efi_part')
        txt = _("EFI ( /boot )")
        part.props.label = txt

        part = self.ui.get_object('swap_part')
        txt = _("Swap")
        part.props.label = txt

        #txt = _("TODO: Here goes a warning message")
        #txt = "<span weight='bold'>%s</span>" % txt
        #label = self.ui.get_object('part_advanced_warning_message')
        #label.set_markup(txt)

        txt = _("New Partition Table")
        button = self.ui.get_object('partition_button_new_label')
        button.set_label(txt)

        #txt = _("Revert")
        #button = self.ui.get_object('partition_button_undo')
        #button.set_label(txt)

        txt = _("Change...")
        button = self.ui.get_object('partition_button_edit')
        button.set_label(txt)

        # Translate dialog "Create partition"
        txt = _("Size:")
        label = self.ui.get_object('partition_size_label')
        label.set_markup(txt)

        txt = _("Type:")
        label = self.ui.get_object('partition_create_type_label')
        label.set_markup(txt)

        txt = _("Primary")
        button = self.ui.get_object('partition_create_type_primary')
        button.set_label(txt)

        txt = _("Logical")
        button = self.ui.get_object('partition_create_type_logical')
        button.set_label(txt)

        txt = _("Extended")
        button = self.ui.get_object('partition_create_type_extended')
        button.set_label(txt)

        txt = _("Beginning of this space")
        button = self.ui.get_object('partition_create_place_beginning')
        button.set_label(txt)

        txt = _("End of this space")
        button = self.ui.get_object('partition_create_place_end')
        button.set_label(txt)

        txt = _("Use As:")
        label = self.ui.get_object('partition_use_label')
        label.set_markup(txt)

        txt = _("Mount Point:")
        label = self.ui.get_object('partition_mount_label')
        label.set_markup(txt)

        txt = _("Label (optional):")
        label = self.ui.get_object('partition_label_label')
        label.set_markup(txt)

        txt = _("Encryption Options...")
        button = self.ui.get_object('partition_encryption_settings')
        button.set_label(txt)

        # Translate dialog "Edit partition"
        txt = _("Use As:")
        label = self.ui.get_object('partition_use_label2')
        label.set_markup(txt)

        txt = _("Mount Point:")
        label = self.ui.get_object('partition_mount_label2')
        label.set_markup(txt)

        txt = _("Label (optional):")
        label = self.ui.get_object('partition_label_label2')
        label.set_markup(txt)

        txt = _("Format:")
        label = self.ui.get_object('partition_format_label')
        label.set_markup(txt)

        # Create disk partition table dialog
        txt = _("Partition Table Type:")
        label = self.ui.get_object('partition_type_label')
        label.set_markup(txt)

        dialog = self.ui.get_object("create_table_dialog")
        dialog.set_title(_("Create Partition Table"))

        # Change "Next" button text
        txt = _("Install Now!")
        self.forward_button.set_label(txt)

        #self.ui.get_object('cancelbutton')
        #self.ui.get_object('partition_dialog_okbutton')

    def prepare(self, direction):
        """ Prepare our dialog to show/hide/activate/deactivate what's necessary """

        self.fill_grub_device_entry()
        self.translate_ui()
        self.fill_partition_list()
        self.show_all()

        # TODO: Enable this and finish LUKS encryption
        button = self.ui.get_object('partition_encryption_settings')
        button.set_sensitive(False)
        button.hide()
        button = self.ui.get_object('partition_encryption_settings2')
        button.set_sensitive(False)
        button.hide()

        #label = self.ui.get_object('part_advanced_recalculating_label')
        #label.hide()
        spinner = self.ui.get_object('partition_recalculating_spinner')
        spinner.hide()

        button = self.ui.get_object('partition_button_lvm')
        button.hide()

        #image = self.ui.get_object('part_advanced_warning_image')
        #image.hide()

        #label = self.ui.get_object('part_advanced_warning_message')
        #label.hide()

        button = self.ui.get_object('partition_button_new')
        button.set_sensitive(False)

        button = self.ui.get_object('partition_button_delete')
        button.set_sensitive(False)

        button = self.ui.get_object('partition_button_edit')
        button.set_sensitive(False)

        button = self.ui.get_object('partition_button_new_label')
        button.set_sensitive(False)

        button = self.ui.get_object('partition_button_undo')
        button.set_sensitive(False)

    def on_partition_list_new_label_activate(self, button):
        """ Create a new partition table """
        # TODO: We should check first if there's any mounted partition (including swap)

        selection = self.partition_list.get_selection()

        if not selection:
            return

        model, tree_iter = selection.get_selected()

        if tree_iter is None:
            return

        disk_path = model[tree_iter][0]

        # Be sure to just call get_devices once
        if self.disks is None:
            self.disks = pm.get_devices()

        (disk_sel, result) = self.disks[disk_path]

        dialog = self.ui.get_object("create_table_dialog")
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            combo = self.ui.get_object('partition_types_combo')
            line = combo.get_active_text()
            if line:
                # by default, use msdos type
                ptype = 'msdos'

                if "GPT" in line:
                    ptype = 'gpt'

                logging.info(_("Creating a new %s partition table for disk %s") % (ptype, disk_path))

                new_disk = pm.make_new_disk(disk_path, ptype)
                self.disks[disk_path] = (new_disk, pm.OK)

                self.fill_grub_device_entry()
                self.fill_partition_list()

                if ptype == 'gpt' and not os.path.exists('/sys/firmware/efi'):
                    # Show warning (see https://github.com/Antergos/Cnchi/issues/63)
                    show.warning(_('GRUB requires a BIOS Boot Partition (2 MiB, no filesystem, EF02 type code in gdisk '
                        'or bios_grub flag in GNU Parted) in BIOS systems to embed its core.img file due to lack of '
                        'post-MBR embed gap in GPT disks.\n\nFor '
                        'a BIOS-GPT configuration, create a 1007 KiB partition at the beginning of the disk with no '
                        'filesystem. That will allow for the next partition on the disk to be correctly '
                        'aligned at 1024 KiB. If needed, the partition can also be located somewhere else on the '
                        'disk, but it should be within the first 2 TiB region. Set the partition type to ef02.\n\n'
                        'The GPT partition also creates a protective MBR partition to stop unsupported tools from '
                        'modifying it. You may need to set a bootable flag on this protective MBR partition if your'
                        'system doesnt boot successfully after installation.\n\n'
                        'Cnchi will create the BIOS Boot Partition for you.'))
                    self.create_bios_gpt_boot_partition(disk_path)

        dialog.hide()

    def create_bios_gpt_boot_partition(self, disk_path):
        """ Create an unformatted partition with no filesystem and with a bios_grub flag on. """
        # It won't be formated
        formatme = False

        part_type = pm.PARTITION_FREESPACE

        self.disks_changed.append(disk_path)

        # Be sure to just call get_devices once
        if self.disks is None:
            self.disks = pm.get_devices()

        (disk, result) = self.disks[disk_path]
        dev = disk.device

        partitions = pm.get_partitions(disk)
        partition_list = pm.order_partitions(partitions)
        for partition_path in partition_list:
            p = partitions[partition_path]

        # Get how many primary partitions are already created on disk
        if disk.primaryPartitionCount > 0:
            # BIOS GPT Boot partition must be the first one on the disk
            logging.error("Can't create BIOS GPT Boot partition!")
            return

        #max_size_mb = int((p.geometry.length * dev.sectorSize) / 1000000) + 1

        mylabel = ""
        mymount = ""
        myfmt = "bios-gpt-boot"
        formatme = False

        # Size must be 2MiB
        size = 2

        beg_var = True

        start_sector = p.geometry.start
        end_sector = p.geometry.end
        geometry = pm.geom_builder(disk, start_sector,
                                   end_sector, size, beg_var)

        part = pm.create_partition(disk, pm.PARTITION_PRIMARY, geometry)

        (res, err) = pm.set_flag(pm.PED_PARTITION_BIOS_GRUB, part)

        if res:
            logging.error(err)

        # Store stage partition info in self.stage_opts
        old_parts = []
        for y in self.all_partitions:
            for z in y:
                old_parts.append(z)

        partitions = pm.get_partitions(disk)
        for e in partitions:
            if e not in old_parts:
                uid = self.gen_partition_uid(p=partitions[e])
                self.stage_opts[uid] = (True, mylabel, mymount, myfmt, formatme)

        # Update partition list treeview
        self.fill_partition_list()
        self.fill_grub_device_entry()

    def on_partition_list_lvm_activate(self, button):
        pass

    def check_mount_points(self):
        """ Check that all necessary mount points are specified.
            At least root (/) partition must be defined and
            in UEFI systems the efi partition (/boot/efi) must be defined too """

        # Initialize our mount point check widgets

        check_parts = ["root", "boot", "boot_efi", "swap"]

        has_part = {}
        for check_part in check_parts:
            has_part[check_part] = False

        # Are we in a EFI system?
        is_uefi = os.path.exists('/sys/firmware/efi')

        # TODO: Check total system RAM in hardware module so we can require swap for low memory systems
        need_swap = False

        part = {}
        for check_part in check_parts:
            part[check_part] = self.ui.get_object(check_part + "_part")
            part[check_part].set_state(has_part[check_part])

        # Only show mount checks that apply to current system.
        part["boot_efi"].hide()
        part["boot"].hide()
        part["swap"].hide()

        if is_uefi:
            part["boot_efi"].show()
        elif self.lv_partitions and not is_uefi:
            part["boot"].show()
        elif need_swap:
            part["swap"].show()

        # Be sure to just call get_devices once
        if self.disks is None:
            self.disks = pm.get_devices()

        # Check mount points and filesystems
        for part_path in self.stage_opts:
            (is_new, lbl, mnt, fs, fmt) = self.stage_opts[part_path]
            if mnt == "/":
                # Don't allow vfat as / filesystem, it will not work!
                # Don't allow ntfs as / filesystem, this is stupid!
                if "fat" not in fs and "ntfs" not in fs:
                    has_part["root"] = True
                    part["root"].set_state(True)
            # /boot or /boot/efi
            if mnt == "/boot":
                if is_uefi and "fat" in fs:
                    # Only fat partitions
                    has_part["boot_efi"] = True
                    part["boot_efi"].set_state(True)
                else:
                    if "f2fs" not in fs and "btrfs" not in fs and self.lv_partitions:
                        has_part["boot"] = True
                        # Not sure if this was an oversight or intended?
                        part["boot"].set_state(True)
            if mnt == "swap":
                has_part["swap"] = True
                part["swap"].set_state(True)

        if is_uefi:
            check_ok = has_part["root"] and has_part["boot_efi"]
        elif self.lv_partitions and not is_uefi:
            check_ok = has_part["root"] and has_part["boot"]
        else:
            check_ok = has_part["root"]

        if need_swap:
            check_ok = check_ok and has_part["swap"]

        self.forward_button.set_sensitive(check_ok)

    def get_changes(self):
        """ Grab all changes for confirmation """
        changelist = []
        # Store values as (path, create?, label?, format?)
        if self.lv_partitions:
            for e in self.lv_partitions:
                relabel = 'No'
                fmt = 'No'
                createme = 'No'
                mnt = ''

                if self.gen_partition_uid(path=e) in self.stage_opts:
                    (is_new, lbl, mnt, fs, fmt) = self.stage_opts[self.gen_partition_uid(path=e)]
                    if fmt:
                        fmt = 'Yes'
                    else:
                        fmt = 'No'
                    # Advanced method formats root by default
                    # https://github.com/Antergos/Cnchi/issues/8
                    if mnt == "/":
                        fmt = 'Yes'
                    if is_new:
                        if lbl != "":
                            relabel = 'Yes'
                        # Avoid extended and bios-gpt-boot partitions getting fmt flag true on new creation
                        if fs != "extended" and fs != "bios-gpt-boot":
                            fmt = 'Yes'
                        createme = 'Yes'
                    else:
                        if e in self.orig_label_dic:
                            if self.orig_label_dic[e] == lbl:
                                relabel = 'No'
                            else:
                                relabel = 'Yes'
                        createme = 'No'
                else:
                    relabel = 'No'
                    fmt = 'No'
                    createme = 'No'
                    mnt = ''

            if createme == 'Yes' or relabel == 'Yes' or fmt == 'Yes' or mnt:
                changelist.append((e, createme, relabel, fmt, mnt))

        if self.disks:
            for disk_path in self.disks:
                (disk, result) = self.disks[disk_path]
                partitions = pm.get_partitions(disk)
                for partition_path in partitions:
                    # Init vars
                    relabel = 'No'
                    fmt = 'No'
                    createme = 'No'
                    mnt = ''

                    if self.gen_partition_uid(path=partition_path) in self.stage_opts:
                        if disk.device.busy:
                            # Check if there's some mounted partition
                            mounted = False
                            if pm.check_mounted(partitions[partition_path]):
                                mount_point, fs_type, writable = self.get_mount_point(partition_path)
                                #if "swap" in fs_type:
                                swap_partition = self.get_swap_partition(partition_path)
                                if swap_partition == partition_path:
                                    msg = _("%s is mounted as swap.\nTo continue it has to be unmounted.\n"
                                        "Click Yes to unmount, or No to return\n") % partition_path
                                    mounted = True
                                elif len(mount_point) > 0:
                                    msg = _("%s is mounted in '%s'.\nTo continue it has to be unmounted.\n"
                                        "Click Yes to unmount, or No to return\n") % (partition_path, mount_point)
                                    mounted = True
                                if "install" in mount_point:
                                    # If we're recovering from a failed/stopped install, there'll be
                                    # some mounted directories. Unmount them without asking.
                                    subp = subprocess.Popen(['umount', '-l', partition_path], stdout=subprocess.PIPE)
                                    logging.debug(_("%s unmounted"), mount_point)
                                elif mounted:
                                    response = show.question(msg)
                                    if response != Gtk.ResponseType.YES:
                                        # User doesn't want to unmount, we can't go on.
                                        return []
                                    else:
                                        # unmount it!
                                        if swap_partition == partition_path:
                                            subp = subprocess.Popen(['sh', '-c', 'swapoff %s'
                                                                    % partition_path], stdout=subprocess.PIPE)
                                            logging.debug(_("Swap partition %s unmounted"), partition_path)
                                        else:
                                            subp = subprocess.Popen(['umount', partition_path], stdout=subprocess.PIPE)
                                            logging.debug(_("%s unmounted"), mount_point)
                                else:
                                    msg = _("%s shows as mounted (busy) but it has no mount point")
                                    logging.warning(msg, partition_path)

                        (is_new, lbl, mnt, fs, fmt) = self.stage_opts[self.gen_partition_uid(path=partition_path)]

                        if fmt:
                            fmt = 'Yes'
                        else:
                            fmt = 'No'

                        # Advanced method formats root by default
                        # https://github.com/Antergos/Cnchi/issues/8
                        if mnt == "/":
                            fmt = 'Yes'

                        if is_new:
                            if lbl != "":
                                relabel = 'Yes'
                            # Avoid extended and bios-gpt-boot partitions getting fmt flag true on new creation
                            if fs != "extended" and fs != "bios-gpt-boot":
                                fmt = 'Yes'
                            createme = 'Yes'
                        else:
                            if partition_path in self.orig_label_dic:
                                if self.orig_label_dic[partition_path] == lbl:
                                    relabel = 'No'
                                else:
                                    relabel = 'Yes'
                            createme = 'No'
                    else:
                        relabel = 'No'
                        fmt = 'No'
                        createme = 'No'
                        mnt = ''

                    if createme == 'Yes' or relabel == 'Yes' or fmt == 'Yes' or mnt:
                        changelist.append((partition_path, createme, relabel, fmt, mnt))
                        msg = "In get_changes(), added to changelist: path[%s] createme[%s] relabel[%s] fmt[%s] mnt[%s]"
                        logging.debug(msg, partition_path, createme, relabel, fmt, mnt)

            return changelist

    def show_changes(self, changelist):
        """ Show all changes to the user before doing anything, just in case. """
        if self.show_changes_grid is not None:
            self.show_changes_grid.destroy()

        vbox = self.ui.get_object("dialog-vbox6")
        grid = Gtk.Grid()
        vbox.pack_start(grid, True, True, 2)
        self.show_changes_grid = grid

        margin = 8

        bold = "<b>%s</b>"
        y = 0

        self.to_be_deleted.sort()

        # First, show partitions that will be deleted
        for ea in self.to_be_deleted:
            lbl = Gtk.Label(_("Partition %s will be deleted") % ea, margin=margin)
            lbl.set_alignment(0, 0.5)
            grid.attach(lbl, 0, y, 4, 1)
            y += 1

        if changelist != []:
            # Partitions that will be modified (header)
            labels = [_("Partition"), _("New"), _("Relabel"), _("Format"), _("Mount")]

            x = 0
            for txt in labels:
                lbl = Gtk.Label(margin=margin)
                lbl.set_markup(bold % txt)
                grid.attach(lbl, x, y, 1, 1)
                x += 1

            y += 1

            # Partitions that will be modified
            for ea in changelist:
                x = 0
                for txt in ea:
                    lbl = Gtk.Label(txt, margin=margin)
                    grid.attach(lbl, x, y, 1, 1)
                    x += 1
                y += 1

        changelist_dialog = self.ui.get_object("changelist_dialog")
        changelist_dialog.set_title(_('We will make changes to partitions on these disks:'))
        changelist_dialog.show_all()
        response = changelist_dialog.run()
        changelist_dialog.hide()
        while Gtk.events_pending():
            Gtk.main_iteration()

        return response

    def store_values(self):
        """ The user clicks 'Install now!' """
        changelist = self.get_changes()
        if changelist == []:
            # Something wrong has happened or nothing to change
            return False

        changelist.sort()

        response = self.show_changes(changelist)
        if response == Gtk.ResponseType.CANCEL:
            return False

        watch = Gdk.Cursor(Gdk.CursorType.WATCH)
        gdk_window = self.get_root_window()
        gdk_window.set_cursor(watch)

        self.create_staged_partitions()
        self.start_installation()

        arrow = Gdk.Cursor(Gdk.CursorType.ARROW)
        gdk_window.set_cursor(arrow)

        # Restore "Next" button's text
        self.forward_button.set_label("gtk-go-forward")
        self.forward_button.set_use_stock(True)
        return True

    def get_prev_page(self):
        """ Tell which one is our previous page (in our case installation_ask) """
        return _prev_page

    def get_next_page(self):
        """ Tell which one is our next page """
        return _next_page

    def create_staged_partitions(self):
        """ Create staged partitions """
        # Sometimes a swap partition can still be active at this point
        subp = subprocess.Popen(['sh', '-c', 'swapoff -a'], stdout=subprocess.PIPE)
        
        partitions = {}
        if self.disks is not None:
            for disk_path in self.disks:
                (disk, result) = self.disks[disk_path]
                # Only commit changes to disks we've changed!
                if disk_path in self.disks_changed:
                    pm.finalize_changes(disk)
                    logging.info(_("Finished saving changes in %s") % disk_path)
                # Now that partitions are created, set fs and label
                partitions.update(pm.get_partitions(disk))
            apartitions = list(partitions) + self.lv_partitions
            if True:
                noboot = True
                efiboot = False
                # Check if a boot partition exists
                for allopts in self.stage_opts:
                    if self.stage_opts[allopts][2] == '/boot':
                        noboot = False
                    if self.stage_opts[allopts][2] == '/boot/efi':
                        noboot = False
                        efiboot = True

                for partition_path in apartitions:
                    # Get label, mount point and filesystem of staged partitions
                    uid = self.gen_partition_uid(path=partition_path)
                    if uid in self.stage_opts:
                        (is_new, lbl, mnt, fisy, fmt) = self.stage_opts[uid]
                        # FIX: Do not label or format extended or bios-gpt-boot partitions
                        if fisy == "extended" or fisy == "bios-gpt-boot":
                            continue
                        if len(lbl) > 0:
                            logging.info(_("Creating new %s filesystem in %s labeled %s") % (fisy, partition_path, lbl))
                        else:
                            logging.info(_("Creating new %s filesystem in %s") % (fisy, partition_path))

                        if ((mnt == '/' and noboot) or (mnt == '/boot')) and ('/dev/mapper' not in partition_path):
                            if not pm.get_flag(partitions[partition_path], pm.PED_PARTITION_BOOT):
                                if self.grub_device or self.grub_device is not None:
                                    (res, err) = pm.set_flag(pm.PED_PARTITION_BOOT, partitions[partition_path])
                            if not self.testing:
                                pm.finalize_changes(partitions[partition_path].disk)
                        if "/dev/mapper" in partition_path:
                            pvs = lvm.get_lvm_partitions()
                            vgname = partition_path.split("/")[-1]
                            vgname = vgname.split('-')[0]
                            if (mnt == '/' and noboot) or (mnt == '/boot'):
                                self.blvm = True
                                for ee in pvs[vgname]:
                                    #print(partitions)
                                    if not pm.get_flag(partitions[ee], pm.PED_PARTITION_BOOT):
                                        if self.grub_device or self.grub_device is not None:
                                            x = pm.set_flag(pm.PED_PARTITION_BOOT, partitions[ee])
                                if not self.testing:
                                    pm.finalize_changes(partitions[ee].disk)

                        #if "swap" in fisy:
                        #    (res, err) = pm.set_flag(pm.PED_PARTITION_SWAP, partitions[partition_path])
                        #    pm.finalize_changes(partitions[partition_path].disk)

                        # Only format if they want formatting
                        if fmt:
                            # All of fs module takes paths, not partition objs
                            if not self.testing:
                                # Create filesystem using mkfs
                                (error, msg) = fs.create_fs(partition_path, fisy, lbl)
                                if error == 0:
                                    logging.info(msg)
                                else:
                                    txt = _("Couldn't format partition '%s' with label '%s' as '%s'") % (partition_path, lbl, fisy)
                                    logging.error(txt)
                                    logging.error(msg)
                                    show.error(txt)
                        elif partition_path in self.orig_label_dic:
                            if self.orig_label_dic[partition_path] != lbl:
                                if not self.testing:
                                    fs.label_fs(fisy, partition_path, lbl)

    def start_installation(self):
        """ Start installation process """
        fs_devices = {}
        mount_devices = {}
        for disk_path in self.disks:
            (disk, result) = self.disks[disk_path]
            partitions = pm.get_partitions(disk)
            self.all_partitions.append(partitions)
            partition_list = pm.order_partitions(partitions)
            for ppath in self.lv_partitions:
                uid = self.gen_partition_uid(path=ppath)
                if uid in self.stage_opts:
                    (is_new, label, mount_point, fs_type, fmt_active) = self.stage_opts[uid]
                    mount_devices[mount_point] = ppath
                    fs_devices[ppath] = fs_type
            for partition_path in partition_list:
                p = partitions[partition_path]
                uid = self.gen_partition_uid(p=p)
                if uid in self.stage_opts:
                    (is_new, label, mount_point, fs_type, fmt_active) = self.stage_opts[uid]
                    # Do not mount extended or bios-gpt-boot partitions
                    if fs_type == "extended" or fs_type == "bios-gpt-boot":
                        continue
                    mount_devices[mount_point] = partition_path
                    fs_devices[partition_path] = fs_type

        checkbox = self.ui.get_object("grub_device_check")
        if checkbox.get_active() is False:
            self.settings.set('install_bootloader', False)
            logging.warning(_("Cnchi will not install any boot loader"))
        else:
            self.settings.set('install_bootloader', True)
            self.settings.set('bootloader_device', self.grub_device)
            if os.path.exists("/sys/firmware/efi/systab"):
                bootloader_type = "UEFI_x86_64"
            else:
                bootloader_type = "GRUB2"
            self.settings.set('bootloader_type', bootloader_type)
            logging.info(_("Antergos will install the bootloader of type %s in %s"), bootloader_type, self.grub_device)

        if not self.testing:
            self.process = installation_process.InstallationProcess(
                        self.settings,
                        self.callback_queue,
                        mount_devices,
                        fs_devices,
                        self.ssd,
                        self.alternate_package_list,
                        self.blvm)

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
    run('InstallationAdvanced')
