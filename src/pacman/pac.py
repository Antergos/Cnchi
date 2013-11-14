#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pac.py
#
#  Copyright (C) 2011 Rémy Oudompheng <remy@archlinux.org>
#  Copyright 2013 Manjaro
#  Copyright 2013 Antergos
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

class Pac(object):
    def __init__(self, conf_path, callback_queue):
        
        self.callback_queue = callback_queue
        
        # Transaction
        self.t = None
        
        self.conflict_to_remove = None
        
        # Packages lists
        self.to_remove = []
        self.to_add = []
        self.to_update = []
        self.to_provide = []
        
        # Some progress indicators (used in cb_progress callback)
        self.last_target = None
        self.last_percent = 100
        self.last_i = -1
        
        # Some download indicators (used in cb_dl callback)
        self.last_dl_filename = None
        self.last_dl_progress = None
        self.last_dl_total = None
        
        # Packages to be removed
        # E.g: connman conflicts with netctl(openresolv), which is installed
        # by default with base group
        self.conflicts = []
        
        # avoid adding a package that has been added in the past
        self.listofpackages = []
        
        self.action = ""
        
        self.already_transferred = 0
        self.total_size = 0
        
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
            
            # Check if HoldPkg option is set
            self.holdpkg = None
            if 'HoldPkg' in self.config.options:
                self.holdpkg = self.config.options['HoldPkg']

