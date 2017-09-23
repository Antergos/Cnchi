#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# welcome.py
#
# Copyright © 2013-2017 Antergos
#
# This file is part of Cnchi.
#
# Cnchi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Cnchi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# The following additional terms are in effect as per Section 7 of the license:
#
# The preservation of all legal notices and author attributions in
# the material or in the Appropriate Legal Notices displayed
# by works containing it is required.
#
# You should have received a copy of the GNU General Public License
# along with Cnchi; If not, see <http://www.gnu.org/licenses/>.

""" Welcome screen """

import subprocess
import os
import logging
import sys
import queue
import misc.extra as misc
from gtkbasebox import GtkBaseBox
from gi.repository import GdkPixbuf


class Welcome(GtkBaseBox):
    """ Welcome screen class """

    def __init__(self, params, prev_page=None, next_page="language"):
        super().__init__(self, params, "welcome", prev_page, next_page)

        data_dir = self.settings.get('data')
        welcome_dir = os.path.join(data_dir, "images", "welcome")

        self.main_window = params['main_window']

        self.labels = {'welcome': self.ui.get_object("welcome_label"),
                       'tryit': self.ui.get_object("tryit_welcome_label"),
                       'installit': self.ui.get_object("installit_welcome_label"),
                       'loading': self.ui.get_object("loading_label")}

        self.buttons = {'tryit': self.ui.get_object("tryit_button"),
                        # 'cli': self.ui.get_object("cli_button"),
                        'graph': self.ui.get_object("graph_button")}

        for key in self.buttons:
            btn = self.buttons[key]
            btn.set_name(key + "_btn")

        self.images = {'tryit': self.ui.get_object("tryit_image"),
                       # 'cli': self.ui.get_object("cli_image"),
                       'graph': self.ui.get_object("graph_image")}

        self.filenames = {
            'tryit': {
                'path': os.path.join(welcome_dir, "try-it.svg"),
                'width': 165,
                'height': 189},
            'graph': {
                'path': os.path.join(welcome_dir, "install-it.svg"),
                'width': 243,
                'height': 174}}

        # a11y
        self.labels['tryit'].set_mnemonic_widget(self.buttons['tryit'])
        self.labels['installit'].set_mnemonic_widget(self.buttons['graph'])

        for key in self.images:
            image = self.filenames[key]
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                image['path'],
                image['width'],
                image['height'])
            self.images[key].set_from_pixbuf(pixbuf)

    def translate_ui(self):
        """ Translates all ui elements """
        if not self.disable_tryit:
            txt = _("Use Antergos without making any changes to your system.") + "\n"
        else:
            txt = ""
        self.labels['tryit'].set_markup(txt)
        self.labels['tryit'].set_name('tryit_label')

        txt = _("Create a permanent place for Antergos on your system.")
        self.labels['installit'].set_markup(txt)
        self.labels['installit'].set_name('installit_label')

        txt = _("Try It")
        self.buttons['tryit'].set_label(txt)

        # txt = _("CLI Installer")
        # self.buttons['cli'].set_label(txt)

        txt = _("Install It")
        self.buttons['graph'].set_label(txt)

        txt = _("Welcome to Antergos!")
        self.header.set_subtitle(txt)

    def quit_cnchi(self):
        misc.remove_temp_files()
        for proc in self.process_list:
            # Wait 'timeout' seconds at most for all processes to end
            proc.join(timeout=5)
            if proc.is_alive():
                proc.terminate()
                proc.join()
        logging.shutdown()
        sys.exit(0)

    def on_tryit_button_clicked(self, widget, data=None):
        self.quit_cnchi()

    def on_graph_button_clicked(self, widget, data=None):
        self.show_loading_message()
        # Tell timezone process to start searching now
        self.settings.set('timezone_start', True)
        # Simulate a forward button click
        self.forward_button.clicked()

    def show_loading_message(self, do_show=True):
        if do_show:
            txt = _("Loading, please wait...")
        else:
            txt = ""
        self.labels['loading'].set_markup(txt)
        self.labels['loading'].queue_draw()
        misc.gtk_refresh()

    def store_values(self):
        self.forward_button.show()
        return True

    def prepare(self, direction):
        self.translate_ui()
        self.show_all()
        self.forward_button.hide()

        # a11y Set install option as default if ENTER is pressed
        self.buttons['graph'].set_can_default(True)
        self.main_window.set_default(self.buttons['graph'])

        if self.disable_tryit:
            self.buttons['tryit'].set_sensitive(False)
        if direction == "backwards":
            self.show_loading_message(do_show=False)


if __name__ == '__main__':
    from test_screen import _, run
    run('Welcome')
