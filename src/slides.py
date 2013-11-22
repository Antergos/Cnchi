#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  slides.py
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

from gi.repository import Gtk, WebKit, GLib
import config
import os

import queue
from multiprocessing import Queue, Lock

import show_message as show
import logging
import subprocess
import misc

# when we reach this page we can't go neither backwards nor forwards
_next_page = None
_prev_page = None

class Slides(Gtk.Box):

    def __init__(self, params):
        self.title = params['title']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        self.exit_button = params['exit_button']
        self.callback_queue = params['callback_queue']
        self.settings = params['settings']
        self.main_progressbar = params['main_progressbar']

        super().__init__()

        builder = Gtk.Builder()

        builder.add_from_file(os.path.join(self.ui_dir, "slides.ui"))
        builder.connect_signals(self)

        self.progress_bar = builder.get_object("progressbar")
        self.progress_bar.set_show_text(True)
        
        self.global_progress_bar = builder.get_object("global_progressbar")
        self.global_progress_bar.set_show_text(True)
        
        self.info_label = builder.get_object("info_label")
        self.scrolled_window = builder.get_object("scrolledwindow")

        self.webview = WebKit.WebView()
        
        if self.settings == None:
            html_file = '/usr/share/cnchi/data/slides.html'
        else:
            html_file = os.path.join(self.settings.get('data'), 'slides.html')
        
        try:
            with open(html_file) as html_stream:
                html = html_stream.read(None)
                data = os.path.join(os.getcwd(), "data")
                self.webview.load_html_string(html, "file://" + data)
        except IOError:
            pass
        
        self.scrolled_window.add(self.webview)
        
        self.install_ok = _("Installation Complete!\n" \
                            "Do you want to restart your system now?")

        super().add(builder.get_object("slides"))
        
        self.fatal_error = False
        
    def translate_ui(self):
        txt = _("Installing Antergos...")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.title.set_markup(txt)

        if len(self.info_label.get_label()) <= 0:
            self.set_message(_("Please wait..."))
        
        self.install_ok = _("Installation Complete!\n" \
                            "Do you want to restart your system now?")
        
    def show_global_progress_bar_if_hidden(self):
        if self.global_progress_bar_is_hidden:
            self.global_progress_bar.show_all()
            self.global_progress_bar_is_hidden = False
        
    def prepare(self, direction):
        self.translate_ui()
        self.show_all()
        
        # Last screen reached, hide main progress bar.
        self.main_progressbar.hide()
        
        self.global_progress_bar.hide()
        self.global_progress_bar_is_hidden = True

        self.backwards_button.hide()
        self.forward_button.hide()
        self.exit_button.hide()

    def store_values(self):
        return False

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page

    def refresh(self):
        while Gtk.events_pending():
            Gtk.main_iteration()

    def set_message(self, txt):
        txt = "<span color='darkred'>%s</span>" % txt
        self.info_label.set_markup(txt)

    # This function is called from cnchi.py with a timeout function
    # We should do as less as possible here, we want to maintain our
    # queue message as empty as possible
    def manage_events_from_cb_queue(self):
        if self.fatal_error:
            return False

        while self.callback_queue.empty() == False:
            try:
                event = self.callback_queue.get_nowait()
            except queue.Empty:
                return True

            if event[0] == 'percent':
                self.progress_bar.set_fraction(event[1])
            elif event[0] == 'global_percent':
                self.show_global_progress_bar_if_hidden()
                self.global_progress_bar.set_fraction(event[1])
            elif event[0] == 'finished':
                logging.info(event[1])
                self.set_message(self.install_ok)
                response = show.question(self.install_ok)
                if response == Gtk.ResponseType.YES:
                    self.reboot()
                else:
                    tmp_files = [".setup-running", ".km-running", "setup-pacman-running", "setup-mkinitcpio-running", ".tz-running", ".setup", "Cnchi.log"]
                    for t in tmp_files:
                        p = os.path.join("/tmp", t)
                        if os.path.exists(p):
                            # TODO: some of these tmp files are created with sudo privileges
                            # (this should be fixed) meanwhile, we need sudo privileges to remove them
                            with misc.raised_privileges():
                                os.remove(p)
                    while Gtk.events_pending():
                        Gtk.main_iteration()
                    Gtk.main_quit()
                        
                self.exit_button.show()
                return False
            elif event[0] == 'error':
                self.callback_queue.task_done()
                # a fatal error has been issued. We empty the queue
                self.empty_queue()
                self.fatal_error = True
                show.fatal_error(event[1])
                return False
            elif event[0] == 'debug':
                logging.debug(event[1])
            elif event[0] == 'warning':
                logging.warning(event[1])
            else:
                # TODO: Check if logging slows down showing messages
                #       remove logging.info in that case (and at least
                #       use the one at pac.py:queue_event)
                logging.info(event[1])
                self.set_message(event[1])
                            
            self.callback_queue.task_done()
        
        return True
        
    def empty_queue(self):
        while self.callback_queue.empty() == False:
            try:
                event = self.callback_queue.get_nowait()
                self.callback_queue.task_done()
            except queue.Empty:
                return

    @misc.raise_privileges
    def reboot(self):
        os.system("sync")
        subprocess.call(["/usr/bin/systemctl", "reboot", "--force", "--no-wall"])
