#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# slides.py
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


""" Shows slides while installing. Also manages installing messages and progress bars """

import sys
import logging
import subprocess

import queue

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, GLib, WebKit2

import show_message as show
import misc.extra as misc

from gtkbasebox import GtkBaseBox

from logging_utils import ContextFilter

# There is a bug (I guess its a bug) where webkit2 renders local html files as plain text.
SLIDES_URI = 'https://antergos.com/cnchi-installer-slideshow'


class Slides(GtkBaseBox):
    def __init__(self, params, prev_page=None, next_page=None):
        """ Initialize class and its vars """
        super().__init__(self, params, "slides", prev_page, next_page)

        self.progress_bar = self.ui.get_object("progress_bar")
        self.progress_bar.set_show_text(True)
        self.progress_bar.set_name('i_progressbar')

        self.downloads_progress_bar = self.ui.get_object("downloads_progress_bar")
        self.downloads_progress_bar.set_show_text(True)
        self.downloads_progress_bar.set_name('a_progressbar')

        self.info_label = self.ui.get_object("info_label")

        self.fatal_error = False
        self.should_pulse = False

        self.web_view = None
        self.web_view_settings = None

        self.web_view_box = self.ui.get_object("scrolledwindow")

        GLib.timeout_add(1000, self.manage_events_from_cb_queue)

    def translate_ui(self):
        """ Translates all ui elements """
        if len(self.info_label.get_label()) <= 0:
            self.set_message(_("Please wait..."))

        self.header.set_subtitle(_("Installing Antergos..."))

    @staticmethod
    def _get_settings_for_webkit():
        return {
            'enable_developer_extras': False,
            'javascript_can_open_windows_automatically': True,
            'allow_file_access_from_file_urls': True,
            'enable_write_console_messages_to_stdout': False
        }

    def _apply_webkit_settings(self):
        self.web_view_settings = WebKit2.Settings()
        all_settings = self._get_settings_for_webkit()

        for setting_name, value in all_settings.items():
            setting_name = 'set_{}'.format(setting_name)
            set_setting = getattr(self.web_view_settings, setting_name)

            set_setting(value)

    def prepare(self, direction):
        """ Prepare slides screen """
        # We don't load webkit until we reach this screen
        if self.web_view is None:
            # Add a webkit view and load our html file to show the slides
            try:
                self._apply_webkit_settings()
                self.web_view = WebKit2.WebView.new_with_settings(self.web_view_settings)
                self.web_view.connect('context-menu', lambda _a, _b, _c, _d: True)
                self.web_view.set_hexpand(True)
                self.web_view.load_uri(SLIDES_URI)
            except IOError as io_error:
                logging.warning(io_error)

            self.web_view_box.add(self.web_view)
            self.web_view_box.set_size_request(800, 335)

        self.translate_ui()
        self.show_all()

        # Last screen reached, hide main progress bar (the one at the top).
        self.main_progressbar.hide()

        # Also hide total downloads progress bar
        self.downloads_progress_bar.hide()

        # Hide backwards and forwards buttons
        self.backwards_button.hide()
        self.forward_button.hide()

        # Hide close button (we've reached the point of no return)
        self.header.set_show_close_button(False)

    @staticmethod
    def store_values(**kwargs):
        """ Nothing to be done here """
        return False

    def set_message(self, txt):
        """ Show information message """
        self.info_label.set_markup(txt)

    def stop_pulse(self):
        """ Stop pulsing progressbar """
        self.should_pulse = False
        # self.progress_bar.hide()
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
        """ We should be quick here and do as less as possible """

        if self.fatal_error:
            return False

        if self.callback_queue is None:
            return True

        while not self.callback_queue.empty():
            try:
                event = self.callback_queue.get_nowait()
            except ValueError as queue_error:
                # Calling get_nowait so many times can issue a ValueError
                # exception with this error: semaphore or lock released too
                # many times. Log it anyways to keep an eye on this error
                logging.error(queue_error)
                return True
            except queue.Empty:
                # Queue is empty, just quit.
                return True

            if event[0] == 'percent':
                self.progress_bar.set_fraction(float(event[1]))
            elif event[0] == 'downloads_percent':
                self.downloads_progress_bar.set_fraction(float(event[1]))
            elif event[0] == 'progress_bar_show_text':
                if len(event[1]) > 0:
                    # self.progress_bar.set_show_text(True)
                    self.progress_bar.set_text(event[1])
                else:
                    # self.progress_bar.set_show_text(False)
                    self.progress_bar.set_text("")
            elif event[0] == 'progress_bar':
                if event[1] == 'hide':
                    self.progress_bar.hide()
                elif event[1] == 'show':
                    self.progress_bar.show()
            elif event[0] == 'downloads_progress_bar':
                if event[1] == 'hide':
                    self.downloads_progress_bar.hide()
                elif event[1] == 'show':
                    self.downloads_progress_bar.show()
            elif event[0] == 'pulse':
                if event[1] == 'stop':
                    self.stop_pulse()
                elif event[1] == 'start':
                    self.start_pulse()
            elif event[0] == 'finished':
                logging.info(event[1])
                log_util = ContextFilter()
                log_util.send_install_result("True")
                if (self.settings.get('bootloader_install') and
                        not self.settings.get('bootloader_installation_successful')):
                    # Warn user about GRUB and ask if we should open wiki page.
                    boot_warn = _("IMPORTANT: There may have been a problem "
                                  "with the bootloader installation which "
                                  "could prevent your system from booting "
                                  "properly. Before rebooting, you may want "
                                  "to verify whether or not the bootloader is "
                                  "installed and configured.\n\n"
                                  "The Arch Linux Wiki contains "
                                  "troubleshooting information:\n"
                                  "\thttps://wiki.archlinux.org/index.php/GRUB\n\n"
                                  "Would you like to view the wiki page now?")
                    response = show.question(self.get_main_window(), boot_warn)
                    if response == Gtk.ResponseType.YES:
                        import webbrowser
                        misc.drop_privileges()
                        wiki_url = 'https://wiki.archlinux.org/index.php/GRUB'
                        webbrowser.open(wiki_url)

                install_ok = _("Installation Complete!\n"
                               "Do you want to restart your system now?")
                response = show.question(self.get_main_window(), install_ok)
                misc.remove_temp_files()
                logging.shutdown()
                if response == Gtk.ResponseType.YES:
                    self.reboot()
                else:
                    sys.exit(0)
                return False
            elif event[0] == 'error':
                log_util = ContextFilter()
                log_util.send_install_result("False")
                self.callback_queue.task_done()
                # A fatal error has been issued. We empty the queue
                self.empty_queue()

                # Add install id to error message (we can lookup logs on bugsnag by the install id)
                tpl = _('Please reference the following number when reporting this error: ')
                error_message = '{0}\n{1}{2}'.format(event[1], tpl, log_util.install_id)

                # Show the error
                show.fatal_error(self.get_main_window(), error_message)
            elif event[0] == 'info':
                logging.info(event[1])
                if self.should_pulse:
                    self.progress_bar.set_text(event[1])
                else:
                    self.set_message(event[1])

            elif event[0] == 'cache_pkgs_md5_check_failed':
                logging.debug(
                    'Adding %s to cache_pkgs_md5_check_failed list',
                    event[1])
                self.settings.set('cache_pkgs_md5_check_failed', event[1])

            self.callback_queue.task_done()

        return True

    def empty_queue(self):
        """ Empties messages queue """
        while not self.callback_queue.empty():
            try:
                self.callback_queue.get_nowait()
                self.callback_queue.task_done()
            except queue.Empty:
                return

    @misc.raise_privileges
    def reboot(self):
        """ Reboots the system, used when installation is finished """
        cmd = ["sync"]
        subprocess.call(cmd)
        cmd = ["/usr/bin/systemctl", "reboot", "--force", "--no-wall"]
        subprocess.call(cmd)


if __name__ == '__main__':
    from test_screen import run

    run('Slides')
