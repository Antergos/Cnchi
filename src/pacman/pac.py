#! /usr/bin/python
# -*-coding:utf-8-*-

#from gi.repository import Gtk

import pyalpm
import traceback
import sys

from pacman import pac_config

import show_message as show

# interface = Gtk.Builder()
# interface.add_from_file('gui/dialogs.glade')

# ProgressWindow = interface.get_object('ProgressWindow')
# progress_bar = interface.get_object('progressbar2')
# progress_label = interface.get_object('progresslabel2')
# ErrorDialog = interface.get_object('ErrorDialog')
# WarningDialog = interface.get_object('WarningDialog')
# QuestionDialog = interface.get_object('QuestionDialog')
# ConfDialog = interface.get_object('ConfDialog')
# transaction_desc = interface.get_object('transaction_desc')
# down_label = interface.get_object('down_label')

class Pac(object):
    def __init__(self, conf):
        self.t = None
        self.transaction_desc = []
        self.t_lock = False
        self.conflict_to_remove = None
        self.to_remove = None
        self.to_add = None
        self.to_update = None
        self.do_syncfirst = False
        self.list_first = []

        if conf is not None:
            self.pacman_conf = PacmanConfig(conf)
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
        self.handle.totaldlcb = self.totaldlcb
        self.handle.eventcb = self.cb_event
        self.handle.questioncb = self.cb_conv
        self.handle.progresscb = self.cb_progress
        self.handle.logcb = self.cb_log
        try:
            _t = handle.init_transaction(**options)
            print(_t.flags)
            self.t_lock = True
            return _t
        except pyalpm.error:
            show.error(traceback.format_exc())
            return False


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
                            if warning:
                                warning = warning + '\n'
                            warning = warning + pkg.name + ' will be replaced by ' + key 
        
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

    
    def do_refresh(self):
        """Sync databases like pacman -Sy"""
        #ProgressWindow.show_all()
        for db in self.handle.get_syncdbs():
            if self.t_lock is False:
                self.t = init_transaction(config.handle)
                try:
                    db.update(force=False)
                    self.t.release()
                    self.t_lock = False
                except pyalpm.error:
                    show.error(traceback.format_exc())
                    self.t_lock = False
                    break
        #ProgressWindow.hide()
        #progress_label.set_text('')
        #progress_bar.set_text('')

    def do_sysupgrade(self):
        """Upgrade a system like pacman -Su"""
        #global t
        #global t_lock
        #global to_remove
        #global to_add
        #global to_update
        if self.t_lock is False:
            if self.do_syncfirst is True:
                self.t = init_transaction(self.handle, recurse = True)
                for pkg in self.list_first:
                    self.t.add_pkg(pkg)
                self.to_remove = self.t.to_remove
                self.to_add = self.t.to_add
                self.set_transaction_desc('update')
                
                response = ConfDialog.run()
                if response == Gtk.ResponseType.OK:
                    t_finalize(self.t)
                if response == Gtk.ResponseType.CANCEL or Gtk.ResponseType.CLOSE or Gtk.ResponseType.DELETE_EVENT:
                    ProgressWindow.hide()
                    ConfDialog.hide()
                    self.t.release()
                    self.t_lock = False
            else:
                try:
                    self.t = init_transaction(self.handle)
                    self.t.sysupgrade(downgrade=False)
                except pyalpm.error:
                    show.error(traceback.format_exc())
                    self.t.release()
                    self.t_lock = False
                
                self.check_conflicts()
                self.to_add = self.t.to_add
                self.to_remove = []
                
                for pkg in self.conflict_to_remove.values():
                    self.to_remove.append(pkg)
                
                if len(self.to_add) + len(self.to_remove) == 0:
                    self.t.release()
                    print("Nothing to update")
                else:
                    self.t.release()
                    self.t = init_transaction(config.handle, noconflicts = True, nodeps = True, nodepversion = True)
                    for pkg in self.to_add:
                        self.t.add_pkg(pkg)
                    for pkg in self.conflict_to_remove.values():
                        self.t.remove_pkg(pkg)
                    self.to_remove = self.t.to_remove
                    self.to_add = self.t.to_add
                    self.set_transaction_desc('update')
                    if len(self.transaction_desc) != 0:
                        response = ConfDialog.run()
                        if response == Gtk.ResponseType.OK:
                                    t_finalize(self.t)
                        if response == Gtk.ResponseType.CANCEL or Gtk.ResponseType.CLOSE or Gtk.ResponseType.DELETE_EVENT:
                            ProgressWindow.hide()
                            ConfDialog.hide()
                            self.t.release()
                            self.t_lock = False
                    else:
                        t_finalize(self.t)
                        self.t.release()
                        self.t_lock = False

    def t_finalize(self, t):
        #ConfDialog.hide()

        try:
            t.prepare()
        except pyalpm.error:
            show.error(traceback.format_exc())
            t.release()
            self.t_lock = False

        try:
            t.commit()
        except pyalpm.error:
            show.error(traceback.format_exc())

        #ProgressWindow.hide()

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

    def set_transaction_desc(mode):
        #global transaction_desc
        #global down_label
        #global to_add
        #global to_remove
        #global to_update
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

