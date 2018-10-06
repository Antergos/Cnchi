#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
#  Copyright (c) 2012 Canonical Ltd.
#  Copyright (c) 2013-2018 Antergos
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

""" Extra functions """

import contextlib
import grp
import http.client
import locale
import logging
import os
import pwd
import random
import re
import shutil
import socket
from socket import timeout
import string
import subprocess
import syslog
import urllib
import ssl
import dbus


NM = 'org.freedesktop.NetworkManager'
NM_STATE_CONNECTED_GLOBAL = 70

_DROPPED_PRIVILEGES = 0


def copytree(src_dir, dst_dir, symlinks=False, ignore=None):
    """ Copy an entire tree with files and folders """
    for item in os.listdir(src_dir):
        src = os.path.join(src_dir, item)
        dst = os.path.join(dst_dir, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst, symlinks, ignore)
        else:
            shutil.copy2(src, dst)


def utf8(my_string, errors="strict"):
    """ Decode a string as UTF-8 if it isn't already Unicode. """
    if isinstance(my_string, str):
        return my_string
    else:
        return str(my_string, "utf-8", errors)


def is_swap(device):
    """ Check if device is a swap device """
    try:
        with open('/proc/swaps') as swaps:
            for line in swaps:
                if line.startswith(device + ' '):
                    return True
    except OSError as os_error:
        logging.warning(os_error)
    return False

# PRIVILEGES STARTS HERE -------------------------------------------------------

def set_groups_for_uid(uid):
    """ Set groups for user id uid """
    if uid == os.geteuid() or uid == os.getuid():
        return

    user = pwd.getpwuid(uid).pw_name

    try:
        os.setgroups([g.gr_gid for g in grp.getgrall() if user in g.gr_mem])
    except OSError:
        import traceback

        for line in traceback.format_exc().split('\n'):
            syslog.syslog(syslog.LOG_ERR, line)


def get_uid_gid():
    """ Returns uid and gid from SUDO_* env vars
        and sets groups for that uid """
    uid = os.environ.get('SUDO_UID')
    gid = os.environ.get('SUDO_GID')
    if uid:
        uid = int(uid)
        set_groups_for_uid(uid)
    if gid:
        gid = int(gid)
    return (uid, gid)


def drop_all_privileges():
    """ Drop root privileges """
    # gconf needs both the UID and effective UID set.
    global _DROPPED_PRIVILEGES

    uid, gid = get_uid_gid()
    if gid:
        os.setregid(gid, gid)
    if uid:
        os.setreuid(uid, uid)
        os.environ['HOME'] = pwd.getpwuid(uid).pw_dir
        os.environ['LOGNAME'] = pwd.getpwuid(uid).pw_name
    _DROPPED_PRIVILEGES = None


def drop_privileges():
    """ Drop privileges """
    global _DROPPED_PRIVILEGES
    if _DROPPED_PRIVILEGES is None:
        raise AssertionError()
    if _DROPPED_PRIVILEGES == 0:
        uid, gid = get_uid_gid()
        if gid:
            os.setegid(gid)
        if uid:
            os.seteuid(uid)
    _DROPPED_PRIVILEGES += 1


def regain_privileges():
    """ Regain root privileges """
    global _DROPPED_PRIVILEGES
    if _DROPPED_PRIVILEGES is None:
        raise AssertionError()
    _DROPPED_PRIVILEGES -= 1
    if _DROPPED_PRIVILEGES == 0:
        os.seteuid(0)
        os.setegid(0)
        os.setgroups([])


def drop_privileges_save():
    """ Drop the real UID/GID as well, and hide them in saved IDs. """
    # At the moment, we only know how to handle this when effective
    # privileges were already dropped.
    #assert _DROPPED_PRIVILEGES is not None and _DROPPED_PRIVILEGES > 0
    if _DROPPED_PRIVILEGES is None or _DROPPED_PRIVILEGES <= 0:
        raise AssertionError()
    uid, gid = get_uid_gid()
    if gid:
        gid = int(gid)
        os.setresgid(gid, gid, 0)
    if uid:
        os.setresuid(uid, uid, 0)


def regain_privileges_save():
    """ Recover our real UID/GID after calling drop_privileges_save. """
    #assert _DROPPED_PRIVILEGES is not None and _DROPPED_PRIVILEGES > 0
    if _DROPPED_PRIVILEGES is None or _DROPPED_PRIVILEGES <= 0:
        raise AssertionError()
    os.setresuid(0, 0, 0)
    os.setresgid(0, 0, 0)
    os.setgroups([])


@contextlib.contextmanager
def raised_privileges():
    """ As regain_privileges/drop_privileges, but in context manager style. """
    regain_privileges()
    try:
        yield
    finally:
        drop_privileges()


