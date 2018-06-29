#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# mirrors.py
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


""" Let advanced users manage mirrorlist files """

import logging
import multiprocessing
import shutil

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject

try:
    gi.require_foreign("cairo")
except ImportError:
    print("No pycairo integration")

import cairo
from pages.gtkbasebox import GtkBaseBox
from rank_mirrors import RankMirrors

if __name__ == '__main__':
    import sys
    sys.path.append('/usr/share/cnchi/src')

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message


class MirrorListBoxRow(Gtk.ListBoxRow):
    """ Represents a mirror """
    def __init__(self, url, active, switch_cb, drag_cbs):
        super(Gtk.ListBoxRow, self).__init__()
        #self.data = data
        # self.add(Gtk.Label(data))

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
        # Source
        self.handle.drag_source_set(
            Gdk.ModifierType.BUTTON1_MASK, [], Gdk.DragAction.MOVE)
        self.handle.drag_source_add_text_targets()
        self.handle.connect("drag-begin", drag_cbs['drag-begin'])
        self.handle.connect("drag-data-get", drag_cbs['drag-data-get'])
        #self.handle.connect("drag-data-delete", self.on_drag_data_delete)
        #self.handle.connect("drag-end", self.on_drag_end)

        # Destination
        self.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.MOVE)
        self.drag_dest_add_text_targets()
        self.connect("drag-data-received", drag_cbs['drag-data-received'])
        #self.connect("drag-motion", self.on_drag_motion);
        #self.connect("drag-crop", self.on_drag_crop);

    def is_active(self):
        """ Returns if the mirror is active """
        return self.switch.get_active()


