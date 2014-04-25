#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_screen.py
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

""" Test screen (simulates main window to test a ui screen) """

from gi.repository import Gtk, GLib

def _(message): return message

def get_screen(screen_name, params):
    screen = None
    if screen_name == "DesktopAsk":
        import desktop
        screen = desktop.DesktopAsk(params)
    elif screen_name == "Check":
        import check
        screen = check.Check(params)
    elif screen_name == "Timezone":
        import timezone
        screen = timezone.Timezone(params)
    elif screen_name == "Wireless":
        import wireless
        screen = wireless.Wireless(params)
    elif screen_name == "Welcome":
        import welcome
        screen = welcome.Welcome(params)
    elif screen_name == "UserInfo":
        import user_info
        screen = user_info.UserInfo(params)
    elif screen_name == "Location":
        import location
        screen = location.Location(params)
    elif screen_name == "Language":
        import language
        screen = language.Language(params)
    elif screen_name == "Keymap":
        import keymap
        screen = keymap.Keymap(params)
    elif screen_name == "Features":
        import features
        screen = features.Features(params)
    elif screen_name == "Slides":
        import slides
        screen = slides.Slides(params)
    elif screen_name == "InstallationAsk":
        import ask
        screen = ask.InstallationAsk(params)
    elif screen_name == "InstallationAdvanced":
        import advanced
        screen = advanced.InstallationAdvanced(params)
    elif screen_name == "InstallationAlongside":
        import alongside
        screen = alongside.InstallationAlongside(params)
    elif screen_name == "InstallationAutomatic":
        import automatic
        screen = automatic.InstallationAutomatic(params)
    return screen

def run(screen_name):
    window = Gtk.Window()
    window.connect('destroy', Gtk.main_quit)
    #window.set_size_request(600, 500)
    window.set_border_width(12)
    window.set_title("Cnchi - Test of %s screen" % screen_name)

    import config
    settings = config.Settings()
    settings.set('data', '/usr/share/cnchi/data')
    from desktop_environments import DESKTOPS
    settings.set('desktops', DESKTOPS)

    params = {}
    params['title'] = "Cnchi"
    params['ui_dir'] = "/usr/share/cnchi/ui"
    params['disable_tryit'] = False
    params['settings'] = settings
    params['forward_button'] = Gtk.Button.new()
    params['backwards_button'] = Gtk.Button.new()
    params['main_progressbar'] = Gtk.ProgressBar.new()
    params['header'] = Gtk.HeaderBar.new()
    params['testing'] = True
    params['callback_queue'] = None
    params['alternate_package_list'] = ""
    screen = get_screen(screen_name, params)
    if screen != None:
        screen.prepare('forward')
        window.add(screen)
        window.show_all()
        Gtk.main()
    else:
        print("Unknown screen")
