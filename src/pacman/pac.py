#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pac.py
#
#  Copyright (C) 2013 Antergos
#
#  This code is based on previous work by Rémy Oudompheng <remy@archlinux.org>
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

""" Module interface to pyalpm """

import traceback
import sys
import math
import logging

try:
    import pyalpm
except ImportError:
    logging.error(_("pyalpm not found! This installer won't work."))

try:
    import pacman.config as config
except ImportError:
    import config

import queue

class Pac(object):
    """ Comunicates with libalpm using pyalpm """
    def __init__(self, conf_path="/etc/pacman.conf", callback_queue=None):
        self.callback_queue = callback_queue

        self.conflict_to_remove = None

        # Some download indicators (used in cb_dl callback)
        self.last_dl_filename = None
        self.last_dl_progress = 0
        self.last_dl_total = 0

        # Store package total download size
        self.total_download_size = 0

        self.last_event = {}

        if conf_path != None:
            self.config = config.PacmanConfig(conf_path)
            self.handle = self.config.initialize_alpm()

            # Set callback functions
            self.handle.logcb = self.cb_log
            self.handle.dlcb = self.cb_dl
            self.handle.totaldlcb = self.cb_totaldl
            self.handle.eventcb = self.cb_event
            self.handle.questioncb = self.cb_conv
            self.handle.progresscb = self.cb_progress

    def finalize(self, t):
        """ Commit a transaction """
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

    def init_transaction(self, options={}):
        """ Transaction initialization """
        try:
            t = self.handle.init_transaction(
                    cascade = options.get('cascade', False),
                    nodeps = options.get('nodeps', False),
                    force = options.get('force', False),
                    dbonly = options.get('dbonly', False),
                    downloadonly = options.get('downloadonly', False),
                    needed = options.get('needed', False),
                    nosave = options.get('nosave', False),
                    recurse = (options.get('recursive', 0) > 0),
                    recurseall = (options.get('recursive', 0) > 1),
                    unneeded = options.get('unneeded', False),
                    alldeps = (options.get('mode', None) == pyalpm.PKG_REASON_DEPEND),
                    allexplicit = (options.get('mode', None) == pyalpm.PKG_REASON_EXPLICIT))
        except pyalpm.error:
            line = traceback.format_exc()
            logging.error(line)
            t = None
        finally:
            return t

    def do_refresh(self):
        """ Sync databases like pacman -Sy """
        force = True
        for db in self.handle.get_syncdbs():
            t = self.init_transaction()
            db.update(force)
            t.release()
        return 0

    def do_install(self, pkgs, conflicts=[], options={}):
        """ Install a list of packages like pacman -S """
        logging.debug(_("Cnchi will install a list of packages like pacman -S"))

        repos = dict((db.name, db) for db in self.handle.get_syncdbs())

        targets = self.get_targets(pkgs, conflicts)

        if len(targets) == 0:
            logging.error(_("No targets found"))
            return 1
        
        t = self.init_transaction(options)

        if t is None:
            return 1

        pkg_names = []
        
        for pkg in targets:
            # Avoid duplicates
            if pkg.name not in pkg_names:
                logging.debug(_("Adding %s to transaction"), pkg.name)
                t.add_pkg(pkg)
                pkg_names.append(pkg.name)

        logging.debug(_("Finalize transaction..."))
        ok = self.finalize(t)

        return (0 if ok else 1)

    def get_targets(self, pkgs, conflicts=[]):
        """ Get the list of packages needed to install package list 'pkgs' """
        if len(pkgs) == 0:
            return []

        repos = dict((db.name, db) for db in self.handle.get_syncdbs())

        targets = []
        for name in pkgs:
            ok, pkg = self.find_sync_package(name, repos)
            if ok:
                # Check that added package is not in our conflicts list
                # Ex: gnome-extra adds brasero, then we don't want xfburn (which is a default) to be installed
                if pkg.name not in conflicts:
                    targets.append(pkg)
            else:
                # Can't find this one, check if it's a group
                group_pkgs = self.get_group_pkgs(name)
                if group_pkgs != None:
                    # It's a group
                    for pkg in group_pkgs:
                        # Check that added package is not in our conflicts list
                        # Ex: connman conflicts with netctl(openresolv),
                        # which is installed by default with base group
                        if pkg.name not in conflicts and pkg.name not in pkgs:
                            targets.append(pkg)
                else:
                    # No, it wasn't neither a package nor a group. Show error message and continue.
                    logging.error(_("Can't find a package or group called '%s'"), name)

        return targets      

    def find_sync_package(self, pkgname, syncdbs):
        """ Finds a package name in a list of DBs """
        for db in syncdbs.values():
            pkg = db.get_pkg(pkgname)
            if pkg is not None:
                return True, pkg
        return False, "Package '%s' was not found." % pkgname

    def get_group_pkgs(self, group):
        """ Get group packages """
        for repo in self.handle.get_syncdbs():
            grp = repo.read_grp(group)
            if grp is None:
                continue
            else:
                name, pkgs = grp
                return pkgs
        return None

    def queue_event(self, event_type, event_text=""):
        """ Queues events to the event list in the GUI thread """
        if event_type in self.last_event:
            if self.last_event[event_type] == event_text:
                # Do not enqueue the same event twice
                return

        self.last_event[event_type] = event_text

        if event_type == "error":
            # Format message to show file, function, and line where the error was issued
            import inspect
            # Get the previous frame in the stack, otherwise it would be this function
            f = inspect.currentframe().f_back.f_code
            # Dump the message + the name of this function to the log.
            event_text = "%s: %s in %s:%i" % (event_text, f.co_name, f.co_filename, f.co_firstlineno)
        
        if self.callback_queue is None:
            print(event_type, event_text)
            if event_type == "error":
                sys.exit(1)
            else:
                return

        try:
            self.callback_queue.put_nowait((event_type, event_text))
        except queue.Full as err:
            pass

        if event_type == "error":
            # We've queued a fatal event so we must exit installer_process process
            # wait until queue is empty (is emptied in slides.py, in the GUI thread), then exit
            self.callback_queue.join()
            sys.exit(1)

    def get_version(self):
        return "Cnchi running on pyalpm v%s - libalpm v%s" % (pyalpm.version(), pyalpm.alpmversion())

    def get_versions(self):
        return (pyalpm.version(), pyalpm.alpmversion())

    # Callback functions

    def cb_conv(self, *args):
        pass

    def cb_totaldl(self, total_size):
        """ Stores total download size for use in cb_progress """
        self.total_download_size = total_size

    def cb_event(self, ID, event, tupel):
        """ Converts action ID to descriptive text and enqueues it to the events queue """
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
            self.queue_event('info', action)

    def cb_log(self, level, line):
        """ Log pyalpm warning and error messages """
        _logmask = pyalpm.LOG_ERROR | pyalpm.LOG_WARNING

        # Only manage error and warning messages
        if not (level & _logmask):
            return

        if level & pyalpm.LOG_ERROR:
            logging.error(line)
        elif level & pyalpm.LOG_WARNING:
            logging.warning(line)
        #elif level & pyalpm.LOG_DEBUG:
        #    logging.debug(line)
        #elif level & pyalpm.LOG_FUNCTION:
        #    pass

    def cb_progress(self, target, percent, n, i):
        """ Shows install progress """
        if target:
            msg = _("Installing %s (%d/%d)") % (target, i, n)
            percent = i / n
        else:
            msg = _("Checking and loading packages... (%d targets)") % n
            percent = percent / 100
        
        self.queue_event('info', msg)
        self.queue_event('percent', percent)


    def cb_dl(self, filename, tx, total):
        """ Shows downloading progress """
        # Check if a new file is coming
        if filename != self.last_dl_filename or self.last_dl_total != total:
            self.last_dl_filename = filename
            self.last_dl_total = total
            self.last_dl_progress = 0

            # If pacman is just updating databases total_download_size will be zero
            if self.total_download_size == 0:
                ext = ".db"
                if filename.endswith(ext):
                    filename = filename[:-len(ext)]
                text = _("Updating %s database") % filename
            else:
                ext = ".pkg.tar.xz"
                if filename.endswith(ext):
                    filename = filename[:-len(ext)]
                text = _("Downloading %s...") % filename

            self.queue_event('info', text)
            self.queue_event('percent', 0)
        else:
            # Compute a progress indicator
            if self.last_dl_total > 0:
                progress = tx / self.last_dl_total
            else:
                # If total is unknown, use log(kBytes)²/2
                progress = (math.log(1 + tx / 1024) ** 2 / 2) / 100

            # Update progress only if it has grown
            if progress > self.last_dl_progress:
                #logging.debug("filename [%s], tx [%d], total [%d]", filename, tx, total)
                self.last_dl_progress = progress
                self.queue_event('percent', progress)

''' Test case '''
if __name__ == "__main__":
    import gettext
    _ = gettext.gettext

    try:
        alpm = Pac("/etc/pacman.conf")
    except Exception as err:
        logging.error(err)
        raise InstallError("Can't initialize pyalpm: %s" % err)        

    #alpm.do_refresh()
    pacman_options = {}
    pacman_options["downloadonly"] = True
    alpm.do_install(pkgs=["base"], conflicts=[], options=pacman_options)
