# -*- coding: utf-8; Mode: Python; indent-tabs-mode: nil; tab-width: 4 -*-
#
# Copyright (C) 2010 Canonical Ltd.
# Written by Evan Dandrea <evan.dandrea@canonical.com>
#
# Copyright (C) 2014 Antergos
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
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

import os
import dbus
from gi.repository import Gtk
from canonical import misc, nm

from gtkbasebox import GtkBaseBox

NAME = 'wireless'

WEIGHT = 12

class Wireless(GtkBaseBox):
    def __init__(self, params):

        self.next_page = "desktop"
        self.prev_page = "check"

        # Check whether we can talk to NM at all
        try:
            misc.has_connection()
        except dbus.DBusException:
            self.page = None
            return

        super().__init__(params, "wireless")

        self.ui.connect_signals(self)

        self.page = self.ui.get_object('wireless')
        self.nmwidget = self.ui.get_object('nmwidget')
        self.nmwidget.connect('connection', self.state_changed)
        self.nmwidget.connect('selection_changed', self.selection_changed)
        self.nmwidget.connect('pw_validated', self.pw_validated)
        self.no_wireless = self.ui.get_object('no_wireless')
        self.use_wireless = self.ui.get_object('use_wireless')
        self.use_wireless.connect('toggled', self.wireless_toggled)
        self.plugin_widgets = self.page
        self.have_selection = False
        self.state = self.nmwidget.get_state()
        self.next_normal = True
        self.back_normal = True
        self.connect_text = None
        self.stop_text = None
        self.skip = False
        
        self.add(self.ui.get_object("wireless"))

    def plugin_translate(self, lang):
        pass
        # get_s = self.controller.get_string
        # label_text = get_s('ubiquity/text/wireless_password_label')
        # display_text = get_s('ubiquity/text/wireless_display_password')
        # self.nmwidget.translate(label_text, display_text)

        # self.connect_text = get_s('ubiquity/text/connect', lang)
        # self.stop_text = get_s('ubiquity/text/stop', lang)
        # frontend = self.controller._wizard
        # if not self.next_normal:
        #     frontend.next.set_label(self.connect_text)
        # if not self.back_normal:
        #     frontend.back.set_label(self.stop_text)

    def selection_changed(self, unused):
        self.have_selection = True
        self.use_wireless.set_active(True)
        assert self.state is not None
        '''
        frontend = self.controller._wizard
        if self.state == nm.NM_STATE_CONNECTING:
            frontend.translate_widget(frontend.next)
            self.next_normal = True
        else:
            if (not self.nmwidget.is_row_an_ap() or
                    self.nmwidget.is_row_connected()):
                frontend.translate_widget(frontend.next)
                self.next_normal = True
            else:
                frontend.next.set_label(self.connect_text)
                self.next_normal = False
        '''

    def wireless_toggled(self, unused):
        print("wireless_toggled")
        '''
        frontend = self.controller._wizard
        if self.use_wireless.get_active():
            if not self.have_selection:
                self.nmwidget.select_usable_row()
            self.state_changed(None, self.state)
        else:
            frontend.connecting_spinner.hide()
            frontend.connecting_spinner.stop()
            frontend.connecting_label.hide()
            frontend.translate_widget(frontend.next)
            self.nmwidget.hbox.set_sensitive(False)
            self.next_normal = True
            self.controller.allow_go_forward(True)
        '''

    def plugin_set_online_state(self, online):
        self.skip = online

    def plugin_skip_page(self):
        if not nm.wireless_hardware_present():
            return True
        else:
            return self.skip

    '''
    def plugin_on_back_clicked(self):
        frontend = self.controller._wizard
        if frontend.back.get_label() == self.stop_text:
            self.nmwidget.disconnect_from_ap()
            return True
        else:
            frontend.connecting_spinner.hide()
            frontend.connecting_spinner.stop()
            frontend.connecting_label.hide()
            self.no_wireless.set_active(True)
            return False

    def plugin_on_next_clicked(self):
        frontend = self.controller._wizard
        if frontend.next.get_label() == self.connect_text:
            self.nmwidget.connect_to_ap()
            return True
        else:
            frontend.connecting_spinner.hide()
            frontend.connecting_spinner.stop()
            frontend.connecting_label.hide()
            return False
    '''
    def state_changed(self, unused, state):
        print("state_changed")
        '''
        self.state = state
        frontend = self.controller._wizard
        if not self.use_wireless.get_active():
            return
        if state != nm.NM_STATE_CONNECTING:
            frontend.connecting_spinner.hide()
            frontend.connecting_spinner.stop()
            frontend.connecting_label.hide()
            self.controller.allow_go_forward(True)

            frontend.translate_widget(frontend.back)
            self.back_normal = True
            frontend.back.set_sensitive(True)
        else:
            frontend.connecting_spinner.show()
            frontend.connecting_spinner.start()
            frontend.connecting_label.show()

            self.next_normal = True

            frontend.back.set_label(self.stop_text)
            self.back_normal = False
            frontend.back.set_sensitive(True)
        self.selection_changed(None)
        '''

    def pw_validated(self, unused, validated):
        pass
        #self.controller.allow_go_forward(validated)

    def prepare(self, direction):
        self.show_all()

    def store_values(self):
        return True

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message): return message

if __name__ == '__main__':
    from test_screen import _,run
    run('Wireless')
