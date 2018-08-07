#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test_hardware_module.py
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

""" Module to test hardware module """

import logging

import gettext
import locale

APP_NAME = "cnchi"
LOCALE_DIR = "/usr/share/locale"


def setup_logging():
    """ Configure our logger """
    logger = logging.getLogger()

    log_level = logging.DEBUG

    logger.setLevel(log_level)

    # Log format
    formatter = logging.Formatter(
        '%(asctime)s - %(filename)s:%(funcName)s() - %(levelname)s: %(message)s')

    # Show log messages to stdout
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def test():
    """ Main function """
    locale_code, _encoding = locale.getdefaultlocale()
    lang = gettext.translation(APP_NAME, LOCALE_DIR, [locale_code], None, True)
    lang.install()

    setup_logging()

    # Get packages needed for detected hardware
    import hardware.hardware as hardware

    hardware_install = hardware.HardwareInstall("/usr/share/cnchi/src/hardware/modules")
    hardware_pkgs = hardware_install.get_packages()
    print("Hardware module added these packages : ", hardware_pkgs)


if __name__ == '__main__':
    test()
