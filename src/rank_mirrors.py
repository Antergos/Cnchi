#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rank_mirrors.py
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
#  
#  Antergos Team:
#   Alex Filgueira (faidoc) <alexfilgueira.antergos.com>
#   Gustau Castells (karasu) <karasu.antergos.com>
#   Alex Skinner (skinner) <skinner.antergos.com>
#   Kirill Omelchenko (omelcheck) <omelchek.antergos.com>
#  Manjaro Team:
#   Philip Müller (philm) <philm.manjaro.org>
#   Mateusz Mikołajczyk (toudi) <mikolajczyk.mateusz.gmail.com>

import threading
import multiprocessing
import subprocess
import logging
import time

NM = 'org.freedesktop.NetworkManager'
NM_STATE_CONNECTED_GLOBAL = 70
        
class AutoRankmirrorsThread(threading.Thread):
    def __init__(self):
        super(AutoRankmirrorsThread, self).__init__()
        self.rankmirrors_pid = None

    def get_prop(self, obj, iface, prop):
        import dbus
        try:
            return obj.Get(iface, prop, dbus_interface=dbus.PROPERTIES_IFACE)
        except dbus.DBusException as e:
            if e.get_dbus_name() == 'org.freedesktop.DBus.Error.UnknownMethod':
                return None
            else:
                raise
        
    def has_connection(self):
        import dbus
        try:
            bus = dbus.SystemBus()
            manager = bus.get_object(NM, '/org/freedesktop/NetworkManager')
            state = self.get_prop(manager, NM, 'state')
        except dbus.exceptions.DBusException:
            logging.warning(_("In rankmirrors, can't get network status"))
            return False
        return state == NM_STATE_CONNECTED_GLOBAL

    def run(self):
        # wait until there is an Internet connection available
        while not self.has_connection():
            time.sleep(2)  # Delay 

        # Run rankmirrors command
        try:
            self.rankmirrors_pid = subprocess.Popen(["/usr/share/cnchi/scripts/rankmirrors-script"]).pid
        except subprocess.CalledProcessError as e:
            logging.error(_("Couldn't execute auto mirroring selection"))
        
