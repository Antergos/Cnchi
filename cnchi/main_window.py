#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# main_window.py
#
# Copyright © 2013-2016 Antergos
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

import logging
import multiprocessing
import os
import sys
import time

import config
import desktop_info
import info
import language
from base_ui import Page, Stack
from ui_controller import UIController

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Atk, GLib

import show_message as show
import misc.extra as misc


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

        # Default window size
        # self._main_window_width = 1200
        # self._main_window_height = 821
        self._main_window_width = 1000
        self._main_window_height = 621

        if cmd_line.resolution:
            self.set_window_size(cmd_line.resolution)

        logging.info("Cnchi installer version %s", info.CNCHI_VERSION)

        logging.debug("Window size %dx%d", self._main_window_width, self._main_window_height)

        self.settings = config.Settings()
        self.cmd_line = cmd_line
        self.params = dict()
        self.data_dir = self.settings.get('data')

        self.gui = {}
        self.nav_buttons = {}
        self.sub_nav_btns = {}

        self.stacks = []
        self.current_stack = None

        # By default, always try to use local /var/cache/pacman/pkg
        self.xz_cache = ["/var/cache/pacman/pkg"]

        # Add xz cache dirs added using the command line
        if cmd_line.cache and cmd_line.cache not in self.xz_cache:
            self.xz_cache.append(cmd_line.cache)

        # Log xz cache dirs
        for xz in self.xz_cache:
            logging.debug("Cnchi will use '%s' as a source for cached xz packages", xz)

        # Store xz cache dirs in config
        self.settings.set('xz_cache', self.xz_cache)

        # For things we are not ready for users to test
        self.settings.set('z_hidden', cmd_line.z_hidden)

        # Set enabled desktops
        if self.settings.get('z_hidden'):
            self.settings.set("desktops", desktop_info.DESKTOPS_DEV)
        else:
            self.settings.set("desktops", desktop_info.DESKTOPS)

        # DE can be forced by command line
        if cmd_line.environment:
            my_desktop = cmd_line.environment.lower()
            if my_desktop in desktop_info.DESKTOPS:
                self.settings.set('desktop', my_desktop)
                self.settings.set('desktop_ask', False)
                logging.debug("Cnchi will install the %s desktop environment", my_desktop)

        # Store if we're running from the minimal ISO (runs openbox instead of Gnome)
        self.is_minimal = os.path.exists('/home/antergos/.config/openbox')

        # Create a queue. Will be used to report pacman messages
        # (pacman/pac.py) to the installer process (installation/install.py)
        self.callback_queue = multiprocessing.JoinableQueue()

        # This list will have all processes (rankmirrors, autotimezone...)
        self.process_list = []

        # Initialize GUI elements
        self.initialize_gui()

        # Prepare params dict to pass common parameters to all screens
        self.prepare_shared_parameters()

        self.pages = UIController(self.params)

        # Top right Language widget
        self.language_widget = language.LanguageWidget(self.params, button=self.gui["language_button"])
        self.popover = Gtk.Popover.new(self.gui["language_button"])
        self.popover.add(self.language_widget)
        self.popover.set_position(Gtk.PositionType.BOTTOM)
        self.popover.connect('closed', self.on_language_popover_closed)

        # User can use an alternate package list
        if cmd_line.packagelist:
            self.settings.set('alternate_package_list', cmd_line.packagelist)
            logging.info(
                "Using '%s' file as package list",
                self.settings.get('alternate_package_list'))

        # Load 1st and 2nd screens
        self.pages.pre_load_pages()

        # main_box is the gtk box that will contain current screen
        self.gui["main_box"].add(self.pages.get_current_page())

        self.settings.set('timezone_start', True)

        # When cnchi is closed
        self.connect('delete-event', self.on_exit_button_clicked)

        # Controls if ESC is pressed
        self.connect('key-release-event', self.on_key_release)

        # Set window size
        self.set_geometry()

        # Set window icon
        icon_path = os.path.join(self.data_dir, "images", "antergos", "antergos-ball.png")
        self.set_icon_from_file(icon_path)

        # Use our css file
        if not self.apply_css():
            # Can't load Cnchi CSS - Error.
            sys.exit(-1)

        # Call prepare from first screen (so it can initialise itself)
        self.pages.prepare_current_page()

        # Show main window
        self.show_all()

        self.progressbar_step = 0
        self.gui["progressbar"].set_fraction(0)
        self.gui["progressbar"].hide()

        self.set_focus(None)

        misc.gtk_refresh()

    def header_for_all_callback(self, widget, data):
        """ Callback for all header elements. """
        if isinstance(widget, Gtk.Box):
            widget.forall(self.header_for_all_callback, self.tooltip_string)
            return

        # Show header tooltip
        if widget.get_style_context().has_class('title'):
            widget.set_tooltip_text(self.tooltip_string)

    def prepare_shared_parameters(self):
        """ Parameters that are common to all screens """

        self.params['main_window'] = self
        self.params['ui_dir'] = self.settings.get('ui')

        self.params['main_box_wrapper'] = self.gui["main_box_wrapper"]
        self.params['header'] = self.gui["header"]
        self.params['forward_button'] = self.gui["forward_button"]
        self.params['main_progressbar'] = self.gui["progressbar"]

        self.params['backwards_button'] = None
        self.params['callback_queue'] = self.callback_queue
        self.params['settings'] = self.settings
        self.params['process_list'] = self.process_list
        self.params['checks_are_optional'] = self.cmd_line.no_check
        self.params['disable_tryit'] = self.cmd_line.disable_tryit if not self.is_minimal else True
        self.params['disable_rank_mirrors'] = self.cmd_line.disable_rank_mirrors

    def apply_css(self):
        """ Loads css file and applies it to our gui """

        style_css = os.path.join(self.data_dir, "css", "gtk-style.css")

        loaded = False

        if os.path.exists(style_css):
            with open(style_css, 'rb') as css:
                css_data = css.read()

            style_provider = Gtk.CssProvider()
            try:
                style_provider.load_from_data(css_data)
                Gtk.StyleContext.add_provider_for_screen(
                    Gdk.Screen.get_default(),
                    style_provider,
                    Gtk.STYLE_PROVIDER_PRIORITY_USER)
                loaded = True
            except GLib.Error as err:
                logging.error("Error loading Cnchi CSS file: %s", err)
        else:
            logging.error("Can't find Cnchi CSS file")

        return loaded

    def load_gui_objects(self):
        """ Load all gui objects in self.gui """
        ui_dir = self.settings.get('ui')

        names = {
            "cnchi.ui": ["main", "main_box_wrapper", "main_box", "main_stack", "sub_nav_box"],
            "header.ui": ["header_overlay", "header", "header_nav", "language_button",
                "header_nav", "progressbar", "logo", "logo_text", "forward_button"]}

        files = ["cnchi.ui", "header.ui"]

        for filename in files:
            ui_path = os.path.join(ui_dir, filename)
            builder = Gtk.Builder()
            builder.add_from_file(ui_path)

            for name in names[filename]:
                self.gui[name] = builder.get_object(name)
            # Connect all ui signals
            builder.connect_signals(self)

    def initialize_gui(self):
        """ Initial setup of our UI elements. This must be called during __init__(). """

        self.load_gui_objects()

        self.add(self.gui["main"])

        self.gui["main_stack"].set_transition_type(Gtk.StackTransitionType.OVER_LEFT_RIGHT)
        self.gui["main_stack"].set_transition_duration(400)

        # Main progress bar (also in header)
        self.gui["progressbar"].set_name('process_progressbar')

        # Top left logo (in header)
        img_path = os.path.join(self.data_dir, "images", "antergos", "image10.png")
        if os.path.exists(img_path):
            self.gui["logo"].set_from_file(img_path)

        # Add all header elements to header_overlay
        self.gui["header_overlay"].add_overlay(self.gui["header"])
        self.gui["header_overlay"].add_overlay(self.gui["header_nav"])
        self.gui["header_overlay"].add_overlay(self.gui["progressbar"])
        self.gui["header_overlay"].set_overlay_pass_through(self.gui["header"], True)
        self.gui["header_overlay"].set_overlay_pass_through(self.gui["progressbar"], True)
        self.gui["header_overlay"].set_overlay_pass_through(self.gui["header_nav"], True)
        self.set_titlebar(self.gui["header_overlay"])

        # Set widget names so Gtk can use our css
        self.gui["header"].set_name("header")
        self.gui["logo"].set_name("logo")

        # Forward button (allows going to next screen)
        atk_set_image_description(self.gui["forward_button"], _("Next step"))
        self.gui["forward_button"].set_name('fwd_btn')
        self.gui["forward_button"].set_always_show_image(True)

        # title = "Cnchi {0}".format(info.CNCHI_VERSION)
        title = _("Cnchi Installer")
        self.set_title(title)
        self.gui["logo_text"].set_text(title)

        welcome_msg = _("Welcome To Antergos!")
        label = Gtk.Label.new()
        label.set_text(welcome_msg)
        # self.header.set_title(welcome_msg)
        self.gui["header"].set_custom_title(label)
        self.gui["header"].get_custom_title().get_style_context().add_class('cnchi_title')
        self.gui["header"].set_show_close_button(False)

    def set_window_size(self, size):
        res = size.split("x")
        try:
            width = int(res[0])
            height = int(res[1])
            if width >= 800 and width <= self._main_window_width:
                self._main_window_width = width
            else:
                logging.warning("User has given a wrong window width. Using default value instead.")
            if height >= 600 and height <= self._main_window_height:
                self._main_window_height = height
            else:
                logging.warning("User has given a wrong window height. Using default value instead.")
        except ValueError:
            logging.warning("User has given a wrong window size. Using defaults.")

    def set_geometry(self):
        """ Sets Cnchi window geometry """
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)
        self.set_size_request(self._main_window_width, self._main_window_height)
        self.set_default_size(self._main_window_width, self._main_window_height)
        # self.set_property('height_request', self._main_window_height)

        geom = Gdk.Geometry()
        geom.min_width = self._main_window_width
        geom.min_height = self._main_window_height
        geom.max_width = self._main_window_width
        geom.max_height = self._main_window_height
        geom.base_width = self._main_window_width
        geom.base_height = self._main_window_height
        geom.width_inc = 0
        geom.height_inc = 0

        self.set_geometry_hints(self, geom, Gdk.WindowHints.MAX_SIZE)

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

    def set_progressbar_step(self, add_value):
        new_value = self.gui["progressbar"].get_fraction() + add_value
        if new_value > 1:
            new_value = 1
        if new_value < 0:
            new_value = 0
        self.gui["progressbar"].set_fraction(new_value)
        if new_value > 0:
            self.gui["progressbar"].show()
        else:
            self.gui["progressbar"].hide()

    # ------------------------------------------------------------------------

    def on_header_nav_button_clicked(self, widget, data=None):
        logging.debug(data)

        if isinstance(data, dict):
            page_name = data.get('name', False)
        else:
            page_name = data

        if hasattr(self.current_stack, 'name'):
            curr_stack = self.current_stack.name
        else:
            curr_stack = None

        page = stack = None

        logging.debug({
            'page_name': page_name,
            'curr_page': self.pages.get_current_page_name(),
            'curr_stack': curr_stack})

        for stack in self.stacks:
            try:
                page = stack.get_child_by_name(page_name)
            except Exception as err:
                logging.debug(err)
            if page:
                break
        else:
            logging.warning('unable to find page in stacks')

        current_page = self.pages.get_current_page()
        if (not page or not page.can_show) and page_name != current_page.next_page:
            return

        logging.debug({'storing page': page})
        stored = current_page.store_values()

        if not stored:
            logging.warning('Unable to store page values: %s', stored)
            return

        if 'timezone' == current_page.name:
            self.gui["main_box_wrapper"].set_property('margin_top', 35)
        if 'welcome' != current_page.name:
            self.gui["header"].set_title('')
            current_page.nav_button.set_state_flags(Gtk.StateFlags.NORMAL, True)
        else:
            self.gui["main_box"].set_visible(False)
            self.gui["main_stack"].set_visible(True)
            self.current_stack = self.gui["main_stack"]
            self.current_stack.can_show = True
            self.current_stack.show_all()

        self.set_progressbar_step(self.progressbar_step)

        prev_page = current_page

        self.pages.set_current_page(page)

        if not isinstance(page, Page):
            self.gui["main_stack"].show_all()
            self.gui["main_stack"].set_visible_child_name(page_name)
            self.current_stack = self.pages.get_sub_page(page_name, 'group')
            self.current_stack.can_show = True
            self.handle_nav_buttons_state(page_name)

            # The sub-stack container itself is not a page. Let's proceed to
            # first page within the sub-stack (a non-top-level page)
            # page = self.pages[page_name][self.current_stack.next_page]
            page = self.pages.get_sub_page(page_name, self.current_stack.next_page)
            self.pages.set_current_page(page)

            self.prepare_sub_nav_buttons({'name': page.name,
                                          'group': page_name,
                                          'previous': page.prev_page,
                                          'nav_button': page.nav_button,
                                          'nav_button_box': page.nav_button_box})
        elif not page.in_group:
            self.current_stack = self.gui["main_stack"]
            self.handle_nav_buttons_state(page_name)
            self.gui["sub_nav_box"].hide()
        else:
            self.current_stack = stack

        page.prepare('forwards')
        page.can_show = True

        if page.name != self.current_stack.get_visible_child_name():
            self.current_stack.show_all()
            self.current_stack.set_visible_child_name(page.name)

        if 'slides' != page.name:
            page.nav_button.set_state_flags(Gtk.StateFlags.SELECTED, True)
            self.gui["header"].set_subtitle('')
        else:
            self.gui["header_nav"].hide()

    def prepare_sub_nav_buttons(self, data):
        page = data['name']
        group = data['group']
        prev = data.get('previous', None)
        curr_btns = self.gui["sub_nav_box"].get_children()
        noop = False
        logging.debug('curr_btns is: %s ', curr_btns)
        self.gui["sub_nav_box"].hide()

        if curr_btns and curr_btns[0] is not data['nav_button_box']:
            logging.debug('curr_btns is not btn_container')
            self.gui["sub_nav_box"].remove(curr_btns[0])
        elif curr_btns and curr_btns[0] is data['nav_button_box']:
            logging.debug('curr_btns is btn_container')
            noop = True

        if not noop:
            self.gui["sub_nav_box"].add(data['nav_button_box'])

        self.gui["sub_nav_box"].height_request = 43
        self.gui["sub_nav_box"].show_all()

    def on_forward_button_clicked(self, widget=None, data=None):
        """ Show next screen """

        curr_page_name = self.pages.get_current_page_name()
        next_page_name = self.pages.get_next_page()

        if not next_page_name:
            logging.warning('next_page_name required: %s', next_page_name)
            return

        if not self.pages.loaded():
            self.load_pages()
            self.progressbar_step = 1.0 / self.pages.get_page_count()

        self.on_header_nav_button_clicked(widget, next_page_name)

    def handle_nav_buttons_state(self, page_name):
        if self.nav_buttons.get('selected', False):
            self.nav_buttons['selected'].set_state_flags(Gtk.StateFlags.NORMAL, True)
        self.nav_buttons[page_name].set_state_flags(Gtk.StateFlags.SELECTED, True)
        self.nav_buttons['selected'] = self.nav_buttons[page_name]

    def load_pages(self):
        """ Load all remaining pages """

        top_level_pages = [
            'check', 'location_grp', 'desktop_grp', 'disk_grp', 'user_info', 'summary']

        # Load pages in our dict
        self.pages.load_all()

        # Prepare page stacks
        self.stacks.append(self.gui["main_stack"])

        diff = 2

        top_pages = self.pages.get_top_pages()
        sub_stacks = self.pages.get_sub_stacks()
        sub_pages = self.pages.get_sub_pages()
        self.all_pages = top_level_pages + sub_pages

        num_pages = len(top_pages) + len(sub_pages)

        self.page_count = num_pages - diff

        if num_pages > 0:
            self.progressbar_step = 1.0 / num_pages

        for page_name in top_level_pages:
            page = self.pages.get_page(page_name)
            if isinstance(page, dict):
                sub_stack = Stack(params=self.params,
                                              name=page_name,
                                              title=page['title'],
                                              prev_page=page['prev_page'],
                                              next_page=page['next_page'])

                sub_stack.get_style_context().add_class('sub_page')
                sub_stack.set_transition_type(Gtk.StackTransitionType.OVER_DOWN_UP)
                sub_stack.set_transition_duration(400)
                self.sub_nav_btns[page_name] = {
                    'box': Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
                }
                self.sub_nav_btns[page_name]['box'].set_halign(Gtk.Align.CENTER)
                self.sub_nav_btns[page_name]['box'].set_hexpand(True)

                for sub_page_name in page['pages']:
                    #sub_page = self.pages[page_name][sub_page_name]
                    sub_page = self.pages.get_sub_page(page_name, sub_page_name)
                    if sub_page:
                        sub_page.stack = sub_stack
                        sub_stack.add_titled(sub_page, sub_page_name, sub_page.title)
                        self.sub_nav_btns[page_name][sub_page_name] = Gtk.Button.new_with_label(
                                sub_page.title)
                        self.sub_nav_btns[page_name][sub_page_name].connect(
                                'clicked',
                                self.on_header_nav_button_clicked,
                                {'group_name': page_name, 'name': sub_page_name})
                        sub_page.nav_button = self.sub_nav_btns[page_name][sub_page_name]
                        self.sub_nav_btns[page_name]['box'].add(
                                self.sub_nav_btns[page_name][sub_page_name])
                        sub_page.nav_button_box = self.sub_nav_btns[page_name]['box']

                # self.pages[page_name]['group'] = page = sub_stack
                self.pages.set_sub_page(page_name, "group", sub_stack)
                page = sub_stack
                self.stacks.append(sub_stack)

            page.show_all()
            self.gui["main_stack"].add_titled(page, page_name, page.title)
            self.nav_buttons[page_name] = Gtk.Button.new_with_label(page.title)
            self.nav_buttons[page_name].connect(
                'clicked', self.on_header_nav_button_clicked, page_name)

            if isinstance(page, Page):
                page.stack = self.gui["main_stack"]

            page.nav_button = self.nav_buttons[page_name]

            self.gui["header_nav"].add(self.nav_buttons[page_name])

        self.nav_buttons['forward_button'] = self.gui["forward_button"]
        self.gui["header_nav"].add(self.nav_buttons['forward_button'])
        self.gui["header_nav"].child_set_property(self.nav_buttons['forward_button'], 'packing', 'end')
        self.gui["header_nav"].show_all()
        self.current_stack = self.gui["main_stack"]
        self.pages_loaded = True
