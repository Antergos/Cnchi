#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pac.py
#
#  Copyright (C) 2011 Rémy Oudompheng <remy@archlinux.org>
#  Copyright (C) 2013 Antergos
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import traceback
import sys
import locale
import gettext
import math
import logging
from multiprocessing import Queue
import queue

try:
    import pyalpm
    from pacman import config
except:
    print("pyalpm not found! This installer won't work.")
    sys.exit(1)

class Pac(object):
    def __init__(self, conf_path, callback_queue):
        self.callback_queue = callback_queue

        self.conflict_to_remove = None

        # Some progress indicators (used in cb_progress callback)
        self.last_target = None
        self.last_percent = 100
        self.last_i = -1

        # Some download indicators (used in cb_dl callback)
        self.last_dl_filename = None
        self.last_dl_progress = None
        self.last_dl_total = None

        self.last_event = {}

        if conf_path != None:
            self.config = config.PacmanConfig(conf_path)
            self.handle = self.config.initialize_alpm()

            # Set callback functions
            self.handle.dlcb = self.cb_dl
            self.handle.totaldlcb = self.cb_totaldl
            self.handle.eventcb = self.cb_event
            self.handle.questioncb = self.cb_conv
            self.handle.progresscb = self.cb_progress
            self.handle.logcb = self.cb_log

    ###################################################################
    # Transaction

    def finalize(self, t):
        # Commit a transaction
        try:
            t.prepare()
            t.commit()
        except pyalpm.error:
            line = traceback.format_exc()
            logging.error(line)
            t.release()
            return False
        t.release()
        return True

    def init_transaction(self, **options):
        # Transaction initialization
        try:
            t = self.handle.init_transaction(**options)
        except pyalpm.error:
            line = traceback.format_exc()
            logging.error(line)
            return None
        return t

    '''
    def init_transaction(self, options):
        # Transaction initialization
        #self.handle.dlcb = self.cb_dl
        #self.handle.eventcb = self.cb_event
        #self.handle.questioncb = self.cb_conv
        #self.handle.progresscb = self.cb_progress
        t = self.handle.init_transaction(
                cascade = getattr(options, "cascade", False),
                nodeps = getattr(options, "nodeps", False),
                force = getattr(options, 'force', False),
                dbonly = getattr(options, 'dbonly', False),
                downloadonly = getattr(options, 'downloadonly', False),
                nosave = getattr(options, 'nosave', False),
                recurse = (getattr(options, 'recursive', 0) > 0),
                recurseall = (getattr(options, 'recursive', 0) > 1),
                unneeded = getattr(options, 'unneeded', False),
                alldeps = (getattr(options, 'mode', None) == pyalpm.PKG_REASON_DEPEND),
                allexplicit = (getattr(options, 'mode', None) == pyalpm.PKG_REASON_EXPLICIT))
        return t
    '''

    ###################################################################
    # pacman -Sy (refresh) and pacman -S (install)

    def do_refresh(self):
        # Sync databases like pacman -Sy
        force = True
        for db in self.handle.get_syncdbs():
            t = self.init_transaction()
            db.update(force)
            t.release()
        return 0

    def do_install(self, pkgs, conflicts=[]):
        # Install a list of packages like pacman -S
        logging.debug("Install a list of packages like pacman -S")
        if len(pkgs) == 0:
            logging.error("No targets specified")
            return 1

        repos = dict((db.name,db) for db in self.handle.get_syncdbs())

        targets = []
        for name in pkgs:
            ok, pkg = self.find_sync_package(name, repos)
            if ok:
                targets.append(pkg)
            else:
                # Can't find this one, check if it's a group
                group_pkgs = self.get_group_pkgs(name)
                if group_pkgs != None:
                    for pkg in group_pkgs:
                        # Check that added package is not in our conflicts list
                        # Ex: connman conflicts with netctl(openresolv), which is
                        # installed by default with base group
                        if pkg.name not in conflicts and pkg.name not in pkgs:
                            targets.append(pkg)
                else:
                    # No, it wasn't neither a package nor a group
                    logging.error(pkg)

        if len(targets) == 0:
            logging.error("No targets found")
            return 1

        t = self.init_transaction()

        if t is None:
            return 1

        pkg_names = []

        for pkg in targets:
            if pkg.name not in pkg_names:
                logging.debug("Adding %s to transaction" % pkg.name)
                t.add_pkg(pkg)
                pkg_names.append(pkg.name)


        ok = self.finalize(t)

        return (0 if ok else 1)

    def find_sync_package(self, pkgname, syncdbs):
        # Finds a package name in a list of DBs
        for db in syncdbs.values():
            pkg = db.get_pkg(pkgname)
            if pkg is not None:
                return True, pkg
        return False, "Package '%s' was not found." % pkgname

    def get_group_pkgs(self, group):
        # Get group packages
        for repo in self.handle.get_syncdbs():
            grp = repo.read_grp(group)
            if grp is None:
                continue
            else:
                name, pkgs = grp
                return pkgs
        return None

    ###################################################################
    # Queue event

    def queue_event(self, event_type, event_text=""):
        if event_type in self.last_event:
            if self.last_event[event_type] == event_text:
                # do not repeat same event
                return

        self.last_event[event_type] = event_text

        if event_type == "error":
            # format message to show file, function, and line where the error
            # was issued
            import inspect
            # Get the previous frame in the stack, otherwise it would be this function
            f = inspect.currentframe().f_back.f_code
            # Dump the message + the name of this function to the log.
            event_text = "%s: %s in %s:%i" % (event_text, f.co_name, f.co_filename, f.co_firstlineno)

        try:
            self.callback_queue.put_nowait((event_type, event_text))
        except queue.Full:
            pass

        if event_type == "error":
            # We've queued a fatal event so we must exit installer_process process
            # wait until queue is empty (is emptied in slides.py), then exit
            self.callback_queue.join()
            sys.exit(1)


    ###################################################################
    # Version functions

    def get_version(self):
        return "Cnchi running on pyalpm v%s - libalpm v%s" % (pyalpm.version(), pyalpm.alpmversion())

    def get_versions(self):
        return (pyalpm.version(), pyalpm.alpmversion())

    ###################################################################
    # Callback functions

    def cb_conv(self, *args):
        pass

    def cb_totaldl(self, total_size):
        pass

    def cb_event(self, ID, event, tupel):
        action = ""

        if ID is 1:
            action = _('Checking dependencies...')
        elif ID is 3:
            action = _('Checking file conflicts...')
        elif ID is 5:
            action = _('Resolving dependencies...')
        elif ID is 7:
            action = _('Checking inter conflicts...')
        elif ID is 9:
            # action = _('Installing...')
            action = ""
        elif ID is 11:
            action = _('Removing...')
        elif ID is 13:
            action = _('Upgrading...')
        elif ID is 15:
            action = _('Checking integrity...')
        elif ID is 17:
            action = _('Loading packages files...')
        elif ID is 26:
            action = _('Configuring...')
        elif ID is 27:
            action = _('Downloading a file')
        else:
            action = ""

        if len(action) > 0:
            self.queue_event('action', action)

    def cb_log(self, level, line):
        _logmask = pyalpm.LOG_ERROR | pyalpm.LOG_WARNING

        # Only manage error and warning messages
        if not (level & _logmask):
            return

        if level & pyalpm.LOG_ERROR:
            logging.error(line)
        elif level & pyalpm.LOG_WARNING:
            logging.warning(line)
        '''
        elif level & pyalpm.LOG_DEBUG:
            logging.debug(line)
        elif level & pyalpm.LOG_FUNCTION:
            pass
        '''

    def cb_progress(self, _target, _percent, n, i):
        if _target:
            target = _("Installing %s (%d/%d)") % (_target, i, n)
            self.queue_event('global_percent', i / n)
        else:
            target = _("Checking and loading packages...")

        percent = _percent / 100
        self.queue_event('target', target)
        self.queue_event('percent', percent)

    def cb_dl(self, filename, tx, total):
        # Check if a new file is coming
        # (if filename has changed or total file size has changed)
        if filename != self.last_dl_filename or self.last_dl_total != total:
            # Yes, new file
            self.last_dl_filename = filename
            self.last_dl_total = total
            self.last_dl_progress = 0
            progress = 0
            # text = _("Downloading %s: %d/%d") % (filename, tx, total)
            text = _("Downloading '%s'") % filename
            self.queue_event('action', text)
            self.queue_event('percent', progress)
        else:
            # Compute a progress indicator
            if self.last_dl_total > 0:
                progress = tx / self.last_dl_total
            else:
                # if total is unknown, use log(kBytes)²/2
                progress = (math.log(1 + tx / 1024) ** 2 / 2) / 100

            if progress > self.last_dl_progress:
                self.last_dl_progress = progress
                #text = _("Downloading %s: %d/%d") % (filename, tx, total)
                #text = _("Downloading '%s'") % filename
                #self.queue_event('action', text)
                self.queue_event('percent', progress)