def raise_privileges(func):
    """ As raised_privileges, but as a function decorator. """
    from functools import wraps

    @wraps(func)
    def helper(*args, **kwargs):
        """ Function that runs func function with raised privileges """
        with raised_privileges():
            return func(*args, **kwargs)

    return helper

# PRIVILEGES ENDS HERE --------------------------------------------------------


def is_removable(device):
    """ Checks if device is removable """
    if device is None:
        return None
    device = os.path.realpath(device)
    devpath = None
    is_partition = False
    removable_bus = False
    cmd = ['/usr/bin/udevadm', 'info', '-q', 'property', '-n', device]
    subp = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        universal_newlines=True)
    for line in subp.communicate()[0].splitlines():
        line = line.strip()
        if line.startswith('DEVPATH='):
            devpath = line[8:]
        elif line == 'DEVTYPE=partition':
            is_partition = True
        elif line == 'ID_BUS=usb' or line == 'ID_BUS=ieee1394':
            removable_bus = True

    if devpath is not None:
        if is_partition:
            devpath = os.path.dirname(devpath)
        is_device_removable = removable_bus
        try:
            removable_path = '/sys{0}/removable'.format(devpath)
            with open(removable_path) as removable:
                if removable.readline().strip() != '0':
                    is_device_removable = True
        except IOError as err:
            logging.warning(err)
        if is_device_removable:
            try:
                cmd = ['/usr/bin/udevadm', 'info', '-q', 'name', '-p', devpath]
                subp = subprocess.Popen(cmd,
                                        stdout=subprocess.PIPE,
                                        universal_newlines=True)
                part = subp.communicate()[0].splitlines()[0].strip()
                return os.path.join('/dev', part)
            except subprocess.CalledProcessError as err:
                logging.warning(err)
    return None


def mount_info(path):
    """ Return filesystem name, type, and ro/rw for a given mountpoint."""
    fsname = ''
    fstype = ''
    writable = ''
    with open('/proc/mounts') as mounts:
        for line in mounts:
            line = line.split()
            if line[1] == path:
                fsname = line[0]
                fstype = line[2]
                writable = line[3].split(',')[0]
    return fsname, fstype, writable


def udevadm_info(args):
    """ Helper function to run udevadm """
    fullargs = ['/usr/bin/udevadm', 'info', '-q', 'property']
    fullargs.extend(args)
    udevadm = {}
    subp = subprocess.Popen(
        fullargs, stdout=subprocess.PIPE, universal_newlines=True)
    for line in subp.communicate()[0].splitlines():
        line = line.strip()
        if '=' not in line:
            continue
        name, value = line.split('=', 1)
        udevadm[name] = value
    return udevadm


def partition_to_disk(partition):
    """ Convert a partition device to its disk device, if any. """
    udevadm_part = udevadm_info(['-n', partition])
    if ('DEVPATH' not in udevadm_part or
            udevadm_part.get('DEVTYPE') != 'partition'):
        return partition

    disk_syspath = os.path.join(
        '/sys',
        udevadm_part['DEVPATH'].rsplit('/', 1)[0])
    udevadm_disk = udevadm_info(['-p', disk_syspath])
    return udevadm_disk.get('DEVNAME', partition)


def cdrom_mount_info():
    """ Return mount information for /cdrom.
    This is the same as mount_info, except that the partition is converted to
    its containing disk, and we don't care whether the mount point is
    writable. """

    cdsrc, cdfs, _ = mount_info('/cdrom')
    cdsrc = partition_to_disk(cdsrc)
    return cdsrc, cdfs


def format_size(size):
    """ Format a partition size. """
    if size < 1000:
        unit = 'B'
        factor = 1
    elif size < 1000 * 1000:
        unit = 'kB'
        factor = 1000
    elif size < 1000 * 1000 * 1000:
        unit = 'MB'
        factor = 1000 * 1000
    elif size < 1000 * 1000 * 1000 * 1000:
        unit = 'GB'
        factor = 1000 * 1000 * 1000
    elif size < 1000 * 1000 * 1000 * 1000 * 1000:
        unit = 'TB'
        factor = 1000 * 1000 * 1000 * 1000
    else:
        unit = 'PB'
        factor = 1000 * 1000 * 1000 * 1000 * 1000
    return '%.1f %s' % (float(size) / factor, unit)


def create_bool(text):
    """ Creates a bool from a str type """

    if text.lower() == "true":
        return True
    elif text.lower() == "false":
        return False
    else:
        return text


