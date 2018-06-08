#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# logging_utils.py
#
# Copyright © 2015-2018 Antergos
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

""" Logging utils to ease log calls """

import logging
import uuid
import json
import os
import requests

from info import CNCHI_VERSION, CNCHI_RELEASE_STAGE


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance

    def __new__(mcs, *args, **kwargs):
        obj = super().__new__(mcs, *args, **kwargs)
        obj.ip = None
        obj.install_id = None
        obj.api_key = None
        obj.have_install_id = False
        obj.after_location_screen = False
        obj.name = 'Cnchi'
        obj.description = 'Installer'
        obj.key = 'X-{}-{}'.format(obj.name, obj.description)

        return obj


class ContextFilter(logging.Filter, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.api_key = self.get_bugsnag_api()
        self.have_install_id = False
        self.after_location_screen = False
        self.install_id = ""
        self.ip = '0.0.0.0'

    def filter(self, record):
        uid = str(uuid.uuid1()).split("-")
        record.uuid = uid[3] + "-" + uid[1] + "-" + uid[2] + "-" + uid[4]
        record.ip = self.ip
        record.install_id = self.install_id
        return True

    def get_and_save_install_id(self, is_location_screen=False):
        if self.have_install_id:
            return

        if is_location_screen:
            self.after_location_screen = True

        if CNCHI_RELEASE_STAGE == 'development':
            self.install_id = 'development'
            self.ip = '0.0.0.0'
            self.have_install_id = True
            return 'development'

        info = {'ip': '0.0.0.0', 'id': '0'}
        url = self.get_url_for_id_request()
        headers = {self.api_key: CNCHI_VERSION}

        try:
            req = requests.get(url, headers=headers)
            req.raise_for_status()
            info = json.loads(req.json())
        except Exception as err:
            logger = logging.getLogger()
            msg = "Unable to get an Id for this installation. Error: {0}".format(err.args)
            logger.debug(msg)

        try:
            self.ip = info['ip']
            self.install_id = info['id']
            self.have_install_id = True
        except (TypeError, KeyError):
            self.have_install_id = False

        return self.install_id

    @staticmethod
    def get_bugsnag_api():
        config_path = '/etc/cnchi.conf'
        alt_config_path = '/usr/share/cnchi/data/cnchi.conf'
        bugsnag_api = None

        if (not os.path.exists(config_path) and 
            os.path.exists(alt_config_path)):
            config_path = alt_config_path

        if os.path.exists(config_path):
            with open(config_path) as bugsnag_conf:
                bugsnag_api = bugsnag_conf.readline().strip()

        return bugsnag_api

    def get_url_for_id_request(self):
        build_server = None

        if self.api_key and 'development' != CNCHI_RELEASE_STAGE:
            parts = {
                1: 'com',
                2: 'http',
                3: 'hook',
                4: 'build',
                5: 'antergos',
                6: 'cnchi',
                7: '://'
            }
            build_server = '{}{}{}.{}.{}/{}?{}={}'.format(
                parts[2], parts[7], parts[4], parts[5],
                parts[1], parts[3], parts[6], self.api_key
            )
        return build_server

    @staticmethod
    def filter_log_lines(log):
        keep_lines = []
        look_for = ['[WARNING]', '[ERROR]']
        log_lines = log.readlines()

        for i in range(0, len(log_lines)):
            for pattern in look_for:
                if pattern in log_lines[i]:
                    try:
                        if 10 < i < (len(log_lines) - 10):
                            keep_lines.extend([log_lines[l]
                                               for l in range(i - 10, i + 10)])
                        elif i < 10:
                            keep_lines.extend([log_lines[l]
                                               for l in range(0, i)])
                        elif i > (len(log_lines) - 10):
                            keep_lines.extend([log_lines[l]
                                               for l in range(i, len(log_lines))])
                    except Exception:
                        pass

        return keep_lines

    def bugsnag_before_notify_callback(self, notification=None):
        if notification is not None:
            excluded = ["No such interface '/org/freedesktop/UPower'"]

            if any(True for pattern in excluded if pattern in str(notification.exception)):
                return False

            if self.after_location_screen and not self.have_install_id:
                self.get_and_save_install_id()

            notification.user = {"id": self.ip,
                                 "name": self.install_id,
                                 "install_id": self.install_id}

            logs = ['/tmp/{0}.log'.format(n)
                    for n in ['cnchi', 'pacman', 'postinstall']]
            missing = [f for f in logs if not os.path.exists(f)]
            if missing:
                for log in missing:
                    open(log, 'a').close()

            with open(logs[0], 'r') as cnchi:
                with open(logs[1], 'r') as pacman:
                    with open(logs[2], 'r') as postinstall:
                        log_dict = {'pacman': pacman,
                                    'postinstall': postinstall}
                        parse = {
                            log: [line.strip() for line in log_dict[log]]
                            for log in log_dict
                        }
                        parse['cnchi'] = self.filter_log_lines(cnchi)
                        notification.add_tab('logs', parse)

            return notification

    def send_install_result(self, result):
        try:
            build_server = self.get_url_for_id_request()
            if build_server and self.install_id:
                url = "{0}&install_id={1}&result={2}"
                url = url.format(build_server, self.install_id, result)
                headers = {self.api_key: CNCHI_VERSION}
                req = requests.get(url, headers=headers)
                json.loads(req.json())
        except Exception as ex:
            logger = logging.getLogger()
            template = "Can't send install result. An exception of type {0} occured. "
            template += "Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logger.error(message)
