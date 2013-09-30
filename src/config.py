#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  config.py
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
#  Cnchi (Antergos) Team:
#   Alex Filgueira (faidoc) <alexfilgueira.antergos.com>
#   Gustau Castells (karasu) <karasu.antergos.com>
#   Alex Skinner (skinner) <skinner.antergos.com>
#   Kirill Omelchenko (omelcheck) <omelchek.antergos.com>

#import queue
from multiprocessing import Queue

class Settings():
    def __init__(self):
        # Create a queue one element size

        self.settings = Queue(1)

        self.settings.put( { \
            'CNCHI_DIR' : '/usr/share/cnchi/', \
            'UI_DIR' : '/usr/share/cnchi/ui/', \
            'DATA_DIR' : '/usr/share/cnchi/data/', \
            'TMP_DIR' : '/tmp', \
            'language_name' : '', \
            'language_code' : '', \
            'locale' : '', \
            'keyboard_layout' : '', \
            'keyboard_variant' : '', \
            'timezone_human_zone' : '', \
            'timezone_country' : '', \
            'timezone_zone' : '', \
            'timezone_human_country' : '', \
            'timezone_comment' : '', \
            'timezone_latitude' : 0, \
            'timezone_longitude' : 0, \
            'timezone_done' : False, \
            'use_ntp' : True, \
            'install_bootloader' : True, \
            'bootloader_device' : '/dev/sda', \
            'bootloader_type' : 'GRUB2', \
            'force_grub_type' : False, \
            'third_party_software' : False, \
            'desktops' : [], \
            'desktop' : 'gnome', \
            'partition_mode' : 'easy', \
            'auto_device' : '/dev/sda', \
            'log_file' : '/tmp/cnchi.log', \
            'fullname' : '', \
            'hostname' : 'antergos', \
            'username' : '', \
            'password' : '', \
            'require_password' : True, \
            'encrypt_home' : False, \
            'user_info_done' : False, \
            'rankmirrors_done' : False, \
            'use_aria2' : False, \
            'feature_bluetooth' : False, \
            'feature_cups' : False, \
            'feature_office' : False, \
            'feature_visual' : False, \
            'feature_firewall' : False, \
            'feature_third_party' : False })

    def _get_settings(self):
        gd = self.settings.get()
        d = gd.copy()
        self.settings.put(gd)
        return d

    def _update_settings(self, d):
        gd = self.settings.get()
        try:
            gd.update(d)
        finally:
            self.settings.put(gd)
        
    def get(self, key):
        d = self._get_settings()
        return d[key]
        
    def set(self, key, value):
        d = self._get_settings()
        d[key] = value
        self._update_settings(d)
