#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# rank_mirrors.py
#
# Copyright © 2012, 2013 Xyne
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


""" Creates mirrorlist sorted by both latest updates and fastest connection """

import queue
import threading
import urllib.request
import urllib.error
import http.client
import subprocess
import logging
import time
import os
import shutil
import tempfile
import multiprocessing

import requests

import misc.extra as misc

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

class AutoRankmirrorsProcess(multiprocessing.Process):
    """ Process class that downloads and sorts the mirrorlist """

    def __init__(self, settings, fraction_pipe):
        """ Initialize process class """
        super().__init__()
        self.rankmirrors_pid = None
        self.json_obj = None
        self.antergos_mirrorlist = "/etc/pacman.d/antergos-mirrorlist"
        self.arch_mirrorlist = "/etc/pacman.d/mirrorlist"
        self.arch_mirror_status = "http://www.archlinux.org/mirrors/status/json/"
        self.arch_mirrorlist_ranked = []
        self.settings = settings
        self.fraction = fraction_pipe

    @staticmethod
    def is_good_mirror(my_mirror):
        """ Check if mirror info is good enough """
        return (my_mirror['last_sync'] and
                my_mirror['completion_pct'] == 1.0 and
                my_mirror['protocol'] == 'http' and
                int(my_mirror['delay']) <= 3600)

    @staticmethod
    def sync():
        """ Synchronize cached writes to persistent storage """
        try:
            subprocess.check_call(['sync'])
        except subprocess.CalledProcessError as why:
            logging.warning(
                "Can't synchronize cached writes to persistent storage: %s",
                why)

    def update_mirrorlist(self):
        """ Make sure we have the latest antergos-mirrorlist files """
        with misc.raised_privileges() as __:
            try:
                cmd = [
                    'pacman',
                    '-Syy',
                    '--noconfirm',
                    '--noprogressbar',
                    '--quiet',
                    'antergos-mirrorlist']
                with open(os.devnull, 'w') as fnull:
                    subprocess.call(cmd, stdout=fnull,
                                    stderr=subprocess.STDOUT)
                # Use the new downloaded mirrorlist (.pacnew) files (if any)
                pacnew_path = self.antergos_mirrorlist + ".pacnew"
                if os.path.exists(pacnew_path):
                    shutil.copy(pacnew_path, self.antergos_mirrorlist)
                self.sync()
                logging.debug("Mirrorlists updated successfully")
            except subprocess.CalledProcessError as why:
                logging.warning(
                    'Cannot update antergos-mirrorlist package: %s', why)
            except OSError as why:
                logging.warning('Error copying new mirrorlist files: %s', why)

    def get_mirror_stats(self):
        """ Retrieve the current mirror status JSON data. """

        mirrors = []

        if not self.json_obj:
            try:
                req = requests.get(
                    self.arch_mirror_status,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                self.json_obj = req.json()
            except requests.RequestException as err:
                logging.debug(
                    'Failed to retrieve mirror status information: %s',
                    err)

        try:
            # Remove servers that have not synced, and parse the "last_sync"
            # times for comparison later.
            mirrors = self.json_obj['urls']

            # Filter incomplete mirrors  and mirrors that haven't synced.
            mirrors = [m for m in mirrors if self.is_good_mirror(m)]
            self.json_obj['urls'] = mirrors
        except KeyError as err:
            logging.debug('Failed to parse retrieved mirror data: %s', err)

        return mirrors

    def sort_mirrors_by_speed(self, mirrors=None, threads=5):
        """ Sorts mirror list """
        # Ensure that "mirrors" is a list and not a generator.
        if not isinstance(mirrors, list):
            mirrors = list(mirrors)

        num_threads = min(threads, len(mirrors))
        # URL input queue.Queue
        q_in = queue.Queue()
        # URL and rate output queue.Queue
        q_out = queue.Queue()

        rates = {}

        # Check version of cryptsetup pkg (used to test mirror speed)
        logging.debug('Checking cryptsetup version with pacman...')
        try:
            cmd = ["pacman", "-Ss", "cryptsetup"]
            line = subprocess.check_output(cmd).decode().split()
            version = line[1]
            logging.debug(
                'cryptsetup version is: %s (used to test mirror speed)', version)
        except subprocess.CalledProcessError as err:
            logging.debug(err)
            version = False

        def worker():
            """ worker thread. Retrieves data to test mirror speed """
            while True:
                if not q_in.empty():
                    url = q_in.get()
                    if version:
                        db_subpath = 'core/os/x86_64/cryptsetup-{0}-x86_64.pkg.tar.xz'
                        db_subpath = db_subpath.format(version)
                    else:
                        db_subpath = 'core/os/x86_64/core.db.tar.gz'
                    db_url = url + db_subpath
                    # Leave the rate as 0 if the connection fails.
                    # TODO: Consider more graceful error handling.
                    rate = 0
                    dtime = float('NaN')

                    req = urllib.request.Request(url=db_url)
                    try:
                        time0 = time.time()
                        with urllib.request.urlopen(req, None, 5) as my_file:
                            size = len(my_file.read())
                            dtime = time.time() - time0
                            rate = size / dtime
                    except (OSError,
                            urllib.error.HTTPError,
                            http.client.HTTPException):
                        pass
                    q_out.put((url, rate, dtime))
                    q_in.task_done()

        # Launch threads
        for _i in range(num_threads):
            my_thread = threading.Thread(target=worker)
            my_thread.start()

        # Load the input queue.Queue
        url_len = 0
        for mirror in mirrors:
            url_len = max(url_len, len(mirror['url']))
            logging.debug("Rating mirror '%s'", mirror['url'])
            q_in.put(mirror['url'])

        # Wait for queue to empty
        old_fraction = 0.0
        while not q_in.empty():
            fraction = 1.0 - float(q_in.qsize()) / float(len(mirrors))
            if fraction != old_fraction:
                self.fraction.send(fraction)
                old_fraction = fraction

        # Wait for all threads to complete
        q_in.join()

        # Log some extra data.
        url_len = str(url_len)
        fmt = '%-' + url_len + 's  %14s  %9s'
        logging.debug(fmt, _("Server"), _("Rate"), _("Time"))

        # Loop over the mirrors just to ensure that we get the rate for each.
        # The value in the loop does not (necessarily) correspond to the mirror.
        fmt = '%-' + url_len + 's  %8.2f KiB/s  %7.2f s'
        for mirror in mirrors:
            url, rate, dtime = q_out.get()
            kibps = rate / 1024.0
            logging.debug(fmt, url, kibps, dtime)
            rates[url] = rate
            q_out.task_done()

        # Sort by rate.
        rated_mirrors = [m for m in mirrors if rates[m['url']] > 0]
        rated_mirrors.sort(key=lambda m: rates[m['url']], reverse=True)

        return rated_mirrors

    def uncomment_antergos_mirrors(self):
        """ Uncomment Antergos mirrors and comment out auto selection so
        rankmirrors can find the best mirror. """

        autoselect = "http://mirrors.antergos.com/$repo/$arch"
        autoselect_on = True
        autoselect_sf = True

        if os.path.exists(self.antergos_mirrorlist):
            with open(self.antergos_mirrorlist) as mirrors:
                lines = [x.strip() for x in mirrors.readlines()]

            for i, line in enumerate(lines):
                srv_comment = line.startswith("#Server")
                srv = line.startswith("Server")

                if autoselect_on and srv and autoselect in line:
                    # Comment out auto selection
                    lines[i] = "#" + line
                    autoselect_on = False
                elif autoselect_sf and srv and 'sourceforge' in line:
                    # Comment out sourceforge auto selection url
                    lines[i] = "#" + line
                    autoselect_sf = False
                elif srv_comment and autoselect not in line and 'sourceforge' not in line:
                    # Uncomment Antergos mirror
                    lines[i] = line.lstrip("#")

            with misc.raised_privileges() as __:
                # Write new one
                with open(self.antergos_mirrorlist, 'w') as mirrors:
                    mirrors.write("\n".join(lines) + "\n")
                self.sync()

    def run_rankmirrors(self):
        """ Runs rankmirrors to sort Antergos mirrors """
        if os.path.exists("/usr/bin/rankmirrors"):
            self.uncomment_antergos_mirrors()
            try:
                # Store rankmirrors output in a temporary file
                with tempfile.TemporaryFile(mode='w+t') as temp_file:
                    cmd = [
                        'rankmirrors',
                        '-n', '0',
                        '-r', 'antergos',
                        self.antergos_mirrorlist]
                    subprocess.call(cmd, stdout=temp_file)
                    temp_file.seek(0)
                    # Copy new mirrorlist to the old one
                    with misc.raised_privileges() as __:
                        with open(self.antergos_mirrorlist, 'w') as antergos_mirrorlist_file:
                            antergos_mirrorlist_file.write(temp_file.read())
                    self.sync()
            except subprocess.CalledProcessError as why:
                logging.debug(
                    'Cannot run rankmirrors on Antergos mirrorlist: %s',
                    why)

    def filter_and_sort_arch_mirrorlist(self):
        """ Sort Arch mirrorlist """
        output = '# Arch Linux mirrorlist generated by Cnchi #\n'
        mlist = self.get_mirror_stats()
        logging.debug("Arch mirror stats downloaded.")
        mirrors = self.sort_mirrors_by_speed(mirrors=mlist)

        for mirror in mirrors:
            self.arch_mirrorlist_ranked.append(mirror['url'])
            output += "Server = {0}{1}/os/{2}\n".format(
                mirror['url'],
                '$repo',
                '$arch')

        # Write modified Arch mirrorlist
        with misc.raised_privileges() as __:
            with open(self.arch_mirrorlist, 'w') as arch_mirrors:
                arch_mirrors.write(output)
            self.sync()

    def run(self):
        """ Run process """

        # Wait until there is an Internet connection available
        while not misc.has_connection():
            time.sleep(2)  # Delay, try again after 2 seconds

        logging.debug("Updating both mirrorlists (Arch and Antergos)...")
        self.update_mirrorlist()

        logging.debug("Filtering and sorting Arch mirrors...")
        self.filter_and_sort_arch_mirrorlist()

        self.arch_mirrorlist_ranked = [
            x for x in self.arch_mirrorlist_ranked if x]
        self.settings.set('rankmirrors_result', self.arch_mirrorlist_ranked)

        logging.debug(
            "Running rankmirrors command to sort Antergos mirrors...")
        self.run_rankmirrors()

        logging.debug("Auto mirror selection has been run successfully.")

        self.fraction.send(1.0)
        self.fraction.close()

def test_module():
    """ Helper function to test this module """
    proc = AutoRankmirrorsProcess({}, None)
    proc.daemon = True
    proc.name = "rankmirrors"
    proc.start()
    proc.join()

if __name__ == '__main__':
    test_module()
