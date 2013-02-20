#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cnchi.py
#  
#  Copyright 2013 Cinnarch
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

from gi.repository import Gtk, Gdk, GObject
import os
import sys

import gettext
import locale

# Insert the src directory at the front of the path.
base_dir = os.path.dirname(__file__) or '.'
src_dir = os.path.join(base_dir, 'src')
sys.path.insert(0, src_dir)

from config import installer_settings

import language
import check
import keymap
import timezone
import installation_ask
import installation_automatic
import installation_easy
import installation_advanced
import user_info
import slides
import misc

import queue

from show_message import fatal_error

# Useful vars for gettext (translations)
APP = "cnchi"
DIR = "po"

_main_window_width = 800
_main_window_height = 500

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
            fatal_error(_('This installer must be run with administrative'
                         ' privileges, and cannot continue without them.'))
        
        # check if we're already running
        tmp_running = "/tmp/.setup-running"
        if os.path.exists(tmp_running):
            fatal_error(_('You cannot run two instances of this installer.\n\n'
                          'If you are sure that the installer is not already running\n'
                          'you can manually delete the file %s\n'
                          'and run this installer again.') % tmp_running)
                
        super().__init__()

        self.ui_dir = installer_settings["UI_DIR"]

        if not os.path.exists(self.ui_dir):
            cnchi_dir = os.path.join(os.path.dirname(__file__), './')
            installer_settings["CNCHI_DIR"] = cnchi_dir
            
            ui_dir = os.path.join(os.path.dirname(__file__), 'ui/')
            installer_settings["UI_DIR"] =  ui_dir
            
            data_dir = os.path.join(os.path.dirname(__file__), 'data/')
            installer_settings["DATA_DIR"] = data_dir
            
            self.ui_dir = installer_settings["UI_DIR"]

        self.ui = Gtk.Builder()
        self.ui.add_from_file(self.ui_dir + "cnchi.ui")

        self.add(self.ui.get_object("main"))

        self.header = self.ui.get_object("box5")

        self.forward_button = self.ui.get_object("forward_button")

        self.logo = self.ui.get_object("logo")

        logo_dir = os.path.join(installer_settings["DATA_DIR"], "logo_mini.png")
                                
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
        self.callback_queue = queue.Queue(0)

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
        
        self.pages["language"] = language.Language(params)
        self.pages["check"] = check.Check(params)
        self.pages["keymap"] = keymap.Keymap(params)
        self.pages["timezone"] = timezone.Timezone(params)
        self.pages["installation_ask"] = installation_ask.InstallationAsk(params)
        self.pages["installation_automatic"] = installation_automatic.InstallationAutomatic(params)
        self.pages["installation_easy"] = installation_easy.InstallationEasy(params)
        self.pages["installation_advanced"] = installation_advanced.InstallationAdvanced(params)
        self.pages["user_info"] = user_info.UserInfo(params)
        self.pages["slides"] = slides.Slides(params)

        self.connect("delete-event", Gtk.main_quit)
        self.ui.connect_signals(self)

        self.set_title(_('Cinnarch Installer'))
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)
        self.set_size_request(_main_window_width, _main_window_height);

        # set window icon
        icon_dir = os.path.join(installer_settings["DATA_DIR"],
                                'cinnarch-icon.png')
        
        self.set_icon_from_file(icon_dir)

        # set the first page to show
        self.current_page = self.pages["language"]
        #self.current_page = self.pages["installation_advanced"]

        self.main_box.add(self.current_page)

        # Header style testing
        style_provider = Gtk.CssProvider()

        style_css = os.path.join(installer_settings["DATA_DIR"],
                                "gtk-style.css")

        css = open(style_css, 'rb')
        css_data = css.read()
        css.close()

        style_provider.load_from_data(css_data)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,     
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # show main window
        self.show_all()

        self.current_page.prepare()

        # hide backwards button
        self.backwards_button.hide()

        # Hide titlebar but show border decoration
        self.get_window().set_accept_focus(True)
        self.get_window().set_decorations(Gdk.WMDecoration.BORDER)

        # we drop privileges, but where we should do it? before this? ¿?
        misc.drop_privileges()

        tmp_file = open(tmp_running, "wt")
        tmp_file.write("Cnchi %d\n" % 1234)
        tmp_file.close()


    def remove_temp_files(self):
         tmp_files = [".setup-running", ".km-running", "setup-pacman-running", "setup-mkinitcpio-running", ".tz-running", ".setup" ]
         for t in tmp_files:
            p = os.path.join("/tmp", t)
            if os.path.exists(p):
                os.remove(p)
         
    def on_exit_button_clicked(self, widget, data=None):
        self.pages["timezone"].stop_thread()
        self.remove_temp_files()
        print("Quiting...")
        Gtk.main_quit()

    def progressbar_step(self, add_value):
        new_value = self.progressbar.get_fraction() + add_value
        if new_value > 1:
            new_value = 1
        if new_value < 0:
            new_value = 0
        self.progressbar.set_fraction(new_value)

    def on_forward_button_clicked(self, widget, data=None):
        next_page = self.current_page.get_next_page()

        if next_page != None:
            stored = self.current_page.store_values()
            
            if stored != False:
                self.progressbar_step(0.1)     
                self.main_box.remove(self.current_page)

                self.current_page = self.pages[next_page]

                if self.current_page != None:
                    self.current_page.prepare()
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
            self.progressbar_step(-0.1)

            # if we go backwards, don't store user changes
            #self.current_page.store_values()
            
            self.main_box.remove(self.current_page)
            self.current_page = self.pages[prev_page]

            if self.current_page != None:
                self.current_page.prepare()
                self.main_box.add(self.current_page)

                if self.current_page.get_prev_page() == None:
                    # we're at the first page
                    self.backwards_button.hide()


if __name__ == '__main__':

    major = Gtk.get_major_version()
    minor = Gtk.get_minor_version()
    micro = Gtk.get_micro_version()

    print("Using Gtk version %d.%d.%d" % (major,minor,micro))

    GObject.threads_init()
    Gdk.threads_init()

    app = Main()

    Gdk.threads_enter()
    Gtk.main()
    Gdk.threads_leave()
