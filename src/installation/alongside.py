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

# Insert the src/parted directory at the front of the path.
base_dir = os.path.dirname(__file__) or '.'
parted_dir = os.path.join(base_dir, 'parted3')
sys.path.insert(0, parted_dir)

try:
    import parted
except ImportError as err:
    logging.error(_("Can't import parted module: %s") % str(err))

import canonical.misc as misc
import show_message as show
import bootinfo

import parted3.partition_module as pm
import parted3.fs_module as fs
import parted3.used_space as used_space

from installation import process as installation_process
from gtkbasebox import GtkBaseBox

# leave at least 6.5GB for Antergos when shrinking
MIN_ROOT_SIZE = 6500

# Our treeview columns
COL_DEVICE = 0
COL_DETECTED_OS = 1
COL_FILESYSTEM = 2
COL_USED = 3
COL_TOTAL = 4

def get_partition_size_info(partition_path, human):
    """ Gets partition used and available space """
    
    tmp_dir = tempfile.mkdtemp()
    min_size = "0"
    max_size = "0"
    
    try:
        subprocess.call(["mount", partition_path, tmp_dir])
        if human:
            cmd = ['df', '-h', partition_path]
        else:
            cmd = ['df', partition_path]
        df_out = subprocess.check_output(cmd).decode()
        subprocess.call(["umount", "-l", tmp_dir])
    except subprocess.CalledProcessError as err:
        txt = "CalledProcessError.output = %s" % err.output
        logging.exception(txt)

    if len(df_out) > 0:
        df_out = df_out.split('\n')
        df_out = df_out[1].split()
        if human:
            max_size = df_out[1]
            min_size = df_out[2]
        else:
            max_size = int(df_out[1]) / 1000
            min_size = int(df_out[2]) / 1000

    return (min_size, max_size)

