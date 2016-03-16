#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pages.py
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

""" Manage Cnchi pages """


import logging

import check
import desktop
import features
import keymap
import location
import slides
import summary
import timezone
import user_info
import welcome

from installation import (
    ask as installation_ask,
    automatic as installation_automatic,
    alongside as installation_alongside,
    advanced as installation_advanced,
    zfs as installation_zfs
)


class Pages():
    def __init__(self, params):
        self.current_stack = None
        self.current_grp = None
        self.current_page = None

        self.next_page = None
        self.prev_page = None
        self.page_count = 0
        self.all_pages = []

        self.pages_loaded = False

        self.stacks = []
        self.top_level_pages = []
        self.pages = {}

        self.params = params

    def get_page_count(self):
        return self.page_count

    def loaded(self):
        return self.pages_loaded

    def prepare_current_page(self):
        if self.current_page:
            self.current_page.prepare('forwards')

    def get_current_page(self):
        return self.current_page

    def get_current_page_name(self):
        if self.current_page:
            return self.current_page.name
        else:
            return None

    def get_next_page(self):
        if self.current_page:
            return self.current_page.get_next_page()
        else:
            return None

    def get_current_stack(self):
        return self.current_stack

    def pre_load_pages(self):
        """ Just load the first two screens (the other ones will be loaded later)
        We do this to reduce Cnchi's initial startup time. """
        self.pages = dict()
        self.pages["location_grp"] = {'title': 'Location',
                                      'prev_page': 'check',
                                      'next_page': 'location',
                                      'pages': ['location', 'timezone', 'keymap']}
        self.pages["check"] = check.Check(self.params, cnchi_main=self)
        self.pages["check"].prepare('forwards', show=False)
        self.pages["welcome"] = welcome.Welcome(self.params)
        self.current_page = self.pages["welcome"]

    def load_pages(self):
        """ Load all remaining pages """

        self.top_level_pages = ['check', 'location_grp', 'desktop_grp',
                                'disk_grp', 'user_info', 'summary']

        # Load pages in our dict
        self.initialize_pages_dict()

        # Prepare page stacks
        self.stacks.append(self.main_stack)

        diff = 2

        top_pages = [p for p in self.pages if not isinstance(self.pages[p], dict)]
        sub_stacks = [self.pages[p]['pages'] for p in self.pages if p not in top_pages]
        sub_pages = [p for x in sub_stacks for p in x]
        self.all_pages = self.top_level_pages + sub_pages

        num_pages = len(top_pages) + len(sub_pages)

        self.page_count = num_pages - diff

        if num_pages > 0:
            self.progressbar_step = 1.0 / num_pages

        for page_name in self.top_level_pages:
            page = self.pages[page_name]
            if isinstance(page, dict):
                sub_stack = substack.SubStack(params=self.params,
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
                    sub_page = self.pages[page_name][sub_page_name]
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

                self.pages[page_name]['group'] = page = sub_stack
                self.stacks.append(sub_stack)

            page.show_all()
            self.main_stack.add_titled(page, page_name, page.title)
            self.nav_buttons[page_name] = Gtk.Button.new_with_label(page.title)
            self.nav_buttons[page_name].connect('clicked',
                                                self.on_header_nav_button_clicked, page_name)

            if isinstance(page, gtkbasebox.GtkBaseBox):
                page.stack = self.main_stack

            page.nav_button = self.nav_buttons[page_name]

            self.header_nav.add(self.nav_buttons[page_name])

        self.nav_buttons['forward_button'] = self.forward_button
        self.header_nav.add(self.nav_buttons['forward_button'])
        self.header_nav.child_set_property(self.nav_buttons['forward_button'], 'packing', 'end')

        self.header_nav.show_all()
        self.current_stack = self.main_stack
        self.pages_loaded = True

    def initialize_pages_dict(self):
        """ Load pages """
        self.pages["location_grp"]["location"] = location.Location(params=self.params)
        if not self.pages["location_grp"].get('timezone', False):
            self.pages["location_grp"]["timezone"] = timezone.Timezone(params=self.params,
                                                                       cnchi_main=self)

        self.pages["desktop_grp"] = {'title': 'Desktop Selection',
                                     'prev_page': 'location_grp',
                                     'next_page': 'desktop',
                                     'pages': ['desktop', 'features']}

        if self.settings.get('desktop_ask') or True:
            self.pages["location_grp"]["keymap"] = keymap.Keymap(params=self.params, is_last=True)
            self.pages["desktop_grp"]["desktop"] = desktop.DesktopAsk(params=self.params)
            self.pages["desktop_grp"]["features"] = features.Features(params=self.params,
                                                                      is_last=True)
        else:
            self.pages["location_grp"]["keymap"] = keymap.Keymap(self.params, next_page='features',
                                                                 is_last=True)
            self.pages["desktop_grp"]["features"] = features.Features(self.params,
                                                                      prev_page='location_grp',
                                                                      is_last=True)

        self.pages["disk_grp"] = {'title': 'Disk Setup',
                                  'prev_page': 'desktop_grp',
                                  'next_page': 'installation_ask',
                                  'pages': ['installation_ask', 'installation_automatic',
                                            'installation_alongside', 'installation_advanced',
                                            'installation_zfs']}

        self.pages["disk_grp"]["installation_ask"] = \
            installation_ask.InstallationAsk(params=self.params)

        self.pages["disk_grp"]["installation_automatic"] = \
            installation_automatic.InstallationAutomatic(params=self.params, is_last=True)

        if self.settings.get("enable_alongside"):
            self.pages["disk_grp"]["installation_alongside"] = \
                installation_alongside.InstallationAlongside(params=self.params)
        else:
            self.pages["disk_grp"]["installation_alongside"] = None

        self.pages["disk_grp"]["installation_advanced"] = \
            installation_advanced.InstallationAdvanced(params=self.params, is_last=True)

        self.pages["disk_grp"]["installation_zfs"] = \
            installation_zfs.InstallationZFS(params=self.params, is_last=True)

        self.pages["user_info"] = user_info.UserInfo(params=self.params)
        self.pages["summary"] = summary.Summary(params=self.params)
        self.pages["slides"] = slides.Slides(params=self.params)
