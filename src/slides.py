#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  slides.py
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

from gi.repository import Gtk, WebKit, GLib
from config import installer_settings
import os
import queue
import show_message as show
import log

_scroll_step = 4

_slide_width = 610
_slide_height = 300

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

        super().__init__()

        builder = Gtk.Builder()

        builder.add_from_file(os.path.join(self.ui_dir, "slides.ui"))
        builder.connect_signals(self)

        self.progress_bar = builder.get_object("progressbar")
        self.info_label = builder.get_object("info_label")
        self.scrolled_window = builder.get_object("scrolledwindow")

        self.webview = WebKit.WebView()
        
        html_file = os.path.join(installer_settings["DATA_DIR"], 'slides.html')
        
        try:
            with open(html_file) as html_stream:
                html = html_stream.read(None)
                data = os.path.join(os.getcwd(), "data")
                self.webview.load_html_string(html, "file://" + data)
        except IOError:
            pass
        
        self.scrolled_window.add(self.webview)

        #self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)

        super().add(builder.get_object("slides"))
        
    def translate_ui(self):
        txt = _("Learn more about Cinnarch")
        txt = "<span weight='bold' size='large'>%s</span>" % txt
        self.title.set_markup(txt)

        txt = _("TODO : Show here information about what's happening....")
        txt = "<span color='darkred'>%s</span>" % txt
        self.info_label.set_markup(txt)

    def prepare(self):
        self.translate_ui()
        self.show_all()

        self.backwards_button.hide()
        self.forward_button.hide()
        self.exit_button.hide()
                
        # stop show.manage_events_from_cb_queue.
        # We will manage our installer messages here.
        # (this is used to be able to shown installer messages in
        #  timezone, keymap and user_info screens)
        show._show_event_queue_messages = False

        # let show_install_messages manage installer messages
        GLib.timeout_add_seconds(2, self.manage_events_from_cb_queue)

    def store_values(self):
        return False

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page

    def refresh(self):
        while Gtk.events_pending():
            Gtk.main_iteration()

    def manage_events_from_cb_queue(self):
        try:
            event = self.callback_queue.get_nowait()
        except queue.Empty:
            event = ()

        install_ok = _("Installation finished!")

        if len(event) > 0:
            show.cb_log_queue_event(event)
            
            if event[0] == "info":
                self.info_label.set_markup(event[1])
            elif event[0] == "debug":
                pass
            elif event[0] == "warning":
                self.info_label.set_markup(event[1])
            elif event[0] == "action":
                self.info_label.set_markup(event[1])
            elif event[0] == "target":
                self.info_label.set_markup(event[1])
            elif event[0] == "percent":
                self.progress_bar.set_fraction(event[1])
            elif event[0] == "finished":
                self.info_label.set_markup(install_ok)
                show.message(install_ok)
                self.done = True
                error = False
                self.exit_button.show()
                return False
            elif event[0] == "error":
                show.fatal_error(event[1])
        
        return True
