#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# _test_page.py
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


""" Test page (simulates main window to test a ui page) """

import sys
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


def get_page(page_name, params):
    """ Import page code so we can execute it """
    page = None

    if page_name == "desktop":
        import pages.desktop as desktop
        page = desktop.DesktopAsk(params)
    elif page_name == "check":
        import pages.check as check
        page = check.Check(params)
    elif page_name == "timezone":
        import pages.timezone as timezone
        page = timezone.Timezone(params)
        params['settings'].set('timezone_start', True)
    elif page_name == "wireless":
        import pages.wireless as wireless
        page = wireless.Wireless(params)
    elif page_name == "welcome":
        import pages.welcome as welcome
        page = welcome.Welcome(params)
    elif page_name == "user_info":
        import pages.user_info as user_info
        page = user_info.UserInfo(params)
    elif page_name == "location":
        import pages.location as location
        page = location.Location(params)
    elif page_name == "language":
        import pages.language as language
        page = language.Language(params)
    elif page_name == "keymap":
        import pages.keymap as keymap
        page = keymap.Keymap(params)
    elif page_name == "features":
        import pages.features as features
        page = features.Features(params)
    elif page_name == "summary":
        import pages.summary as summary
        page = summary.Summary(params)
    elif page_name == "slides":
        import pages.slides as slides
        page = slides.Slides(params)
    elif page_name == "ask":
        import pages.ask as ask
        page = ask.InstallationAsk(params)
    elif page_name == "advanced":
        import pages.advanced as advanced
        page = advanced.InstallationAdvanced(params)
    elif page_name == "alongside":
        import pages.alongside as alongside
        page = alongside.InstallationAlongside(params)
    elif page_name == "automatic":
        import pages.automatic as automatic
        page = automatic.InstallationAutomatic(params)
    elif page_name == "zfs":
        import pages.zfs as zfs
        page = zfs.InstallationZFS(params)
    elif page_name == "mirrors":
        import pages.mirrors as mirrors
        page = mirrors.Mirrors(params)
    elif page_name == "cache":
        import pages.cache as cache
        page = cache.Cache(params)
    return page


def run(page_name):
    """ Run page to be able to test it """

    window = Gtk.Window()
    window.connect('destroy', Gtk.main_quit)
    # window.set_size_request(600, 500)
    window.set_border_width(0)
    window.set_title("Cnchi - Test of {0} page".format(page_name))

    import logging

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '[%(asctime)s] [%(module)s] %(levelname)s: %(message)s',
        "%Y-%m-%d %H:%M:%S")
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Use our css file
    style_provider = Gtk.CssProvider()

    style_css = "/usr/share/cnchi/data/css/gtk-style.css"
    if os.path.exists(style_css):
        with open(style_css, 'rb') as css:
            css_data = css.read()

        style_provider.load_from_data(css_data)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )
    else:
        logging.warning("Cannot load CSS data")

    import config

    settings = config.Settings()
    settings.set('data', '/usr/share/cnchi/data')

    from desktop_info import DESKTOPS

    settings.set('desktops', DESKTOPS)
    settings.set('language_code', 'ca')

    settings.set('main_window', None)

    params = {
        'a11y': False,
        'title': "Cnchi",
        'main_window': window,
        'ui_dir': "/usr/share/cnchi/ui",
        'disable_tryit': False,
        'settings': settings,
        'forward_button': Gtk.Button.new(),
        'backwards_button': Gtk.Button.new(),
        'main_progressbar': Gtk.ProgressBar.new(),
        'header': Gtk.HeaderBar.new(),
        'callback_queue': None,
        'alternate_package_list': "",
        'process_list': []}

    page = get_page(page_name, params)

    if page is not None:
        # page.set_property("halign", Gtk.Align.CENTER)
        window.add(page)
        window.show_all()
        page.prepare('forward')
        Gtk.main()
    else:
        print("Unknown page")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python test_page.py [page_name]")
    else:
        TEST_PAGE = sys.argv[1]
        if TEST_PAGE.endswith('.py'):
            TEST_PAGE = TEST_PAGE[:-3]
        run(TEST_PAGE)