##########################################################################################

    def init_transaction(self, **options):
        try:
            _t = self.handle.init_transaction(**options)
            # print(_t.flags)
            return _t
        except pyalpm.error:
            line = traceback.format_exc()
            self.queue_event("error", line)
            return None

    def release_transaction(self):
        if self.t != None:
            try:
                self.t.release()
                self.t = None
            except pyalpm.error:
                self.queue_event("error", traceback.format_exc())


        
    # Sync databases like pacman -Sy
    def do_refresh(self):
        self.release_transaction()
        for db in self.handle.get_syncdbs():
            try:
                self.t = self.init_transaction()                
                db.update(force=False)
                if self.t != None:
                    self.t.release()
                    self.t = None
            except pyalpm.error:
                self.queue_event("error", traceback.format_exc())
                return

    def format_size(self, size):
        KiB_size = size / 1024
        if KiB_size < 1000:
            size_string = '%.1f KiB' % KiB_size
        else:
            size_string = '%.2f MiB' % (KiB_size / 1024)
        return size_string

    def install_packages(self, pkg_names, conflicts):
        self.to_add = []
        self.conflicts = conflicts

        for pkgname in pkg_names:
            self.to_add.append(pkgname)

        self.to_remove = []

        if self.to_add and self.t == None:
            self.t = self.init_transaction()
            if self.t != None:
                for pkgname in self.to_add:
                    self.add_package(pkgname)
                try:
                    self.t.prepare()
                    self.t.commit()
                except pyalpm.error:
                    line = traceback.format_exc()
                    if "pm_errno 25" in line:
                        pass
                    elif "pm_errno 27" in line:
                        # transaction is not ready
                        print(line)
                    else:
                        self.queue_event("error", line)
                self.release_transaction()
    
    def add_package(self, pkgname):
        #print("searching %s" % pkgname)
        found = False
        try:
            for repo in self.handle.get_syncdbs():
                if pkgname not in self.conflicts:
                    pkg = repo.get_pkg(pkgname)
                    if pkg:
                        #print("adding %s" % pkgname)
                        if pkg not in self.listofpackages:
                            self.listofpackages.append(pkg)
                            self.t.add_pkg(pkg)
                        found = True
                        break
                    else:
                        # Couldn't find package in repo, 
                        # maybe it's a group of packages.
                        group_list = self.select_from_groups([repo], pkgname)
                        if group_list:
                            # Yes, it was a group of packages
                            for pkg_in_group in group_list:
                                if pkg_in_group not in self.listofpackages and \
                                   pkg_in_group not in self.conflicts:
                                    self.listofpackages.append(pkg_in_group)
                                    self.t.add_pkg(pkg_in_group)
                            found = True
                            break
        except pyalpm.error:
            line = traceback.format_exc()
            if "pm_errno 25" in line:
                pass
            else:
                self.queue_event("error", line)
                
        if not found:
            print(_("Package %s not found in any repo!") % pkgname)

    def select_from_groups(self, repos, pkg_group):
        pkgs_in_group = []
        for repo in repos:
            grp = repo.read_grp(pkg_group)
            if grp is None:
                continue
            else:
                name, pkgs = grp
                for pkg in pkgs:
                    if pkg.name not in self.conflicts:
                        pkgs_in_group.append(repo.get_pkg(pkg.name))
                break

        return pkgs_in_group

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
            # Get the previous frame in the stack, otherwise it would
            # be this function!!!
            f = inspect.currentframe().f_back.f_code
            # Dump the message + the name of this function to the log.
            event_text = "%s: %s in %s:%i" % (event_text, f.co_name, f.co_filename, f.co_firstlineno)

        try:
            self.callback_queue.put_nowait((event_type, event_text))
        except queue.Full:
            pass

        #if event_type != "percent":
        #    logging.info(event_text)
        
        if event_type == "error":
            # We've queued a fatal event so we must exit installer_process process
            # wait until queue is empty (is emptied in slides.py), then exit
            self.callback_queue.join()
            sys.exit(1)
        
    # Callback functions ####################################################################################
    
    def cb_event(self, ID, event, tupel):
        if ID is 1:
            self.action = _('Checking dependencies...')
        elif ID is 3:
            self.action = _('Checking file conflicts...')
        elif ID is 5:
            self.action = _('Resolving dependencies...')
        elif ID is 7:
            self.action = _('Checking inter conflicts...')
        elif ID is 9:
            #self.action = _('Installing...')
            self.action = ''
        elif ID is 11:
            self.action = _('Removing...')
        elif ID is 13:
            self.action = _('Upgrading...')
        elif ID is 15:
            self.action = _('Checking integrity...')
            self.already_transferred = 0
        elif ID is 17:
            self.action = _('Loading packages files...')
        elif ID is 26:
            self.action = _('Configuring...')
        elif ID is 27:
            self.action = _('Downloading a file')
        else:
            self.action = ''

        if len(self.action) > 0:
            self.queue_event("action", self.action)

    def cb_conv(self, *args):
        pass

    def cb_log(self, level, line):
        # Only manage error and warning messages
        _logmask = pyalpm.LOG_ERROR | pyalpm.LOG_WARNING

        if not (level & _logmask):
            return

        if level & pyalpm.LOG_ERROR or level & pyalpm.LOG_WARNING:
            # Even if there is a real error we're not sure we want to abort all installation
            # Instead of issuing a fatal error we just log an error message
            logging.error(line)
        
        '''
        if level & pyalpm.LOG_ERROR:
            if 'linux' not in self.target and 'lxdm' not in self.target:
                self.error = _("ERROR: %s") % line
                self.release_transaction()
                self.queue_event("error", line)
                logging.warning(line)
            else:
                logging.warning(line)
        elif level & pyalpm.LOG_WARNING:
            self.warning = _("WARNING: %s") % line
            self.queue_event('warning', line)
        elif level & pyalpm.LOG_DEBUG:
            line = _("DEBUG: %s") % line
            print(line)
        elif level & pyalpm.LOG_FUNCTION:
            line = _("FUNC: %s") % line
            print(line)
        '''

    def cb_totaldl(self, _total_size):
        self.total_size = _total_size

    def get_size(self, size):
        size_txt = "%db" % size
        if size >= 1000000000:
            size /= 1000000000
            size_txt = "%dG" % size
        elif size >= 1000000:
            size /= 1000000
            size_txt = "%dM" % size
        elif size >= 1000:
            size /= 1000
            size_txt = "%dK" % size

        return size_txt






    def cb_dl(self, filename, tx, total):
        # Check if a new file is coming
        if filename != self.last_dl_filename or self.last_dl_total != total:
            self.last_dl_filename = filename
            self.last_dl_total = total
            self.last_dl_progress = 0
            text = _("Download %s: %d/%d" % (filename, tx, total))
            self.queue_event('action', text)

        # Compute a progress indicator
        if self.last_dl_total > 0:
            progress = (tx * 25) // _last_dl_total
        else:
            # if total is unknown, use log(kBytes)²/2
            progress = int(math.log(1 + tx / 1024) ** 2 / 2)

        if progress > self.last_dl_progress:
            self.last_dl_progress = progress
            #text = _("Download %s: %d/%d" % (filename, tx, total))
            #self.queue_event('action', text)
            self.queue_event('percent', progress)

    # Display progress percentage for target i/n
    def cb_progress(self, target, percent, n, i):
        if len(target) == 0:
            # Abstract progress
            if percent < self.last_percent or i < self.last_i:
                self.queue_event('info', _("Progress (%d targets)") % n)
            self.last_i = i
            self.queue_event('target', _("Checking and loading packages..."))
            self.queue_event('percent', percent / 100)
        else:
            # Progress for some target
            if target != self.last_target or percent < self.last_percent:
                self.last_target = target
                self.last_percent = 0
                self.target = _("Installing %s (%d/%d)") % (target, i, n)
                self.queue_event('target', target)
                self.queue_event('percent', percent / 100)
                self.queue_event('global_percent', i / n)
        
        self.last_percent = percent