@raise_privileges
def dmimodel():
    """ Use dmidecode to get hardware info
    dmidecode is a tool for dumping a computer's DMI (some say SMBIOS) table
    contents in a human-readable format. This table contains a description of
    the system's hardware components, as well as other useful pieces of
    information such as serial numbers and BIOS revision """
    model = ''
    kwargs = {}
    if os.geteuid() != 0:
        # Silence annoying warnings during the test suite.
        kwargs['stderr'] = open('/dev/null', 'w')
    try:
        cmd = ['/usr/bin/dmidecode', '--string', 'system-manufacturer']
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, universal_newlines=True, **kwargs)
        manufacturer = proc.communicate()[0]
        if not manufacturer:
            return ""
        manufacturer = manufacturer.lower()
        if 'to be filled' in manufacturer:
            # Don't bother with products in development.
            return ""
        if 'bochs' in manufacturer or 'vmware' in manufacturer:
            model = 'virtual machine'
            # VirtualBox sets an appropriate system-product-name.
        else:
            if 'lenovo' in manufacturer or 'ibm' in manufacturer:
                key = 'system-version'
            else:
                key = 'system-product-name'
            proc = subprocess.Popen(
                ['/usr/bin/dmidecode', '--string', key],
                stdout=subprocess.PIPE,
                universal_newlines=True)
            model = proc.communicate()[0]
        if 'apple' in manufacturer:
            # MacBook4,1 - strip the 4,1
            model = re.sub(r'[^a-zA-Z\s]', '', model)
        # Replace each gap of non-alphanumeric characters with a dash.
        # Ensure the resulting string does not begin or end with a dash.
        model = re.sub('[^a-zA-Z0-9]+', '-', model).rstrip('-').lstrip('-')
        if model.lower() == 'not-available':
            return ""
    except subprocess.CalledProcessError:
        syslog.syslog(syslog.LOG_ERR, 'Unable to determine the model from DMI')
    finally:
        if 'stderr' in kwargs:
            kwargs['stderr'].close()
    return model


def get_prop(obj, iface, prop):
    """ Get network interface property """
    try:
        return obj.Get(iface, prop, dbus_interface=dbus.PROPERTIES_IFACE)
    except (dbus.DBusException, dbus.exceptions.DBusException) as err:
        logging.warning(err)
        return None


def is_wireless_enabled():
    """ Networkmanager. Checks if wireless is enabled """
    bus = dbus.SystemBus()
    manager = bus.get_object(NM, '/org/freedesktop/NetworkManager')
    return get_prop(manager, NM, 'WirelessEnabled')


def get_nm_state():
    """ Checks Networkmanager connection status """
    state = False
    try:
        bus = dbus.SystemBus()
        manager = bus.get_object(NM, '/org/freedesktop/NetworkManager')
        state = get_prop(manager, NM, 'State')
    except (dbus.DBusException, dbus.exceptions.DBusException) as dbus_err:
        logging.warning(dbus_err)
    return state


def has_connection():
    """ Checks if we have an Internet connection """
    # The ips are reversed (to avoid spam)
    urls = [
        ('http', '20.13.206.130'),
        ('https', '167.140.27.104'),
        ('https', '167.141.27.104')]

    for prot, ip_addr in urls:
        try:
            ip_addr = '.'.join(ip_addr.split('.')[::-1])
            url = "{0}://{1}".format(prot, ip_addr)
            #print("*" * 10, url)
            if prot == 'http':
                urllib.request.urlopen(url, timeout=5)
            elif prot == 'https':
                conn = http.client.HTTPSConnection(ip_addr, timeout=5)
                conn.request("GET", "/")
                conn.close()
        except ssl.SSLError as err:
            # Cannot establish a SSL connection but site exists, so it's fine.
            conn.close()
        except (KeyError, OSError, timeout, urllib.error.URLError, http.client.InvalidURL) as err:
            # Cannot connect, either site is down or there is no Internet connection
            logging.error("%s: %s", url, err)
            return False

    return True
    ## We cannot connect to any url, let's ask NetworkManager
    ## Problem: In a Virtualbox VM this returns true even when
    ## the host OS has no connection
    #if get_nm_state() == NM_STATE_CONNECTED_GLOBAL:
    #    return True
    #
    #return False


def add_connection_watch(func):
    """ Add connection watch to Networkmanager """
    def connection_cb(state):
        """ Callback function that will be called if something changes """
        func(state == NM_STATE_CONNECTED_GLOBAL)

    bus = dbus.SystemBus()
    bus.add_signal_receiver(connection_cb, 'StateChanged', NM, NM)
    try:
        func(has_connection())
    except (dbus.DBusException, dbus.exceptions.DBusException) as err:
        logging.warning(err)
        # We can't talk to NM, so no idea.  Wild guess: we're connected
        # using ssh with X forwarding, and are therefore connected.  This
        # allows us to proceed with a minimum of complaint.
        func(True)


