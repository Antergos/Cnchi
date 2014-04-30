#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  installation_alongside.py
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

import xml.etree.ElementTree as etree

from gi.repository import Gtk, Gdk

import sys
import os
import logging
import subprocess

if __name__ == '__main__':
    # Insert the parent directory at the front of the path.
    # This is used only when we want to test this screen
    base_dir = os.path.dirname(__file__) or '.'
    parent_dir = os.path.join(base_dir, '..')
    sys.path.insert(0, parent_dir)

import canonical.misc as misc
import show_message as show
import bootinfo

try:
    import parted
except:
    pass

# Insert the src/parted directory at the front of the path.
base_dir = os.path.dirname(__file__) or '.'
parted_dir = os.path.join(base_dir, 'parted3')
sys.path.insert(0, parted_dir)

import parted3.partition_module as pm
import parted3.fs_module as fs

from installation import process as installation_process

_next_page = "user_info"
_prev_page = "installation_ask"

# leave at least 6.5GB for Antergos when shrinking
MIN_ROOT_SIZE = 6500

class InstallationAlongside(Gtk.Box):
    def __init__(self, params):
        self.header = params['header']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        self.callback_queue = params['callback_queue']
        self.settings = params['settings']
        self.alternate_package_list = params['alternate_package_list']
        self.testing = params['testing']

        super().__init__()
        self.ui = Gtk.Builder()
        self.ui.add_from_file(os.path.join(self.ui_dir, "alongside.ui"))

        self.ui.connect_signals(self)

        self.label = self.ui.get_object('label_info')

        self.treeview = self.ui.get_object("treeview1")
        self.treeview_store = None
        self.prepare_treeview()
        self.populate_treeview()

        # Init dialog slider
        self.init_slider()

        super().add(self.ui.get_object("installation_alongside"))

    def init_slider(self):
        dialog = self.ui.get_object("shrink-dialog")
        slider = self.ui.get_object("scale")

        slider.set_name("myslider")
        path = os.path.join(self.settings.get("data"), "css", "scale.css")

        self.available_slider_range = [0, 0]

        if os.path.exists(path):
            with open(path, "rb") as css:
                css_data = css.read()

            provider = Gtk.CssProvider()

            try:
                provider.load_from_data(css_data)

                Gtk.StyleContext.add_provider_for_screen(
                    Gdk.Screen.get_default(), provider,
                    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
                )
            except:
                logging.exception(_("Can't load %s css") % path)


        #slider.add_events(Gdk.EventMask.SCROLL_MASK)

        slider.connect("change-value", self.slider_change_value)
        '''
        slider.connect("value_changed",
                self.main.on_volume_changed)
        slider.connect("button_press_event",
                self.on_scale_button_press_event)
        slider.connect("button_release_event",
                self.on_scale_button_release_event)
        slider.connect("scroll_event",
                self.on_scale_scroll_event)
        '''

    def slider_change_value(self, slider, scroll, value):
        if value <= self.available_slider_range[0] or \
           value >= self.available_slider_range[1]:
            return True
        else:
            slider.set_fill_level(value)
            self.update_ask_shrink_size_labels(value)
            return False

    def translate_ui(self):
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

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page

    def prepare_treeview(self):
        """ Create columns for our treeview """
        render_text = Gtk.CellRendererText()

        col = Gtk.TreeViewColumn(_("Device"), render_text, text=0)
        self.treeview.append_column(col)

        col = Gtk.TreeViewColumn(_("Detected OS"), render_text, text=1)
        self.treeview.append_column(col)

        col = Gtk.TreeViewColumn(_("Filesystem"), render_text, text=2)
        self.treeview.append_column(col)

    @misc.raise_privileges
    def populate_treeview(self):
        if self.treeview_store != None:
            self.treeview_store.clear()

        self.treeview_store = Gtk.TreeStore(str, str, str)

        oses = {}
        oses = bootinfo.get_os_dict()

        self.partitions = {}

        try:
            device_list = parted.getAllDevices()
        except:
            logging.error(_("Can't import parted module! This installer won't work."))
            device_list = []

        for dev in device_list:
            # Avoid cdrom and any raid, lvm volumes or encryptfs
            if not dev.path.startswith("/dev/sr") and \
               not dev.path.startswith("/dev/mapper"):
                try:
                    disk = parted.Disk(dev)
                    # Create list of partitions for this device (p.e. /dev/sda)
                    partition_list = disk.partitions

                    for p in partition_list:
                        if p.type != pm.PARTITION_EXTENDED:
                            ## Get filesystem
                            fs_type = ""
                            if p.fileSystem and p.fileSystem.type:
                                fs_type = p.fileSystem.type
                            if "swap" not in fs_type:
                                if p.path in oses:
                                    row = [p.path, oses[p.path], fs_type]
                                else:
                                    row = [p.path, _("unknown"), fs_type]
                                self.treeview_store.append(None, row)
                        self.partitions[p.path] = p
                except Exception as e:
                    logging.warning(_("Unable to create list of partitions for alongside installation."))

        # Assign our new model to our treeview
        self.treeview.set_model(self.treeview_store)
        self.treeview.expand_all()

    def on_treeview_cursor_changed(self, widget):
        selection = self.treeview.get_selection()

        if not selection:
            return

        model, tree_iter = selection.get_selected()

        if tree_iter == None:
            return

        self.row = model[tree_iter]

        partition_path = self.row[0]
        other_os_name = self.row[1]

        self.min_size = 0
        self.max_size = 0
        self.new_size = 0

        try:
            subprocess.call(["mount", partition_path, "/mnt"], stderr=subprocess.DEVNULL)
            x = subprocess.check_output(['df', partition_path]).decode()
            subprocess.call(["umount", "-l", "/mnt"], stderr=subprocess.DEVNULL)
            x = x.split('\n')
            x = x[1].split()
            self.max_size = int(x[1]) / 1000
            self.min_size = int(x[2]) / 1000
        except subprocess.CalledProcessError as e:
            logging.exception("CalledProcessError.output = %s" % e.output)

        if self.min_size + MIN_ROOT_SIZE < self.max_size:
            self.new_size = self.ask_shrink_size(other_os_name)
        else:
            show.error(_("Can't shrink the partition (maybe it's nearly full)"))
            return

        if self.new_size > 0 and self.is_room_available():
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
        self.available_slider_range = [ self.min_size, self.max_size - MIN_ROOT_SIZE ]

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

    def is_room_available(self):
        partition_path = self.row[0]
        otherOS = self.row[1]
        fs_type = self.row[2]

        # what if path is sda10 (two digits) ? this is wrong
        device_path = self.row[0][:-1]

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

        # We only allow installing if only 2 partitions are already occupied, otherwise there's no room for root + swap
        if len(primary_partitions) >= 4:
            logging.error("There're too many primary partitions, can't create a new one")
            return False

        self.extended_path = extended_path

        return True

    def start_installation(self):
        """ Alongside method shrinks selected partition
        and creates root and swap partition in the available space """

        if self.is_room_available() == False:
            return

        partition_path = self.row[0]
        otherOS = self.row[1]
        fs_type = self.row[2]

        # What if path is sda10 (two digits) ? this is wrong
        device_path = self.row[0][:-1]

        #re.search(r'\d+$', self.row[0])

        new_size = self.new_size

        # First, shrink filesystem
        res = fs.resize(partition_path, fs_type, new_size)
        if res:
            #logging.info("Filesystem on " + partition_path + " shrunk.\nWill recreate partition now on device " + device_path + " partition " + partition_path)
            txt = _("Filesystem on %s shrunk.") % partition_path
            txt += "\n"
            txt += _("Will recreate partition now on device %s partition %s") % (device_path, partition_path)
            logging.debug(txt)
            # destroy original partition and create a new resized one
            res = pm.split_partition(device_path, partition_path, new_size)
        else:
            txt = _("Can't shrink %s(%s) filesystem") % (otherOS, fs_type)
            logging.error(txt)
            show.error(txt)
            return

        # 'res' is either False or a parted.Geometry for the new free space
        if res is not None:
            txt = _("Partition %s shrink complete") % partition_path
            logging.debug(txt)
        else:
            txt = _("Can't shrink %s(%s) partition") % (otherOS, fs_type)
            logging.error(txt)
            show.error(txt)
            txt = _("*** FILESYSTEM IN UNSAFE STATE ***")
            txt += "\n"
            txt += _("Filesystem shrink succeeded but partition shrink failed.")
            logging.error(txt)
            return

        disc_dic = pm.get_devices()
        disk = disc_dic[device_path][0]
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
                show.error(txt)
                return
            else:
                no_swap = True

        if no_swap:
            npart = pm.create_partition(device_path, 0, res)
            if npart is None:
                txt = _("Cannot create new partition.")
                logging.error(txt)
                show.error(txt)
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
                show.error(txt)
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
                show.error(txt)
                return

            pm.finalize_changes(disk)

            # Mount points
            mount_devices["swap"] = swappart.path
            fs_devices[swappart.path] = "swap"
            fs.create_fs(swappart.path, 'swap', 'SWAP')

            mount_devices["/"] = npart.path
            fs_devices[npart.path] = "ext4"
            fs.create_fs(npart.path, 'ext4', 'ROOT')

        self.settings.set('install_bootloader', True)
        
        if self.settings.get('install_bootloader'):
            if self.settings.get('efi'):
                self.settings.set('bootloader_type', "UEFI_x86_64")
                self.settings.set('bootloader_location', '/boot')
            else:
                self.settings.set('bootloader_type', "GRUB2")
                self.settings.set('bootloader_location', device_path)

            logging.info(_("Thus will install the bootloader of type %s in %s") %
                          (self.settings.get('bootloader_type'),
                           self.settings.get('bootloader_location')))
        else:
            logging.warning("Cnchi will not install any boot loader")

        if not self.testing:
            self.process = installation_process.InstallationProcess( \
                            self.settings, \
                            self.callback_queue, \
                            mount_devices, \
                            fs_devices, \
                            None, \
                            self.alternate_package_list)

            self.process.start()


# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message): return message

if __name__ == '__main__':
    from test_screen import _,run
    run('InstallationAlongside')
