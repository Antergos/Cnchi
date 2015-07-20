#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rank_mirrors.py
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

""" Creates mirrorlist sorted by both latest updates and fastest connection """

import threading
import subprocess
import logging
import time
import os
import shutil
import requests
import tempfile

import misc.misc as misc


class AutoRankmirrorsThread(threading.Thread):
    """ Thread class that downloads and sorts the mirrorlist """

    def __init__(self):
        """ Initialize thread class """
        super(AutoRankmirrorsThread, self).__init__()
        self.rankmirrors_pid = None
        self.antergos_mirrorlist = "/etc/pacman.d/antergos-mirrorlist"
        self.arch_mirrorlist = "/etc/pacman.d/mirrorlist"
        self.arch_mirror_status = "http://www.archlinux.org/mirrors/status/json/"

    @staticmethod
    def check_mirror_status(mirrors, url):
        for mirror in mirrors:
            if mirror['url'] in url and mirror['completion_pct'] == 1 and mirror['score'] <= 4:
                return True
        return False

    def sync(self, files_to_sync=None):
        """ Synchronize cached writes to persistent storage """
        with misc.raised_privileges():
            try:
                cmd = ['sync']
                if files_to_sync:
                    cmd.extend(files_to_sync)
                subprocess.check_call(cmd)
            except subprocess.CalledProcessError as why:
                logging.warning(_("Can't synchronize cached writes to persistent storage: %s"), why)

    def update_mirrorlists(self):
        """ Make sure we have the latest mirrorlist and antergos-mirrorlist files """
        with misc.raised_privileges():
            try:
                cmd = [
                    'pacman', '-Syy', '--noconfirm', '--noprogressbar',
                    '--quiet', 'pacman-mirrorlist', 'antergos-mirrorlist']
                subprocess.check_call(cmd)
                # Use the new downloaded mirrorlist (.pacnew) files (if any)
                files = ['mirrorlist', 'antergos-mirrorlist']
                for filename in files:
                    path = os.path.join("/etc/pacman.d", filename)
                    pacnew_path = path + ".pacnew"
                    if os.path.exists(pacnew_path):
                        shutil.copy(pacnew_path, path)
            except subprocess.CalledProcessError as why:
                logging.debug(_('Update of antergos-mirrorlist package failed with error: %s'), why)
            except OSError as why:
                logging.debug(_('Error copying new mirrorlist files: %s'), why)
        self.sync([self.arch_mirrorlist, self.antergos_mirrorlist])

    def run_reflector(self):
        """
        Reflector actually does perform speed tests when called and doesn't use speed results
        from Arch's main server like we originally thought. If you monitor your network I/O
        while running reflector command, you will see it is doing much more than
        downloading the 4kb mirrorlist file. If ran with --verbose and without --save param it
        will output the speed test results to STDOUT.
        """
        if os.path.exists("/usr/bin/reflector"):
            with misc.raised_privileges():
                try:
                    cmd = ['reflector', '-l', '30', '-p', 'http', '-f', '20', '--save', self.arch_mirrorlist]
                    subprocess.check_call(cmd)
                except subprocess.CalledProcessError as why:
                    logging.debug(_('Error running reflector on Arch mirrorlist: %s'), why)
            self.sync([self.arch_mirrorlist])

    def uncomment_antergos_mirrors(self):
        """ Uncomment Antergos mirrors and comment out auto selection so
        rankmirrors can find the best mirror. """

        autoselect = "http://mirrors.antergos.com/$repo/$arch"

        if os.path.exists(self.antergos_mirrorlist):
            with open(self.antergos_mirrorlist) as mirrors:
                lines = [x.strip() for x in mirrors.readlines()]

            for i in range(len(lines)):
                if lines[i].startswith("Server") and autoselect in lines[i]:
                    # Comment out auto selection
                    lines[i] = "#" + lines[i]
                elif lines[i].startswith("#Server") and autoselect not in lines[i]:
                    # Uncomment Antergos mirror
                    lines[i] = lines[i].lstrip("#")

                # sourceforge server does not get updated as often as necessary
                if "sourceforge" in lines[i]:
                    lines[i] = "#" + lines[i]

            with misc.raised_privileges():
                # Write new one
                with open(self.antergos_mirrorlist, 'w') as mirrors:
                    mirrors.write("\n".join(lines) + "\n")
            self.sync([self.antergos_mirrorlist])

    def run_rankmirrors(self):
        if os.path.exists("/usr/bin/rankmirrors"):
            # Uncomment Antergos mirrors and comment out auto selection so
            # rankmirrors can find the best mirror.
            self.uncomment_antergos_mirrors()

            with misc.raised_privileges():
                try:
                    # Store rankmirrors output in a temporary file
                    with tempfile.TemporaryFile(mode='w+t') as temp_file:
                        cmd = ['rankmirrors', '-n', '0', '-r', 'antergos', self.antergos_mirrorlist]
                        subprocess.call(cmd, stdout=temp_file)
                        temp_file.seek(0)
                        # Copy new mirrorlist to the old one
                        with open(self.antergos_mirrorlist, 'w') as antergos_mirrorlist_file:
                            antergos_mirrorlist_file.write(temp_file.read())
                except subprocess.CalledProcessError as why:
                    logging.debug(_('Error running rankmirrors on Antergos mirrorlist: %s'), why)
            self.sync([self.antergos_mirrorlist])

    def remove_bad_mirrors(self):
        if os.path.exists(self.arch_mirrorlist):
            # Use session to avoid silly warning
            # See https://github.com/kennethreitz/requests/issues/1882
            with requests.Session() as session:
                status = session.get(self.arch_mirror_status).json()
                mirrors = status['urls']

            with open(self.arch_mirrorlist) as arch_mirrors:
                lines = [x.strip() for x in arch_mirrors.readlines()]

            for i in range(len(lines)):
                server_uncommented = lines[i].startswith("Server")
                server_commented = lines[i].startswith("#Server")
                if server_commented or server_uncommented:
                    url = lines[i].split('=')[1].strip()
                    check = self.check_mirror_status(mirrors, url)
                    if not check and server_uncommented:
                        # Bad mirror, comment it
                        logging.debug('Removing bad mirror: %s', lines[i])
                        lines[i] = "#" + lines[i]
                    if check and server_commented:
                        # It's a good mirror, uncomment it
                        lines[i] = lines[i].lstrip("#")

            # Write modified Arch mirrorlist
            with misc.raised_privileges():
                with open(self.arch_mirrorlist, 'w') as arch_mirrors:
                    arch_mirrors.write("\n".join(lines) + "\n")
            self.sync([self.arch_mirrorlist])

    def run(self):
        """ Run thread """

        # Wait until there is an Internet connection available
        while not misc.has_connection():
            time.sleep(4)  # Delay, try again after 4 seconds

        logging.debug(_("Update both mirrorlists (Arch and Antergos)"))
        self.update_mirrorlists()

        logging.debug(_("Run reflector command to sort Arch mirrors"))
        self.run_reflector()

        logging.debug(_("Run rankmirrors command to sort Antergos mirrors"))
        self.run_rankmirrors()

        logging.debug(_("Check Arch mirrorlist against mirror status data and remove any bad mirrors."))
        self.remove_bad_mirrors()

        logging.debug(_("Auto mirror selection has been run successfully"))


if __name__ == '__main__':
    def _(x): return x

    rank_mirrors = AutoRankmirrorsThread()
    rank_mirrors.start()
