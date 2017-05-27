#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# systemd_networkd.py
#
# Copyright © 2013-2017 Antergos
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


""" systemd-networkd configuration in base install. """
# https://wiki.archlinux.org/index.php/Systemd-networkd

# TODO: Setup wireless interfaces
# https://wiki.archlinux.org/index.php/WPA_supplicant

import os
import subprocess
import logging

from misc.run_cmd import chroot_call

DEST_DIR = "/install"



def setup(ssid=None, passphrase=None):
    """ Configure system-networkd for base installs """

    # For compatibility with resolv.conf, delete the existing file and
    # create the following symbolic link:
    source = os.path.join("/run/systemd/resolve/resolv.conf")
    link_name = os.path.join(DEST_DIR, "etc/resolv.conf")

    # Delete /etc/resolv.conf if it already exists
    if os.path.exists(link_name):
        os.unlink(link_name)

    # Creates the symlink
    try:
        os.symlink(source, link_name)
    except OSError as os_error:
        logging.warning(os_error)

    # Get interface names (links)
    links = []
    links_wireless = []
    try:
        cmd = ['networkctl', 'list']
        output = subprocess.check_output(cmd).decode().split('\n')
        for line in output:
            fields = line.split()
            if len(fields) > 0:
                link = fields[1]
                if link.startswith("eth") or link.startswith("enp"):
                    links.append(link)
                elif link.startswith("wlp"):
                    links.append(link)
                    links_wireless.append(link)
    except subprocess.CalledProcessError as process_error:
        logging.warning("systemd-networkd configuration failed: %s", process_error)
        return

    logging.debug(
        "Found [%s] links and [%s] are wireless",
        " ".join(links),
        " ".join(links_wireless))

    # Setup DHCP by default for all interfaces found
    for link in links:
        fname = "etc/systemd/network/{0}.network".format(link)
        wired_path = os.path.join(DEST_DIR, fname)
        with open(wired_path, 'w') as wired_file:
            wired_file.write("# {0} adapter using DHCP (written by Cnchi)\n".format(link))
            wired_file.write("[Match]\n")
            wired_file.write("Name={0}\n\n".format(link))
            wired_file.write("[Network]\n")
            wired_file.write("DHCP=ipv4\n")
        logging.debug("Created %s configuration file", wired_path)

    # One needs to have configured a wireless adapter with another service
    # such as wpa_supplicant and the corresponding service is required to be enabled.
    # /etc/wpa_supplicant/wpa_supplicant-interface.conf.
    # systemctl enable wpa_supplicant@interface

    # Setup wpa_supplicant. We need the SID and the passphrase
    # TODO: Ask for different sid's or passphrases for each interface

    if ssid is not None and passphrase is not None:
        for link in links_wireless:
            conf_path = os.path.join(
                DEST_DIR,
                "etc/wpa_supplicant/wpa_supplicant-{0}.conf".format(link))
            try:
                conf = subprocess.check_output(["wpa_passphrase", ssid, passphrase])
                with open(conf_path, "w") as conf_file:
                    conf_file.write(conf)
            except subprocess.CalledProcessError as process_error:
                logging.warning(process_error)
            cmd = ["systemctl", "enable", "wpa_supplicant@{0}".format(link)]
            chroot_call(cmd)
            # cmd = ["systemctl", "enable", "dhcpcd@{0}".format(link)]
            # chroot_run(cmd)


if __name__ == '__main__':
    def _(msg):
        return msg
    DEST_DIR = "/"
    setup()
