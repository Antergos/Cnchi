#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pac.py
#
#  This file has fragments of code from 'pamac'
#  (pamac is a package manager from Manjaro team)
#  Check it at http://git.manjaro.org/core/pamac
#  
#  Copyright 2013 Manjaro (http://manjaro.org)
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
#  
#  Antergos Team:
#   Alex Filgueira (faidoc) <alexfilgueira.antergos.com>
#   Raúl Granados (pollitux) <raulgranados.antergos.com>
#   Gustau Castells (karasu) <karasu.antergos.com>
#   Kirill Omelchenko (omelcheck) <omelchek.antergos.com>
#   Marc Miralles (arcnexus) <arcnexus.antergos.com>
#   Alex Skinner (skinner) <skinner.antergos.com>
    
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
    from pacman import pac_config
except:
    print("pyalpm not found! This installer won't work.")


class Pac(object):
    def __init__(self, conf, callback_queue):
        
        self.callback_queue = callback_queue
        self.t = None
        self.conflict_to_remove = None
        self.to_remove = []
        self.to_add = []
        self.to_update = []
        self.to_provide = []
        
        # Packages to be removed
        # E.g: connman conflicts with netctl(openresolv), which is installed
        # by default with base group
        self.conflicts = []
        
        # avoid adding a package that has been added in the past
        self.listofpackages = []
        
        self.action = ""
        self.percent = 0
        
        self.already_transferred = 0
        self.total_size = 0
        
        self.last_event = {}
        
        if conf != None:
            self.pacman_conf = pac_config.PacmanConfig(conf)
            self.handle = self.pacman_conf.initialize_alpm()
            self.handle.dlcb = self.cb_dl
            self.handle.totaldlcb = self.cb_totaldl
            self.handle.eventcb = self.cb_event
            self.handle.questioncb = self.cb_conv
            self.handle.progresscb = self.cb_progress
            self.handle.logcb = self.cb_log
            self.holdpkg = None
            if 'HoldPkg' in self.pacman_conf.options:
                self.holdpkg = self.pacman_conf.options['HoldPkg']

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

    '''
    # OLD Install_packages
    def install_packages(self, pkg_names):
        self.to_add = []

        for pkgname in pkg_names:
            self.to_add.append(pkgname)

        self.to_remove = []

        if self.to_add and self.t_lock is False:    
            self.t = self.init_transaction()
            if self.t is not False:
                for pkgname in self.to_add:
                    self.add_package(pkgname)
                try:
                    self.t.prepare()
                    self.t.commit()
                    self.t_lock = False
                except pyalpm.error:
                    line = traceback.format_exc()
                    self.queue_event("error", line)
                self.t.release()
    '''
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

    '''
    # old add_package
    def add_package(self, pkgname):
        #print("searching %s" % pkgname)
        try:
            for repo in self.handle.get_syncdbs():
                pkg = repo.get_pkg(pkgname)
                if pkg:
                    #print("adding %s" % pkgname)
                    self.t.add_pkg(pkg)
                    break
                else:
                    #this is used for groups.  However, antergos repo coming
                    # first causes errors.  So I just moved them to the back.
                    l = pyalpm.find_grp_pkgs([repo], pkgname)
                    if l:
                        lss = []
                        for pakg in l:
                                self.t.add_pkg(pakg)
        except pyalpm.error:
            line = traceback.format_exc()
            self.queue_event("error", line)    
    '''
    
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

        logging.info(event_text)
        
        if event_type == "error":
            # We've queued a fatal event so we must exit installer_process process
            # wait until queue is empty (is emptied in slides.py), then exit
            self.callback_queue.join()
            sys.exit(1)

         
    # Callback functions 
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
            print('Loading packages files')
        elif ID is 26:
            self.action = _('Configuring...')
            print(_('Configuring a package'))
        elif ID is 27:
            print(_('Downloading a file'))
        else:
            self.action = ''

        if len(self.action) > 0:
            self.queue_event("action", self.action)
        #self.queue_event("target", '')
        #self.queue_event("percent", 0)

        #print(ID, event)

    def cb_conv(self, *args):
        pass
        #print("conversation", args)

    def cb_log(self, level, line):
        # Only manage error and warning messages
        _logmask = pyalpm.LOG_ERROR | pyalpm.LOG_WARNING

        if not (level & _logmask):
            return

        if level & pyalpm.LOG_ERROR:
            if 'linux' not in self.target and 'lxdm' not in self.target:
                self.error = _("ERROR: %s") % line
                #print(line)
                self.release_transaction()
                self.queue_event("error", line)
            else:
                pass
        elif level & pyalpm.LOG_WARNING:
            self.warning = _("WARNING: %s") % line
            self.queue_event("warning", line)
            #print(line)
        '''
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

    def cb_dl(self, _target, _transferred, total):
        if self.t != None:
            if self.total_size > 0:
                fraction = (_transferred + self.already_transferred) / self.total_size
            size = 0
            if self.t.to_remove or self.t.to_add:
                for pkg in self.t.to_remove + self.t.to_add:
                    if pkg.name + '-' + pkg.version in _target:
                        size = pkg.size
                if _transferred == size:
                    self.already_transferred += size
                fsize = self.get_size(self.total_size)
                self.action = _('Downloading %s...') % _target
                self.target = _target
                if fraction > 1:
                    self.percent = 0
                else:
                    self.percent = math.floor(fraction * 100) / 100
                self.queue_event("action", self.action)
                self.queue_event("percent", self.percent)
            else:
                self.action = _('Refreshing %s...') % _target
                self.target = _target
                # can't we know which percent has 'refreshed' ?
                self.percent = 0
                self.queue_event("action", self.action)
                #self.queue_event("percent", self.percent)

    def cb_progress(self, _target, _percent, n, i):
        if _target:
            self.target = _("Installing %s (%d/%d)") % (_target, i, n)
        else:
            self.target = _("Checking and loading packages...")
        self.percent = _percent / 100
        self.queue_event("target", self.target)
        self.queue_event("percent", self.percent)
