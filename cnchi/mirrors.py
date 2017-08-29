#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# mirrors.py
#
# Copyright © 2013-2017 Antergos
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


""" Let advanced users manage mirrorlist files """

import os
import sys
import queue
import time
import logging
import subprocess

import bootinfo

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

try:
    gi.require_foreign("cairo")
except ImportError:
    print("No pycairo integration")

import cairo

from gtkbasebox import GtkBaseBox

import misc.extra as misc

from rank_mirrors import AutoRankmirrorsProcess

# 6 mirrors for Arch repos and 6 for Antergos repos
MAX_MIRRORS = 6

class MirrorListBoxRow(Gtk.ListBoxRow):
    def __init__(self, url, active, switch_cb, drag_cbs):
        super(Gtk.ListBoxRow, self).__init__()
        #self.data = data
        #self.add(Gtk.Label(data))

        self.data = url

        box = Gtk.Box(spacing=20)

        self.handle = Gtk.EventBox.new()
        self.handle.add(Gtk.Image.new_from_icon_name("open-menu-symbolic", 1))
        box.pack_start(self.handle, False, False, 0)

        # Add mirror url label
        self.label = Gtk.Label.new()
        self.label.set_halign(Gtk.Align.START)
        self.label.set_justify(Gtk.Justification.LEFT)
        self.label.set_name(url)
        # Only show site address
        url_parts = url.split('/')
        text_url = url_parts[0] + "//" + url_parts[2]
        self.label.set_text(text_url)
        box.pack_start(self.label, False, True, 0)

        # Add mirror switch
        self.switch = Gtk.Switch.new()
        self.switch.set_name("switch_" + url)
        self.switch.set_property('margin_top', 2)
        self.switch.set_property('margin_bottom', 2)
        self.switch.set_property('margin_end', 10)
        self.switch.connect("notify::active", switch_cb)
        self.switch.set_active(active)
        box.pack_end(self.switch, False, False, 0)

        self.add(box)

        self.set_selectable(True)

        # Drag and drop
        entries = [Gtk.TargetEntry.new("GTK_LIST_BOX_ROW", Gtk.TargetFlags.SAME_APP, 8080)]

        # Source
        self.handle.drag_source_set(
            Gdk.ModifierType.BUTTON1_MASK,
            entries,
            Gdk.DragAction.MOVE)
        self.handle.connect("drag-begin", drag_cbs['drag-begin'])
        self.handle.connect("drag-data-get", drag_cbs['drag-data-get'])
        #self.handle.connect("drag-data-delete", self.on_drag_data_delete)
        #self.handle.connect("drag-end", self.on_drag_end)

        # Destination
        self.drag_dest_set(
            Gtk.DestDefaults.ALL,
            entries,
            Gdk.DragAction.MOVE)
        self.connect("drag-data-received",drag_cbs['drag-data-received']);
        #self.connect("drag-motion", self.on_drag_motion);
        #self.connect("drag-crop", self.on_drag_crop);

    def is_active(self):
        return self.switch.get_active()


class MirrorListBox(Gtk.ListBox):
    def __init__(self, mirror_file_path):
        super(Gtk.ListBox, self).__init__()
        self.mirror_path = mirror_file_path

        self.set_selection_mode(Gtk.SelectionMode.NONE)
        # self.set_selection_mode(Gtk.SelectionMode.BROWSE)
        # self.connect("row-selected", self.on_listbox_row_selected)
        # self.sort_func(self.listbox_sort_by_name, None)

        # Disabled by default
        self.set_sensitive(False)

        for listboxrow in self.get_children():
            self.destroy()

        lines = []

        # Load mirror file contents
        with open(mirror_file_path) as mfile:
            lines = mfile.readlines()

        # Discard lines that are not server lines
        tmp_lines = lines
        lines = []
        for line in tmp_lines:
            line = line.strip()
            if line.startswith("Server") or line.startswith("#Server"):
                lines.append(line)
        tmp_lines = []

        # Use MAX_MIRRORS at max
        if len(lines) > MAX_MIRRORS:
            lines = lines[0:MAX_MIRRORS]

        drag_cbs = {
            'drag-begin': self.on_drag_begin,
            'drag-data-get': self.on_drag_data_get,
            'drag-data-received': self.on_drag_data_received
        }

        # Read mirror info and create listboxrows
        for line in lines:
            if line.startswith("#Server"):
                active = False
                line = line[1:]
            else:
                active = True

            logging.debug(">>> %s", line)

            try:
                box = Gtk.Box(spacing=20)
                url = line.split("=")[1].strip()
                box.set_name(url)
                row = MirrorListBoxRow(url, active, self.on_switch_activated, drag_cbs)
                self.add(row)
            except KeyError:
                # Not a Mirror line, skip
                pass
        self.show_all()


    def on_switch_activated(self, switch, gparam):
        row = switch.get_ancestor(Gtk.ListBoxRow)
        if row:
            if switch.get_active():
                logging.debug("Mirror %s enabled!", row.data)
            else:
                logging.debug("Mirror %s disabled!", row.data)


    def on_drag_begin(self, widget, drag_context):
        """ User starts a drag """
        #logging.debug(widget)
        #logging.debug(drag_context)
        row = widget.get_ancestor(Gtk.ListBoxRow)
        alloc = row.get_allocation()
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, alloc.width, alloc.height)
        ctx = cairo.Context(surface)

        row.get_style_context().add_class("drag-icon")
        row.draw(ctx)
        row.get_style_context().remove_class("drag-icon")

        (x, y) = widget.translate_coordinates (row, 0, 0)

        surface.set_device_offset(-x, -y)
        #drag_context.set_icon_surface(surface)
        Gtk.drag_set_icon_surface(drag_context, surface)


    def on_drag_data_get(self, widget, drag_context, data, info, time):
        """ When drag data is requested by the destination """
        row = widget.get_ancestor(Gtk.ListBoxRow)
        logging.debug(data)
        logging.debug(info)
        #selected_path = self.get_selected_items()[0]
        #selected_iter = self.get_model().get_iter(selected_path)

    def on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        """ When drag data is received by the destination """
        row = widget.get_ancestor(Gtk.ListBoxRow)
        logging.debug(data)


