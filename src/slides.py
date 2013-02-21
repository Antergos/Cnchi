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

from gi.repository import Gtk, WebKit
from config import installer_settings
import os

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

        self.progressbar = builder.get_object("progressbar")
        self.info_label = builder.get_object("info_label")
        self.scrolled_window = builder.get_object("scrolledwindow")

        self.webview = WebKit.WebView()
        #self.webview.open("http://www.cinnarch.com")
        
        html_file = os.path.join(installer_settings["DATA_DIR"], 'slides.html')
        
        try:
            with open(html_file) as html_stream:
                html = html_stream.read(None)
                data = os.path.join(os.getcwd(), "data")
                print("file://" + data)
                self.webview.load_html_string(html, "file://" + data)
        except IOError:
            pass
        
        self.scrolled_window.add(self.webview)

        #self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)

        super().add(builder.get_object("slides"))
        
        # pac gui part (used to report pacman messages)
        '''
        self.pac_ui = Gtk.Builder()
        self.pac_ui.add_from_file(os.path.join(self.ui_dir, 'pac.ui'))

        self.progress_window = self.pac_ui.get_object('ProgressWindow')
        self.progress_bar = self.pac_ui.get_object('progressbar2')
        self.progress_label = self.pac_ui.get_object('progresslabel2')
        self.error_dialog = self.pac_ui.get_object('ErrorDialog')
        self.warning_dialog = self.pac_ui.get_object('WarningDialog')
        self.question_dialog = self.pac_ui.get_object('QuestionDialog')
        self.config_dialog = self.pac_ui.get_object('ConfDialog')
        self.transaction_desc = self.pac_ui.get_object('transaction_desc')
        self.down_label = self.pac_ui.get_object('down_label')
        '''

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
        
        self.show_install_messages()

    def store_values(self):
        return False

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page

    def refresh(self):
        while Gtk.events_pending():
            Gtk.main_iteration()

    def show_install_messages(self):
        # TODO: Check self.callback_queue and show message
        # self.callback_queue
        # self.progress_bar
        
        done = False
        
        while not done:
            try:
                event = self.callback_queue.get(False)
            except queue.Empty:
                event = ()

            if len(event) > 0:
                if event[0] == "action":
                    print(event[1])
                    self.info_label.set_markup(event[1])
                elif event[0] == "icon":
                    print(event[1])
                elif event[0] == "target":
                    print(event[1])
                    self.info_label.set_markup(event[1])
                elif event[0] == "percent":
                    print(event[1])
                    self.progress_bar.set_fraction(event[1])
                elif event[0] == "finished":
                    done = True

            self.refresh()