def get_network():
    """ Get our own network ip """
    # Open a connection to our server
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        mysocket.connect(("antergos.com", 1234))
    except OSError as err:
        logging.error(err)
        return ""
    myip = mysocket.getsockname()[0]
    mysocket.close()

    # Parse our ip
    intip = False
    spip = myip.split(".")
    if spip[0] == '192':
        if spip[1] == '168':
            intip = True
    elif spip[0] == '10':
        intip = True
    elif spip[0] == '172':
        if 15 < int(spip[1]) < 32:
            intip = True
    if intip:
        ipran = '.'.join(spip[:-1]) + ".0/24"
    else:
        ipran = '.'.join(spip)
    return ipran


def sort_list(my_list, my_locale=""):
    """ Sorts list using locale specifics """
    try:
        import functools
    except ImportError as err:
        logging.warning(err)
        return my_list

    if my_locale != "":
        locale.setlocale(locale.LC_COLLATE, my_locale)

    sorted_list = sorted(my_list, key=functools.cmp_to_key(locale.strcoll))

    return sorted_list


def gtk_refresh():
    """ Tell Gtk loop to run pending events """
    from gi.repository import Gtk

    while Gtk.events_pending():
        Gtk.main_iteration()


def remove_temp_files(tmp_dir):
    """ Remove Cnchi temporary files """
    temp_files = [
        ".setup-running", ".km-running",
        "setup-pacman-running",
        "setup-mkinitcpio-running",
        ".tz-running", ".setup"]
    for temp in temp_files:
        path = os.path.join(tmp_dir, temp)
        if os.path.exists(path):
            with raised_privileges():
                os.remove(path)


def set_cursor(cursor_type):
    """ Set mouse cursor """
    try:
        from gi.repository import Gdk

        screen = Gdk.Screen.get_default()
        window = Gdk.Screen.get_root_window(screen)

        if window:
            display = Gdk.Display.get_default()
            cursor = Gdk.Cursor.new_for_display(display, cursor_type)
            window.set_cursor(cursor)
            gtk_refresh()
    except Exception as ex:
        logging.debug(ex)


def partition_exists(partition):
    """ Check if a partition already exists """
    if "/dev/" in partition:
        partition = partition[len("/dev/"):]

    exists = False
    with open("/proc/partitions") as partitions:
        if partition in partitions.read():
            exists = True
    return exists


def is_partition_extended(partition):
    """ Check if a partition is of extended type """

    if "/dev/mapper" in partition:
        return False

    # In automatic LVM volume is called AntergosVG
    if "/dev/AntergosVG" in partition:
        return False

    if "/dev/" in partition:
        partition = partition[len("/dev/"):]

    with open("/proc/partitions") as partitions:
        lines = partitions.readlines()

    for line in lines:
        if "major" not in line:
            info = line.split()
            if len(info) > 3 and info[2] == '1' and info[3] == partition:
                return True

    return False


def get_partitions():
    """ Get all system partitions """
    partitions_list = []
    with open("/proc/partitions") as partitions:
        lines = partitions.readlines()
    for line in lines:
        if "major" not in line:
            info = line.split()
            if info and len(info[3]) > len("sdX") and "loop" not in info[3]:
                partitions_list.append("/dev/" + info[3])
    return partitions_list


def check_pid(pid):
    """ Check for the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def random_generator(size=4, chars=string.ascii_lowercase + string.digits):
    """ Generates a random string. """
    return ''.join(random.choice(chars) for x in range(size))


def select_combobox_value(combobox, value):
    """ Force combobox to select a specific value """
    model = combobox.get_model()
    combo_iter = model.get_iter(0)
    index = 0
    found = False
    while combo_iter is not None and not found:
        if value.lower() == model[combo_iter][0].lower():
            combobox.set_active_iter(combo_iter)
            combo_iter = None
            found = True
        else:
            index += 1
            combo_iter = model.iter_next(combo_iter)
    return found


def select_first_combobox_item(combobox):
    """ Automatically select the first entry """
    tree_model = combobox.get_model()
    tree_iter = tree_model.get_iter_first()
    combobox.set_active_iter(tree_iter)


class InstallError(Exception):
    """ Exception class called upon an installer error """

    def __init__(self, message):
        """ Initialize exception class """
        super().__init__(message)
        self.message = str(message)

    def __repr__(self):
        """ Returns exception message """
        return repr(self.message)

    def __str__(self):
        """ Returns exception message """
        return repr(self.message)