class MirrorListBox(Gtk.ListBox):
    """ List that stores all mirrors """
    __gsignals__ = {
        'switch-activated': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    # 6 mirrors for Arch repos and 6 for Antergos repos
    MAX_MIRRORS = 6
    # DND_ID_LISTBOX_ROW = 6791

    def __init__(self, mirrors_file_path, settings):
        super(Gtk.ListBox, self).__init__()
        self.mirrors_file_path = mirrors_file_path
        self.set_selection_mode(Gtk.SelectionMode.NONE)
        # self.set_selection_mode(Gtk.SelectionMode.BROWSE)
        # self.connect("row-selected", self.on_listbox_row_selected)
        # self.sort_func(self.listbox_sort_by_name, None)

        self.settings = settings

        # List. Each element is a tuple (url, active)
        self.mirrors = []

        self.load_mirrors()
        self.fillme()

    def load_mirrors(self):
        """ Load mirrors from text file """
        lines = []

        # Load mirror file contents
        with open(self.mirrors_file_path) as mfile:
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
        if len(lines) > MirrorListBox.MAX_MIRRORS:
            lines = lines[0:MirrorListBox.MAX_MIRRORS]

        # Read mirror info and create mirrors list
        for line in lines:
            if line.startswith("#Server"):
                active = False
                line = line[1:]
            else:
                active = True

            try:
                url = line.split("=")[1].strip()
                logging.debug(url)
                self.mirrors.append((url, active))
            except KeyError:
                pass

    def fillme(self):
        """ Fill listbox with mirrors info """
        for listboxrow in self.get_children():
            listboxrow.destroy()

        drag_cbs = {
            'drag-begin': self.on_drag_begin,
            'drag-data-get': self.on_drag_data_get,
            'drag-data-received': self.on_drag_data_received
        }

        for (url, active) in self.mirrors:
            box = Gtk.Box(spacing=20)
            box.set_name(url)
            row = MirrorListBoxRow(
                url, active, self.on_switch_activated, drag_cbs)
            self.add(row)

    def set_mirror_active(self, url, active):
        """ Changes the active status in our mirrors list """
        for index, item in enumerate(self.mirrors):
            murl, _mact = item
            if url == murl:
                self.mirrors[index] = (url, active)

    def get_active_mirrors(self):
        """ Returns a list with all active mirrors """
        active_mirrors = []
        for (url, active) in self.mirrors:
            if active:
                active_mirrors.append(url)
        return active_mirrors

    def on_switch_activated(self, switch, _gparam):
        """ Mirror activated """
        row = switch.get_ancestor(Gtk.ListBoxRow)
        if row:
            self.set_mirror_active(row.data, switch.get_active())
            self.emit("switch-activated")

    def on_drag_begin(self, widget, drag_context):
        """ User starts a drag """
        row = widget.get_ancestor(Gtk.ListBoxRow)
        alloc = row.get_allocation()
        surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32, alloc.width, alloc.height)
        ctx = cairo.Context(surface)

        row.get_style_context().add_class("drag-icon")
        row.draw(ctx)
        row.get_style_context().remove_class("drag-icon")

        pos_x, pos_y = widget.translate_coordinates(row, 0, 0)

        surface.set_device_offset(-pos_x, -pos_y)
        Gtk.drag_set_icon_surface(drag_context, surface)

        hand_cursor = Gdk.Cursor(Gdk.CursorType.HAND1)
        self.get_window().set_cursor(hand_cursor)

    def on_drag_data_get(self, widget, _drag_context, selection_data, _info, _time):
        """ When drag data is requested by the destination """
        row = widget.get_ancestor(Gtk.ListBoxRow)
        listbox_str = str(self)
        row_index = row.get_index()
        data = "{0}|{1}".format(listbox_str, row_index)
        selection_data.set_text(data, len(data))
        self.get_window().set_cursor(None)

    def on_drag_data_received(self, widget, _drag_context, _x, _y, selection_data, _info, _time):
        """ When drag data is received by the destination """
        data = selection_data.get_text()
        try:
            listbox_str = data.split('|')[0]
            if listbox_str == str(self):
                old_index = int(data.split('|')[1])
                new_index = widget.get_index()
                self.mirrors.insert(new_index, self.mirrors.pop(old_index))
                self.fillme()
                self.show_all()
        except (KeyError, ValueError) as err:
            logging.warning(err)

    @staticmethod
    def trim_mirror_url(url):
        """ Get url from full mirrorlist line """
        url = url.ltrim("Server = ")
        url = url.rtrim("/$repo/os/$arch")
        return url

    def save_changes(self, use_rankmirrors=False):
        """ Save mirrors in mirrors list file """
        # Save a backup if possible
        src = self.mirrors_file_path
        dst = src + ".cnchi-backup"

        try:
            shutil.copy2(src, dst)
        except (FileNotFoundError, FileExistsError, OSError) as err:
            logging.warning(err)

        # ok, now save our changes
        with open(src, 'w') as mfile:
            line = "# Mirrorlist file modified by Cnchi\n\n"
            mfile.write(line)
            for (url, active) in self.mirrors:
                line = "Server = {}\n".format(url)
                if not active:
                    line = "#" + line
                mfile.write(line)

        # If this is the Arch mirrorlist and we are not using rankmirrors,
        # we need to save it to rankmirrors_result in settings
        arch_mirrors = []
        if not use_rankmirrors and self.mirrors_file_path == "/etc/pacman.d/mirrorlist":
            for (url, active) in self.mirrors:
                if active:
                    arch_mirrors.append(self.trim_mirror_url(url))
            self.settings.set('rankmirrors_result', arch_mirrors)


