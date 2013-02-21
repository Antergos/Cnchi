#!/usr/bin/env python
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

#from collections import OrderedDict

# Useful vars for gettext (translations)
APP = "cnchi"
DIR = "po"

if __name__ == '__main__':
    import queue
    import pac_config
else:   
    from pacman import pac_config


class Pac(object):
    def __init__(self, conf, callback_queue):
        
        self.callback_queue = callback_queue
        self.t = None
        self.transaction_desc = []
        self.t_lock = False
        self.conflict_to_remove = None
        self.to_remove = []
        self.to_add = []
        self.to_update = []
        self.to_provide = []

        self.total_size = 0
        
        self.do_syncfirst = False
        #self.list_first = []
        
        #self.syncpkgs = OrderedDict()
        #self.localpkgs = OrderedDict()
        
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
    
    def do_refresh(self):
        """Sync databases like pacman -Sy"""
        #ProgressWindow.show_all()
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
        #ProgressWindow.hide()
        #progress_label.set_text('')
        #progress_bar.set_text('')

    def do_sysupgrade(self):
        """Upgrade a system like pacman -Su"""
        if self.t_lock is False:
            if self.do_syncfirst is True:
                self.t = self.init_transaction(recurse = True)
                for pkg in self.list_first:
                    self.t.add_pkg(pkg)
                self.to_remove = self.t.to_remove
                self.to_add = self.t.to_add
                self.set_transaction_desc('update')
                
                #response = ConfDialog.run()
                #if response == Gtk.ResponseType.OK:
                self.t_finalize()
                #if response == Gtk.ResponseType.CANCEL or Gtk.ResponseType.CLOSE or Gtk.ResponseType.DELETE_EVENT:
                #    ProgressWindow.hide()
                #    ConfDialog.hide()
                #    self.t.release()
                #    self.t_lock = False
            else:
                try:
                    self.t = self.init_transaction()
                    self.t.sysupgrade(downgrade=False)
                except pyalpm.error:
                    print(traceback.format_exc())
                    self.t.release()
                    self.t_lock = False
                
                # Kamikaze mode, don't check possible conflicts
                #self.check_conflicts()

                self.to_add = self.t.to_add
                self.to_remove = []
                
                for pkg in self.conflict_to_remove.values():
                    self.to_remove.append(pkg)
                
                if len(self.to_add) + len(self.to_remove) == 0:
                    self.t.release()
                    print(_("Nothing to update"))
                else:
                    self.t.release()
                    self.t = self.init_transaction(noconflicts = True, nodeps = True, nodepversion = True)
                    for pkg in self.to_add:
                        self.t.add_pkg(pkg)
                    for pkg in self.conflict_to_remove.values():
                        self.t.remove_pkg(pkg)
                    self.to_remove = self.t.to_remove
                    self.to_add = self.t.to_add
                    self.set_transaction_desc('update')
                    if len(self.transaction_desc) != 0:
                        #response = ConfDialog.run()
                        #if response == Gtk.ResponseType.OK:
                        self.t_finalize(self.t)
                        #if response == Gtk.ResponseType.CANCEL or Gtk.ResponseType.CLOSE or Gtk.ResponseType.DELETE_EVENT:
                            #ProgressWindow.hide()
                            #ConfDialog.hide()
                            #self.t.release()
                            #self.t_lock = False
                    else:
                        self.t_finalize()
                        self.t.release()
                        self.t_lock = False

    def t_finalize(self):
        #ConfDialog.hide()

        try:
            self.t.prepare()
        except pyalpm.error:
            print(traceback.format_exc())
            self.t.release()
            self.t_lock = False

        try:
            self.t.commit()
        except pyalpm.error:
            print(traceback.format_exc())

        #ProgressWindow.hide()

    '''
    def get_updates(self):
        """Return a list of package objects in local db which can be updated"""
        if self.pacman_conf.syncfirst:
            for name in self.pacman_conf.syncfirst:
                pkg = self.handle.get_localdb().get_pkg(name)
                candidate = pyalpm.sync_newversion(pkg, self.handle.get_syncdbs())
                if candidate:
                    self.list_first.append(candidate)
            if self.list_first:
                self.do_syncfirst = True
                return self.list_first
        result = []
        installed_pkglist = self.handle.get_localdb().pkgcache
        for pkg in installed_pkglist:
            candidate = pyalpm.sync_newversion(pkg, self.handle.get_syncdbs())
            if candidate:
                result.append(candidate)
        return result
    '''

    def get_new_version_available(self, pkgname):
        for repo in self.handle.get_syncdbs():
            pkg = repo.get_pkg(pkgname)
            if pkg is not None:
                return pkg.version
                break

    def format_size(self, size):
        KiB_size = size / 1024
        if KiB_size < 1000:
            size_string = '%.1f KiB' % (KiB_size)
            return size_string
        else:
            size_string = '%.2f MiB' % (KiB_size / 1024)
            return size_string

    def set_transaction_desc(self, mode):
        self.transaction_desc.clear()
        if self.to_remove:
            self.transaction_desc.append(['To remove:', to_remove[0].name])
            i = 1
            while i < len(self.to_remove):
                self.transaction_desc.append([' ', to_remove[i].name])
                i += 1
            self.down_label.set_markup('')
        if self.to_add:
            installed_name = []
            for pkg_object in self.handle.get_localdb().pkgcache:
                installed_name.append(pkg_object.name)
            to_add_name = []
            for pkg_object in self.to_add:
                to_add_name.append(pkg_object.name)
            self.to_update = sorted(set(installed_name).intersection(to_add_name))
            to_remove_from_add_name = sorted(set(self.to_update).intersection(to_add_name))
            for name in to_remove_from_add_name:
                to_add_name.remove(name)
            if to_add_name:
                self.transaction_desc.append(['To install:', to_add_name[0]])
                i = 1
                while i < len(to_add_name):
                    self.transaction_desc.append([' ', to_add_name[i]])
                    i += 1
            if mode == 'normal':
                if self.to_update:
                    self.transaction_desc.append(['To update:', to_update[0]])
                    i = 1
                    while i < len(to_update):
                        self.transaction_desc.append([' ', to_update[i]])
                        i += 1
            self.down_label.set_markup('')
        #	down_label.set_markup('<b>Total Download size: </b>'+format_size(totaldlcb))

    def install_packages(self, pkg_names):
        self.to_add = []
        for pkgname in pkg_names:
            self.to_add.append(pkgname)
        self.to_remove = []
        
        #check_conflicts(transaction_dict.values())
        
        if self.to_add:
            self.t.release()
            self.t = self.init_transaction(noconflicts = True)

            if self.t is not False:
                for pkgname in self.to_add:
                    self.t.add_pkg(pkgname)
                self.t_finalize()
            #self.t.release()
            #self.t_lock = False

    # queue operations
    
    def queue_action(self, action):
        self.callback_queue.put(("action", action))

    def queue_icon(self, icon):
        self.callback_queue.put(("icon", icon))

    def queue_target(self, target):
        self.callback_queue.put(("target", target))

    def queue_percent(self, percent):
        self.callback_queue.put(("percent", percent))

    # Callbacks
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

        self.queue_action(self.action)
        self.queue_target('')
        self.queue_percent(0)
        self.queue_icon(self.icon)
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
            for pkg in t.to_remove+t.to_add:
                if pkg.name+'-'+pkg.version in _target:
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

        print(self.action)
        
        self.queue_action(self.action)
        self.queue_icon(self.icon)
        self.queue_target(self.target)
        self.queue_percent(self.percent)

    def cb_progress(self, _target, _percent, n, i):
        #self.target = _target + ' (' + str(i) + '/' + str(n) + ')'
        self.target = "%s (%d/%d)" % (_target, i, n)
        self.percent = _percent / 100
        self.queue_target(self.target)
        self.queue_percent(self.percent)

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
    
    pac.do_refresh()

    #pac.do_sysupgrade()
