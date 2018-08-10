#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# luks.py
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

""" Luks helper functions for AutoPartition module """

import logging
import os

from installation import wrapper
from misc.run_cmd import call, popen


def close_antergos_devices():
    """ Close LUKS devices (they may have been left open because of a previous
    failed installation) """

    volumes = ["/dev/mapper/cryptAntergos", "/dev/mapper/cryptAntergosHome"]

    err_msg = "Can't close already opened LUKS devices"

    for volume in volumes:
        if os.path.exists(volume):
            cmd = ["/usr/bin/cryptsetup", "luksClose", volume]
            call(cmd, msg=err_msg)


def setup(luks_device, luks_name, luks_options):
    """ Setups a luks device """
    # get luks options (or set a default if missing)
    luks_pass = luks_options.get('password', None)
    luks_key = luks_options.get('key', None)
    luks_cypher = luks_options.get('cypher', "aes-xts-plain64")

    #luks_cypher = 'aes-xts-plain64'
    #luks_cypher = 'serpent-xts-plain64'

    if luks_pass in [None, ""] and luks_key is None:
        txt = "Can't setup LUKS in device {0}. Either password or a key file are needed"
        txt = txt.format(luks_device)
        logging.error(txt)
        return

    # For now, we we'll use the same password for root and /home
    # If instead user wants to use a key file, we'll have two different key files.

    logging.debug("Cnchi will setup LUKS on device %s", luks_device)

    # Wipe LUKS header (just in case we're installing on a pre LUKS setup)
    # For 512 bit key length the header is 2MiB
    # If in doubt, just be generous and overwrite the first 10MiB or so
    wrapper.run_dd("/dev/zero", luks_device, bytes_block=512, count=20480)

    err_msg = "Can't format and open the LUKS device {0}".format(luks_device)

    if luks_pass in [None, ""]:
        # No key password given, let's create a random keyfile
        wrapper.run_dd("/dev/urandom", luks_key, bytes_block=1024, count=4)

        # Set up luks with a keyfile
        cmd = ["/usr/bin/cryptsetup", "luksFormat", "-q", "-c", luks_cypher,
               "-s", "512", "-h", "sha512", luks_device, luks_key]
        call(cmd, msg=err_msg, fatal=True)

        cmd = ["/usr/bin/cryptsetup", "luksOpen", luks_device, luks_name, "-q",
               "--key-file", luks_key]
        call(cmd, msg=err_msg, fatal=True)
    else:
        # Set up luks with a password key

        luks_pass_bytes = bytes(luks_pass, 'UTF-8')

        cmd = ["/usr/bin/cryptsetup", "luksFormat", "-q", "-c", luks_cypher,
               "-s", "512", "-h", "sha512", "--key-file=-", luks_device]
        proc = popen(cmd, msg=err_msg, fatal=True)
        proc.communicate(input=luks_pass_bytes)

        cmd = ["/usr/bin/cryptsetup", "luksOpen", luks_device, luks_name, "-q", "--key-file=-"]
        proc = popen(cmd, msg=err_msg, fatal=True)
        proc.communicate(input=luks_pass_bytes)
