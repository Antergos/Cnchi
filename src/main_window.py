#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main_window.py
#
#  Copyright © 2013,2014 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

""" Main Cnchi Window """

from gi.repository import Gtk, Gdk

import os
import sys
import multiprocessing
import logging

import config
import welcome
import language
import location
import check
import desktop
import features
import keymap
import timezone
import user_info
import slides
import canonical.misc as misc
import info
import show_message as show
import desktop_environments as desktops

from installation import ask as installation_ask
from installation import automatic as installation_automatic
from installation import alongside as installation_alongside
from installation import advanced as installation_advanced

# Constants (must be uppercase)
MAIN_WINDOW_WIDTH = 825
MAIN_WINDOW_HEIGHT = 500

# Some of these tmp files are created with sudo privileges
# (this should be fixed) meanwhile, we need sudo privileges to remove them
@misc.raise_privileges
def remove_temp_files():
    """ Remove Cnchi temporary files """
    temp_files = [".setup-running", ".km-running", "setup-pacman-running", \
        "setup-mkinitcpio-running", ".tz-running", ".setup", "Cnchi.log" ]
    for temp in temp_files:
        path = os.path.join("/tmp", temp)
        if os.path.exists(path):
            os.remove(path)

class MainWindow(Gtk.ApplicationWindow):
    """ Cnchi main window """
    def __init__(self, app, cmd_line):
        Gtk.Window.__init__(self, title="Cnchi", application=app)

        # Check if we have administrative privileges
        if os.getuid() != 0:
            msg = _('This installer must be run with administrative privileges, '
                'and cannot continue without them.')
            show.error(self, msg)
            sys.exit(1)

        # Check if we're already running
        tmp_running = "/tmp/.setup-running"
        if os.path.exists(tmp_running):
            msg = _('You cannot run two instances of this installer.\n\n'
                'If you are sure that the installer is not already running\n'
                'you can manually delete the file %s\n'
                'and run this installer again.') % tmp_running
            show.error(self, msg)
            sys.exit(1)

        logging.info(_("Cnchi installer version %s"), info.CNCHI_VERSION)

        self.settings = config.Settings()
        self.ui_dir = self.settings.get('ui')

        if not os.path.exists(self.ui_dir):
            cnchi_dir = os.path.join(os.path.dirname(__file__), './')
            self.settings.set('cnchi', cnchi_dir)

            ui_dir = os.path.join(os.path.dirname(__file__), 'ui/')
            self.settings.set('ui', ui_dir)

            data_dir = os.path.join(os.path.dirname(__file__), 'data/')
            self.settings.set('data', data_dir)

            self.ui_dir = self.settings.get('ui')

        if cmd_line.cache:
            logging.debug("Cnchi will use '%s' as a source directory for cached xz packages", cmd_line.cache)
            self.settings.set('cache', cmd_line.cache)

        # For things we are not ready for users to test
        self.settings.set('z_hidden', cmd_line.z_hidden)

        # Set enabled desktops
        if self.settings.get('z_hidden'):
            self.settings.set("desktops", desktops.DESKTOPS_DEV)
        else:
            self.settings.set("desktops", desktops.DESKTOPS)

        self.ui = Gtk.Builder()
        self.ui.add_from_file(self.ui_dir + "cnchi.ui")

        self.add(self.ui.get_object("main"))

        self.header_ui = Gtk.Builder()
        self.header_ui.add_from_file(self.ui_dir + "header.ui")
        self.header = self.header_ui.get_object("header")

        self.logo = self.header_ui.get_object("logo")
        data_dir = self.settings.get('data')
        logo_path = os.path.join(data_dir, "images", "antergos", "antergos-logo-mini2.png")
        self.logo.set_from_file(logo_path)

        # To honor our css
        self.header.set_name("header")
        self.logo.set_name("logo")

        self.main_box = self.ui.get_object("main_box")
        self.progressbar = self.ui.get_object("main_progressbar")
        self.progressbar.set_name('process_progressbar')

        self.forward_button = self.header_ui.get_object("forward_button")
        self.backwards_button = self.header_ui.get_object("backwards_button")
        
        #image1 = Gtk.Image.new_from_icon_name("go-next", Gtk.IconSize.LARGE_TOOLBAR)
        #self.forward_button.set_label("")
        #self.forward_button.set_image(image1)
        self.forward_button.set_name('fwd_btn')
        self.forward_button.set_always_show_image(True)
        #self.forward_button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        
        #image2 = Gtk.Image.new_from_icon_name("go-previous", Gtk.IconSize.LARGE_TOOLBAR)
        #self.backwards_button.set_label("")
        #self.backwards_button.set_image(image2)
        self.backwards_button.set_name('bk_btn')
        self.backwards_button.set_always_show_image(True)
        #self.backwards_button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE)) 
        
        # Create a queue. Will be used to report pacman messages (pacman/pac.py)
        # to the main thread (installation/process.py)
        self.callback_queue = multiprocessing.JoinableQueue()

        # Save in config if we have to use aria2 to download pacman packages
        self.settings.set("use_aria2", cmd_line.aria2)
        if cmd_line.aria2:
            logging.info(_("Using Aria2 to download packages - EXPERIMENTAL"))
            
        self.set_titlebar(self.header)

        # Load all pages
        # (each one is a screen, a step in the install process)

        self.params = dict()
        self.params['header'] = self.header
        self.params['ui_dir'] = self.ui_dir
        self.params['forward_button'] = self.forward_button
        self.params['backwards_button'] = self.backwards_button
        self.params['callback_queue'] = self.callback_queue
        self.params['settings'] = self.settings
        self.params['main_progressbar'] = self.progressbar
        
        if cmd_line.packagelist:
            self.params['alternate_package_list'] = cmd_line.packagelist
            logging.info(_("Using '%s' file as package list"), self.params['alternate_package_list'])
        else:
            self.params['alternate_package_list'] = ""
        
        self.params['disable_tryit'] = cmd_line.disable_tryit
        self.params['testing'] = cmd_line.testing

        # Just load the first two screens (the other ones will be loaded later)
        # We do this so the user has not to wait for all the screens to be loaded        
        self.pages = dict()
        self.pages["welcome"] = welcome.Welcome(self.params)

        self.connect('delete-event', self.on_exit_button_clicked)
        
        self.ui.connect_signals(self)
        self.header_ui.connect_signals(self)

        title = "Cnchi %s" % info.CNCHI_VERSION
        self.set_title(title)
        self.header.set_title(title)
        self.header.set_subtitle(_("Antergos Installer"))
        self.header.set_show_close_button(True)
        
        self.set_geometry()
        
        # Set window icon
        icon_path = os.path.join(data_dir, "images", "antergos", "antergos-icon.png")
        self.set_icon_from_file(icon_path)

        # Set the first page to show
        self.current_page = self.pages["welcome"]

        self.main_box.add(self.current_page)

        # Header style testing

        style_provider = Gtk.CssProvider()

        style_css = os.path.join(data_dir, "css", "gtk-style.css")

        with open(style_css, 'rb') as css:
            css_data = css.read()

        style_provider.load_from_data(css_data)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Show main window
        self.show_all()

        self.current_page.prepare('forwards')

        # Hide backwards button
        self.backwards_button.hide()
        
        # Hide titlebar but show border decoration
        #self.get_window().set_accept_focus(True)
        #self.get_window().set_decorations(Gdk.WMDecoration.BORDER)

        # Hide progress bar as it's value is zero
        self.progressbar.set_fraction(0)
        self.progressbar.hide()
        self.progressbar_step = 0

        with open(tmp_running, "w") as tmp_file:
            tmp_file.write("Cnchi %d\n" % 1234)

        self.refresh()

    def refresh(self):
        # Force Gtk to show the main screen
        while Gtk.events_pending():
            Gtk.main_iteration()
        
    def set_cursor(self, cursor_type):
        screen = Gdk.Screen.get_default()
        window = Gdk.Screen.get_root_window(screen)
        if window:
            cursor = Gdk.Cursor(cursor_type)
            window.set_cursor(cursor)
            self.refresh()

    def load_pages(self):
        self.set_cursor(Gdk.CursorType.WATCH)
        self.pages["language"] = language.Language(self.params)
        self.pages["location"] = location.Location(self.params)
        self.pages["check"] = check.Check(self.params)
        self.pages["desktop"] = desktop.DesktopAsk(self.params)
        self.pages["features"] = features.Features(self.params)
        self.pages["keymap"] = keymap.Keymap(self.params)
        self.pages["timezone"] = timezone.Timezone(self.params)
        self.pages["installation_ask"] = installation_ask.InstallationAsk(self.params)
        self.pages["installation_automatic"] = installation_automatic.InstallationAutomatic(self.params)
        self.pages["installation_alongside"] = installation_alongside.InstallationAlongside(self.params)
        self.pages["installation_advanced"] = installation_advanced.InstallationAdvanced(self.params)
        self.pages["user_info"] = user_info.UserInfo(self.params)
        self.pages["slides"] = slides.Slides(self.params)       
        self.set_cursor(Gdk.CursorType.ARROW)
        
        if (len(self.pages) - 2) > 0:
            self.progressbar_step = 1.0 / (len(self.pages) - 2)

    def set_geometry(self):
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)
        self.set_size_request(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        self.set_default_size(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)

        geom = Gdk.Geometry()
        geom.min_width = MAIN_WINDOW_WIDTH
        geom.min_height = MAIN_WINDOW_HEIGHT
        geom.max_width = MAIN_WINDOW_WIDTH
        geom.max_height = MAIN_WINDOW_HEIGHT
        geom.base_width = MAIN_WINDOW_WIDTH
        geom.base_height = MAIN_WINDOW_HEIGHT

        hints = Gdk.WindowHints.MIN_SIZE | Gdk.WindowHints.MAX_SIZE | Gdk.WindowHints.BASE_SIZE
        self.set_geometry_hints(None, geom, hints)

    def on_exit_button_clicked(self, widget, data=None):
        """ Quit Cnchi """
        remove_temp_files()
        logging.info(_("Quiting installer..."))
        self.settings.set('stop_all_threads', True)
        logging.shutdown()

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
        """ Show next screen """
        next_page = self.current_page.get_next_page()

        if next_page != None:
            if next_page not in self.pages.keys():
                # Load all pages
                self.load_pages()
                self.progressbar_step = 1.0 / (len(self.pages) - 2)

            stored = self.current_page.store_values()

            if stored != False:
                self.set_progressbar_step(self.progressbar_step)
                self.main_box.remove(self.current_page)

                self.current_page = self.pages[next_page]

                if self.current_page != None:
                    self.current_page.prepare('forwards')
                    self.main_box.add(self.current_page)
                    if self.current_page.get_prev_page() != None:
                        # There is a previous page, show button
                        self.backwards_button.show()
                        self.backwards_button.set_sensitive(True)
                    else:
                        self.backwards_button.hide()

    def on_backwards_button_clicked(self, widget, data=None):
        """ Show previous screen """
        prev_page = self.current_page.get_prev_page()

        if prev_page != None:
            self.set_progressbar_step(-self.progressbar_step)

            # If we go backwards, don't store user changes
            # self.current_page.store_values()

            self.main_box.remove(self.current_page)
            self.current_page = self.pages[prev_page]

            if self.current_page != None:
                self.current_page.prepare('backwards')
                self.main_box.add(self.current_page)

                if self.current_page.get_prev_page() == None:
                    # We're at the first page
                    self.backwards_button.hide()
