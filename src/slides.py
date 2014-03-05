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

import queue
from multiprocessing import Queue, Lock

import show_message as show
import logging
import subprocess
import canonical.misc as misc

# When we reach this page we can't go neither backwards nor forwards
_next_page = None
_prev_page = None

class Slides(Gtk.Box):
    def __init__(self, params):
        """ Initialize class and its vars """
        self.header = params['header']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
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

        self.progress_bar.set_name('i_progressbar')
        self.global_progress_bar.set_name('a_progressbar')

        self.info_label = builder.get_object("info_label")
        self.scrolled_window = builder.get_object("scrolledwindow")

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

        super().add(builder.get_object("slides"))

        self.fatal_error = False
        self.global_progress_bar_is_hidden = True
        self.should_pulse = False

    def translate_ui(self):
        if len(self.info_label.get_label()) <= 0:
            self.set_message(_("Please wait..."))

        self.header.set_subtitle(_("Installing Antergos..."))

    def show_global_progress_bar_if_hidden(self):
        if self.global_progress_bar_is_hidden:
            self.global_progress_bar.show_all()
            self.global_progress_bar_is_hidden = False

    def prepare(self, direction):
        self.translate_ui()
        self.show_all()

        # Last screen reached, hide main progress bar.
        self.main_progressbar.hide()

        # Hide global progress bar
        self.global_progress_bar.hide()
        self.global_progress_bar_is_hidden = True

        # Hide backwards and forwards button
        self.backwards_button.hide()
        self.forward_button.hide()

        self.header.set_show_close_button(False)

    def store_values(self):
        """ Nothing to be done here """
        return False

    def get_prev_page(self):
        """ No previous page available """
        return _prev_page

    def get_next_page(self):
        """ This is the last page """
        return _next_page

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

    def manage_events_from_cb_queue(self):
        """ This function is called from cnchi.py with a timeout function
            We should do as less as possible here, we want to maintain our
            queue message as empty as possible """
        if self.fatal_error:
            return False

        while self.callback_queue.empty() == False:
            try:
                event = self.callback_queue.get_nowait()
            except queue.Empty:
                return True

            if event[0] == 'local_percent':
                self.progress_bar.set_fraction(event[1])
            elif event[0] == 'global_percent':
                self.show_global_progress_bar_if_hidden()
                self.global_progress_bar.set_fraction(event[1])
            elif event[0] == 'pulse':
                if event[1] == 'stop':
                    self.stop_pulse()
                elif event[1] == 'start':
                    self.start_pulse()
            elif event[0] == 'progress_bars':
                if event[1] == 'hide_all' or event[1] == 'hide_global':
                    self.global_progress_bar.hide()
                    self.global_progress_bar_is_hidden = True
                if event[1] == 'hide_all' or event[1] == 'hide_local':
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
                if response == Gtk.ResponseType.YES:
                    logging.shutdown()
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
                    logging.shutdown()
                    Gtk.main_quit()
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
                    logging.debug("Restarting installation process...")
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
