#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  check.py
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

""" Check screen (detects if Antergos prerequisites are meet) """

from gi.repository import Gtk, GLib
import subprocess
import os
import logging
import canonical.gtkwidgets as gtkwidgets
import canonical.misc as misc

from gtkbasebox import GtkBaseBox

from rank_mirrors import AutoRankmirrorsThread

# Constants
NM = 'org.freedesktop.NetworkManager'
NM_STATE_CONNECTED_GLOBAL = 70
UPOWER = 'org.freedesktop.UPower'
UPOWER_PATH = '/org/freedesktop/UPower'
MIN_ROOT_SIZE = 4000000000

class Check(GtkBaseBox):
    """ Check class """
    def __init__(self, params):
        """ Init class ui """
        self.next_page = "location"
        self.prev_page = "language"

        self.testing = params['testing']

        super().__init__(params, "check")
        self.ui.connect_signals(self)

        self.remove_timer = False

        self.thread = None

        self.prepare_power_source = None
        self.prepare_network_connection = None
        self.prepare_enough_space = None
        self.timeout_id = None
        self.prepare_best_results = None

        self.add(self.ui.get_object("check"))

    def translate_ui(self):
        txt = _("System Check")
        #txt = '<span weight="bold" size="large">%s</span>' % txt
        #self.title.set_markup(txt)
        #self.header.set_title("Cnchi")
        self.header.set_subtitle(txt)

        self.prepare_enough_space = self.ui.get_object("prepare_enough_space")
        txt = _("has at least %dGB available storage space.") % int(MIN_ROOT_SIZE / 1000000000)
        txt += " (*)"
        self.prepare_enough_space.props.label = txt

        self.label_space = self.ui.get_object("label_space")
        txt = _("This highly depends on which desktop environment you choose, so you might need more space.")
        txt = "(*) <i>%s</i>" % txt
        self.label_space.set_markup(txt)

        self.prepare_power_source = self.ui.get_object("prepare_power_source")
        txt = _("is plugged in to a power source")
        self.prepare_power_source.props.label = txt

        self.prepare_network_connection = self.ui.get_object("prepare_network_connection")
        txt = _("is connected to the Internet")
        self.prepare_network_connection.props.label = txt

        self.prepare_best_results = self.ui.get_object("prepare_best_results")
        txt = _("For best results, please ensure that this computer:")
        txt = '<span weight="bold" size="large">%s</span>' % txt
        self.prepare_best_results.set_markup(txt)

    def check_all(self):
        has_internet = misc.has_connection()
        self.prepare_network_connection.set_state(has_internet)

        on_power = not self.on_battery()
        self.prepare_power_source.set_state(on_power)

        space = self.has_enough_space()
        self.prepare_enough_space.set_state(space)

        if has_internet and space:
            return True

        return False

    def on_battery(self):
        import dbus
        if self.has_battery():
            bus = dbus.SystemBus()
            upower = bus.get_object(UPOWER, UPOWER_PATH)
            return misc.get_prop(upower, UPOWER_PATH, 'OnBattery')

        return False

    def has_battery(self):
        # UPower doesn't seem to have an interface for this.
        path = '/sys/class/power_supply'
        if not os.path.exists(path):
            return False
        for folder in os.listdir(path):
            type_path = os.path.join(path, folder, 'type')
            if os.path.exists(type_path):
                with open(type_path) as power_file:
                    if power_file.read().startswith('Battery'):
                        return True
        return False

    def has_enough_space(self):
        lsblk = subprocess.Popen(["lsblk", "-lnb"], stdout=subprocess.PIPE)
        output = lsblk.communicate()[0].decode("utf-8").split("\n")

        max_size = 0

        for item in output:
            col = item.split()
            if len(col) >= 5:
                if col[5] == "disk" or col[5] == "part":
                    size = int(col[3])
                    if size > max_size:
                        max_size = size
        # we need 4GB
        #3221225472
        if max_size >= MIN_ROOT_SIZE:
            return True

        return False

    def on_timer(self):
        if not self.remove_timer:
            self.forward_button.set_sensitive(self.check_all())
        return not self.remove_timer

    def store_values(self):
        # remove timer
        self.remove_timer = True

        logging.info(_("We have Internet connection."))
        logging.info(_("We're connected to a power source."))
        logging.info(_("We have enough disk space."))

        # Enable forward button
        self.forward_button.set_sensitive(True)

        if not self.testing:
            # Launch reflector script to determine the 10 fastest mirrors
            self.thread = AutoRankmirrorsThread()
            self.thread.start()

        return True

    def prepare(self, direction):
        self.translate_ui()
        self.show_all()

        self.forward_button.set_sensitive(self.check_all())

        # set timer
        #self.timeout_id = GObject.timeout_add(1000, self.on_timer, None)
        self.timeout_id = GLib.timeout_add(1000, self.on_timer)

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message): return message

if __name__ == '__main__':
    from test_screen import _,run
    run('Check')
