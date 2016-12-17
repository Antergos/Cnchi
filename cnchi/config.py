#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pacman_conf.py
#
#  Copyright © 2013-2016 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  The following additional terms are in effect as per Section 7 of the license:
#
#  The preservation of all legal notices and author attributions in
#  the material or in the Appropriate Legal Notices displayed
#  by works containing it is required.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; If not, see <http://www.gnu.org/licenses/>.


""" Configuration module for Cnchi """

import multiprocessing
import os
import strictyaml as yaml
from strictyaml.validators import CommentedMap


class ConfigLoader:
    config_path = '/etc/cnchi.yml'
    config_path_fallback = '/usr/share/cnchi/dist/etc/cnchi.yml'
    config = {}

    def __init__(self, logger):
        self.config_loaded = False
        self.logger = logger

    def load_config(self):
        if self.config_loaded:
            return

        config_paths = [self.config_path, self.config_path_fallback]
        config_files = [p for p in config_paths if os.path.exists(p)]

        if not any(config_files):
            self.logger.error('Config file not found (load_config() failed!)')
            return

        data = open(config_files[0], 'r').read()
        config = yaml.load(data, CommentedMap)

        for key, value in config.items():
            self.config[key] = value


settings = {
    'GRUB_CMDLINE_LINUX': '',
    'alternate_package_list': '',
    'auto_device': '/dev/sda',
    'bootloader': 'grub2',
    'bootloader_device': '/dev/sda',
    'bootloader_install': True,
    'bootloader_installation_successful': False,
    'btrfs': False,
    'country_code': '',
    'country_name': '',
    'data': '/usr/share/cnchi/data/',
    'desktop': 'gnome',
    'desktop_ask': True,
    'desktop_manager': 'lightdm',
    'desktops': [],
    'enable_alongside': True,
    'encrypt_home': False,
    'f2fs': False,
    'feature_aur': False,
    'feature_bluetooth': False,
    'feature_cups': False,
    'feature_firefox': False,
    'feature_firewall': False,
    'feature_flash': False,
    'feature_fonts': False,
    'feature_games': False,
    'feature_lamp': False,
    'feature_lemp': False,
    'feature_lts': False,
    'feature_office': False,
    'feature_smb': False,
    'feature_visual': False,
    'fullname': '',
    'hostname': 'antergos',
    'is_iso': False,
    'is_vbox': False,
    'keyboard_layout': '',
    'keyboard_variant': '',
    'language_code': '',
    'language_name': '',
    'laptop': 'False',
    'locale': '',
    'location': '',
    'log_file': '/tmp/cnchi.log',
    'luks_root_device': '',
    'luks_root_password': '',
    'luks_root_volume': '',
    'network_manager': 'NetworkManager',
    'partition_mode': 'automatic',
    'password': '',
    'rankmirrors_done': False,
    'rankmirrors_result': '',
    'require_password': True,
    'ruuid': '',
    'sentry_dsn': '',
    'third_party_software': False,
    'timezone_comment': '',
    'timezone_country': '',
    'timezone_done': False,
    'timezone_human_country': '',
    'timezone_human_zone': '',
    'timezone_latitude': 0,
    'timezone_longitude': 0,
    'timezone_start': False,
    'timezone_zone': '',
    'tmp': '/tmp',
    'ui': '/usr/share/cnchi/cnchi/ui/tpl',
    'use_home': False,
    'use_luks': False,
    'use_luks_in_root': False,
    'use_lvm': False,
    'use_timesyncd': True,
    'use_zfs': False,
    'user_info_done': False,
    'username': '',
    'xz_cache': [],
    'z_hidden': False,
    'zfs': False,
    'zfs_pool_id': 0,
    'zfs_pool_name': 'antergos'}


class Settings(object):
    """ Store all Cnchi setup options here """

    def __init__(self):
        """ Initialize default configuration """

        # Creates a one element size queue
        self.settings = multiprocessing.Queue(1)

        self.settings.put({
            'alternate_package_list': '',
            'auto_device': '/dev/sda',
            'bootloader': 'grub2',
            'bootloader_device': '/dev/sda',
            'bootloader_install': True,
            'bootloader_installation_successful': False,
            'btrfs': False,
            'cache_pkgs_md5_check_failed': [],
            'cnchi': '/usr/share/cnchi/',
            'country_name': '',
            'country_code': '',
            'data': '/usr/share/cnchi/data/',
            'desktop': 'gnome',
            'desktop_ask': True,
            'desktop_manager': 'lightdm',
            'desktops': [],
            'enable_alongside': True,
            'encrypt_home': False,
            'f2fs': False,
            'feature_aur': False,
            'feature_bluetooth': False,
            'feature_cups': False,
            'feature_firefox': False,
            'feature_firewall': False,
            'feature_flash': False,
            'feature_fonts': False,
            'feature_games': False,
            'feature_lamp': False,
            'feature_lemp': False,
            'feature_lts': False,
            'feature_office': False,
            'feature_smb': False,
            'feature_visual': False,
            'fullname': '',
            'GRUB_CMDLINE_LINUX': '',
            'hostname': 'antergos',
            'is_vbox': False,
            'is_iso': False,
            'keyboard_layout': '',
            'keyboard_variant': '',
            'language_name': '',
            'language_code': '',
            'location': '',
            'laptop': 'False',
            'locale': '',
            'log_file': '/tmp/cnchi.log',
            'luks_root_password': '',
            'luks_root_volume': '',
            'luks_root_device': '',
            'network_manager': 'NetworkManager',
            'partition_mode': 'automatic',
            'password': '',
            'rankmirrors_done': False,
            'rankmirrors_result': '',
            'require_password': True,
            'ruuid': '',
            'sentry_dsn': '',
            'third_party_software': False,
            'timezone_human_zone': '',
            'timezone_country': '',
            'timezone_zone': '',
            'timezone_human_country': '',
            'timezone_comment': '',
            'timezone_latitude': 0,
            'timezone_longitude': 0,
            'timezone_done': False,
            'timezone_start': False,
            'tmp': '/tmp',
            'ui': '/usr/share/cnchi/cnchi/ui/tpl',
            'use_home': False,
            'use_luks': False,
            'use_luks_in_root': False,
            'use_lvm': False,
            'use_timesyncd': True,
            'use_zfs': False,
            'user_info_done': False,
            'username': '',
            'xz_cache': [],
            'z_hidden': False,
            'zfs': False,
            'zfs_pool_name': 'antergos',
            'zfs_pool_id': 0})

    def _get_settings(self):
        """ Get a copy of our settings """
        settings = self.settings.get()
        copy = settings.copy()
        self.settings.put(settings)
        return copy

    def _update_settings(self, new_settings):
        """ Updates global settings """
        settings = self.settings.get()
        try:
            settings.update(new_settings)
        finally:
            self.settings.put(settings)

    def get(self, key):
        """ Get one setting value """
        settings = self._get_settings()
        return settings.get(key, None)

    def set(self, key, value):
        """ Set one setting's value """
        settings = self._get_settings()
        current = settings.get(key, 'keyerror')
        exists = 'keyerror' != current

        if exists and current and isinstance(current, list) and not isinstance(value, list):
            settings[key].append(value)
        else:
            settings[key] = value

        self._update_settings(settings)
