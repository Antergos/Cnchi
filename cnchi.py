#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cnchi.py
#  
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

from gi.repository import Gtk, Gdk, GObject, GLib
import os
import sys
import getopt
import gettext
import locale

# Insert the src directory at the front of the path.
base_dir = os.path.dirname(__file__) or '.'
src_dir = os.path.join(base_dir, 'src')
sys.path.insert(0, src_dir)

# Used in installation_process if we pass the packages.xml as an option
_alternate_package_list = ""

# Download packages using aria2 downloader
_use_aria2 = False

import config

import welcome
import language
import location
import check
import desktop
import keymap
import timezone
import installation_ask
import installation_automatic
import installation_alongside
import installation_advanced
import user_info
import slides
import misc
import log
import info
import updater

#import queue
from multiprocessing import Queue

import show_message as show

# Useful vars for gettext (translations)
APP = "cnchi"
DIR = "/usr/share/locale"

_main_window_width = 800
_main_window_height = 500

_debug = False

class Main(Gtk.Window):

    def __init__(self):
       
        # This allows to translate all py texts (not the glade ones)
        gettext.textdomain(APP)
        gettext.bindtextdomain(APP, DIR)

        locale_code, encoding = locale.getdefaultlocale()
        lang = gettext.translation (APP, DIR, [locale_code], None, True)
        lang.install()

        # With this we can use _("string") to translate
        gettext.install(APP, localedir=DIR, codeset=None, names=[locale_code])

        if os.getuid() != 0:
            show.fatal_error(_('This installer must be run with administrative'
                         ' privileges, and cannot continue without them.'))
        
        # check if we're already running
        tmp_running = "/tmp/.setup-running"
        if os.path.exists(tmp_running):
            show.error(_('You cannot run two instances of this installer.\n\n'
                          'If you are sure that the installer is not already running\n'
                          'you can manually delete the file %s\n'
                          'and run this installer again.') % tmp_running)
            sys.exit(1)
                
        super().__init__()
        
        self.settings = config.Settings()

        self.ui_dir = self.settings.get("UI_DIR")

        if not os.path.exists(self.ui_dir):
            cnchi_dir = os.path.join(os.path.dirname(__file__), './')
            self.settings.set("CNCHI_DIR", cnchi_dir)
            
            ui_dir = os.path.join(os.path.dirname(__file__), 'ui/')
            self.settings.set("UI_DIR", ui_dir)
            
            data_dir = os.path.join(os.path.dirname(__file__), 'data/')
            self.settings.set("DATA_DIR", data_dir)
            
            self.ui_dir = self.settings.get("UI_DIR")

        self.ui = Gtk.Builder()
        self.ui.add_from_file(self.ui_dir + "cnchi.ui")

        self.add(self.ui.get_object("main"))

        self.header = self.ui.get_object("box5")

        self.forward_button = self.ui.get_object("forward_button")

        self.logo = self.ui.get_object("logo")

        logo_dir = os.path.join(self.settings.get("DATA_DIR"), "antergos-logo-mini.png")
                                
        self.logo.set_from_file(logo_dir)

        self.title = self.ui.get_object("title")

        # To honor our css
        self.title.set_name("header")
        self.logo.set_name("header")

        self.main_box = self.ui.get_object("main_box")
        self.progressbar = self.ui.get_object("progressbar1")

        self.forward_button = self.ui.get_object("forward_button")
        self.exit_button = self.ui.get_object("exit_button")
        self.backwards_button = self.ui.get_object("backwards_button")
        
        # Create a queue. Will be used to report pacman messages (pac.py)
        # to the main thread (installer_*.py)
        #self.callback_queue = queue.Queue(0)
        # Doing some tests with a LIFO queue
        #self.callback_queue = queue.LifoQueue(0)
        self.callback_queue = Queue()

        # save in config if we have to use aria2 to download pacman packages
        self.settings.set("use_aria2", _use_aria2)
        if _use_aria2:
            log.debug(_("Cnchi will use pm2ml and aria2 to download packages - EXPERIMENTAL"))

        # load all pages
        # (each one is a screen, a step in the install process)

        self.pages = dict()

        params = dict()
        params['title'] = self.title
        params['ui_dir'] = self.ui_dir
        params['forward_button'] = self.forward_button
        params['backwards_button'] = self.backwards_button
        params['exit_button'] = self.exit_button
        params['callback_queue'] = self.callback_queue
        params['settings'] = self.settings
        params['alternate_package_list'] = _alternate_package_list
        
        if len(_alternate_package_list) > 0:
            log.debug(_("Using '%s' file as package list") % _alternate_package_list)
        
        self.pages["welcome"] = welcome.Welcome(params)
        self.pages["language"] = language.Language(params)
        self.pages["location"] = location.Location(params)
        self.pages["check"] = check.Check(params)
        self.pages["desktop"] = desktop.DesktopAsk(params)
        self.pages["keymap"] = keymap.Keymap(params)
        self.pages["timezone"] = timezone.Timezone(params)
        self.pages["installation_ask"] = installation_ask.InstallationAsk(params)
        self.pages["installation_automatic"] = installation_automatic.InstallationAutomatic(params)
        self.pages["installation_alongside"] = installation_alongside.InstallationAlongside(params)
        self.pages["installation_advanced"] = installation_advanced.InstallationAdvanced(params)
        self.pages["user_info"] = user_info.UserInfo(params)
        self.pages["slides"] = slides.Slides(params)

        self.connect("delete-event", Gtk.main_quit)
        self.ui.connect_signals(self)

        self.set_title(_('Antergos Installer'))
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)
        self.set_size_request(_main_window_width, _main_window_height);

        # set window icon
        icon_dir = os.path.join(self.settings.get("DATA_DIR"), 'antergos-icon.png')
        
        self.set_icon_from_file(icon_dir)

        # set the first page to show
        self.current_page = self.pages["welcome"]

        self.main_box.add(self.current_page)

        # Header style testing
        style_provider = Gtk.CssProvider()

        style_css = os.path.join(self.settings.get("DATA_DIR"), "css", "gtk-style.css")

        with open(style_css, 'rb') as css:
            css_data = css.read()

        style_provider.load_from_data(css_data)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,     
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # show main window
        self.show_all()

        self.current_page.prepare('forwards')

        # hide backwards button
        self.backwards_button.hide()

        # Hide titlebar but show border decoration
        self.get_window().set_accept_focus(True)
        self.get_window().set_decorations(Gdk.WMDecoration.BORDER)
        
        # hide progress bar as it's value is zero
        self.progressbar.set_fraction(0)
        self.progressbar.hide()
        self.progressbar_step = 1.0 / (len(self.pages) - 2)

        # we drop privileges, but where we should do it? before this? ¿?
        misc.drop_privileges()

        with open(tmp_running, "wt") as tmp_file:
            tmp_file.write("Cnchi %d\n" % 1234)

        GLib.timeout_add(100, self.pages["slides"].manage_events_from_cb_queue)

    # TODO: some of these tmp files are created with sudo privileges
    # (this should be fixed) meanwhile, we need sudo privileges to remove them
    @misc.raise_privileges
    def remove_temp_files(self):
        tmp_files = [".setup-running", ".km-running", "setup-pacman-running", "setup-mkinitcpio-running", ".tz-running", ".setup", "Cnchi.log" ]
        for t in tmp_files:
            p = os.path.join("/tmp", t)
            if os.path.exists(p):
                os.remove(p)
         
    def on_exit_button_clicked(self, widget, data=None):
        self.remove_temp_files()
        print("Quiting...")
        Gtk.main_quit()

    def set_progressbar_step(self, add_value):
        new_value = self.progressbar.get_fraction() + add_value
        if new_value > 1:
            new_value = 1
        if new_value < 0:
            new_value = 0
        self.progressbar.set_fraction(new_value)        
        if new_value > 0:
            self.progressbar.show()
        else:
            self.progressbar.hide()

    def on_forward_button_clicked(self, widget, data=None):
        next_page = self.current_page.get_next_page()

        if next_page != None:
            stored = self.current_page.store_values()
            
            if stored != False:
                self.set_progressbar_step(self.progressbar_step)     
                self.main_box.remove(self.current_page)

                self.current_page = self.pages[next_page]

                if self.current_page != None:
                    self.current_page.prepare('forwards')
                    self.main_box.add(self.current_page)

                    if self.current_page.get_prev_page() != None:
                        # there is a previous page, show button
                        self.backwards_button.show()
                        self.backwards_button.set_sensitive(True)
                    else:
                        self.backwards_button.hide()

    def on_backwards_button_clicked(self, widget, data=None):
        prev_page = self.current_page.get_prev_page()

        if prev_page != None:
            self.set_progressbar_step(-self.progressbar_step)

            # if we go backwards, don't store user changes
            #self.current_page.store_values()
            
            self.main_box.remove(self.current_page)
            self.current_page = self.pages[prev_page]

            if self.current_page != None:
                self.current_page.prepare('backwards')
                self.main_box.add(self.current_page)

                if self.current_page.get_prev_page() == None:
                    # we're at the first page
                    self.backwards_button.hide()

if __name__ == '__main__':
    print("Cnchi installer version %s" % info.cnchi_VERSION)

    argv = sys.argv[1:]
    
    try:
        opts, args = getopt.getopt(argv, "adup:", ["aria2", "debug", "update", "packages"])
    except getopt.GetoptError as e:
        print(str(e))
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ('-d', '--debug'):
            log._debug = True
            log.debug("Debug mode on")
        elif opt in ('-u', '--update'):
            upd = updater.Updater()
            if upd.update():
                print("Program updated! Restarting...")
                os.execl(sys.executable, *([sys.executable] + sys.argv))
        elif opt in ('-p', '--packages'):
            _alternate_package_list = arg
        elif opt in ('-a', '--aria2'):
            _use_aria2 = True
        else:
            assert False, "unhandled option"
                
    GObject.threads_init()
    Gdk.threads_init()

    app = Main()
    
    Gdk.threads_enter()
    Gtk.main()
    Gdk.threads_leave()
