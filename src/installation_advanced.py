#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  installation_advanced.py
#  
#  Copyright 2013 Cinnarch
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
#  
#  Cinnarch Team:
#   Alex Filgueira (faidoc) <alexfilgueira.cinnarch.com>
#   Raúl Granados (pollitux) <raulgranados.cinnarch.com>
#   Gustau Castells (karasu) <karasu.cinnarch.com>
#   Kirill Omelchenko (omelcheck) <omelchek.cinnarch.com>
#   Marc Miralles (arcnexus) <arcnexus.cinnarch.com>
#   Alex Skinner (skinner) <skinner.cinnarch.com>

import xml.etree.ElementTree as etree

from gi.repository import Gtk
import subprocess
import gettext
import sys
import os
import log
import misc

# Insert the src/parted directory at the front of the path.
base_dir = os.path.dirname(__file__) or '.'
parted_dir = os.path.join(base_dir, 'parted')
sys.path.insert(0, parted_dir)

import partition_module as pm
import fs_module as fs
import used_space
import installation_thread
import show_message as show

_next_page = "timezone"
_prev_page = "installation_ask"

class InstallationAdvanced(Gtk.Box):

    def __init__(self, params):
        ## Store class parameters
        self.title = params['title']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        self.callback_queue = params['callback_queue']
        self.settings = params['settings']

        self.disks_changed = []
        self.my_first_time = True
        self.orig_label_dic = {}        
        self.orig_part_dic = {}

        #stage_opts holds info about newly created partitions
        #format is tuple (label, mountpoint, fs(text), Format)
        #see its usage in listing, creating, and deleting partitions
        self.stage_opts = {}
        self.used_dic = {}

        #hold deleted partitions that exist now
        self.to_be_deleted = []

        ## Call base class
        super().__init__()

        ## Get UI items
        self.ui = Gtk.Builder()
        ui_file = os.path.join(self.ui_dir, "installation_advanced.ui")
        self.ui.add_from_file(ui_file)

        ## Connect UI signals
        self.ui.connect_signals(self)

        ## Load create and edit partition dialogs
        self.create_partition_dialog = self.ui.get_object('create_partition_dialog')
        self.edit_partition_dialog = self.ui.get_object('edit_partition_dialog')

        ## Initialize our create partition dialog filesystems' combo.
        use_combo = self.ui.get_object('partition_use_combo')
        use_combo.remove_all()
        for fs_name in sorted(fs._names):
            use_combo.append_text(fs_name)
        use_combo.set_wrap_width(2)

        ## Initialize our edit partition dialog filesystems' combo.
        use_combo = self.ui.get_object('partition_use_combo2')
        use_combo.remove_all()
        for fs_name in sorted(fs._names):
            use_combo.append_text(fs_name)
        use_combo.set_wrap_width(2)

        ## Initialize partition_types_combo
        combo = self.ui.get_object('partition_types_combo')
        combo.remove_all()
        combo.append_text("msdos (aka MBR)")
        combo.append_text("GUID Partition Table (GPT)")
        ## Automatically select first entry
        self.select_first_combobox_item(combo)

        ## Initialize our create and edit partition dialog mount points' combo.
        mount_combos = []
        mount_combos.append(self.ui.get_object('partition_mount_combo'))
        mount_combos.append(self.ui.get_object('partition_mount_combo2'))
        
        for combo in mount_combos:
            combo.remove_all()
            for mp in sorted(fs._common_mount_points):
                combo.append_text(mp)

        ## We will store our devices here
        self.disks = None
        
        ## we will store if our device is SSD or not
        self.ssd = {}

        self.grub_device_entry = self.ui.get_object('grub_device_entry')      
        self.grub_devices = dict()
        self.grub_device = {}

        ## Initialise our partition list treeview
        self.partition_list = self.ui.get_object('partition_list_treeview')
        self.partition_list_store = None
        self.prepare_partition_list()

        ## Connect changing selection in the partition list treeview
        select = self.partition_list.get_selection()
        select.connect("changed", self.on_partition_list_treeview_selection_changed)

        self.show_changes_grid = None
        
        ## Add ourselves to the parent class
        super().add(self.ui.get_object("installation_advanced"))

    ## Function to generate uid by partition object or path
    def gen_partition_uid(self, p=None, path=None):
        if path and not p:
            if "free" in path:
                return None
            for zz in self.all_partitions:
                for yy in zz:
                    if zz[yy].path == path:
                        p = zz[yy]
        try:
            dev = p.disk.device.path
        except:
            dev = 'thinking'
        if p:
            ends = p.geometry.end
            starts = p.geometry.start
        else:
            ends = 'none'
            starts = 'none'
        uid = dev + str(starts) + str(ends)
        return uid

    ## Activates/deactivates our buttons depending on which is selected in the
    ## partition treeview
    def check_buttons(self, selection):
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
        if tree_iter != None:
            path = model[tree_iter][0]
            if path == _("free space"):
                button_new.set_sensitive(True)
            else:
                disks = pm.get_devices()
                if not path in disks:
                    ## A partition is selected
                    for i in self.all_partitions:
                        if path in i:
                            diskobj = i[path].disk.device.path
                    if diskobj and model[tree_iter][1] == 'extended' and \
                     self.diskdic[diskobj]['has_logical']:
                        button_delete.set_sensitive(False)
                        button_edit.set_sensitive(False)
                    else:
                        button_delete.set_sensitive(True)    
                        button_edit.set_sensitive(True)
                else:
                    ## A drive (disk) is selected
                    button_new_label.set_sensitive(True)

    ## Get all devices where we can put our Grub boot code
    ## Not using partitions (but we'll have to)
    def fill_grub_device_entry(self):       
        self.grub_device_entry.remove_all()
        self.grub_devices.clear()
        
        ## Just call get_devices once
        if self.disks == None:
            self.disks = pm.get_devices()

        for path in sorted(self.disks):
            disk = self.disks[path]
            if disk is not None:
                dev = disk.device
                ## avoid cdrom and any raid, lvm volumes or encryptfs
                if not dev.path.startswith("/dev/sr") and \
                   not dev.path.startswith("/dev/mapper"):
                    ## Hard drives measure themselves assuming kilo=1000, mega=1mil, etc
                    size_in_gigabytes = int((dev.length * dev.sectorSize) / 1000000000)
                    line = '{0} [{1} GB] ({2})'.format(dev.model, size_in_gigabytes, dev.path)
                    self.grub_device_entry.append_text(line)
                    self.grub_devices[line] = dev.path
                    self.grub_device = self.grub_devices[line]
        
        ## Automatically select first entry
        self.select_first_combobox_item(self.grub_device_entry)

    ## Automatically select first entry
    def select_first_combobox_item(self, combobox):
        tree_model = combobox.get_model()
        tree_iter = tree_model.get_iter_first()
        combobox.set_active_iter(tree_iter)

    ## Get new selected GRUB device
    def on_select_grub_drive_changed(self, widget):
        line = self.grub_device_entry.get_active_text()
        if line != None:
            self.grub_device = self.grub_devices[line]

    ## Create columns for our treeview
    def prepare_partition_list(self):
        
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

        col = Gtk.TreeViewColumn(_("Solid State Drive (SSD)"), ssd_toggle, active=12, visible=13, sensitive=14)
        self.partition_list.append_column(col)   

    ## Helper function to get a disk/partition size in human format
    def get_size(self, length, sectorSize):
        size = length * sectorSize
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

    ## Fill the partition list with all the data.
    def fill_partition_list(self):
        self.diskdic = {}
        self.all_partitions = []
        ## We will store our data model in 'partition_list_store'
        if self.partition_list_store != None:
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
            Gtk.TreeStore(str, str, str, str, bool, bool, str, str, str, \
            str, int, bool, bool, bool, bool)
            
        ## Be sure to call get_devices once
        if self.disks == None:
            self.disks = pm.get_devices()

        self.diskdic['mounts'] = []

        ## Here we fill our model
        for disk_path in sorted(self.disks):
            if '/dev/mapper/arch_' in disk_path:
                continue
            
            self.diskdic[disk_path] = {}
            self.diskdic[disk_path]['has_logical'] = False
            self.diskdic[disk_path]['has_extended'] = False           

            if disk_path not in self.ssd:
                self.ssd[disk_path] = fs.is_ssd(disk_path)
            
            is_ssd = self.ssd[disk_path]
            
            disk = self.disks[disk_path]
            
            if disk is None:
                # Maybe disk without a partition table?
                row = [disk_path, "", "", "", False, False, "", "", "", \
                    "", 0, False, is_ssd, False, False]
                self.partition_list_store.append(None, row)
            else:
                dev = disk.device

                ## Get device size
                size_txt = self.get_size(dev.length, dev.sectorSize)
                
                row = [dev.path, "", "", "", False, False, size_txt, "", \
                    "", "", 0, False, is_ssd, True, True]
                disk_parent = self.partition_list_store.append(None, row)
                
                parent = disk_parent

                # Create a list of partitions for this device (/dev/sda for example)
                partitions = pm.get_partitions(disk)
                self.all_partitions.append(partitions)
                partition_list = pm.order_partitions(partitions)

                for partition_path in partition_list:
                    ## Get partition size
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
                    
                    ## Get file system
                    if p.fileSystem and p.fileSystem.type:
                        fs_type = p.fileSystem.type
                    else:
                        #kludge, btrfs not being detected...
                        if 'free' not in partition_path:
                            uid = self.gen_partition_uid(p=p)
                            if uid not in self.stage_opts:
                                if used_space.is_btrfs(p.path):
                                    fs_type = 'btrfs'
                            else:
                                fs_type = '?'
                        else:
                            fs_type = _("none")
                    
                    # Commenting out.  Nothing should be mounted...
                    ## Get mount point
                    #if pm.check_mounted(p) and not "swap" in fs_type:
                    #    mount_point, notused_fs, notused_writable = self.get_mount_point(p.path)
                    
                    if p.type == pm.PARTITION_EXTENDED:
                        formatable = False
                        self.diskdic[disk_path]['has_extended'] = True
                    elif p.type == pm.PARTITION_LOGICAL:
                        formatable = True
                        self.diskdic[disk_path]['has_logical'] = True
                    
                    if p.type in (pm.PARTITION_FREESPACE,
                                  pm.PARTITION_FREESPACE_EXTENDED):
                        ## Show 'free space' instead of /dev/sda-1    
                        path = _("free space")
                        formatable = False
                    else:                        
                        ## Get partition flags
                        flags = pm.get_flags(p)
                    
                    uid = self.gen_partition_uid(p=p)
                    if uid in self.stage_opts:
                        (is_new, label, mount_point, fs_type, fmt_active) = self.stage_opts[uid]
                        fmt_enable = not is_new
                    else:
                        fmt_enable = True
                        if _("free space") not in path:
                            if self.my_first_time:
                                if mount_point:
                                    used = pm.get_used_space(p)
                                else:
                                    used = self.get_size(used_space.get_used_space(partition_path, fs_type) * p.geometry.length, dev.sectorSize)
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
                        ## Show 'extended' in file system type column
                        fs_type = _("extended")

                    ## do not show swap version, only the 'swap' word
                    if 'swap' in fs_type:
                        fs_type = 'swap'

                    row = [path, fs_type, mount_point, label, fmt_active, \
                           formatable, size_txt, used, partition_path, \
                           "", p.type, fmt_enable, False, False, False]
            
                    if p.type in (pm.PARTITION_LOGICAL,
                                  pm.PARTITION_FREESPACE_EXTENDED):
                        parent = myparent
                    else:
                        parent = disk_parent
                    
                    tree_iter = self.partition_list_store.append(parent, row)

                    ## If we're an extended partition, all the logical
                    ## partitions that follow will be shown as children
                    ## of this one
                    if p.type == pm.PARTITION_EXTENDED:
                        myparent = tree_iter 
                    
                    if self.my_first_time:
                        self.orig_part_dic[p.path] = self.gen_partition_uid(p)
                        self.orig_label_dic[p.path] = label
        
        self.my_first_time = False
        # assign our new model to our treeview
        self.partition_list.set_model(self.partition_list_store)
        self.partition_list.expand_all()
        
        # check if correct mount points are already defined, so we
        # can proceed with installation
        self.check_mount_points()

    ## Mark a partition to be formatted
    def on_format_cell_toggled(self, widget, path):
        #selected_path = Gtk.TreePath(path)
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

    ## Mark disk as ssd
    def on_ssd_cell_toggled(self, widget, path):
        # ssd cell
        self.partition_list_store[path][12] = not self.partition_list_store[path][12]
        disk_path = self.partition_list_store[path][0]
        self.ssd[disk_path] = self.partition_list_store[path][12]

    ## The user wants to edit a partition
    def on_partition_list_edit_activate(self, button):
        selection = self.partition_list.get_selection()
        
        if not selection:
            return
            
        model, tree_iter = selection.get_selected()

        if tree_iter == None:
            return
            
        ## Get necessary row data
        row = model[tree_iter]

        fs = row[1]
        mount_point = row[2]
        label = row[3]
        fmt = row[4]
        partition_path = row[8]
        fmtable = row[11]
        
        # set fs in dialog combobox
        use_combo = self.ui.get_object('partition_use_combo2')
        use_combo_model = use_combo.get_model()
        use_combo_iter = use_combo_model.get_iter_first()

        while use_combo_iter != None:
            use_combo_row = use_combo_model[use_combo_iter]
            if use_combo_row[0] and use_combo_row[0] in fs:
                use_combo.set_active_iter(use_combo_iter)
                use_combo_iter = None
            else:
                use_combo_iter = use_combo_model.iter_next(use_combo_iter)

        # set mount point in dialog combobox
        mount_combo_entry = self.ui.get_object('combobox-entry2')
        mount_combo_entry.set_text(mount_point)
        
        # set label entry
        label_entry = self.ui.get_object('partition_label_entry2')
        label_entry.set_text(label)
        
        # must format?
        format_check = self.ui.get_object('partition_format_check')
        format_check.set_active(fmt)
        format_check.set_sensitive(fmtable)

        # Be sure to just call get_devices once
        if self.disks == None:
            self.disks = pm.get_devices()

        # Get disk_path and disk
        disk_path = self.get_disk_path_from_selection(model, tree_iter)    
        disk = self.disks[disk_path]

        # show edit partition dialog
        response = self.edit_partition_dialog.run()
        
        if response == Gtk.ResponseType.OK:
            mylabel = label_entry.get_text()
            mymount = mount_combo_entry.get_text().strip()

            if mymount in self.diskdic['mounts'] and mymount != mount_point:
                show.warning(_('Cannot use same mount twice...'))
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

                # Should we force a format if the partition is new?

                self.stage_opts[uid] = (is_new, mylabel, mymount, myfmt, fmtop)
            
        self.edit_partition_dialog.hide()

        ## Update the partition list treeview
        self.fill_partition_list()

    ## This returns the disk path where the selected partition is in
    def get_disk_path_from_selection(self, model, tree_iter):
        if tree_iter != None and model != None:
            row = model[tree_iter]
            partition_path = row[8]
            
            ## Get partition type from the user selection
            part_type = row[10]
            
            # Get our parent drive
            parent_iter = model.iter_parent(tree_iter)

            if part_type == pm.PARTITION_LOGICAL:
                ## If we are a logical partition, our drive won't be our father
                ## but our grandpa (we have to skip the extended partition we're in)
                parent_iter = model.iter_parent(parent_iter)

            return model[parent_iter][0]
        else:
            return None

    ## Delete partition
    def on_partition_list_delete_activate(self, button):
        selection = self.partition_list.get_selection() 
        if not selection:
            return
            
        model, tree_iter = selection.get_selected()

        if tree_iter == None:
            return
        am_new = False
        ## Get row data
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

        log.debug("You will delete from disk [%s] partition [%s]" % (disk_path, partition_path))

        # Be sure to just call get_devices once
        if self.disks == None:
            self.disks = pm.get_devices()

        disk = self.disks[disk_path]

        partitions = pm.get_partitions(disk)
        
        part = partitions[partition_path]
        if (disk.device.path, part.geometry.start) in self.used_dic:
            del self.used_dic[(disk.device.path, part.geometry.start)]
       
        ## Before delete the partition, check if it's already mounted
        if pm.check_mounted(part):
            ## We unmount the partition. Should we ask first?
            log.debug("Unmounting %s..." % part.path)
            subp = subprocess.Popen(['umount', part.path], stdout=subprocess.PIPE)

        ## Is it worth to show some warning message here?
        ## No, created delete list as part of confirmation screen.
        pm.delete_partition(disk, part)
        
        ## Update the partition list treeview
        self.fill_partition_list()

    def get_mount_point(self, partition_path):
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

    ## Add a new partition
    def on_partition_list_new_activate(self, button):
        selection = self.partition_list.get_selection()
             
        if not selection:
            return

        #assume it will be formatted, unless it's extended
        formatme = True      
        model, tree_iter = selection.get_selected()

        if tree_iter == None:
            return
            
        ## Get necessary row data
        row = model[tree_iter]

        ## Get partition type from the user selection
        part_type = row[10]

        ## Check that the user has selected a free space row.
        if part_type not in (pm.PARTITION_FREESPACE,
                             pm.PARTITION_FREESPACE_EXTENDED):
            return

        size_available = row[6]
        partition_path = row[8]

        # Get our parent drive
        parent_iter = model.iter_parent(tree_iter)
        
        parent_part_type = model[parent_iter][10]
 
        if parent_part_type == pm.PARTITION_EXTENDED:
            ## We're creating a partition inside an already created extended
            ## partition. Our drive won't be our father but our grandpa
            ## (we have to skip the extended partition we're in)
            parent_iter = model.iter_parent(parent_iter)
            isbase = False
        else:
            isbase = True
            
        disk_path = model[parent_iter][0]
        self.disks_changed.append(disk_path)
        # Be sure to just call get_devices once
        if self.disks == None:
            self.disks = pm.get_devices()
                
        disk = self.disks[disk_path]
        dev = disk.device
            
        partitions = pm.get_partitions(disk)
        p = partitions[partition_path]
        
        #added extended, moving extended details up here

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

        ## Get how many primary partitions are already created on disk
        primary_count = disk.primaryPartitionCount
        if primary_count >= disk.maxPrimaryPartitionCount:
            ## No room left for another primary partition
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

        #use
        use_combo = self.ui.get_object('partition_use_combo')
        use_combo.set_active(3) 

        # mount combo entry
        mount_combo_entry = self.ui.get_object('combobox-entry')
        mount_combo_entry.set_text("")

        # finally, show the create partition dialog

        response = self.create_partition_dialog.run()
        if response == Gtk.ResponseType.OK:
            mylabel = label_entry.get_text()
            mymount = mount_combo_entry.get_text().strip()
            if mymount in self.diskdic['mounts']:
                show.warning(_('Cannot use same mount twice...'))
            else:
                if mymount:         
                    self.diskdic['mounts'].append(mymount)       
                myfmt = use_combo.get_active_text()
                if myfmt == None:
                    myfmt = ""
                # Get selected size
                size = int(size_spin.get_value())

                beg_var = beginning_radio.get_active()

                start_sector = p.geometry.start
                end_sector = p.geometry.end
                geometry = pm.geom_builder(disk, start_sector, 
                                           end_sector, size, beg_var)

                # user wants to create an extended, logical or primary partition
                if primary_radio.get_active():
                    log.debug(_("Creating primary partition"))
                    pm.create_partition(disk, pm.PARTITION_PRIMARY, geometry)
                elif extended_radio.get_active():
                    #No mounting extended partitions...
                    if mymount:
                        self.diskdic['mounts'].remove(mymount)
                        mymount = ''   
                    #No labeling either..
                    mylabel = ''
                    myfmt = ''
                    formatme = False 
                    log.debug(_("Creating extended partition"))
                    pm.create_partition(disk, pm.PARTITION_EXTENDED, geometry)
                elif logical_radio.get_active():
                    logical_count = len(list(disk.getLogicalPartitions()))
                    max_logicals = disk.getMaxLogicalPartitions()        
                    if logical_count < max_logicals:
                        log.debug(_("Creating logical partition"))
                        # which geometry should we use here?
                        pm.create_partition(disk, pm.PARTITION_LOGICAL, geometry)
                
                # Store stage partition info in self.stage_opts
                old_parts = []
                for y in self.all_partitions:
                    for z in y:
                        old_parts.append(z)
                partitions = pm.get_partitions(disk)
                for e in partitions:
                    if e not in old_parts:
                        #Changing back to disabling format box.  
                        self.stage_opts[self.gen_partition_uid(p=partitions[e])] = (True, mylabel, mymount, myfmt, True)
                ## Update partition list treeview
                self.fill_partition_list()

        self.create_partition_dialog.hide()

    def on_partition_list_undo_activate(self, button):
        ## To undo user changes, we simply reload all devices        
        self.disks = pm.get_devices()
        self.disks_changed = []

        ## Empty stage partitions' options
        self.stage_opts = {}
        
        ## Empty to be deleted partitions list
        self.to_be_deleted = []
        
        ## refresh our partition treeview
        self.fill_partition_list()

    ## Selection changed, call check_buttons to update them
    def on_partition_list_treeview_selection_changed(self, selection):
        self.check_buttons(selection)
        return False

    ## Called when clicked on the partition list treeview
    ## Inherited from Ubiquity. Not doing anything here (return false to not stop the chain of events)
    def on_partition_list_treeview_button_press_event(self, widget, event):
        return False

    ## Called when a key is pressed when the partition list treeview has focus
    ## Inherited from Ubiquity. Not doing anything here (return false to not stop the chain of events)
    def on_partition_list_treeview_key_press_event(self, widget, event):
        return False

    def on_partition_list_treeview_row_activated(self, path, column, user_data):
        button_edit = self.ui.get_object('partition_button_edit')
        button_new = self.ui.get_object('partition_button_new')

        if button_edit.get_sensitive():
            self.on_partition_list_edit_activate(None)
        elif button_new.get_sensitive():
            self.on_partition_list_new_activate(None)
            
        return False

    ## Inherited from Ubiquity. Not doing anything here (return false to not stop the chain of events)
    def on_partition_list_treeview_popup_menu(self, widget):
        return False

    ## As the installer language can change anytime the user changes it, we have
    ## to "retranslate" all our widgets calling this function
    def translate_ui(self):
        txt = _("Advanced installation mode")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.title.set_markup(txt)
        
        txt = _("Device for boot loader installation:")
        txt = "<span weight='bold' size='small'>%s</span>" % txt
        label = self.ui.get_object('grub_device_label')
        label.set_markup(txt)
        
        #txt = _("TODO: Here goes a warning message")
        #txt = "<span weight='bold'>%s</span>" % txt
        #label = self.ui.get_object('part_advanced_warning_message')
        #label.set_markup(txt)
        
        txt = _("New partition table")
        button = self.ui.get_object('partition_button_new_label')
        button.set_label(txt)
        
        #txt = _("Revert")
        #button = self.ui.get_object('partition_button_undo')
        #button.set_label(txt)
        
        txt = _("Change...")
        button = self.ui.get_object('partition_button_edit')
        button.set_label(txt)

        ## Translate dialog "Create partition"
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
        
        txt = _("Use as:")
        label = self.ui.get_object('partition_use_label')
        label.set_markup(txt)
        
        txt = _("Mount point:")
        label = self.ui.get_object('partition_mount_label')
        label.set_markup(txt)

        txt = _("Label (optional):")
        label = self.ui.get_object('partition_label_label')
        label.set_markup(txt)
        
        txt = _("Encryption options...")
        button = self.ui.get_object('partition_encryption_settings')
        button.set_label(txt)
        
        ## Translate dialog "Edit partition"
        txt = _("Use as:")
        label = self.ui.get_object('partition_use_label2')
        label.set_markup(txt)
        
        txt = _("Mount point:")
        label = self.ui.get_object('partition_mount_label2')
        label.set_markup(txt)

        txt = _("Label (optional):")
        label = self.ui.get_object('partition_label_label2')
        label.set_markup(txt)
        
        txt = _("Format:")
        label = self.ui.get_object('partition_format_label')
        label.set_markup(txt)
        
        ## Create disk partition table dialog
        txt = _("Partition table type:")
        label = self.ui.get_object('partition_type_label')
        label.set_markup(txt)

        dialog = self.ui.get_object("create_table_dialog")    
        dialog.set_title(_("Create partition table"))

        ## Change "Next" button text
        txt = _("Install now!")
        self.forward_button.set_label(txt)

        #self.ui.get_object('cancelbutton')
        #self.ui.get_object('partition_dialog_okbutton')

    ## Prepare our dialog to show/hide/activate/deactivate what's necessary
    def prepare(self, direction):
        self.fill_grub_device_entry()

        self.fill_partition_list() 

        self.translate_ui()
        self.show_all()

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
        button.set_sensitive(True)

    ## Create a new partition table
    def on_partition_list_new_label_activate(self, button):
        ## TODO: We should check first if there's any mounted partition (including swap)'
        
        selection = self.partition_list.get_selection()
        
        if not selection:
            return
            
        model, tree_iter = selection.get_selected()

        if tree_iter == None:
            return
            
        path = model[tree_iter][0]

        # Be sure to just call get_devices once
        if self.disks == None:
            self.disks = pm.get_devices()

        disk_sel = self.disks[path]
        
        dialog = self.ui.get_object("create_table_dialog")
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            combo = self.ui.get_object('partition_types_combo')
            line = combo.get_active_text()
            if line:
                ## by default, use msdos type
                ptype = 'msdos'

                if "GPT" in line:
                    ptype = 'gpt'

                log.debug(_("Creating a new partition table of type %s for disk %s") % (ptype, path))
                #remove debug, this doesn't actually do anything... 
                new_disk = pm.make_new_disk(path, ptype)
                self.disks[path] = new_disk
                
                self.fill_grub_device_entry()
                self.fill_partition_list()

        dialog.hide()

    def on_partition_list_lvm_activate(self, button):
        pass

    def check_mount_points(self):
        ## at least root (/) partition must be defined

        # TODO:

        check_ok = False

        # Be sure to just call get_devices once
        if self.disks == None:
            self.disks = pm.get_devices()

        # Commenting all this out...no device should be mounted now
        # except install media!
        '''
        for disk_path in self.disks:
            disk = self.disks[disk_path]
            if not disk:
                continue
            partitions = pm.get_partitions(disk)
            for partition_path in partitions:
                p = partitions[partition_path]
                if pm.check_mounted(p):
                    mount_point, fs, writable = self.get_mount_point(p.path)
                    if "/" in mount_point:
                        # don't allow vfat as / filesystem, it will not work!
                        # don't allow ntfs as / filesystem, this is stupid!
                        if "vfat" not in fs and "ntfs" not in fs:
                            check_ok = True
        '''
        
        for part_path in self.stage_opts:
            (is_new, lbl, mnt, fs, fmt) = self.stage_opts[part_path]
            if mnt == "/":
                # don't allow vfat as / filesystem, it will not work!
                # don't allow ntfs as / filesystem, this is stupid!
                if "fat" not in fs and "ntfs" not in fs:
                    check_ok = True

        self.forward_button.set_sensitive(check_ok)

    ## Grab all changes for confirmation
    def get_changes(self):
        changelist = []
        #store values as (path, create?, label?, format?)
        if self.disks:
            for disk_path in self.disks:
                disk = self.disks[disk_path]
                partitions = pm.get_partitions(disk)
                for partition_path in partitions:
                    if self.gen_partition_uid(path=partition_path) in self.stage_opts:
                        if disk.device.busy:
                            # There's some mounted partition
                            if pm.check_mounted(partitions[partition_path]):
                                mount_point, fs, writable = self.get_mount_point(partition_path)
                                msg = _("%s is mounted in '%s'.\nTo continue it has to be unmounted.\nClick Yes to unmount, or No to return\n") % (partition_path, mount_point)
                                response = show.question(msg)
                                if response != Gtk.ResponseType.YES:
                                    return []
                                else:
                                    # unmount it!
                                    subp = subprocess.Popen(['umount', partition_path], stdout=subprocess.PIPE)
                                
                        (is_new, lbl, mnt, fs, fmt) = self.stage_opts[self.gen_partition_uid(path=partition_path)]
                        
                        if fmt:
                            fmt = 'Yes'
                        else:
                            fmt = 'No'
                        if is_new:
                            relabel = 'Yes'
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
                    
            return changelist
    
    
    def show_changes(self, changelist):
        if self.show_changes_grid is not None:
            self.show_changes_grid.destroy()

        vbox = self.ui.get_object("dialog-vbox6")
        grid = Gtk.Grid()           
        vbox.pack_start(grid, True, True, 2)
        self.show_changes_grid = grid
            
        margin = 8
        
        bold = "<b>%s</b>"
        y = 0

        ## First, show partitions that will be deleted            
        for ea in self.to_be_deleted:
            lbl = Gtk.Label(_("Partition %s will be deleted") % ea, margin=margin)
            lbl.set_alignment(0, 0.5)
            grid.attach(lbl, 0, y, 4, 1)
            y += 1

        if changelist != []:
            ## Partitions that will be modified (header)        
            labels = [_("Partition"), _("New"), _("Relabel"), _("Format"), _("Mount")]

            x = 0
            for txt in labels:
                lbl = Gtk.Label(margin=margin)
                lbl.set_markup(bold % txt)
                grid.attach(lbl, x, y, 1, 1)
                x += 1        
            
            y += 1 
            
            ## Partitions that will be modified
            for ea in changelist:
                x = 0
                for txt in ea:
                    lbl = Gtk.Label(txt, margin=margin)
                    grid.attach(lbl, x, y, 1, 1)
                    x += 1
                y += 1
            
        changelist_dialog = self.ui.get_object("changelist_dialog")
        changelist_dialog.set_title(_('These disks will have partition actions:'))
        changelist_dialog.show_all()
        response = changelist_dialog.run()
        changelist_dialog.hide()
        
        return response

    ## The user clicks "Install now!"
    def store_values(self):
        changelist = self.get_changes()
        if changelist == []:
            # something wrong has happened or Nothing to change?
            return False
        
        response = self.show_changes(changelist)
        if response == Gtk.ResponseType.CANCEL:
            return False

        ## Create staged partitions 
        if self.disks != None:
            for disk_path in self.disks:
                disk = self.disks[disk_path]
                #only commit changes to disks we've changed!
                if disk_path in self.disks_changed:
                    pm.finalize_changes(disk)
                    log.debug(_("Saving changes done in %s") % disk_path)
                ## Now that partitions are created, set fs and label
                partitions = pm.get_partitions(disk)
                for partition_path in partitions:
                    log.debug(partition_path)
                    ## Get label, mount point and filesystem of staged partitions
                    uid = self.gen_partition_uid(path=partition_path)
                    if uid in self.stage_opts:
                        (is_new, lbl, mnt, fisy, fmt) = self.stage_opts[uid]
                        log.debug(_("Creating fs of type %s in %s with label %s") % (fisy, partition_path, lbl))
                        if mnt == '/':
                            if not pm.get_flag(partitions[partition_path], 
                                               1):
                                x = pm.set_flag(1, partitions[partition_path])
                                pm.finalize_changes(partitions[partition_path].disk)
                         #only format if they want formatting
                        if fmt:  
                         #all of fs module takes paths, not partition objs
                            (error, msg) = fs.create_fs(partition_path, fisy, lbl)
                            log.debug(msg)
                            log.debug(_("FORMATTED"))
                        elif partition_path in self.orig_label_dic:
                            if self.orig_label_dic[partition_path] != lbl:
                                fs.label_fs(fisy, partition_path, lbl)
        self.start_installation()
        
        ## Restore "Next" button text
        stock = "gtk-go-forward"
        self.forward_button.set_label(stock)
        self.forward_button.set_use_stock(True)
        return True
    
    ## Tell which one is our previous page (in our case installation_ask)
    def get_prev_page(self):
        return _prev_page

        ## Tell which one is our next page
    def get_next_page(self):
        return _next_page

    ## Start installation process
    def start_installation(self):
        ## TODO: should we add already mounted partitions to the list of
        ## partitions we will mount in the new system?
        fs_devices = {} 
        mount_devices = {} 
        for disk_path in self.disks:
            disk = self.disks[disk_path]
            partitions = pm.get_partitions(disk)
            self.all_partitions.append(partitions)
            partition_list = pm.order_partitions(partitions)
            for partition_path in partition_list:
                p = partitions[partition_path]
                uid = self.gen_partition_uid(p=p)
                if uid in self.stage_opts:
                    (is_new, label, mount_point, fs_type, fmt_active) = self.stage_opts[uid]
                    mount_devices[mount_point] = partition_path
                    fs_devices[partition_path] = fs_type
                elif pm.check_mounted(p):
                    mount_point, fs, writable = self.get_mount_point(p.path)
                    mount_devices[mount_point] = partition_path

        self.thread = installation_thread.InstallationThread( \
                    self.settings, \
                    self.callback_queue, \
                    mount_devices, \
                    self.grub_device, \
                    fs_devices, \
                    self.ssd)
                    
        self.thread.start()
