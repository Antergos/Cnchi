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
#  Copyright 2013 Cinnarch (http://www.cinnarch.com)
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
#  Cinnarch Team:
#   Alex Filgueira (faidoc) <alexfilgueira.cinnarch.com>
#   Raúl Granados (pollitux) <raulgranados.cinnarch.com>
#   Gustau Castells (karasu) <karasu.cinnarch.com>
#   Kirill Omelchenko (omelcheck) <omelchek.cinnarch.com>
#   Marc Miralles (arcnexus) <arcnexus.cinnarch.com>
#   Alex Skinner (skinner) <skinner.cinnarch.com>

import pyalpm
import traceback
import sys
import locale
import gettext

from pacman import pac_config

class Pac(object):
    def __init__(self, conf, callback_queue):
        
        self.callback_queue = callback_queue
        self.t = None
        self.t_lock = False
        self.conflict_to_remove = None
        self.to_remove = []
        self.to_add = []
        self.to_update = []
        self.to_provide = []
        
        self.action = ""
        self.percent = 0
        
        self.already_transferred = 0
        self.total_size = 0
        
        
        if conf is not None:
            self.pacman_conf = pac_config.PacmanConfig(conf)
            self.handle = self.pacman_conf.initialize_alpm()
            self.holdpkg = None
            if 'HoldPkg' in self.pacman_conf.options:
                self.holdpkg = self.pacman_conf.options['HoldPkg']

    def init_transaction(self, **options):
        # Transaction initialization
        self.handle.dlcb = self.cb_dl
        self.handle.totaldlcb = self.cb_totaldl
        self.handle.eventcb = self.cb_event
        self.handle.questioncb = self.cb_conv
        self.handle.progresscb = self.cb_progress
        self.handle.logcb = self.cb_log
        try:
            _t = self.handle.init_transaction(**options)
            #print(_t.flags)
            self.t_lock = True
            return _t
        except pyalpm.error:
            line = traceback.format_exc()
            self.queue_event("error", line)
            return False
    
    # Sync databases like pacman -Sy
    def do_refresh(self):
        for db in self.handle.get_syncdbs():
            if self.t_lock is False:
                self.t = self.init_transaction()
                try:
                    db.update(force=False)
                    self.t.release()
                    self.t_lock = False
                except pyalpm.error:
                    line = traceback.format_exc()
                    self.queue_event("error", line)
                    self.t_lock = False
                    break

    def format_size(self, size):
        KiB_size = size / 1024
        if KiB_size < 1000:
            size_string = '%.1f KiB' % KiB_size
            return size_string
        else:
            size_string = '%.2f MiB' % (KiB_size / 1024)
            return size_string

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
                    #this is used for groups.  However, cinnarch repo coming
                    # first causes errors.  So I just moved them to the back.
                    l = pyalpm.find_grp_pkgs([repo], pkgname)
                    if l:
                        lss = []
                        for pakg in l:
                                self.t.add_pkg(pakg)
        except pyalpm.error:
            line = traceback.format_exc()
            self.queue_event("error", line)

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
    
    def queue_event(self, event_type, event_text=""):
        self.callback_queue.put((event_type, event_text))
        #print("%s : %s" % (event_type, event_text))
         
    # Callback functions 

    def cb_event(self, ID, event, tupel):
        if ID is 1:
            self.action = _('Checking dependencies...')
            self.icon = '/usr/share/pamac/icons/24x24/status/package-search.png'
        elif ID is 3:
            self.action = _('Checking file conflicts...')
            self.icon = '/usr/share/pamac/icons/24x24/status/package-search.png'
        elif ID is 5:
            self.action = _('Resolving dependencies...')
            self.icon = '/usr/share/pamac/icons/24x24/status/setup.png'
        elif ID is 7:
            self.action = _('Checking inter conflicts...')
            self.icon = '/usr/share/pamac/icons/24x24/status/package-search.png'
        elif ID is 9:
            #self.action = _('Installing...')
            #self.icon = '/usr/share/pamac/icons/24x24/status/package-add.png'
            self.action = ''
        elif ID is 11:
            self.action = _('Removing...')
            self.icon = '/usr/share/pamac/icons/24x24/status/package-delete.png'
        elif ID is 13:
            self.action = _('Upgrading...')
            self.icon = '/usr/share/pamac/icons/24x24/status/package-update.png'
        elif ID is 15:
            self.action = _('Checking integrity...')
            self.icon = '/usr/share/pamac/icons/24x24/status/package-search.png'
            self.already_transferred = 0
        elif ID is 17:
            self.action = _('Loading packages files...')
            self.icon = '/usr/share/pamac/icons/24x24/status/package-search.png'
            print('Loading packages files')
        elif ID is 26:
            self.action = _('Configuring...')
            self.icon = '/usr/share/pamac/icons/24x24/status/setup.png'
            print(_('Configuring a package'))
        elif ID is 27:
            print(_('Downloading a file'))
        else:
            self.action = ''

        if len(self.action) > 0:
            self.queue_event("action", self.action)
        #self.queue_event("target", '')
        #self.queue_event("percent", 0)
        #self.queue_event("icon", self.icon)

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
            self.error = _("ERROR: %s") % line
            print(line)
            self.queue_event("error", line)
        elif level & pyalpm.LOG_WARNING:
            self.warning = _("WARNING: %s") % line
            self.queue_event("warning", line)
            print(line)
        elif level & pyalpm.LOG_DEBUG:
            line = _("DEBUG: %s") % line
            print(line)
        elif level & pyalpm.LOG_FUNCTION:
            line = _("FUNC: %s") % line
            print(line)

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
        if self.t is not False:
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
                self.action = _('Downloading %s') % _target
                self.target = _target
                if fraction > 1:
                    self.percent = 0
                else:
                    self.percent = fraction
                self.icon = '/usr/share/pamac/icons/24x24/status/package-download.png'
            else:
                self.action = _('Refreshing %s...') % _target
                self.target = _target
                # can't we know wich percent has 'refreshed' ?
                self.percent = 0
                self.icon = '/usr/share/pamac/icons/24x24/status/refresh-cache.png'
            self.queue_event("action", self.action)
            self.queue_event("percent", self.percent)

    def cb_progress(self, _target, _percent, n, i):
        if _target:
            self.target = "Installing %s (%d/%d)" % (_target, i, n)
        else:
            self.target = "Checking and loading packages..."
        self.percent = _percent / 100
        self.queue_event("target", self.target)
        self.queue_event("percent", self.percent)
