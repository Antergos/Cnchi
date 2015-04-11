#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  countries.py
#
#  Copyright © 2013-2015 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

""" Reads countries json info """

# Thanks to Mohammed Le Doze (mledoze in GitHub) for collecting all this data in the countries.json file
# See https://mledoze.github.io/countries for more info

COUNTRIES_JSON = '/usr/share/cnchi/data/locale/countries.json'

import json
from pprint import pprint

class Countries():
    def __init__(self):
        with open(COUNTRIES_JSON) as data_file:
            self.data = json.load(data_file)
        # pprint(data)
    
    def are_the_same_country(self, name1, name2):
        """ Compares two country names (they can be in any language) """
        
        for country in self.data:
            found1 = False
            found2 = False
            
            official_name = country['name']['official']
            if name1 in official_name:
                found1 = True
            else:
                native_names = country['name']['native']
                for lang in native_names:
                    if name1 in native_names[lang]:
                        found1 = True
            
            if found1:
                if name2 in official_name:
                    found2 = True
                else:
                    native_names = country['name']['native']
                    for lang in native_names:
                        if name2 in native_names[lang]['official']:
                            found2 = True
                        elif name2 in native_names[lang]['common']:
                            found2 = True
            
            if found1 and found2:
                return True
        return False

countries = Countries()
print(countries.are_the_same_country('Finland', 'Suomi'))
print(countries.are_the_same_country('Spain', 'España'))
