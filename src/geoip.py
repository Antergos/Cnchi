#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  geoip.py
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

""" GeoIP Location module
    Needs python-geoip2 python-maxminddb geoip2-database """

import json
import logging
import os
import time
import requests

import maxminddb
import geoip2.database
import misc.extra as misc

class GeoIP():
    """ Store GeoIP information """

    REPO_CITY_DATABASE = '/usr/share/GeoIP/GeoLite2-City.mmdb'
    LOCAL_CITY_DATABASE = '/usr/share/cnchi/data/GeoLite2-City.mmdb'

    SERVERS = ["moc.tsetnosj.pi", "pi/0003:kt.ateb-sogretna"]

    def __init__(self):
        self.record = None
        self._maybe_wait_for_network()
        self._load_data_and_ip()

    @staticmethod
    def _maybe_wait_for_network():
        # Wait until there is an Internet connection available
        if not misc.has_connection():
            logging.warning(
                "Can't get network status. Cnchi will try again in a moment")
            while not misc.has_connection():
                time.sleep(4)  # Wait 4 seconds and try again

        logging.debug("A working network connection has been detected.")

    def _load_data_and_ip(self):
        """ Gets public IP and loads GeoIP2 database """
        db_path = GeoIP.REPO_CITY_DATABASE
        if not os.path.exists(db_path):
            db_path = GeoIP.LOCAL_CITY_DATABASE

        if os.path.exists(db_path):
            myip = self._get_external_ip()
            logging.debug("Your external IP address is: %s", myip)
            if myip:
                self._load_database(db_path, myip)
                if self.record:
                    logging.debug("GeoIP database loaded (%s)", db_path)
            else:
                logging.error("Cannot get your external IP address!")
        else:
            logging.error("Cannot find Cities GeoIP database")


    @staticmethod
    def _get_external_ip():
        """ Get external IP """
        for srv in GeoIP.SERVERS:
            srv = "http://" + srv[::-1]
            try:
                json_text = requests.get(srv).text
                if not "503 Over Quota" in json_text:
                    data = json.loads(json_text)
                    return data['ip']
            except (requests.ConnectionError, json.decoder.JSONDecodeError) as err:
                logging.warning(
                    "Error getting external IP from %s: %s", srv, err)
        return None

    def _load_database(self, db_path, myip):
        """ Loads cities database """
        try:
            reader = geoip2.database.Reader(db_path)
            self.record = reader.city(myip)
        except maxminddb.errors.InvalidDatabaseError as err:
            logging.error(err)

    def get_city(self):
        """ Returns city information
            'city': {'geoname_id', 'names'} """
        if self.record:
            return self.record.city
        return None

    def get_country(self):
        """ Returns country information
            'country': {'geoname_id', 'is_in_european_union', 'iso_code', 'names'} """
        if self.record:
            return self.record.country
        return None

    def get_continent(self):
        """ Returns continent information
            'continent': {'code', 'geoname_id', 'names'} """
        if self.record:
            return self.record.continent
        return None

    def get_location(self):
        """ Returns location information
            'location': {'accuracy_radius', 'latitude', 'longitude', 'time_zone'} """
        if self.record:
            return self.record.location
        return None



def test_module():
    """ Test module """
    geo = GeoIP()
    print("City:", geo.get_city())
    print("Country:", geo.get_country())
    print("Continent:", geo.get_continent())
    print("Location:", geo.get_location())


if __name__ == "__main__":
    test_module()
