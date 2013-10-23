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

from multiprocessing import Queue

class Settings():
    def __init__(self):
        # Create a one element size queue

        self.settings = Queue(1)

        self.settings.put( { \
            'auto_device' : '/dev/sda', \
            'bootloader_device' : '/dev/sda', \
            'bootloader_type' : 'GRUB2', \
            'cache' : '', \
            'cnchi' : '/usr/share/cnchi/', \
            'data' : '/usr/share/cnchi/data/', \
            'desktop' : 'gnome', \
            'desktops' : [], \
            'encrypt_home' : False, \
            'feature_bluetooth' : False, \
            'feature_cups' : False, \
            'feature_office' : False, \
            'feature_visual' : False, \
            'feature_firewall' : False, \
            'feature_third_party' : False, \
            'force_grub_type' : False, \
            'fullname' : '', \
            'hostname' : 'antergos', \
            'install_bootloader' : True, \
            'keyboard_layout' : '', \
            'keyboard_variant' : '', \
            'language_name' : '', \
            'language_code' : '', \
            'locale' : '', \
            'log_file' : '/tmp/cnchi.log', \
            'luks_key_pass' : "", \
            'partition_mode' : 'easy', \
            'password' : '', \
            'rankmirrors_done' : False, \
            'require_password' : True, \
            'third_party_software' : False, \
            'timezone_human_zone' : '', \
            'timezone_country' : '', \
            'timezone_zone' : '', \
            'timezone_human_country' : '', \
            'timezone_comment' : '', \
            'timezone_latitude' : 0, \
            'timezone_longitude' : 0, \
            'timezone_done' : False, \
            'tmp' : '/tmp', \
            'ui' : '/usr/share/cnchi/ui/', \
            'use_aria2' : False, \
            'use_luks' : False, \
            'use_lvm' : False, \
            'use_ntp' : True, \
            'user_info_done' : False, \
            'username' : '' })

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
