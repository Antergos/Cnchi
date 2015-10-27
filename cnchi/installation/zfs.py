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

try:
    from gtkbasebox import GtkBaseBox
except ImportError:
    import sys
    sys.path.append('/usr/share/cnchi/cnchi')
    from gtkbasebox import GtkBaseBox


class ZFS(GtkBaseBox):
    def __init__(self, params, prev_page="", next_page=""):
        super().__init__(self, params, "zfs", prev_page, next_page)

        self.page = self.ui.get_object('zfs')

        '''
        liststore
        pool_type_label
        pool_type_combo
        partition_scheme_label
        partition_scheme_combo
        scrolledwindow
        treeview
        password_check_lbl
        password_check_entry
        encrypt_swap_btn
        password_entry
        password_lbl
        encrypt_disk_btn
        swap_size_lbl
        swap_size_entry
        pool_name_btn
        pool_name_entry
        force_4k_btn
        '''

    def translate_ui(self):
        #lbl = self.ui.get_object('wireless_section_label')
        #lbl.set_markup(_("Connecting this computer to a wi-fi network"))

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

        combo = self.ui.get_object('pool_type_combo')
        combo.remove_all()
        combo.append_text(_("None"))
        combo.append_text(_("Stripe"))
        combo.append_text(_("Mirror"))
        combo.append_text(_("RAID-Z"))
        combo.append_text(_("RAID-Z2"))

        lbl = self.ui.get_object('partition_scheme_label')
        lbl.set_markup(_("Partition scheme"))

        combo = self.ui.get_object('partition_scheme_combo')
        combo.remove_all()
        combo.append_text(_("GPT"))
        combo.append_text(_("MBR"))

        lbl = self.ui.get_object('password_check_lbl')
        lbl.set_markup(_("Validate password"))

        lbl = self.ui.get_object('password_lbl')
        lbl.set_markup(_("Password"))

        lbl = self.ui.get_object('swap_size_lbl')
        lbl.set_markup(_("Swap size"))

        btn = self.ui.get_object('encrypt_swap_btn')
        btn.set_label(_("Encrypt swap"))

        btn = self.ui.get_object('encrypt_disk_btn')
        btn.set_label(_("Encrypt disk"))

        btn = self.ui.get_object('pool_name_btn')
        btn.set_label(_("Pool name"))

        btn = self.ui.get_object('force_4k_btn')
        btn.set_label(_("Force ZFS 4k block size"))

    def prepare(self, direction):
        self.translate_ui()
        self.show_all()

    def store_values():
        return True

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

if __name__ == '__main__':
    from test_screen import _, run
    run('zfs')
