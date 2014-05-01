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

""" Shows slides while installing. Also manages installing messages and progress bars """

from gi.repository import Gtk, WebKit, GLib
import config
import os
import sys

import queue
from multiprocessing import Queue, Lock

import show_message as show
import logging
import subprocess
import canonical.misc as misc

from gtkbasebox import GtkBaseBox

# When we reach this page we can't go neither backwards nor forwards

class Slides(GtkBaseBox):
    def __init__(self, params):
        """ Initialize class and its vars """
        self.next_page = None
        self.prev_page = None

        self.callback_queue = params['callback_queue']
        self.main_progressbar = params['main_progressbar']

        super().__init__(params, "slides")

        self.ui.connect_signals(self)

        self.progress_bar = self.ui.get_object("progressbar")
        self.progress_bar.set_show_text(True)
        self.progress_bar.set_name('i_progressbar')

        self.info_label = self.ui.get_object("info_label")
        self.scrolled_window = self.ui.get_object("scrolledwindow")

        # Add a webkit view to show the slides
        self.webview = WebKit.WebView()

        if self.settings is None:
            html_file = '/usr/share/cnchi/data/slides.html'
        else:
            html_file = os.path.join(self.settings.get('data'), 'slides.html')

        try:
            with open(html_file) as html_stream:
                html = html_stream.read(None)
                data = os.path.join(os.getcwd(), "data")
                self.webview.load_string(html, "text/html", "utf-8", "file://" + data)
        except IOError:
            pass

        self.scrolled_window.add(self.webview)

        self.add(self.ui.get_object("slides"))

        self.fatal_error = False
        self.should_pulse = False

    def translate_ui(self):
        if len(self.info_label.get_label()) <= 0:
            self.set_message(_("Please wait..."))

        self.header.set_subtitle(_("Installing Antergos..."))

    def prepare(self, direction):
        self.translate_ui()
        self.show_all()

        # Last screen reached, hide main progress bar (the one at the top).
        self.main_progressbar.hide()

        # Hide backwards and forwards button
        self.backwards_button.hide()
        self.forward_button.hide()

        self.header.set_show_close_button(False)
        
        GLib.timeout_add(100, self.manage_events_from_cb_queue)

    def store_values(self):
        """ Nothing to be done here """
        return False

    def set_message(self, txt):
        """ Show information message """
        #txt = "<span color='darkred'>%s</span>" % txt
        self.info_label.set_markup(txt)

    def stop_pulse(self):
        """ Stop pulsing progressbar """
        self.should_pulse = False
        self.progress_bar.hide()
        self.info_label.show_all()

    def start_pulse(self):
        """ Start pulsing progressbar """
        def pbar_pulse():
            """ Pulse progressbar """
            if self.should_pulse:
                self.progress_bar.pulse()
            return self.should_pulse
        
        if not self.should_pulse:
            # Hide any text that might be in info area
            self.info_label.set_markup("")
            self.info_label.hide()
            # Show progress bar (just in case)
            self.progress_bar.show_all()
            self.progress_bar.set_show_text(True)
            self.should_pulse = True
            GLib.timeout_add(100, pbar_pulse)

    @misc.raise_privileges
    def remove_temp_files(self):
        tmp_files = [".setup-running", ".km-running", "setup-pacman-running", "setup-mkinitcpio-running", ".tz-running", ".setup" ]
        for t in tmp_files:
            p = os.path.join("/tmp", t)
            if os.path.exists(p):
                os.remove(p)

    def manage_events_from_cb_queue(self):
        """ We should do as less as possible here, we want to maintain our
            queue message as empty as possible """
        
        if self.fatal_error:
            return False

        while self.callback_queue.empty() == False:
            try:
                event = self.callback_queue.get_nowait()
            except queue.Empty:
                return True

            if event[0] == 'percent':
                self.progress_bar.set_fraction(event[1])
            elif event[0] == 'text':
                if event[1] == 'hide':
                    self.progress_bar.set_show_text(False)
                    self.progress_bar.set_text("")
                else:
                    self.progress_bar.set_show_text(True)
                    self.progress_bar.set_text(event[1])
            elif event[0] == 'pulse':
                if event[1] == 'stop':
                    self.stop_pulse()
                elif event[1] == 'start':
                    self.start_pulse()
            elif event[0] == 'progress_bar':
                if event[1] == 'hide':
                    self.progress_bar.hide()
            elif event[0] == 'finished':
                logging.info(event[1])
                if not self.settings.get('bootloader_ok'):
                    # Warn user about GRUB and ask if we should open wiki page.
                    boot_warn = _("IMPORTANT: There may have been a problem with the Grub(2) bootloader\n"
                                  "installation which could prevent your system from booting properly. Before\n"
                                  "rebooting, you may want to verify whether or not GRUB(2) is installed and\n"
                                  "configured. The Arch Linux Wiki contains troubleshooting information:\n"
                                  "\thttps://wiki.archlinux.org/index.php/GRUB\n"
                                  "\nWould you like to view the wiki page now?")
                    response = show.question(boot_warn)
                    if response == Gtk.ResponseType.YES:
                        import webbrowser
                        misc.drop_privileges()
                        webbrowser.open('https://wiki.archlinux.org/index.php/GRUB')

                install_ok = _("Installation Complete!\nDo you want to restart your system now?")
                response = show.question(install_ok)
                self.remove_temp_files()
                self.settings.set('stop_all_threads', True)
                #while Gtk.events_pending():
                #    Gtk.main_iteration()
                logging.shutdown()
                if response == Gtk.ResponseType.YES:
                    self.reboot()
                else:
                    sys.exit(0)
                return False
            elif event[0] == 'error':
                self.callback_queue.task_done()
                # A fatal error has been issued. We empty the queue
                self.empty_queue()

                # Show the error
                show.fatal_error(event[1])

                # Ask if user wants to retry
                res = show.question(_("Do you want to retry the installation using the same configuration?"))
                if res == GTK_RESPONSE_YES:
                    # Restart installation process
                    logging.debug(_("Restarting installation process..."))
                    p = self.settings.get('installer_thread_call')

                    self.process = installation_process.InstallationProcess(self.settings, self.callback_queue,
                        p['mount_devices'], p['fs_devices'], p['ssd'], p['alternate_package_list'], p['blvm'])

                    self.process.start()
                    return True
                else:
                    self.fatal_error = True
                    return False
            elif event[0] == 'info':
                logging.info(event[1])
                if self.should_pulse:
                    self.progress_bar.set_text(event[1])
                else:
                    self.set_message(event[1])

            self.callback_queue.task_done()

        return True

    def empty_queue(self):
        """ Empties messages queue """
        while self.callback_queue.empty() == False:
            try:
                event = self.callback_queue.get_nowait()
                self.callback_queue.task_done()
            except queue.Empty:
                return

    @misc.raise_privileges
    def reboot(self):
        """ Reboots the system, used when installation is finished """
        os.system("sync")
        subprocess.call(["/usr/bin/systemctl", "reboot", "--force", "--no-wall"])

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message): return message

if __name__ == '__main__':
    from test_screen import _,run
    run('Slides')
