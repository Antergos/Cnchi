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

import xml.etree.ElementTree as etree

from gi.repository import Gtk

import subprocess

import gettext

import sys
import os

import misc

# Insert the src/parted directory at the front of the path.
base_dir = os.path.dirname(__file__) or '.'
parted_dir = os.path.join(base_dir, 'parted')
sys.path.insert(0, parted_dir)
# import Alex modules
import partition_module as pm
import fs_module as fs

# Useful vars for gettext (translations)
APP="cnchi"
DIR="po"

# This allows to translate all py texts (not the glade ones)
gettext.textdomain(APP)
gettext.bindtextdomain(APP, DIR)

# With this we can use _("string") to translate
_ = gettext.gettext

from config import installer_settings

from show_message import show_error

_next_page = "timezone"
_prev_page = "installation_ask"

class InstallationAdvanced(Gtk.Box):

    def __init__(self, params):

        self.title = params['title']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        
        super().__init__()

        self.ui = Gtk.Builder()
        ui_file = os.path.join(self.ui_dir, "installation_advanced.ui")
        self.ui.add_from_file(ui_file)

        self.ui.connect_signals(self)
        
        self.edit_partition_dialog = self.ui.get_object('partition_dialog')

        use_combo = self.ui.get_object('partition_use_combo')
        use_combo.remove_all()
        for fs_name in sorted(fs._names):
            use_combo.append_text(fs_name)
        use_combo.set_wrap_width(2)

        mount_combo = self.ui.get_object('partition_mount_combo')
        mount_combo.remove_all()
        for mp in sorted(fs._common_mount_points):
            mount_combo.append_text(mp)

        # store here get_devices
        self.disks = None

        self.grub_device_entry = self.ui.get_object('grub_device_entry')      
        self.grub_devices = dict()
        
        self.partition_list = self.ui.get_object('partition_list_treeview')
        self.partition_list_store = None
        self.prepare_partition_list()
        
        select = self.partition_list.get_selection()
        select.connect("changed", self.on_partition_list_treeview_selection_changed)
        
        super().add(self.ui.get_object("installation_advanced"))

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

        if tree_iter != None:
            path = model[tree_iter][0]
            if path == _("free space"):
                button_new.set_sensitive(True)
            else:
                disks = pm.get_devices()
                if not path in disks:
                    # a partition is selected
                    button_delete.set_sensitive(True)    
                    button_edit.set_sensitive(True)
                else:
                    # a drive is selected
                    button_new_label.set_sensitive(True)
                    

    def fill_grub_device_entry(self):       
        self.grub_device_entry.remove_all()
        self.grub_devices.clear()
        
        if self.disks == None:
            # just call get_devices once
            self.disks = pm.get_devices()

        #for path in referenceElement.keys()
        
        for path in sorted(self.disks):
            disk = self.disks[path]
            if disk is not None:
                dev = disk.device
                # hard drives measure themselves assuming kilo=1000, mega=1mil, etc
                size_in_gigabytes = int((dev.length * dev.sectorSize) / 1000000000)
                line = '{0} [{1} GB] ({2})'.format(dev.model, size_in_gigabytes, dev.path)
                self.grub_device_entry.append_text(line)
                self.grub_devices[line] = dev.path

        self.select_first_combobox_item(self.grub_device_entry)

    def select_first_combobox_item(self, combobox):
        tree_model = combobox.get_model()
        tree_iter = tree_model.get_iter_first()
        combobox.set_active_iter(tree_iter)

    def on_select_grub_drive_changed(self, widget):
        line = self.grub_device_entry.get_active_text()
        if line != None:
            self.grub_device = self.grub_devices[line]
    
    def prepare_partition_list(self):
        # create columns for our treeview
        render_text = Gtk.CellRendererText()
        
        render_toggle = Gtk.CellRendererToggle()
        render_toggle.connect("toggled", self.on_format_cell_toggled)
        
        col = Gtk.TreeViewColumn(_("Device"), render_text, text=0)
        self.partition_list.append_column(col)
        
        col = Gtk.TreeViewColumn(_("Type"), render_text, text=1)
        self.partition_list.append_column(col)
        
        col = Gtk.TreeViewColumn(_("Mount point"), render_text, text=2)
        self.partition_list.append_column(col)
        
        col = Gtk.TreeViewColumn(_("Label"), render_text, text=3)
        self.partition_list.append_column(col)
        
        col = Gtk.TreeViewColumn(_("Format?"), render_toggle, active=4, visible=5)
        self.partition_list.append_column(col)
        
        col = Gtk.TreeViewColumn(_("Size"), render_text, text=6)
        self.partition_list.append_column(col)
        
        col = Gtk.TreeViewColumn(_("Used"), render_text, text=7)
        self.partition_list.append_column(col)   

        col = Gtk.TreeViewColumn(_("Flags"), render_text, text=9)
        self.partition_list.append_column(col)   

    def get_size(self, length, sectorSize):
        size = length * sectorSize
        #aas# fixing below sizes
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
        # create tree store 'partition_list_store' for our model

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
        
        self.partition_list_store = \
            Gtk.TreeStore(str, str, str, str, bool, bool, str, str, str, str, int)
            
        if self.disks == None:
            # just call get_devices once
            self.disks = pm.get_devices()
        
        for disk_path in sorted(self.disks):
            disk = self.disks[disk_path]
            
            if disk is None:
                # maybe disk without a partition table?
                print(disk_path)
                row = [disk_path, "", "", "", False, False, "", "", "", "", 0]
                self.partition_list_store.append(None, row)
            else:
                dev = disk.device

                size_txt = self.get_size(dev.length, dev.sectorSize)
                
                row = [dev.path, "", "", "", False, False, size_txt, "", "", "", 0]
                disk_parent = self.partition_list_store.append(None, row)
                
                parent = disk_parent

                # create list of partitions for this device (/dev/sda for example)
                partitions = pm.get_partitions(disk)
                partition_list = pm.order_partitions(partitions)
                
                for partition_path in partition_list:
                    p = partitions[partition_path]
                    
                    size_txt = self.get_size(p.geometry.length, dev.sectorSize)
                    
                    label = ""
                    fs_type = ""
                    mount_point = ""
                    used = ""
                    flags = ""
                    formatable = True

                    path = p.path

                    if p.fileSystem:
                        fs_type = p.fileSystem.type
                    else:
                        fs_type = _("none")

                    if pm.check_mounted(p) and not "swap" in fs_type:
                        mount_point = self.get_mount_point(p.path)

                    if p.type == pm.PARTITION_EXTENDED:
                        fs_type = _("extended")
                        formatable = False
                        
                    if p.type == pm.PARTITION_FREESPACE:
                        path = _("free space")
                        formatable = False
                    else:
                        used = str(pm.get_used_space(p))
                        flags = pm.get_flags(p)
                        # cannot get label from staged partition
                        try:
                            info = fs.get_info(partition_path)
                            if 'LABEL' in info:
                                label = info['LABEL']
                        except:
                            label = ""
                                     
                    row = [path, fs_type, mount_point, label, False, \
                           formatable, size_txt, used, partition_path, \
                           "", p.type]
                    tree_iter = self.partition_list_store.append(parent, row)

                    if p.type == pm.PARTITION_EXTENDED:
                        parent = tree_iter
                    elif p.type == pm.PARTITION_PRIMARY:
                        parent = disk_parent

        # assign our new model to our treeview
        self.partition_list.set_model(self.partition_list_store)
        self.partition_list.expand_all()
       
    def on_format_cell_toggled(self, widget, path):
        print("on_format_cell_toggled")
        selected_path = Gtk.TreePath(path)
        self.partition_list_store[path][4] = not self.partition_list_store[path][4]
        print(self.partition_list_store[path][4])

    def on_partition_use_combo_changed(self, widget):
        fs_name = widget.get_active_text()
        print("on_partition_use_combo_changed : creating new partition, setting new fs to %s" % fs_name)

    def on_partition_list_edit_activate(self, button):
        print("on_partition_list_edit_activate : edit the selected partition")

    def on_partition_list_delete_activate(self, button):
        selection = self.partition_list.get_selection()
        
        if not selection:
            return
            
        model, tree_iter = selection.get_selected()

        if tree_iter == None:
            return
                  
        #No es pot crear una taula de particions nova quan hi ha
        # particions actives.  Les particions actives són aquelles
        # que s'estan utilitzant, com ara un sistema de fitxers muntat
        # o un espai d'intercanvi habilitat.
        #Utilitzeu les opcions del menú Partició, com ara «Desmunta»
        # o «Partició d'intercanvi inactiva», per desactivar totes
        # les particions d'aquest dispositiu abans de crear una taula
        # de particions nova.
        
        parent_iter = model.iter_parent(tree_iter)
                
        part_type = model[tree_iter][10]
        
        if part_type == pm.PARTITION_LOGICAL:
            parent_iter = model.iter_parent(parent_iter)

        disk_path = model[parent_iter][0]

        logical_partition = False
        
        row = model[tree_iter]
        
        size_available = row[6]
        partition_path = row[8]

        print ("You will delete from disk [%s] partition [%s]" % (disk_path, partition_path))

        if self.disks == None:
            # just call get_devices once
            self.disks = pm.get_devices()

        disk = self.disks[disk_path]

        partitions = pm.get_partitions(disk)
        
        part = partitions[partition_path]
        
        if pm.check_mounted(part):
            # Should we ask first?
            subp = subprocess.Popen(['umount', part.path], stdout=subprocess.PIPE)

        # Is it worth to show some warning message here?
        pm.delete_partition(disk, part)
        
        # Update treeview
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
        return fsname

    def on_partition_list_new_activate(self, button):
        # print("on_partition_list_new_activate : add a new partition")

        selection = self.partition_list.get_selection()
        
        if not selection:
            return
            
        model, tree_iter = selection.get_selected()

        if tree_iter == None:
            return
            
        print ("You selected %s" % model[tree_iter][0])
        
        if model[tree_iter][0] == _("free space"):
            
            parent_iter = model.iter_parent(tree_iter)
            
            disk_path = model[parent_iter][0]
            
            row = model[tree_iter]
            
            size_available = row[6]
            partition_path = row[8]

            if self.disks == None:
                self.disks = pm.get_devices()
                
            disk = self.disks[disk_path]
            dev = disk.device
            
            partitions = pm.get_partitions(disk)
            p = partitions[partition_path]

            # Get the objects from the dialog
            primary_radio = self.ui.get_object('partition_create_type_primary')
            logical_radio = self.ui.get_object('partition_create_type_logical')
            primary_radio.set_active(True)
            logical_radio.set_active(False)
            
            primary_count = disk.primaryPartitionCount
            
            if primary_count >= disk.maxPrimaryPartitionCount:
                # no room left for another primary partition
                primary_radio.set_sensitive(False)

            beginning_radio = self.ui.get_object('partition_create_place_beginning')
            end_radio = self.ui.get_object('partition_create_place_end')
            beginning_radio.set_active(True)
            end_radio.set_active(False)
            

            # prepare size spin
            #aas# +1 as not to leave unusably small space behind
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

            # mount combo entry
            mount_combo_entry = self.ui.get_object('combobox-entry4')
            mount_combo_entry.set_text("")

            # finally, show the create partition dialog

            response = self.edit_partition_dialog.run()
            
            if response == Gtk.ResponseType.OK:
                
                size = int(size_spin.get_value())
                print("size : %d" % size)

                beg_var = beginning_radio.get_active()

                start_sector = p.geometry.start
                end_sector = p.geometry.end
                              
                extended = disk.getExtendedPartition()
                supports_extended = disk.supportsFeature(pm.PARTITION_EXTENDED)

                geometry = pm.geom_builder(disk, start_sector, 
                                           end_sector, size, beg_var)

                # if the partition is of type LOGICAL, we must search if an
                # extended partition is already there. If it is, we must add
                # our logical partition to it, if it's not, we must create
                # an extended partition and then create our logical partition
                # inside.

                if primary_radio.get_active():
                    print("Creating primary partition")
                    pm.create_partition(disk, pm.PARTITION_PRIMARY, geometry)
                elif supports_extended:
                    if not extended:
                        print("Creating extended partition")
                        # Can we make an extended partition? now's our chance.
                        # Should we use all remaining free space?
                        # Which geometry should we use here?
                        pm.create_partition(disk, pm.PARTITION_EXTENDED, geometry)

                        logical_count = len(disk.getLogicalPartitions())
                        max_logicals = disk.getMaxLogicalPartitions()
                        
                        if logical_count < max_logicals:
                            print("Creating logical partition")
                            # which geometry should we use here?
                            pm.create_partition(disk, pm.PARTITION_LOGICAL, geometry)
                    else:
                        logical_count = len(disk.getLogicalPartitions())
                        max_logicals = disk.getMaxLogicalPartitions()
                        
                        if logical_count < max_logicals:
                            print("Creating logical partition")
                            pm.create_partition(disk, pm.PARTITION_LOGICAL, geometry)
                
                # TODO: Don't forget these ones!
                #use_as
                #label
                #mount_point

                print("OK!")
                self.fill_partition_list()
            else:
                print("Cancel or closed!")
            
            self.edit_partition_dialog.hide()
        
    def on_partition_list_undo_activate(self, button):
        print("on_partition_list_undo_activate")

        self.disks = pm.get_devices()
        
        self.fill_partition_list()
    
    def on_partition_list_new_label_activate(self, button):
        print("on_partition_list_new_label_activate : new partition table")
        #3 partitions are currently active on device /dev/sda
        #No es pot crear una taula de particions nova quan hi ha
        # particions actives.  Les particions actives són aquelles
        # que s'estan utilitzant, com ara un sistema de fitxers muntat
        # o un espai d'intercanvi habilitat.
        #Utilitzeu les opcions del menú Partició, com ara «Desmunta»
        # o «Partició d'intercanvi inactiva», per desactivar totes
        # les particions d'aquest dispositiu abans de crear una taula
        # de particions nova.
        
        selection = self.partition_list.get_selection()
        
        if not selection:
            return
            
        model, tree_iter = selection.get_selected()

        if tree_iter == None:
            return
            
        path = model[tree_iter][0]

        disks = pm.get_devices()
            
        for disk_path in sorted(disks):
            disk = disks[disk_path]
            #dev = disk.device
		
		# FIXME: end it!
		
		

    def on_partition_list_treeview_selection_changed(self, selection):
        print("on_partition_list_treeview_selection_changed")
        
        self.check_buttons(selection)
        
        #model, tree_iter = selection.get_selected()
        #if tree_iter != None:
        #    print ("You selected %s" % model[tree_iter][0])
        
    def on_partition_list_treeview_button_press_event(self, widget, event):
        print("on_partition_list_treeview_button_press_event")
        #clicked on the partition treeview
        
        #print(event.type)
        #print(event.x_root)
        #print(event.y_root)
 
        return False

    def on_partition_list_treeview_key_press_event(self, widget, event):
        print("on_partition_list_treeview_key_press_event")
        # key pressed while on the partition treeview
        return False

    def on_partition_list_treeview_row_activated(self, path, column, user_data):
        print("on_partition_list_treeview_row_activated")

    def on_partition_list_treeview_popup_menu(self, widget):
        print("on_partition_list_treeview_popup_menu")

    def translate_ui(self):
        txt = _("Cinnarch advanced installation mode")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.title.set_markup(txt)
        
        txt = _("Device for boot loader installation:")
        txt = "<span weight='bold' size='small'>%s</span>" % txt
        label = self.ui.get_object('grub_device_label')
        label.set_markup(txt)
        
        txt = _("TODO: Here goes a warning message")
        txt = "<span weight='bold'>%s</span>" % txt
        label = self.ui.get_object('part_advanced_warning_message')
        label.set_markup(txt)
        
        txt = _("New partition table")
        button = self.ui.get_object('partition_button_new_label')
        button.set_label(txt)
        
        txt = _("Revert")
        button = self.ui.get_object('partition_button_undo')
        button.set_label(txt)
        
        txt = _("Change...")
        button = self.ui.get_object('partition_button_edit')
        button.set_label(txt)
        
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
        
        txt = _("Install now!")
        self.forward_button.set_label(txt)

        #self.ui.get_object('cancelbutton1')
        #self.ui.get_object('partition_dialog_okbutton')

    def prepare(self):
        self.fill_grub_device_entry()

        self.fill_partition_list() 

        self.translate_ui()
        self.show_all()

        label = self.ui.get_object('part_advanced_recalculating_label')
        label.hide()
        
        spinner = self.ui.get_object('part_advanced_recalculating_spinner')
        spinner.hide()
        
        button = self.ui.get_object('partition_button_lvm')
        button.hide()
        
        image = self.ui.get_object('part_advanced_warning_image')
        image.hide()
        
        label = self.ui.get_object('part_advanced_warning_message')
        label.hide()
        
        self.forward_button.set_sensitive(False)

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

    def store_values(self):
        self.start_installation()

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page

    def start_installation(self):
        #self.install_progress.set_sensitive(True)
        print(script_path)

        #root_device = self.combobox["root"].get_active_text()
        #swap_device = self.combobox["swap"].get_active_text()
        #mount_devices =

        self.thread = installation_thread.InstallationThread("advanced")
        #self.thread.set_devices(None, self.root_device, self.swap_device, mount_devices)
        #self.thread.start()

