#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  systemd_networkd.py
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

""" systemd-networkd configuration in base install. """
# https://wiki.archlinux.org/index.php/Systemd-networkd

# TODO: Setup wireless interfaces
# https://wiki.archlinux.org/index.php/WPA_supplicant

import os
import subprocess
import logging

import chroot

DEST_DIR = "/install"


def chroot_run(cmd):
    chroot.run(cmd, DEST_DIR)


def setup(ssid=None, passphrase=None):
    """ Configure system-networkd for base installs """

    # For compatibility with resolv.conf, delete the existing file and
    # create the following symbolic link:
    source = os.path.join(DEST_DIR, "run/systemd/resolve/resolv.conf")
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
        output = subprocess.check_output(cmd).decode()
        for line in output:
            if len(line) > 0:
                link = line[1:]
                if link.startswith("eth") or link.startswith("enp"):
                    links.append(link)
                elif link.startswith("wlp"):
                    links.append(link)
                    links_wireless.append(link)
    except subprocess.CalledProcessError as process_error:
        logging.warning(process_error)
        logging.warning(_("systemd-networkd configuration failed."))
        return

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
            chroot_run(cmd)
            # cmd = ["systemctl", "enable", "dhcpcd@{0}".format(link)]
            # chroot_run(cmd)


if __name__ == '__main__':
    setup()
