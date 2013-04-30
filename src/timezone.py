#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  timezone.py
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
#   Raúl Granados (pollitux) <raulgranados.antergos.com>
#   Gustau Castells (karasu) <karasu.antergos.com>
#   Kirill Omelchenko (omelcheck) <omelchek.antergos.com>
#   Marc Miralles (arcnexus) <arcnexus.antergos.com>
#   Alex Skinner (skinner) <skinner.antergos.com>

from gi.repository import Gtk, Gdk, TimezoneMap

import os
import threading
import multiprocessing
import queue
import urllib.request
import time
import queue
import datetime
import show_message as show
import config
import log
import tz
import dbus
import subprocess
from urllib.request import urlopen
import misc

_geoname_url = 'http://geoname-lookup.ubuntu.com/?query=%s&release=%s'

_next_page = "keymap"
_prev_page = None

NM = 'org.freedesktop.NetworkManager'
NM_STATE_CONNECTED_GLOBAL = 70

class Timezone(Gtk.Box):

    def __init__(self, params):
        self.title = params['title']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        self.settings = params['settings']
        
        super().__init__()

        self.ui = Gtk.Builder()
        self.ui.add_from_file(os.path.join(self.ui_dir, "timezone.ui"))
        self.ui.connect_signals(self)

        self.map_window = self.ui.get_object('timezone_map_window')

        self.combobox_zone = self.ui.get_object('comboboxtext_zone')
        self.combobox_region = self.ui.get_object('comboboxtext_region')

        # Show regions in three columns
        self.combobox_region.set_wrap_width(3)

        self.tzdb = tz.Database()
        self.timezone = None

        # this is for populate_cities
        self.old_zone = None

        # setup window
        self.tzmap = TimezoneMap.TimezoneMap()
        self.tzmap.connect('location-changed', self.on_location_changed)

        # Strip .UTF-8 from locale, icu doesn't parse it
        self.locale = os.environ['LANG'].rsplit('.', 1)[0]

        self.map_window.add(self.tzmap)
        self.tzmap.show()

        # autotimezone thread will store detected coords in this queue
        self.auto_timezone_coords = multiprocessing.Queue()

        # thread to try to determine timezone.
        self.auto_timezone_thread = None
        self.start_auto_timezone_thread()
        
        # thread to generate a pacman mirrorlist based on country code
        self.mirrorlist_thread = None
        self.start_mirrorlist_thread()

        super().add(self.ui.get_object('location'))

        self.autodetected_coords = None

    def translate_ui(self):
        txt = _("Where are you?")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.title.set_markup(txt)

        label = self.ui.get_object('label_zone')
        txt = _("Zone:")
        label.set_markup(txt)

        label = self.ui.get_object('label_region')
        txt = _("Region:")
        label.set_markup(txt)

    def on_location_changed(self, unused_widget, city):
        #("timezone.location_changed started!")
        self.timezone = city.get_property('zone')
        loc = self.tzdb.get_loc(self.timezone)
        if not loc:
            self.timezone = None
            self.forward_button.set_sensitive(False)
        else:
            log.debug(_("location changed to : %s") % self.timezone)
            self.update_comboboxes(self.timezone)
            self.forward_button.set_sensitive(True)

    def update_comboboxes(self, timezone):
        zone, region = timezone.split('/', 1)
        self.select_combobox_item(self.combobox_zone, zone)
        self.populate_cities(zone)
        self.select_combobox_item(self.combobox_region, region)

    def select_combobox_item(self, combobox, item):
        tree_model = combobox.get_model()
        tree_iter = tree_model.get_iter_first()

        while tree_iter != None:
            value = tree_model.get_value(tree_iter, 0)
            if value == item:
                combobox.set_active_iter(tree_iter)
                tree_iter = None
            else:
                tree_iter = tree_model.iter_next(tree_iter)

    def set_timezone(self, timezone):
        self.timezone = timezone
        self.tzmap.set_timezone(timezone)
        self.forward_button.set_sensitive(True)

    def on_zone_combobox_changed(self, widget):
        new_zone = self.combobox_zone.get_active_text()
        if new_zone is not None:
            self.populate_cities(new_zone)

    def on_region_combobox_changed(self, widget):
        new_zone = self.combobox_zone.get_active_text()
        new_region = self.combobox_region.get_active_text()
        if new_zone != None and new_region != None:
            self.set_timezone("{0}/{1}".format(new_zone, new_region))

    def populate_zones(self):
        zones = []
        for loc in self.tzdb.locations:
            zone = loc.zone.split('/', 1)[0]
            if not zone in zones:
                zones.append(zone)
        zones.sort()
        tree_model = self.combobox_zone.get_model()
        tree_model.clear()
        for z in zones:
            tree_model.append([z, z])

    def populate_cities(self, selected_zone):
        if self.old_zone != selected_zone:
            regions = []
            for loc in self.tzdb.locations:
                zone, region = loc.zone.split('/', 1)
                if zone == selected_zone:
                    regions.append(region)
            regions.sort()
            tree_model = self.combobox_region.get_model()
            tree_model.clear()
            for r in regions:
                tree_model.append([r, r])
            self.old_zone = selected_zone

    def refresh(self):
        while Gtk.events_pending():
            Gtk.main_iteration()

    def set_cursor(self, cursor_type):
        cursor = Gdk.Cursor(cursor_type)
        window = super().get_root_window()

        if window:
            window.set_cursor(cursor)
            self.refresh()

    def prepare(self, direction):
        self.translate_ui()
        self.populate_zones()
        self.timezone = None
        self.forward_button.set_sensitive(False)
        tr = 0
        if self.autodetected_coords is None:
            try:
                self.autodetected_coords = self.auto_timezone_coords.get(False, timeout=20)
                # Put the coords again in the queue (in case GenerateMirrorList still needs them)
                #self.autodetected_coords.put_nowait(self.autodetected_coords)
            except queue.Empty:
                log.debug(_("Can't autodetect timezone coordinates"))

        if self.autodetected_coords != None:
            coords = self.autodetected_coords
            timezone = self.tzmap.get_timezone_at_coords(float(coords[0]), float(coords[1]))
            self.set_timezone(timezone)
            self.forward_button.set_sensitive(True)

        # restore forward button text (from install now! to next)
        self.forward_button.set_label("gtk-go-forward")
        
        self.show_all()

    def start_auto_timezone_thread(self):
        self.auto_timezone_thread = AutoTimezoneThread(self.auto_timezone_coords)
        self.auto_timezone_thread.start()

    def start_mirrorlist_thread(self):
        scripts_dir = os.path.join(self.settings.get("CNCHI_DIR"), "scripts")
        self.mirrorlist_thread = GenerateMirrorListThread(self.auto_timezone_coords, scripts_dir)
        self.mirrorlist_thread.start()

    def store_values(self):
        loc = self.tzdb.get_loc(self.timezone)
        
        if loc:
            self.settings.set("timezone_human_zone", loc.human_zone)
            self.settings.set("timezone_country", loc.country)
            self.settings.set("timezone_zone", loc.zone)
            self.settings.set("timezone_human_country", loc.human_country)

            if loc.comment:
                self.settings.set("timezone_comment", loc.comment)
            else:
                self.settings.set("timezone_comment", "")

            if loc.latitude:
                self.settings.set("timezone_latitude", loc.latitude)
            else:
                self.settings.set("timezone_latitude", "")

            if loc.longitude:
                self.settings.set("timezone_longitude", loc.longitude)
            else:
                self.settings.set("timezone_longitude", "")

        # this way installer_thread will know all info has been entered
        self.settings.set("timezone_done", True)
        
        return True

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page
        
    def stop_thread(self):
        log.debug(_("Stoping timezone threads..."))
        self.auto_timezone_thread.stop()
        self.mirrorlist_thread.stop()