########################################################################################################################
# Callbacks
event_text = ' '
def cb_event(ID, event, tupel):
	global event_text
	ProgressWindow.show_all()
	while Gtk.events_pending():
		Gtk.main_iteration()
	for i in [1,3,5,7,9,11,15]:
		if ID is i:
			progress_label.set_text(event)
			break
		else :
			progress_label.set_text(' ')
	if ID is 27:
		progress_label.set_text('Downloading '+format_size(total_size))
		print('Downloading a file')
	if ID is 17:
		progress_label.set_text('Checking signatures')
		print('Checking signatures')
	progress_bar.set_fraction(0.0)
	progress_bar.set_text('')
	print(ID,event)

def cb_conv(*args):
	print("conversation", args)

_logmask = pyalpm.LOG_ERROR | pyalpm.LOG_WARNING

def cb_log(level, line):
	#global t
	#try:
	#	_line = str(_line, encoding='utf-8').strip("\n")
	#except:
	#	_line = str(_line, encoding='latin-1').strip("\n")
	if not (level & _logmask):
		return
	if level & pyalpm.LOG_ERROR:
		ErrorDialog.format_secondary_text("ERROR: "+line)
		response = ErrorDialog.run()
		if response:
			ErrorDialog.hide()
			#t.release()
	elif level & pyalpm.LOG_WARNING:
		WarningDialog.format_secondary_text("WARNING: "+line)
		response = WarningDialog.run()
		if response:
			WarningDialog.hide()
	elif level & pyalpm.LOG_DEBUG:
		line = "DEBUG: " + line
		print(line)
	elif level & pyalpm.LOG_FUNCTION:
		line = "FUNC: " + line
		print(line)
	#sys.stderr.write(line)

total_size = 0
def totaldlcb(_total_size):
	global total_size
	total_size = _total_size

already_transferred = 0
def cb_dl(_target, _transferred, total):
	global already_transferred
	while Gtk.events_pending():
		Gtk.main_iteration()
	if total_size > 0:
		fraction = (_transferred+already_transferred)/total_size
	size = 0
	if (to_remove or to_add):
		for pkg in to_remove+to_add:
			if pkg.name+'-'+pkg.version in _target:
				size = pkg.size
		if _transferred == size:
			already_transferred += size
		progress_label.set_text('Downloading '+format_size(total_size))
		progress_bar.set_text(_target)
		progress_bar.set_fraction(fraction)
	else:
		progress_label.set_text('Refreshing...')
		progress_bar.set_text(_target)
		progress_bar.pulse()

def cb_progress(_target, _percent, n, i):
	while Gtk.events_pending():
		Gtk.main_iteration()
	target = _target+' ('+str(i)+'/'+str(n)+')'
	progress_bar.set_fraction(_percent/100)
	progress_bar.set_text(target) 


if __name__ == "__main__":
	True
