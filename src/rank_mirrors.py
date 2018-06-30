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

import http.client
import logging
import multiprocessing
import os
import queue
import subprocess
import threading
import time
import urllib.request
import urllib.error

import feedparser
import requests

import update_db
import misc.extra as misc

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

class RankMirrors(multiprocessing.Process):
    """ Process class that downloads and sorts the mirrorlist """

    REPOSITORIES = ['arch', 'antergos']
    MIRROR_OK_RSS = 'Alert Details: Successful response received'

    MIRROR_STATUS = {
        'antergos': 'http://rss.uptimerobot.com/u600152-d6c3c10d099982e3a185c2c5ce561a7b',
        'arch': 'http://www.archlinux.org/mirrors/status/json/'}
    MIRRORLIST = {
        'antergos': '/etc/pacman.d/antergos-mirrorlist',
        'arch': '/etc/pacman.d/mirrorlist'}

    MIRRORLIST_URL = {
        'arch': "https://www.archlinux.org/mirrorlist/all/",
        'antergos': ("https://raw.githubusercontent.com/Antergos/antergos-packages/master/"
                     "antergos/antergos-mirrorlist/antergos-mirrorlist")}

    DB_SUBPATHS = {
        'arch': 'core/os/x86_64/{0}-{1}-x86_64.pkg.tar.xz',
        'antergos': '/{0}-{1}-any.pkg.tar.xz'}

    def __init__(self, settings=None, fraction_pipe=None):
        """ Initialize process class
            fraction_pipe is a pipe used to send progress for a gtk.progress widget update
            in another process (see start_rank_mirrors() in mirrors.py) """
        super().__init__()
        self.rankmirrors_pid = None
        # Antergos mirrors info is returned as RSS, arch's as JSON
        self.data = {'arch': {}, 'antergos': {}}
        self.mirrorlist_ranked = {'arch': [], 'antergos': []}
        self.settings = settings
        self.fraction = fraction_pipe

    @staticmethod
    def is_good_mirror(mirror):
        """ Check if mirror info is good enough """
        if 'summary' in mirror.keys():
            # RSS antergos status mirror
            return bool(mirror['summary'] == RankMirrors.MIRROR_OK_RSS)
        # JSON arch status mirror
        return (mirror['last_sync'] and
                mirror['completion_pct'] == 1.0 and
                mirror['protocol'] == 'http' and
                int(mirror['delay']) <= 3600)

    def get_mirror_stats(self):
        """ Retrieve all mirrors status RSS data. """
        if not self.data['arch']:
            try:
                req = requests.get(
                    RankMirrors.MIRROR_STATUS['arch'],
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                self.data['arch'] = req.json()
            except requests.RequestException as err:
                logging.debug(
                    'Failed to retrieve mirror status information: %s', err)

        if not self.data['antergos']:
            self.data['antergos'] = feedparser.parse(
                RankMirrors.MIRROR_STATUS['antergos'])

        mirrors = {'arch': [], 'antergos': []}

        try:
            # Filter incomplete mirrors  and mirrors that haven't synced.
            mirrors['arch'] = self.data['arch']['urls']
            mirrors['arch'] = [m for m in mirrors['arch'] if self.is_good_mirror(m)]
            #self.data['arch']['urls'] = mirrors['arch']
        except KeyError as err:
            logging.debug('Failed to parse retrieved mirror data: %s', err)

        for mirror in self.data['antergos']['items']:
            mirror['url'] = mirror['link']
            if self.is_good_mirror(mirror):
                mirrors['antergos'].append(mirror)

        return mirrors

    @staticmethod
    def get_antergos_mirror_url(mirror_url):
        """ Get full mirror url from the stats mirror url """
        lines = []
        mirrorlist_path = RankMirrors.MIRRORLIST['antergos']
        with open(mirrorlist_path, 'r') as mirror_file:
            lines = mirror_file.readlines()
        for url in lines:
            if mirror_url in url:
                url = url.split('=')[1].strip()
                return url
        logging.warning("%s not found in %s", mirror_url, mirrorlist_path)
        return mirror_url

    @staticmethod
    def get_package_version(name):
        """ Returns pkg_name package version """
        logging.debug('Checking %s version with pacman...', name)
        try:
            cmd = ["/usr/bin/pacman", "-Ss", name]
            line = subprocess.check_output(cmd).decode().split()
            version = line[1]
            logging.debug(
                '%s version is: %s (used to test mirror speed)', name, version)
        except subprocess.CalledProcessError as err:
            logging.debug(err)
            version = False
        return version

    def sort_mirrors_by_speed(self, mirrors=None, max_threads=5):
        """ Sorts mirror list """
        test_packages = {
            'arch': {'name':'cryptsetup', 'version': ''},
            'antergos': {'name': 'ttf-myanmar3', 'version': ''}}

        rated_mirrors = {'arch': [], 'antergos': []}

        for key, value in test_packages.items():
            test_packages[key]['version'] = self.get_package_version(value['name'])

        total_num_mirrors = 0
        for key in mirrors.keys():
            total_num_mirrors += len(mirrors[key])
        num_mirrors_done = 0
        old_fraction = 0.0

        num_threads = min(max_threads, total_num_mirrors)
        # URL input queue.Queue
        q_in = queue.Queue()
        # URL and rate output queue.Queue
        q_out = queue.Queue()

        name = ""
        version = ""
        rates = {}

        for repo in RankMirrors.REPOSITORIES:
            name = test_packages[repo]['name']
            version = test_packages[repo]['version']

            logging.debug("Testing %s mirrors...", repo)

            def worker():
                """ worker thread. Retrieves data to test mirror speed """
                while True:
                    if not q_in.empty():
                        mirror_url, full_url = q_in.get()
                        # Leave the rate as 0 if the connection fails.
                        rate = 0
                        dtime = float('NaN')
                        if full_url:
                            req = urllib.request.Request(url=full_url)
                            try:
                                time0 = time.time()
                                with urllib.request.urlopen(req, None, 5) as my_file:
                                    size = len(my_file.read())
                                    dtime = time.time() - time0
                                    rate = size / dtime
                            except (OSError, urllib.error.HTTPError,
                                    http.client.HTTPException) as err:
                                logging.warning("Couldn't download %s", full_url)
                                logging.warning(err)
                        q_out.put((mirror_url, rate, dtime))
                        q_in.task_done()

            # Launch threads
            for _i in range(num_threads):
                my_thread = threading.Thread(
                    target=worker)
                my_thread.start()

            # Load the input queue.Queue
            url_len = 0
            for mirror in mirrors[repo]:
                url_len = max(url_len, len(mirror['url']))
                logging.debug("Rating mirror '%s'", mirror['url'])
                if repo == 'antergos':
                    url = self.get_antergos_mirror_url(
                        mirror['url'])
                    # Save mirror url
                    mirror['url'] = url
                    # Compose package url
                    package_url = url.replace('$repo', 'antergos')
                    package_url = package_url.replace('$arch', 'x86_64')
                    db_subpath = RankMirrors.DB_SUBPATHS['antergos']
                    db_subpath = db_subpath.format(name, version)
                    package_url += db_subpath
                else:
                    package_url = mirror['url']
                print(mirror['url'], package_url)
                q_in.put((mirror['url'], package_url))

            # Wait for queue to empty
            while not q_in.empty():
                fraction = (float(q_out.qsize()) + num_mirrors_done) / float(total_num_mirrors)
                if fraction != old_fraction:
                    if self.fraction:
                        self.fraction.send(fraction)
                old_fraction = fraction

            num_mirrors_done += q_out.qsize()

            # Wait for all threads to complete
            q_in.join()

            # Log some extra data.
            url_len = str(url_len)
            fmt = '%-' + url_len + 's  %14s  %9s'
            logging.debug(fmt, _("Server"), _("Rate"), _("Time"))

            # Loop over the mirrors just to ensure that we get the rate for each.
            # The value in the loop does not (necessarily) correspond to the mirror.
            fmt = '%-' + url_len + 's  %8.2f KiB/s  %7.2f s'
            for mirror in mirrors[repo]:
                url, rate, dtime = q_out.get()
                kibps = rate / 1024.0
                logging.debug(fmt, url, kibps, dtime)
                rates[url] = rate
                q_out.task_done()

            # Sort by rate.
            try:
                rated_mirrors[repo] = [m for m in mirrors[repo] if rates[m['url']] > 0]
                rated_mirrors[repo].sort(key=lambda m: rates[m['url']], reverse=True)
            except KeyError as err:
                logging.warning(err)

        return rated_mirrors

    @staticmethod
    def uncomment_mirrors():
        """ Uncomment mirrors and comment out auto selection so
        rankmirrors can find the best mirror. """

        comment_urls = [
            'http://mirrors.antergos.com/$repo/$arch',
            'sourceforge']

        for repo in RankMirrors.REPOSITORIES:
            if os.path.exists(RankMirrors.MIRRORLIST[repo]):
                with open(RankMirrors.MIRRORLIST[repo]) as mirrors:
                    lines = [x.strip() for x in mirrors.readlines()]

                for i, line in enumerate(lines):
                    if line.startswith("#Server"):
                        # if server is commented, uncoment it.
                        lines[i] = line.lstrip("#")

                    if line.startswith("Server"):
                        # Let's see if we have to comment out this server
                        for url in comment_urls:
                            if url in line:
                                lines[i] = '#' + line

                # Write new one
                with misc.raised_privileges():
                    try:
                        with open(RankMirrors.MIRRORLIST[repo], 'w') as mirrors_file:
                            mirrors_file.write("\n".join(lines) + "\n")
                    except (OSError, PermissionError) as err:
                        logging.error(err)
        update_db.sync()

    def filter_and_sort_mirrorlists(self):
        """ Filter and sort mirrors """

        mlist = self.get_mirror_stats()
        logging.debug("Mirror stats downloaded.")
        mirrors = self.sort_mirrors_by_speed(mirrors=mlist)

        for repo in ['arch', 'antergos']:
            self.mirrorlist_ranked[repo] = []

        for repo in ['arch', 'antergos']:
            output = '# {} mirrorlist generated by cnchi #\n'.format(repo)
            for mirror in mirrors[repo]:
                self.mirrorlist_ranked[repo].append(mirror['url'])
                if repo == 'arch':
                    output += "Server = {0}{1}/os/{2}\n".format(mirror['url'], '$repo', '$arch')
                else:
                    output += "Server = {0}\n".format(mirror['url'])
            print('*' * 60)
            print(output)
            print('*' * 60)
            # Write modified mirrorlist
            with misc.raised_privileges():
                try:
                    with open(RankMirrors.MIRRORLIST[repo], 'w') as mirrors_file:
                        mirrors_file.write(output)
                except (OSError, PermissionError) as err:
                    logging.error(err)
                update_db.sync()

    def run(self):
        """ Run process """
        # Wait until there is an Internet connection available
        while not misc.has_connection():
            time.sleep(2)  # Delay, try again after 2 seconds

        #logging.debug("Updating both mirrorlists (Arch and Antergos)...")
        #self.update_mirrorlists()

        self.uncomment_mirrors()

        logging.debug("Filtering and sorting mirrors...")
        self.filter_and_sort_mirrorlists()

        if self.settings:
            self.mirrorlist_ranked['arch'] = [
                x for x in self.mirrorlist_ranked['arch'] if x]
            self.settings.set('rankmirrors_result', self.mirrorlist_ranked['arch'])

        logging.debug("Auto mirror selection has been run successfully.")

        if self.fraction:
            self.fraction.send(1.0)
            self.fraction.close()

    @staticmethod
    def update_mirrorlists():
        """ Download mirror lists from archlinux and github """
        for repo in RankMirrors.REPOSITORIES:
            url = RankMirrors.MIRRORLIST_URL[repo]
            req = urllib.request.Request(url=url)
            try:
                with urllib.request.urlopen(req, None, 5) as my_file:
                    data = my_file.read()
                with misc.raised_privileges():
                    with open(RankMirrors.MIRRORLIST[repo], 'wb') as mirror_file:
                        mirror_file.write(data)
            except (OSError, urllib.error.HTTPError, http.client.HTTPException) as err:
                logging.warning("Couldn't download %s", url)
                logging.warning(err)

def test_module():
    """ Helper function to test this module """
    proc = RankMirrors()
    proc.daemon = True
    proc.name = "rankmirrors"
    proc.start()
    proc.join()

if __name__ == '__main__':
    test_module()