class InstallationAlongside(GtkBaseBox):
    """ Performs an automatic installation next to a previous installed OS """
    def __init__(self, params, prev_page="installation_ask", next_page="user_info"):
        super().__init__(self, params, "alongside", prev_page, next_page)

        self.ui.connect_signals(self)

        self.label = self.ui.get_object('label_info')

        self.treeview = self.ui.get_object("treeview")
        self.treeview_store = None
        self.prepare_treeview()
        self.populate_treeview()

        # Init dialog slider
        self.init_slider()

    def init_slider(self):
        dialog = self.ui.get_object("shrink-dialog")
        slider = self.ui.get_object("scale")

        slider.set_name("myslider")
        path = os.path.join(self.settings.get("data"), "css", "scale.css")

        self.available_slider_range = [0, 0]

        if os.path.exists(path):
            with open(path, "rb") as css:
                css_data = css.read()
            try:
                provider = Gtk.CssProvider()
                provider.load_from_data(css_data)

                Gtk.StyleContext.add_provider_for_screen(
                    Gdk.Screen.get_default(),
                    provider,
                    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
            except:
                logging.exception(_("Can't load %s css") % path)

        #slider.add_events(Gdk.EventMask.SCROLL_MASK)

        slider.connect("change-value", self.slider_change_value)

        btn = self.ui.get_object("button_ok")
        btn.set_label("_Apply")
        btn.set_use_underline(True)
        btn.set_always_show_image(True)

        btn = self.ui.get_object("button_cancel")
        btn.set_label("_Cancel")
        btn.set_use_underline(True)
        btn.set_always_show_image(True)
        
        '''
        slider.connect("value_changed", self.main.on_volume_changed)
        slider.connect("button_press_event", self.on_scale_button_press_event)
        slider.connect("button_release_event", self.on_scale_button_release_event)
        slider.connect("scroll_event", self.on_scale_scroll_event)
        '''

    def slider_change_value(self, slider, scroll, value):
        """ Check that the value is inside our range and if it is, change it """
        min_range = self.available_slider_range[0]
        max_range = self.available_slider_range[1]
        if value <= min_range or value >= max_range:
            return True
        else:
            slider.set_fill_level(value)
            self.update_ask_shrink_size_labels(value)
            return False

    def translate_ui(self):
        """ Translates all ui elements """
        txt = _("Select the OS you would like Antergos installed next to.")
        txt = '<span size="large">%s</span>' % txt
        self.label.set_markup(txt)

        self.header.set_subtitle(_("Antergos Alongside Installation"))

        txt = _("Install Now!")
        self.forward_button.set_label(txt)

    def prepare(self, direction):
        self.translate_ui()
        self.show_all()
        self.forward_button.set_sensitive(False)

    def store_values(self):
        self.start_installation()
        return True

    def prepare_treeview(self):
        """ Create columns for our treeview """
        #render_pixbuf = Gtk.CellRendererPixbuf()
        #col = Gtk.TreeViewColumn("", render_pixbuf, text="")
        #self.treeview.append_column(col)

        render_text = Gtk.CellRendererText()

        headers = [
            (COL_DEVICE, _("Device")),
            (COL_DETECTED_OS, _("Detected OS")),
            (COL_FILESYSTEM, _("Filesystem")),
            (COL_USED, _("Used")),
            (COL_TOTAL, _("Total"))]
        
        for (header_id, header_text) in headers:
            col = Gtk.TreeViewColumn(header_text, render_text, text=header_id)
            self.treeview.append_column(col)

    @misc.raise_privileges
    def populate_treeview(self):
        if self.treeview_store is not None:
            self.treeview_store.clear()

        self.treeview_store = Gtk.TreeStore(str, str, str, str, str)

        oses = {}
        oses = bootinfo.get_os_dict()
        
        #print(oses)

        self.partitions = {}

        try:
            device_list = parted.getAllDevices()
        except (ImportError, NameError) as err:
            logging.error(_("Can't import parted module: %s"), str(err))
            device_list = []

        for dev in device_list:
            # Avoid cdrom and any raid, lvm volumes or encryptfs
            if not dev.path.startswith("/dev/sr") and not dev.path.startswith("/dev/mapper"):
                try:
                    disk = parted.Disk(dev)
                    # Create list of partitions for this device (p.e. /dev/sda)
                    partition_list = disk.partitions

                    for partition in partition_list:
                        if partition.type != pm.PARTITION_EXTENDED:
                            # Get filesystem
                            fs_type = ""
                            if partition.fileSystem and partition.fileSystem.type:
                                fs_type = partition.fileSystem.type
                            if "swap" not in fs_type:
                                (min_size, max_size) = get_partition_size_info(partition.path, human=True)
                                if partition.path in oses:
                                    row = [partition.path, oses[partition.path], fs_type, min_size, max_size]
                                else:
                                    row = [partition.path, _("unknown"), fs_type, min_size, max_size]
                                # parent is None so we append the row to the upper level
                                self.treeview_store.append(None, row)
                        self.partitions[partition.path] = partition
                except Exception as err:
                    txt = _("Unable to create list of partitions for alongside installation: %s") % err
                    logging.warning(txt)

        # Assign our new model to our treeview
        self.treeview.set_model(self.treeview_store)
        self.treeview.expand_all()

    def get_selected_row(self):
        selection = self.treeview.get_selection()

        if not selection:
            return None

        model, tree_iter = selection.get_selected()

        if tree_iter is None:
            return None

        return model[tree_iter]

    def on_treeview_cursor_changed(self, widget):
        row = self.get_selected_row()
        
        if row is None:
            return

        partition_path = row[COL_DEVICE]
        other_os_name = row[COL_DETECTED_OS]

        self.min_size = 0
        self.max_size = 0
        self.new_size = 0

        (self.min_size, self.max_size) = get_partition_size_info(partition_path, human=False)

        if self.min_size + MIN_ROOT_SIZE < self.max_size:
            self.new_size = self.ask_shrink_size(other_os_name)
        else:
            txt = _("Can't shrink partition %s (maybe it's nearly full?)") % partition_path
            logging.warning(txt)
            #show.error(self.get_toplevel(), txt)
            return

        if self.new_size > 0 and self.is_room_available(row):
            self.forward_button.set_sensitive(True)
        else:
            self.forward_button.set_sensitive(False)

    def update_ask_shrink_size_labels(self, new_value):
        label_other_os_size = self.ui.get_object("label_other_os_size")
        label_other_os_size.set_markup(str(int(new_value)) + " MB")

        label_antergos_size = self.ui.get_object("label_antergos_size")
        label_antergos_size.set_markup(str(int(self.max_size - new_value)) + " MB")

    def ask_shrink_size(self, other_os_name):
        dialog = self.ui.get_object("shrink-dialog")

        slider = self.ui.get_object("scale")

        # leave space for Antergos
        self.available_slider_range = [self.min_size, self.max_size - MIN_ROOT_SIZE]

        slider.set_fill_level(self.min_size)
        slider.set_show_fill_level(True)
        slider.set_restrict_to_fill_level(False)
        slider.set_range(0, self.max_size)
        slider.set_value(self.min_size)
        slider.set_draw_value(False)

        label_other_os = self.ui.get_object("label_other_os")
        txt = "<span weight='bold' size='large'>%s</span>" % other_os_name
        label_other_os.set_markup(txt)

        label_antergos = self.ui.get_object("label_antergos")
        txt = "<span weight='bold' size='large'>Antergos</span>"
        label_antergos.set_markup(txt)

        self.update_ask_shrink_size_labels(self.min_size)

        response = dialog.run()

        value = 0

        if response == Gtk.ResponseType.OK:
            value = int(slider.get_value()) + 1

        dialog.hide()

        return value

    def is_room_available(self, row):
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

        if len(primary_partitions) >= 4:
            txt = _("There are too many primary partitions, can't create a new one")
            logging.error(txt)
            show.error(self.get_toplevel(), txt)
            return False

        self.extended_path = extended_path

        # We only allow installing if only 2 partitions are already occupied, otherwise there's no room for root + swap


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
