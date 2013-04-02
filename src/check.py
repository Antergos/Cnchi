#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  check.py
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

from gi.repository import Gtk, GObject

import subprocess
import os
import gtkwidgets
import log

from rank_mirrors import AutoRankmirrorsThread

NM = 'org.freedesktop.NetworkManager'
NM_STATE_CONNECTED_GLOBAL = 70

UPOWER = 'org.freedesktop.UPower'
UPOWER_PATH = '/org/freedesktop/UPower'

_next_page = "installation_ask"
_prev_page = "location"

class Check(Gtk.Box):

    def __init__(self, params):

        self.title = params['title']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']

        super().__init__()

        self.ui = Gtk.Builder()

        self.ui.add_from_file(os.path.join(self.ui_dir, "check.ui"))
        self.ui.connect_signals(self)

        self.remove_timer = False

        super().add(self.ui.get_object("check"))

    def translate_ui(self):
        txt = _("Check your computer")
        txt = '<span weight="bold" size="large">%s</span>' % txt
        self.title.set_markup(txt)

        self.prepare_sufficient_space = self.ui.get_object("prepare_sufficient_space")
        txt = _("has at least 3GB available drive space")
        self.prepare_sufficient_space.props.label = txt

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

    def get_prop(self, obj, iface, prop):
        try:
            import dbus
            return obj.Get(iface, prop, dbus_interface=dbus.PROPERTIES_IFACE)
        except dbus.DBusException as e:
            if e.get_dbus_name() == 'org.freedesktop.DBus.Error.UnknownMethod':
                return None
            else:
                raise

    def has_connection(self):
        try:
            import dbus
            bus = dbus.SystemBus()
            manager = bus.get_object(NM, '/org/freedesktop/NetworkManager')
            state = self.get_prop(manager, NM, 'state')
        except dbus.exceptions.DBusException:
            log.debug(_("Can't get network status"))
            return False
        return state == NM_STATE_CONNECTED_GLOBAL

    def check_all(self):
        has_internet = self.has_connection()
        self.prepare_network_connection.set_state(has_internet)       

        on_power = not self.on_battery()
        self.prepare_power_source.set_state(on_power)
        
        space = self.has_enough_space()
        self.prepare_sufficient_space.set_state(space)

        if has_internet and on_power and space:
            return True

        return False

    def on_battery(self):
        import dbus
        if self.has_battery():
            bus = dbus.SystemBus()
            upower = bus.get_object(UPOWER, UPOWER_PATH)
            return self.get_prop(upower, UPOWER_PATH, 'OnBattery')

        return False

    def has_battery(self):
        # UPower doesn't seem to have an interface for this.
        path = '/sys/class/power_supply'
        if not os.path.exists(path):
            return False
        for d in os.listdir(path):
            p = os.path.join(path, d, 'type')
            if os.path.exists(p):
                with open(p) as fp:
                    if fp.read().startswith('Battery'):
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
        # we need 3GB
        if max_size >= 3221225472:
            return True

        return False

    def on_timer(self, time):
        if not self.remove_timer:
            self.forward_button.set_sensitive(self.check_all())
        return not self.remove_timer

    def store_values(self):
        # remove timer
        self.remove_timer = True

        log.debug(_("We have Internet connection."))
        log.debug(_("We're connected to a power source."))
        log.debug(_("We have enough space in disk."))
          
        # Enable forward button
        self.forward_button.set_sensitive(True)
        
        ## Launch rankmirrors script to determine the 5 fastest mirrors
        self.thread = None
        self.thread = AutoRankmirrorsThread()
        self.thread.start()
        return True

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page

    def prepare(self, direction):
        self.translate_ui()
        self.show_all()
        self.forward_button.set_sensitive(self.check_all())
        # set timer
        self.timeout_id = GObject.timeout_add(1000, self.on_timer, None)
