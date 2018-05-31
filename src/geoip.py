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
import requests
import geoip2.database

class GeoIP(object):
    """ Store GeoIP information """

    CITY_DATABASE = '/usr/share/GeoIP/GeoLite2-City.mmdb'

    def __init__(self):
        self.myip = None
        self.reader = None
        self.response = None

        self.get_external_ip()
        if self.myip:
            self.load_database()
        else:
            logging.error("Cannot get your external IP address!")

    def get_external_ip(self):
        """ Get external IP """
        json_text = requests.get("http://ip.jsontest.com/").text
        data = json.loads(json_text)
        self.myip = data['ip']
        print(self.myip)

    def load_database(self):
        """ Loads cities database """
        self.reader = geoip2.database.Reader('/usr/share/GeoIP/GeoLite2-City.mmdb')
        self.response = self.reader.city(self.myip)

    def get_country(self):
        """ Return country based on ip """
        return self.response.country

    def get_city(self):
        """ Return city based on ip """
        #response = self.reader.city(self.myip)
        #print(response.country)
        #return response
        pass


def test_module():
    """ Test module """
    geo = GeoIP()
    print(geo.get_country())


if __name__ == "__main__":
    test_module()
