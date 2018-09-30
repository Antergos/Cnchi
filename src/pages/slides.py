#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# slides.py
#
# Copyright © 2013-2018 Antergos
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
import os
import queue
import subprocess


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GdkPixbuf

import show_message as show
import misc.extra as misc

from pages.gtkbasebox import GtkBaseBox

from logging_utils import ContextFilter

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

class Slides(GtkBaseBox):
    """ Slides page """

    # Check events queue every second
    MANAGE_EVENTS_TIMER = 1000

    # Change image slide every half minute
    SLIDESHOW_TIMER = 30000

    def __init__(self, params, prev_page=None, next_page=None):
        """ Initialize class and its vars """
        super().__init__(self, params, 'slides', prev_page, next_page)

        self.progress_bar = self.gui.get_object('progress_bar')
        self.progress_bar.set_show_text(True)
        self.progress_bar.set_name('i_progressbar')

        self.downloads_progress_bar = self.gui.get_object('downloads_progress_bar')
        self.downloads_progress_bar.set_show_text(True)
        self.downloads_progress_bar.set_name('a_progressbar')

        self.info_label = self.gui.get_object('info_label')

        self.fatal_error = False
        self.should_pulse = False

        self.revealer = self.gui.get_object('revealer1')
        self.revealer.connect('notify::child-revealed', self.image_revealed)
        self.slide = 0
        self.stop_slideshow = False

        GLib.timeout_add(Slides.MANAGE_EVENTS_TIMER, self.manage_events_from_cb_queue)

    def translate_ui(self):
        """ Translates all ui elements """
        if not self.info_label.get_label():
            self.info_label.set_markup(_("Please wait..."))

        self.header.set_subtitle(_("Installing Antergos..."))

    def prepare(self, direction):
        """ Prepare slides screen """
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

        # Set slide image (and show it)
        self.reveal_next_slide()

    def reveal_next_slide(self):
        """ Loads slide and reveals it """
        if not self.stop_slideshow:
            self.slide = ((self.slide + 1) % 3) + 1
            if 0 < self.slide <= 3:
                try:
                    data_dir = self.settings.get('data')
                    path = os.path.join(data_dir, 'images/slides',
                                        '{}.png'.format(self.slide))
                    img = self.gui.get_object('slide1')
                    # img.set_from_file(path)
                    # 800x334
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                        path, 820, 334, False)
                    # set the content of the image as the pixbuf
                    img.set_from_pixbuf(pixbuf)
                    # Reveal image
                    self.revealer.set_reveal_child(True)
                except FileNotFoundError:
                    # FIXME: Installation process finishes before we can read these values ?¿
                    logging.warning("Can't get configuration values.")
                    self.stop_slideshow = True

    def image_revealed(self, revealer, _revealed):
        """ Called when a image slide is shown
            revealer: Gtk.Revealer
            revealed: GParamBoolean """
        if not self.stop_slideshow:
            if revealer.get_child_revealed() and not self.stop_slideshow:
                GLib.timeout_add(Slides.SLIDESHOW_TIMER, self.hide_slide)
            else:
                self.reveal_next_slide()

    def hide_slide(self):
        """ Hide image shown in slideshow, this will trigger image_revealed()
        so the next slide image will be revealed """
        self.revealer.set_reveal_child(False)
        return False

    @staticmethod
    def store_values():
        """ Nothing to be done here """
        return False

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
                if event[1]:
                    self.progress_bar.set_text(event[1])
                else:
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
                self.installation_finished()
            elif event[0] == 'error':
                self.callback_queue.task_done()
                self.install_error(event[1])
            elif event[0] == 'info':
                logging.info(event[1])
                if self.should_pulse:
                    self.progress_bar.set_text(event[1])
                else:
                    self.info_label.set_markup(event[1])
            elif event[0] == 'cache_pkgs_md5_check_failed':
                logging.debug(
                    'Adding %s to cache_pkgs_md5_check_failed list', event[1])
                self.settings.set('cache_pkgs_md5_check_failed', event[1])
            else:
                logging.warning("Event %s not recognised. Ignoring.", event[0])

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

    @staticmethod
    def reboot():
        """ Reboots the system, used when installation is finished """
        with misc.raised_privileges():
            try:
                cmd = ["sync"]
                subprocess.call(cmd)
                cmd = ["/usr/bin/systemctl", "reboot", "--force", "--no-wall"]
                subprocess.call(cmd)
            except subprocess.CalledProcessError as error:
                logging.error(error)

    def installation_finished(self):
        """ Installation finished """
        log_util = ContextFilter()
        log_util.send_install_result("True")

        self.stop_slideshow = True

        try:
            bootloader_install = self.settings.get('bootloader_install')
            bootloader_install_ok = self.settings.get('bootloader_installation_successful')

            if bootloader_install and not bootloader_install_ok:
                # Warn user about GRUB and ask if we should open wiki page.
                boot_warn = _(
                    "IMPORTANT: There may have been a problem with the bootloader installation "
                    "which could prevent your system from booting properly. Before rebooting, "
                    "you may want to verify whether or not the bootloader is installed and "
                    "configured.\n\n"
                    "The Arch Linux Wiki contains troubleshooting information:\n"
                    "\thttps://wiki.archlinux.org/index.php/GRUB\n\n"
                    "Would you like to view the wiki page now?")
                response = show.question(self.get_main_window(), boot_warn)
                if response == Gtk.ResponseType.YES:
                    import webbrowser
                    misc.drop_privileges()
                    wiki_url = 'https://wiki.archlinux.org/index.php/GRUB'
                    webbrowser.open(wiki_url)
        except FileNotFoundError:
            # FIXME: Installation process finishes before we can read these values ?¿
            logging.warning("Can't get configuration values.")

        install_ok = _(
            "Installation Complete!\n"
            "Do you want to restart your system now?")
        response = show.question(self.get_main_window(), install_ok)
        misc.remove_temp_files(self.settings.get('temp'))
        logging.shutdown()
        if response == Gtk.ResponseType.YES:
            self.reboot()
        else:
            sys.exit(0)

    def install_error(self, error):
        """ A fatal error has been issued """

        self.stop_slideshow = True

        # Empty the events queue
        self.empty_queue()

        log_util = ContextFilter()
        log_util.send_install_result("False")
        if log_util.have_install_id:
            # Add install id to error message
            # (we can lookup logs on bugsnag by the install id)
            tpl = _(
                'Please reference the following number when reporting this error: ')
            error_message = '{0}\n{1}{2}'.format(
                error, tpl, log_util.install_id)
        else:
            error_message = error

        show.fatal_error(self.get_main_window(), error_message)
