#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# main_window.py
#
# Copyright © 2013-2015 Antergos
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


""" Main Cnchi Window """

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
import desktop_info
import features
import keymap
import timezone
import user_info
import slides
import summary
import info
import substack

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Atk

import show_message as show
import misc.extra as misc

from installation import ask as installation_ask
from installation import automatic as installation_automatic
from installation import alongside as installation_alongside
from installation import advanced as installation_advanced
from installation import zfs as installation_zfs


def atk_set_image_description(widget, description):
    """ Sets the textual description for a widget that displays image/pixmap
        information onscreen. """
    atk_widget = widget.get_accessible()
    if atk_widget is not None:
        atk_widget.set_image_description(description)


class MainWindow(Gtk.ApplicationWindow):
    """ Cnchi main window """

    def __init__(self, app, cmd_line):
        super().__init__(title="Cnchi", application=app)

        self.cnchi_app = app
        self._main_window_width = 960
        self._main_window_height = 600

        logging.info("Cnchi installer version %s", info.CNCHI_VERSION)

        self.settings = config.Settings()
        self.ui_dir = self.settings.get('ui')
        self.cmd_line = cmd_line
        self.params = dict()
        self.data_dir = self.settings.get('data')
        self.current_stack = None
        self.current_group = None
        self.nav_buttons = {}

        # By default, always try to use local /var/cache/pacman/pkg
        self.xz_cache = ["/var/cache/pacman/pkg"]

        # Check command line
        if cmd_line.cache and cmd_line.cache not in self.xz_cache:
            self.xz_cache.append(cmd_line.cache)

        # Log cache dirs
        for xz in self.xz_cache:
            logging.debug("Cnchi will use '%s' as a source for cached xz packages", xz)

        # Store cache dirs in config
        self.settings.set('xz_cache', self.xz_cache)

        # For things we are not ready for users to test
        self.settings.set('z_hidden', cmd_line.z_hidden)

        # Set enabled desktops
        if self.settings.get('z_hidden'):
            self.settings.set("desktops", desktop_info.DESKTOPS_DEV)
        else:
            self.settings.set("desktops", desktop_info.DESKTOPS)

        if cmd_line.environment:
            my_desktop = cmd_line.environment.lower()
            if my_desktop in desktop_info.DESKTOPS:
                self.settings.set('desktop', my_desktop)
                self.settings.set('desktop_ask', False)
                logging.debug(
                    "Cnchi will install the %s desktop environment",
                    my_desktop)

        # Create a queue. Will be used to report pacman messages
        # (pacman/pac.py) to the main thread (installation/process.py)
        self.callback_queue = multiprocessing.JoinableQueue()

        # This list will have all processes (rankmirrors, autotimezone...)
        self.process_list = []

        # Initialize GUI elements
        self.initialize_gui()

        # Prepare params dict to pass common parameters to all screens
        self.prepare_shared_parameters()

        self.language_widget = language.LanguageWidget(self.params)
        self.popover = Gtk.Popover.new(self.language_menu_btn)
        self.popover.add(self.language_widget)
        self.popover.set_position(Gtk.PositionType.BOTTOM)
        self.popover.connect('closed', self.on_language_popover_closed)

        if cmd_line.packagelist:
            self.settings.set('alternate_package_list', cmd_line.packagelist)
            logging.info(
                "Using '%s' file as package list",
                self.settings.get('alternate_package_list'))

        # Just load the first screen (the other ones will be loaded later)
        # We do this to reduce Cnchi's initial startup time.
        self.pages = dict()
        if os.path.exists('/home/antergos/.config/openbox'):
            # In minimal iso, load the system check screen now
            self.pages["check"] = check.Check(self.params)
            self.current_page = self.pages["check"]
            self.settings.set('timezone_start', True)

            # Fix buggy Gtk window size when using Openbox
            self._main_window_width = 960
            self._main_window_height = 600
        else:
            self.pages["welcome"] = welcome.Welcome(self.params)
            self.current_page = self.pages["welcome"]
            self.main_box.add(self.current_page)

        self.connect('delete-event', self.on_exit_button_clicked)
        self.connect('key-release-event', self.on_key_release)

        self.ui.connect_signals(self)
        self.header_ui.connect_signals(self)

        self.set_geometry()

        # Set window icon
        icon_path = os.path.join(
            self.data_dir,
            "images",
            "antergos",
            "antergos-ball.png")
        self.set_icon_from_file(icon_path)

        # Use our css file
        style_provider = Gtk.CssProvider()

        style_css = os.path.join(self.data_dir, "css", "gtk-style.css")

        with open(style_css, 'rb') as css:
            css_data = css.read()

        style_provider.load_from_data(css_data)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        # Show main window
        self.show_all()

        self.current_page.prepare('forwards')

        # Hide backwards button
        self.backwards_button.hide()

        self.progressbar.set_fraction(0)
        self.progressbar_step = 0

        # Do not hide progress bar for minimal iso as it would break
        # the widget alignment on language page.
        if not os.path.exists('/home/antergos/.config/openbox'):
            # Hide progress bar
            self.progressbar.hide()

        misc.gtk_refresh()

    def prepare_shared_parameters(self):
        """
        Parameters that are common to all screens

        """

        self.params['main_window'] = self
        self.params['main_box_wrapper'] = self.main_box_wrapper
        self.params['header'] = self.header
        self.params['ui_dir'] = self.ui_dir
        self.params['forward_button'] = self.forward_button
        self.params['backwards_button'] = self.backwards_button
        self.params['callback_queue'] = self.callback_queue
        self.params['settings'] = self.settings
        self.params['main_progressbar'] = self.progressbar
        self.params['process_list'] = self.process_list
        self.params['checks_are_optional'] = self.cmd_line.no_check
        self.params['disable_tryit'] = self.cmd_line.disable_tryit
        self.params['disable_rank_mirrors'] = self.cmd_line.disable_rank_mirrors
        self.params['testing'] = self.cmd_line.testing

    def initialize_gui(self):
        """
        Initial setup of our UI elements.

        """
        self.ui = Gtk.Builder()
        path = os.path.join(self.ui_dir, "cnchi.ui")
        self.ui.add_from_file(path)
        self.add(self.ui.get_object("main"))

        self.main_box_wrapper = self.ui.get_object("main_box_wrapper")
        self.main_box = self.ui.get_object("main_box")
        self.main_stack = self.ui.get_object("main_stack")

        self.progressbar = self.ui.get_object("main_progressbar")
        self.progressbar.set_name('process_progressbar')

        self.header_ui = Gtk.Builder()
        path = os.path.join(self.ui_dir, "header.ui")
        self.header_ui.add_from_file(path)
        self.header = self.header_ui.get_object("header")
        self.header_overlay = self.header_ui.get_object("header_overlay")
        self.header_nav = self.header_ui.get_object("header_nav")
        self.language_menu_btn = self.header_ui.get_object('language_button')

        self.logo = self.header_ui.get_object("logo")
        path = os.path.join(self.data_dir, "images", "antergos", "image10.png")
        self.logo.set_from_file(path)

        self.header_overlay.add_overlay(self.header)
        self.header_overlay.add_overlay(self.header_nav)
        self.header_overlay.add_overlay(self.progressbar)
        self.header_overlay.set_overlay_pass_through(self.header, True)
        self.header_overlay.set_overlay_pass_through(self.progressbar, True)
        self.header_overlay.set_overlay_pass_through(self.header_nav, True)
        self.set_titlebar(self.header_overlay)


        # To honor our css
        self.header.set_name("header")
        self.logo.set_name("logo")

        self.forward_button = self.header_ui.get_object("forward_button")
        self.backwards_button = self.header_ui.get_object("backwards_button")

        atk_set_image_description(self.forward_button, _("Next step"))
        atk_set_image_description(self.backwards_button, _("Previous step"))

        self.forward_button.set_name('fwd_btn')
        self.forward_button.set_always_show_image(True)

        self.backwards_button.set_name('bk_btn')
        self.backwards_button.set_always_show_image(True)

        title = "Cnchi {0}".format(info.CNCHI_VERSION)
        self.set_title(title)
        self.header.set_title(title)
        self.header.set_subtitle(_("Antergos Installer"))
        self.header.set_show_close_button(False)

    def load_pages(self):

        top_level_pages = ['check', 'location_group', 'desktop', 'features', 'disk_group',
                           'user_info', 'summary']
        if not os.path.exists('/home/antergos/.config/openbox'):
            self.pages["check"] = check.Check(params=self.params)

        self.pages["location_group"] = {'title': 'Location',
                                        'prev_page': 'check',
                                        'next_page': 'location',
                                        'pages': ['location', 'timezone', 'keymap']}
        self.pages["location_group"]["location"] = location.Location(params=self.params, in_group=True)
        self.pages["location_group"]["timezone"] = timezone.Timezone(params=self.params, in_group=True)

        if self.settings.get('desktop_ask'):
            self.pages["location_group"]["keymap"] = keymap.Keymap(params=self.params, in_group=True)
            self.pages["desktop"] = desktop.DesktopAsk(params=self.params)
            self.pages["features"] = features.Features(params=self.params)
        else:
            self.pages["location_group"]["keymap"] = keymap.Keymap(
                self.params,
                next_page='features',
                in_group=True)
            self.pages["features"] = features.Features(
                self.params,
                prev_page='location_group')

        self.pages["disk_group"] = {'title': 'Disk Setup',
                                    'prev_page': 'features',
                                    'next_page': 'installation_ask',
                                    'pages': ['installation_ask', 'installation_automatic',
                                              'installation_alongside', 'installation_advanced',
                                              'installation_zfs']}
        self.pages["disk_group"]["installation_ask"] = installation_ask.InstallationAsk(
                params=self.params,
                in_group=True)
        self.pages["disk_group"]["installation_automatic"] = installation_automatic.InstallationAutomatic(
                params=self.params,
                in_group=True)

        if self.settings.get("enable_alongside"):
            self.pages["disk_group"]["installation_alongside"] = installation_alongside.InstallationAlongside(
                    params=self.params,
                    in_group=True)
        else:
            self.pages["disk_group"]["installation_alongside"] = None

        self.pages["disk_group"]["installation_advanced"] = installation_advanced.InstallationAdvanced(
                params=self.params,
                in_group=True)
        self.pages["disk_group"]["installation_zfs"] = installation_zfs.InstallationZFS(
                params=self.params,
                in_group=True)
        self.pages["user_info"] = user_info.UserInfo(params=self.params)
        self.pages["summary"] = summary.Summary(params=self.params)
        self.pages["slides"] = slides.Slides(params=self.params)

        diff = 2
        if os.path.exists('/home/antergos/.config/openbox'):
            # In minimal (openbox) we don't have a welcome screen
            diff = 3

        num_pages = len(self.pages) - diff

        if num_pages > 0:
            self.progressbar_step = 1.0 / num_pages

        for page_name in top_level_pages:
            page = self.pages[page_name]
            if isinstance(page, dict):
                sub_stack = substack.SubStack(params=self.params,
                                              name=page_name,
                                              title=page['title'],
                                              prev_page=page['prev_page'],
                                              next_page=page['next_page'])

                for sub_page_name in page['pages']:
                    sub_page = self.pages[page_name][sub_page_name]
                    if sub_page:
                        sub_stack.add_titled(sub_page, sub_page_name, sub_page.title)

                self.pages[page_name]['group'] = page = sub_stack

            page.show_all()
            self.main_stack.add_titled(page, page_name, page.title)
            self.nav_buttons[page_name] = Gtk.Button.new_with_label(page.title)
            self.nav_buttons[page_name].connect('clicked', self.on_header_nav_button_clicked, page_name)
            self.header_nav.add(self.nav_buttons[page_name])

        self.header_nav.show_all()
        # self.header_nav.set_stack(self.main_stack)
        self.current_stack = self.main_stack

    def del_pages(self):
        """ When we get to user_info page we can't go back
        therefore we can delete all previous pages for good """
        # FIXME: As there are more references, this does nothing
        try:
            del self.pages["welcome"]
            del self.pages["language"]
            del self.pages["location"]
            del self.pages["check"]
            del self.pages["desktop"]
            del self.pages["features"]
            del self.pages["keymap"]
            del self.pages["timezone"]
            del self.pages["installation_ask"]
            del self.pages["installation_automatic"]
            if self.pages["installation_alongside"] is not None:
                del self.pages["installation_alongside"]
            del self.pages["installation_advanced"]
            del self.pages["installation_zfs"]
        except KeyError as key_error:
            pass

    def set_geometry(self):
        """ Sets Cnchi window geometry """
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)
        self.set_size_request(self._main_window_width, self._main_window_height)
        self.set_default_size(self._main_window_width, self._main_window_height)

        geom = Gdk.Geometry()
        geom.min_width = self._main_window_width
        geom.min_height = self._main_window_height
        geom.max_width = self._main_window_width
        geom.max_height = self._main_window_height
        geom.base_width = self._main_window_width
        geom.base_height = self._main_window_height
        geom.width_inc = 0
        geom.height_inc = 0

        hints = (Gdk.WindowHints.MIN_SIZE |
                 Gdk.WindowHints.MAX_SIZE |
                 Gdk.WindowHints.BASE_SIZE |
                 Gdk.WindowHints.RESIZE_INC)

        self.set_geometry_hints(None, geom, hints)

    def on_key_release(self, widget, event, data=None):
        """ Params: GtkWidget *widget, GdkEventKey *event, gpointer data """
        if event.keyval == Gdk.keyval_from_name('Escape'):
            response = self.confirm_quitting()
            if response == Gtk.ResponseType.YES:
                self.on_exit_button_clicked(self)
                self.destroy()

    def confirm_quitting(self):
        message = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            destroy_with_parent=True,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=_("Do you really want to quit the installer?"))
        response = message.run()
        message.destroy()
        return response

    def on_exit_button_clicked(self, widget, data=None):
        """ Quit Cnchi """
        try:
            misc.remove_temp_files()
            logging.info("Quiting installer...")
            for proc in self.process_list:
                if proc.is_alive():
                    proc.terminate()
                    proc.join()
            logging.shutdown()
        except KeyboardInterrupt:
            pass

    def on_language_button_clicked(self, widget, data=None):
        self.popover.show_all()
        self.language_widget.popover_is_visible = True

    def on_language_popover_closed(self, widget, data=None):
        self.language_widget.popover_is_visible = False

    def on_header_nav_button_clicked(self, widget, data=None):
        page_name = data
        page = self.current_stack.get_child_by_name(page_name)
        can_show = page_name != self.current_page.name and page.can_show
        is_next = page_name == self.current_page.get_next_page()

        if is_next:
            self.on_forward_button_clicked(None)
            return

        if can_show:
            self.current_stack.set_visible_child(page)

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

        if next_page is not None:
            if next_page not in self.pages.keys():
                # Load all pages
                self.load_pages()
                self.progressbar_step = 1.0 / (len(self.pages) - 2)

            stored = self.current_page.store_values()

            if stored:
                self.set_progressbar_step(self.progressbar_step)
                if 'welcome' == self.current_page.get_name():
                    self.main_box.set_visible(False)
                    # self.header_nav.set_stack(self.main_stack)
                    self.main_stack.set_visible(True)
                else:
                    self.nav_buttons[self.current_page.get_name()].set_state(Gtk.StateFlags.NORMAL)

                if self.current_group:
                    self.current_page = self.pages[self.current_group][next_page]
                else:
                    self.current_page = self.pages[next_page]

                if self.current_page is not None:
                    if isinstance(self.current_page, dict):
                        self.current_stack.set_visible_child_name(next_page)
                        self.current_stack.can_show = True
                        self.current_group = next_page
                        self.current_stack = self.current_page['group']
                        page_after_next = self.current_page['group'].get_next_page()
                        self.current_page = self.pages[next_page][page_after_next]
                        self.nav_buttons[self.current_group].set_state(Gtk.StateFlags.SELECTED)
                    elif not self.current_page.in_group:
                        self.current_stack = self.main_stack
                        self.current_group = None
                        self.nav_buttons[self.current_page.get_name()].set_state(Gtk.StateFlags.SELECTED)

                    self.current_page.prepare('forwards')
                    self.current_page.can_show = True
                    self.current_stack.set_visible_child_name(self.current_page.get_name())

                    if self.current_page.get_prev_page() is not None:
                        # There is a previous page, show back button
                        self.backwards_button.show()
                        self.backwards_button.set_sensitive(True)
                    else:
                        # We can't go back, hide back button
                        self.backwards_button.hide()
                        if self.current_page == "slides":
                            # Show logo in slides screen
                            self.logo.show_all()

    def on_backwards_button_clicked(self, widget, data=None):
        """ Show previous screen """
        prev_page = self.current_page.get_prev_page()

        if prev_page is not None:
            self.set_progressbar_step(-self.progressbar_step)

            # If we go backwards, don't store user changes
            # self.current_page.store_values()

            if 'welcome' == prev_page:
                self.main_stack.set_visible(False)
                self.main_box.set_visible(True)

            self.current_page = self.pages[prev_page]

            if self.current_page is not None:
                self.current_page.prepare('backwards')

                if self.current_page.get_prev_page() is None:
                    # We're at the first page
                    self.backwards_button.hide()
                    self.progressbar.hide()
                    self.logo.show_all()
                else:
                    self.main_stack.set_visible_child_name(self.current_page.get_name())