class Mirrors(GtkBaseBox):
    def __init__(self, params, prev_page="location", next_page="timezone"):
        super().__init__(self, params, "mirrors", prev_page, next_page)

        data_dir = self.settings.get("data")

        self.disable_rank_mirrors = params["disable_rank_mirrors"]

        self.listbox_rows = {}

        # Set up lists
        self.listboxes = []

        mirror_listbox = MirrorListBox("/etc/pacman.d/mirrorlist")
        self.listboxes.append(mirror_listbox)
        sw = self.ui.get_object("scrolledwindow1")
        sw.add(mirror_listbox)

        mirror_listbox = MirrorListBox("/etc/pacman.d/antergos-mirrorlist")
        self.listboxes.append(mirror_listbox)
        sw = self.ui.get_object("scrolledwindow2")
        sw.add(mirror_listbox)

        # TODO: By default, select automatic mirror list ranking

        # Boolean variable to check if rank_mirrors has already been run
        self.rank_mirrors_launched = False
        self.disable_rank_mirrors = params['disable_rank_mirrors']


    def set_listboxes_sensitive(self, status):
        for listbox in self.listboxes:
            listbox.set_sensitive(status)

    def on_rank_radiobutton_toggled(self, widget):
        self.set_listboxes_sensitive(False)

    def on_leave_radiobutton_toggled(self, widget):
        self.set_listboxes_sensitive(False)

    def on_user_radiobutton_toggled(self, widget):
        self.set_listboxes_sensitive(True)


    def start_rank_mirrors(self):
        # Launch rank mirrors process to optimize Arch and Antergos mirrorlists
        if (not self.disable_rank_mirrors and not self.rank_mirrors_launched):
            proc = AutoRankmirrorsProcess(self.settings)
            proc.daemon = True
            proc.name = "rankmirrors"
            proc.start()
            self.process_list.append(proc)
            self.rank_mirrors_launched = True
        else:
            logging.debug("Not running rank mirrors. This is discouraged.")

    def prepare(self, direction):
        """ Prepares screen """
        self.translate_ui()
        self.show_all()
        self.forward_button.set_sensitive(True)

    def translate_ui(self):
        """ Translates screen before showing it """
        self.header.set_subtitle(_("Mirrors Selection"))

        self.forward_button.set_always_show_image(True)
        self.forward_button.set_sensitive(True)

        bold_style = '<span weight="bold">{0}</span>'

        radio = self.ui.get_object("rank_radiobutton")
        txt = _("Let Cnchi sort the mirrors lists (recommended)")
        radio.set_label(txt)
        radio.set_name('rank_radio_btn')

        radio = self.ui.get_object("leave_radiobutton")
        txt = _("Leave the mirrors lists as they are (by default)")
        radio.set_label(txt)
        radio.set_name('leave_radio_btn')

        radio = self.ui.get_object("user_radiobutton")
        txt = _("Let me manage the mirrors lists (advanced)")
        radio.set_label(txt)
        radio.set_name('user_radio_btn')

        intro_txt = _("How would you like to proceed?")
        intro_label = self.ui.get_object("introduction")
        # intro_txt = bold_style.format(intro_txt)
        intro_label.set_text(intro_txt)
        intro_label.set_name("intro_label")
        intro_label.set_hexpand(False)
        intro_label.set_line_wrap(True)

        intro_label.set_max_width_chars(80)


    '''
    def fill_listbox(self):
        for listbox_row in self.listbox.get_children():
            listbox_row.destroy()

        self.listbox_rows = {}

        # Only add graphic-driver feature if an AMD or Nvidia is detected
        if "graphic_drivers" in self.features:
            allow = False
            if self.detect.amd():
                allow = True
            if self.detect.nvidia() and not self.detect.bumblebee():
                allow = True
            if not allow:
                logging.debug("Removing proprietary graphic drivers feature.")
                self.features.remove("graphic_drivers")

        for feature in self.features:
            box = Gtk.Box(spacing=20)
            box.set_name(feature + "-row")

            self.listbox_rows[feature] = []

            self.add_feature_icon(feature, box)
            self.add_feature_label(feature, box)
            self.add_feature_switch(feature, box)
            # Add row to our gtklist
            self.listbox.add(box)

        self.listbox.show_all()
    '''














    def store_values(self):
        """ Store selected values """
        return True

    def get_next_page(self):
        return self.next_page



if __name__ == '__main__':
    from test_screen import _, run

    run('Mirrors')