class Mirrors(GtkBaseBox):
    """ Page that shows mirrolists so the user can arrange them manually """

    MIRRORLISTS = [
        "/etc/pacman.d/mirrorlist",
        "/etc/pacman.d/antergos-mirrorlist"]

    def __init__(self, params, prev_page="cache", next_page="installation_ask"):
        super().__init__(self, params, "mirrors", prev_page, next_page)

        # Set up lists
        self.listboxes = []
        self.scrolledwindows = []

        self.scrolledwindows.append(self.ui.get_object("scrolledwindow1"))
        self.scrolledwindows.append(self.ui.get_object("scrolledwindow2"))

        for mirror_file in Mirrors.MIRRORLISTS:
            mirror_listbox = MirrorListBox(mirror_file, self.settings)
            mirror_listbox.connect(
                "switch-activated", self.on_switch_activated)
            self.listboxes.append(mirror_listbox)

        for index, scrolled_window in enumerate(self.scrolledwindows):
            scrolled_window.add(self.listboxes[index])

        self.listboxes_box = self.ui.get_object("listboxes_box")

        self.use_rankmirrors = True
        self.use_listboxes = False

        # Boolean variable to check if rank_mirrors has already been run
        self.rank_mirrors_launched = False

    def on_switch_activated(self, _widget):
        """ A mirror has been activated/deactivated. We must check if
        at least there is one mirror active for each list """
        self.check_active_mirrors()

    def check_active_mirrors(self):
        """ Checks if at least there is one mirror active for each list """
        ok_to_proceed = True
        for listbox in self.listboxes:
            if not listbox.get_active_mirrors():
                ok_to_proceed = False
        self.forward_button.set_sensitive(ok_to_proceed)

    def on_rank_radiobutton_toggled(self, _widget):
        """ Use rankmirrors """
        self.use_rankmirrors = True
        self.use_listboxes = False
        self.forward_button.set_sensitive(True)
        # self.listboxes_box.hide()
        self.listboxes_box.set_sensitive(False)

    def on_leave_radiobutton_toggled(self, _widget):
        """ Do not modify mirror lists """
        self.use_rankmirrors = False
        self.use_listboxes = False
        self.forward_button.set_sensitive(True)
        # self.listboxes_box.hide()
        self.listboxes_box.set_sensitive(False)

    def on_user_radiobutton_toggled(self, _widget):
        """ Let user choose mirrorlist ordering """
        self.use_rankmirrors = False
        self.use_listboxes = True
        self.show_all()
        self.check_active_mirrors()
        self.listboxes_box.set_sensitive(True)

    def start_rank_mirrors(self):
        """ Launch rank mirrors process to optimize Arch and Antergos mirrorlists
            As user can come and go from/to this screen, we must get sure he/she
            has not already run Rankmirrors before """
        if not self.rank_mirrors_launched:
            logging.debug("Cnchi is ranking your mirrors lists...")
            parent_conn, child_conn = multiprocessing.Pipe(duplex=False)
            # Store parent_conn for later use in ask.py (rankmirrors dialog)
            proc = RankMirrors(self.settings, child_conn)
            proc.daemon = True
            proc.name = "rankmirrors"
            proc.start()
            self.process_list.append((proc, parent_conn))
            self.rank_mirrors_launched = True

    def prepare(self, direction):
        """ Prepares screen """
        self.translate_ui()
        self.show_all()
        # self.listboxes_box.hide()
        self.listboxes_box.set_sensitive(False)
        self.forward_button.set_sensitive(True)

    def translate_ui(self):
        """ Translates screen before showing it """
        self.header.set_subtitle(_("Mirrors Selection"))

        self.forward_button.set_always_show_image(True)
        self.forward_button.set_sensitive(True)

        #bold_style = '<span weight="bold">{0}</span>'

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
        intro_label.set_text(intro_txt)
        intro_label.set_name("intro_label")
        intro_label.set_hexpand(False)
        intro_label.set_line_wrap(True)

        intro_label.set_max_width_chars(80)

    def store_values(self):
        """ Store selected values """
        if self.use_rankmirrors:
            self.start_rank_mirrors()
        if self.use_listboxes:
            for listbox in self.listboxes:
                listbox.save_changes(self.use_rankmirrors)
        return True

    def get_next_page(self):
        """ Returns next page """
        return self.next_page
