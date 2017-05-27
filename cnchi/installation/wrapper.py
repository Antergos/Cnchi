#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  wrapper.py
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

""" Helper module to run some disk/partition related utilities """

import subprocess
import logging

from misc.extra import InstallError
from misc.run_cmd import call


def wipefs(device, fatal=True):
    """ Wipe fs from device """
    err_msg = "Cannot wipe the filesystem of device {0}".format(device)
    cmd = ["wipefs", "-a", device]
    call(cmd, msg=err_msg, fatal=fatal)


def dd(input_device, output_device, bs=512, count=2048, seek=0):
    """ Helper function to call dd """
    cmd = [
        'dd',
        'if={0}'.format(input_device),
        'of={0}'.format(output_device),
        'bs={0}'.format(bs),
        'count={0}'.format(count),
        'seek={0}'.format(seek),
        'status=noxfer']
    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        logging.warning("Command %s failed: %s", err.cmd, err.output)


def sgdisk(command, device):
    """ Helper function to call sgdisk (GPT) """
    cmd = ['sgdisk', "--{0}".format(command), device]
    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        logging.error("Command %s failed: %s", err.cmd, err.output.decode())
        txt = _("Command {0} failed: {1}").format(err.cmd, err.output.decode())
        raise InstallError(txt)


def sgdisk_new(device, part_num, label, size, hex_code):
    """ Helper function to call sgdisk --new (GPT) """
    # --new: Create a new partition, numbered partnum, starting at sector start
    #        and ending at sector end.
    # Parameters: partnum:start:end (zero in start or end means using default
    # value)
    # --typecode: Change a partition's GUID type code to the one specified by
    #             hexcode. Note that hexcode is a gdisk/sgdisk internal
    #             two-byte hexadecimal code.
    #             You can obtain a list of codes with the -L option.
    # Parameters: partnum:hexcode
    # --change-name: Change the name of the specified partition.
    # Parameters: partnum:name

    # logging.debug(" ".join(cmd))

    cmd = [
        'sgdisk',
        '--new={0}:0:+{1}M'.format(part_num, size),
        '--typecode={0}:{1}'.format(part_num, hex_code),
        '--change-name={0}:{1}'.format(part_num, label),
        device]
    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        txt = "Cannot create a new partition on device {0}. Command {1} has failed: {2}"
        txt = txt.format(device, err.cmd, err.output.decode())
        logging.error(txt)
        txt = _("Cannot create a new partition on device {0}. Command {1} has failed: {2}")
        txt = txt.format(device, err.cmd, err.output.decode())
        raise InstallError(txt)


def parted_set(device, number, flag, state):
    """ Helper function to call set parted command """
    cmd = [
        'parted', '--align', 'optimal', '--script', device,
        'set', number, flag, state]
    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        txt = "Cannot set flag {0} on device {1}. Command {2} has failed: {3}"
        txt = txt.format(flag, device, err.cmd, err.output.decode())
        logging.error(txt)


def parted_mkpart(device, ptype, start, end, filesystem=""):
    """ Helper function to call mkpart parted command """
    # If start is < 0 we assume we want to mkpart at the start of the disk
    if start < 0:
        start_str = "1"
    else:
        start_str = "{0}MiB".format(start)

    # -1s means "end of disk"
    if end == "-1s":
        end_str = end
    else:
        end_str = "{0}MiB".format(end)

    cmd = [
        'parted', '--align', 'optimal', '--script', device,
        '--',
        'mkpart', ptype, filesystem, start_str, end_str]

    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        txt = "Cannot create a new partition on device {0}. Command {1} has failed: {2}"
        txt = txt.format(device, err.cmd, err.output.decode())
        logging.error(txt)
        txt = _("Cannot create a new partition on device {0}. Command {1} has failed: {2}")
        txt = txt.format(device, err.cmd, err.output.decode())
        raise InstallError(txt)


def parted_mklabel(device, label_type="msdos"):
    """ Helper function to call mktable parted command """

    cmd = [
        "parted", "--align", "optimal", "--script", device,
        "mklabel", label_type]

    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        txt = ("Cannot create a new partition table on device {0}. "
               "Command {1} failed: {2}")
        txt = txt.format(device, err.cmd, err.output.decode())
        logging.error(txt)
        txt = _("Cannot create a new partition table on device {0}. "
                "Command {1} failed: {2}")
        txt = txt.format(device, err.cmd, err.output.decode())
        raise InstallError(txt)