class AutoTimezoneThread(threading.Thread):
    def __init__(self, coords_queue):
        super(AutoTimezoneThread, self).__init__()
        self.coords_queue = coords_queue
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def get_prop(self, obj, iface, prop):
        try:
            return obj.Get(iface, prop, dbus_interface=dbus.PROPERTIES_IFACE)
        except dbus.DBusException as e:
            if e.get_dbus_name() == 'org.freedesktop.DBus.Error.UnknownMethod':
                return None
            else:
                raise
        
    def has_connection(self):
        try:
            bus = dbus.SystemBus()
            manager = bus.get_object(NM, '/org/freedesktop/NetworkManager')
            state = self.get_prop(manager, NM, 'state')
        except dbus.exceptions.DBusException:
            log.debug(_("In timezone, can't get network status"))
            return False
        return state == NM_STATE_CONNECTED_GLOBAL

    def run(self):
        # wait until there is an Internet connection available
        while not self.has_connection():
            time.sleep(2)  # Delay and try again
            if self.stop_event.is_set():
                return

        # ok, now get our timezone

        try:
            url = "http://geo.antergos.com"
            conn = urllib.request.urlopen(url)
            coords = conn.read().decode('utf-8').strip()
        except:
            coords = 'error'
        
        if coords != 'error':
            coords = coords.split()
            self.coords_queue.put(coords)

