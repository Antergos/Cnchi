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

# Useful vars for gettext (translations)
APP = "cnchi"
DIR = "po"

import queue

if __name__ == '__main__':
    import pac_config
else:   
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
        
        self.already_transferred = 0
        self.total_size = 0
        
        self.do_syncfirst = False
        
        if conf is not None:
            self.pacman_conf = pac_config.PacmanConfig(conf)
            self.handle = self.pacman_conf.initialize_alpm()
            self.holpkg = None
            self.syncfirst = None
            if 'HoldPkg' in self.pacman_conf.options:
                self.holdpkg = self.pacman_conf.options['HoldPkg']
            if 'SyncFirst' in self.pacman_conf.options:
                self.syncfirst = self.pacman_conf.options['SyncFirst']

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
            print(_t.flags)
            self.t_lock = True
            return _t
        except pyalpm.error:
            print(traceback.format_exc())
            return False

    # TODO: Fix check_conflicts (is this needed?)
    '''
    def check_conflicts(self):
        self.conflict_to_remove = {}
        installed_conflicts = {}
        for pkg in self.handle.get_localdb().pkgcache:
            if pkg.conflicts:
                installed_conflicts[pkg.name] = pkg.conflicts
        targets_conflicts = {}
        targets_replaces = {}
        for pkg in t.to_add:
            if pkg.replaces:
                targets_replaces[pkg.name] = pkg.replaces
            if pkg.conflicts:
                targets_conflicts[pkg.name] = pkg.conflicts

        warning = ''
        
        if targets_replaces:
            for key, value in targets_replaces.items():
                for name in value:
                    pkg = self.handle.get_localdb().get_pkg(name)
                    if pkg:
                        if not pkg.name in self.conflict_to_remove.keys():
                            self.conflict_to_remove[pkg.name] = pkg
                            warning += _("%s will be replaced by %s\n") % (pkg.name, key)
        
        if targets_conflicts:
            for key, value in targets_conflicts.items():
                for name in value:
                    pkg = self.handle.get_localdb().get_pkg(name)
                    if pkg:
                        if not pkg.name in self.conflict_to_remove.keys():
                            self.conflict_to_remove[pkg.name] = pkg
        
        if installed_conflicts:
            for key, value in installed_conflicts.items():
                for name in value:
                    for pkg in t.to_add:
                        if pkg.name == name:
                            if not pkg.name in self.conflict_to_remove.keys():
                                self.conflict_to_remove[pkg.name] = pkg
        if self.conflict_to_remove:
            show.warning(warning)
    '''
    
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
                    print(traceback.format_exc())
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
        print("searching %s" % pkgname)
        try:
            for repo in self.handle.get_syncdbs():
                pkg = repo.get_pkg(pkgname)
                if pkg:
                    print("adding %s" % pkgname)
                    self.t.add_pkg(pkg)
                    break
        except pyalpm.error:
            error = traceback.format_exc()

    def install_packages(self, pkg_names):
        self.to_add = []

        for pkgname in pkg_names:
            self.to_add.append(pkgname)

        self.to_remove = []

        # TODO: Fix check_conflicts. Meanwhile (just for testing)
        # we disable it
        #self.check_conflicts(transaction_dict.values())
        
        if self.to_add and self.t_lock is False:            
            self.t = self.init_transaction(noconflicts = True)

            if self.t is not False:
                for pkgname in self.to_add:
                    self.add_package(pkgname)
                        
                try:
                    self.t.prepare()
                    print('to_add:', self.t.to_add)
                    print('to_remove:', self.t.to_remove)

                    self.t.commit()
                    self.t.release()
                    self.t_lock = False
                except pyalpm.error:
                    self.t.release()
                    self.t_lock = False
                    print(traceback.format_exc())
    
    def queue_event(self, event_type, event_text):
        self.callback_queue.put((event_type, event_text))
        print("%s : %s" % (event_type, event_text))
         
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
            self.action = _('Installing...')
            self.icon = '/usr/share/pamac/icons/24x24/status/package-add.png'
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

        self.queue_event("action", self.action)
        self.queue_event("target", '')
        self.queue_event("percent", 0)
        self.queue_event("icon", self.icon)

        print(ID, event)

    def cb_conv(self, *args):
        print("conversation", args)

    def cb_log(self, level, line):
        _logmask = pyalpm.LOG_ERROR | pyalpm.LOG_WARNING

        if not (level & _logmask):
            return

        if level & pyalpm.LOG_ERROR:
            self.error = _("ERROR: %s") % line
            print(line)
            self.t.release()
        elif level & pyalpm.LOG_WARNING:
            self.warning = _("WARNING: %s") % line
            print(line)
        elif level & pyalpm.LOG_DEBUG:
            line = _("DEBUG: %s") % line
            print(line)
        elif level & pyalpm.LOG_FUNCTION:
            line = _("FUNC: %s") % line
            print(line)

    def cb_totaldl(self, _total_size):
        self.total_size = _total_size

    def cb_dl(self, _target, _transferred, total):
        if self.total_size > 0:
            fraction = (_transferred + self.already_transferred) / self.total_size
        size = 0
        if (self.t.to_remove or self.t.to_add):
            for pkg in t.to_remove + t.to_add:
                if pkg.name + '-' + pkg.version in _target:
                    size = pkg.size
            if _transferred == size:
                self.already_transferred += size
            fsize = common.format_size(self.total_size)
            self.action = _('Downloading %s') % fsize
            self.target = _target
            if fraction > 1:
                self.percent = 0
            else:
                self.percent = fraction
            self.icon = '/usr/share/pamac/icons/24x24/status/package-download.png'
        else:
            self.action = _('Refreshing...')
            self.target = _target
            self.percent = 0
            self.icon = '/usr/share/pamac/icons/24x24/status/refresh-cache.png'

        self.queue_event("action", self.action)
        self.queue_event("icon", self.icon)
        self.queue_event("target", self.target)
        self.queue_event("percent", self.percent)

    def cb_progress(self, _target, _percent, n, i):
        self.target = "%s (%d/%d)" % (_target, i, n)
        self.percent = _percent / 100
        self.queue_event("target", self.target)
        self.queue_event("percent", self.percent)

if __name__ == '__main__':
    # This allows to translate all py texts (not the glade ones)
    gettext.textdomain(APP)
    gettext.bindtextdomain(APP, DIR)

    locale_code, encoding = locale.getdefaultlocale()
    lang = gettext.translation (APP, DIR, [locale_code], None, True)
    lang.install()

    # With this we can use _("string") to translate
    gettext.install(APP, localedir=DIR, codeset=None, names=[locale_code])

    callback_queue = queue.Queue(0)
    pac = Pac("/etc/pacman.conf", callback_queue)
    
    # pac.do_refresh()

    packages = ["bzflag"]
    
    pac.install_packages(packages)

