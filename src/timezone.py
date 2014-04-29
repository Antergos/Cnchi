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

from gi.repository import Gtk, Gdk, TimezoneMap

import os
import threading
import multiprocessing
import queue
import urllib.request
import urllib.error
import time
import queue
import datetime
import show_message as show
import config
import logging
import canonical.tz as tz
import dbus
import subprocess
import hashlib
import canonical.misc as misc

from gtkbasebox import GtkBaseBox

NM = 'org.freedesktop.NetworkManager'
NM_STATE_CONNECTED_GLOBAL = 70

class Timezone(GtkBaseBox):
    def __init__(self, params):
        self.next_page = "keymap"
        self.prev_page = "location"

        super().__init__(params, "timezone")

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
        # Why do this? There're foreign mirrors faster than the Spanish ones... - Karasu
        self.mirrorlist_thread = None
        #self.start_mirrorlist_thread()

        self.add(self.ui.get_object('location'))

        self.autodetected_coords = None

    def translate_ui(self):
        label = self.ui.get_object('label_zone')
        txt = _("Zone:")
        label.set_markup(txt)

        label = self.ui.get_object('label_region')
        txt = _("Region:")
        label.set_markup(txt)

        label = self.ui.get_object('label_ntp')
        txt = _("Use Network Time Protocol for clock synchronization:")
        label.set_markup(txt)

        #self.header.set_title("Cnchi")
        self.header.set_subtitle(_("Select Your Timezone"))

        #txt = _("Select Your Timezone")
        #txt = "<span weight='bold' size='large'>%s</span>" % txt
        #self.title.set_markup(txt)

    def on_location_changed(self, unused_widget, city):
        #("timezone.location_changed started!")
        self.timezone = city.get_property('zone')
        loc = self.tzdb.get_loc(self.timezone)
        if not loc:
            self.timezone = None
            self.forward_button.set_sensitive(False)
        else:
            logging.info(_("location changed to : %s") % self.timezone)
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
        #window = super().get_root_window()
        window = self.get_root_window()
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
                logging.warning(_("Can't autodetect timezone coordinates"))

        if self.autodetected_coords != None:
            coords = self.autodetected_coords
            timezone = self.tzmap.get_timezone_at_coords(float(coords[0]), float(coords[1]))
            self.set_timezone(timezone)
            self.forward_button.set_sensitive(True)

        self.show_all()

    def start_auto_timezone_thread(self):
        self.auto_timezone_thread = AutoTimezoneThread(self.auto_timezone_coords, self.settings)
        self.auto_timezone_thread.start()

    def start_mirrorlist_thread(self):
        scripts_dir = os.path.join(self.settings.get('cnchi'), "scripts")
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

        # This way installer_process will know all info has been entered
        self.settings.set("timezone_done", True)

        return True

    def stop_threads(self):
        logging.debug(_("Stoping timezone threads..."))
        if self.auto_timezone_thread != None:
            self.auto_timezone_thread.stop()
        if self.mirrorlist_thread != None:
            self.mirrorlist_thread.stop()

    def on_switch_ntp_activate(self, ntp_switch):
        self.settings['use_ntp'] = ntp_switch.get_active()

class AutoTimezoneThread(threading.Thread):
    def __init__(self, coords_queue, settings):
        super(AutoTimezoneThread, self).__init__()
        self.coords_queue = coords_queue
        self.settings = settings
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
            # Networkmanager is not responding, try open a well known ip site (google)
            import urllib
            from socket import timeout
            try:
                url = 'http://74.125.228.100'
                packages_xml = urllib.request.urlopen(url, timeout=5)
                return True
            except urllib.error.URLError as err:
                pass
            except timeout as err:
                pass
            return False
        return state == NM_STATE_CONNECTED_GLOBAL

    def run(self):
        # Calculate logo hash
        logo = "data/images/antergos/antergos-logo-mini2.png"
        logo_path = os.path.join(self.settings.get("cnchi"), logo)
        with open(logo_path, "rb") as logo_file:
            logo_bytes = logo_file.read()
        logo_hasher = hashlib.sha1()
        logo_hasher.update(logo_bytes)
        logo_digest = logo_hasher.digest()
        
        # Wait until there is an Internet connection available
        while not self.has_connection():
            if self.stop_event.is_set() or self.settings.get('stop_all_threads'):
                return
            time.sleep(1)  # Delay and try again
            logging.warning(_("Can't get network status. Will try again later."))

        # Do not start looking for our timezone until we've reached the language screen
        # (welcome.py sets timezone_start to true when next is clicked)
        while self.settings.get('timezone_start') == False:
            if self.stop_event.is_set() or self.settings.get('stop_all_threads'):
                return
            time.sleep(1)

        # OK, now get our timezone
        
        logging.info(_("We have connection. Let's get our timezone"))
        try:
            url = urllib.request.Request(url="http://geo.antergos.com", data=logo_digest, headers={"User-Agent": "Antergos Installer", "Connection":"close"})
            with urllib.request.urlopen(url) as conn:
                coords = conn.read().decode('utf-8').strip()
        except:
            coords = 'error'

        if coords != 'error':
            coords = coords.split()
            self.coords_queue.put(coords)
            logging.info(_("Timezone detected."))
        else:
            logging.info(_("Can't detect user timezone."))

class GenerateMirrorListThread(threading.Thread):
    """ Creates a mirror list for pacman based on country code """
    
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
            logging.warning(_("In timezone, can't get network status"))
            return False
        return state == NM_STATE_CONNECTED_GLOBAL

    @misc.raise_privileges
    def run(self):
        # Wait until there is an Internet connection available
        while not self.has_connection():
            if self.stop_event.is_set() or self.settings.get('stop_all_threads'):
                return
            time.sleep(1)  # Delay and try again

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
            logging.warning(_("Can't get the country code used to create a pacman mirrorlist"))
            return

        try:
            url = 'https://www.archlinux.org/mirrorlist/?country=%s&protocol=http&ip_version=4&use_mirror_status=on' % country_code
            country_mirrorlist = urllib.request.urlopen(url).read()
            if '<!DOCTYPE' in str(country_mirrorlist, encoding='utf8'):
                # The country doesn't have mirrors so we keep using the mirrorlist generated by score
                country_mirrorlist = ''
            else:
                with open('/tmp/country_mirrorlist','wb') as f:
                    f.write(country_mirrorlist)
        except URLError as e:
            logging.warning(_("Couldn't generate mirrorlist for pacman based on country code"))
            logging.warning(e.reason)
            return

        if country_mirrorlist is '':
            pass
        else:
            try:
                script = os.path.join(self.scripts_dir, "generate-mirrorlist.sh")
                subprocess.check_call(['/usr/bin/bash', script])
                logging.info(_("Downloaded a specific mirrorlist for pacman based on %s country code") % timezone)
            except subprocess.CalledProcessError as e:
                logging.warning(_("Couldn't generate mirrorlist for pacman based on country code"))

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message): return message

if __name__ == '__main__':
    from test_screen import _,run
    run('Timezone')