# Creates a mirror list for pacman based on country code
class GenerateMirrorListThread(threading.Thread):
    def __init__(self, coords_queue, scripts_dir):
        super(GenerateMirrorListThread, self).__init__()
        self.coords_queue = coords_queue
        self.scripts_dir = scripts_dir
        self.stop_event = threading.Event()
        self.tzdb = tz.Database()

    def stop(self):
        self.stop_event.set()

    def get_prop(self, obj, iface, prop):
        try:
            return obj.Get(iface, prop, dbus_interface=dbus.PROPERTIES_IFACE)
        except dbus.DBusException as e:
            if e.get_dbus_name() == 'org.freedesktop.DBus.Error.UnknownMethod':
                return None
            else:
                raise
        
    def has_connection(self):
        try:
            bus = dbus.SystemBus()
            manager = bus.get_object(NM, '/org/freedesktop/NetworkManager')
            state = self.get_prop(manager, NM, 'state')
        except dbus.exceptions.DBusException:
            log.debug(_("In timezone, can't get network status"))
            return False
        return state == NM_STATE_CONNECTED_GLOBAL

    @misc.raise_privileges
    def run(self):
        # wait until there is an Internet connection available
        while not self.has_connection():
            time.sleep(2)  # Delay and try again
            if self.stop_event.is_set():
                return

        timezone = ""
        
        try:
            coords = self.coords_queue.get(True)
            self.coords_queue.put_nowait(coords)
            tzmap = TimezoneMap.TimezoneMap()
            timezone = tzmap.get_timezone_at_coords(float(coords[0]), float(coords[1]))
            loc = self.tzdb.get_loc(timezone)
            country_code = ''
            if loc:
                country_code = loc.country
        except (queue.Empty, IndexError) as e:
            log.debug(_("Can't get the country code used to create a pacman mirrorlist"))

        try:
            url = 'https://www.archlinux.org/mirrorlist/?country=%s&protocol=http&ip_version=4&use_mirror_status=on' % country_code
            country_mirrorlist = urlopen(url).read()
            if '<!DOCTYPE' in str(country_mirrorlist, encoding='utf8'):
                # The country doesn't have mirrors so we keep using the mirrorlist generated by score
                country_mirrorlist = ''
            else:
                with open('/tmp/country_mirrorlist','wb') as f:
                    f.write(country_mirrorlist)
        except URLError as e:
            self.queue_event('error', "Can't retrieve country mirrorlist.")

        try:
            if country_mirrorlist is '':
                pass
            else:
                script = os.path.join(self.scripts_dir, "generate-mirrorlist.sh")
                subprocess.check_call(['/bin/bash', script])
                log.debug(_("Downloaded a specific mirrorlist for pacman based on %s country code") % timezone)
        except subprocess.CalledProcessError as e:
            print(_("Couldn't generate mirrorlist for pacman based on country code"))
        
        
