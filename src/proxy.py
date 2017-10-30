#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  proxy.py
#
#  Copyright © 2013-2017 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  The following additional terms are in effect as per Section 7 of the license:
#
#  The preservation of all legal notices and author attributions in
#  the material or in the Appropriate Legal Notices displayed
#  by works containing it is required.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; If not, see <http://www.gnu.org/licenses/>.

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os
import logging


def _(x): return x


class ProxyDialog(Gtk.Dialog):
    """ Asks user for proxy settings """

    def __init__(self, transient_for, proxies, use_same_proxy, ui_dir):
        Gtk.Dialog.__init__(self)

        self.set_transient_for(transient_for)
        self.ui_dir = ui_dir

        self.ui = Gtk.Builder()
        self.ui_file = os.path.join(self.ui_dir, "proxy.ui")
        self.ui.add_from_file(self.ui_file)

        self.translate_ui()

        self.setup_port_spin_buttons()

        self.add_button(Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)

        # Load values (if any)
        if proxies:
            self.set_proxies(proxies)

        # Connect UI signals
        switch = self.ui.get_object("use_same_proxy_switch")
        switch.connect("notify::active", self.on_use_same_proxy_activated)

        if use_same_proxy:
            switch.set_active(True)

        dialog_grid = self.ui.get_object("ProxyDialogGrid")
        content_area = self.get_content_area()
        content_area.add(dialog_grid)

    def on_use_same_proxy_activated(self, switch, data):
        widget_names = [
            "https_proxy_label", "ftp_proxy_label", "socks_proxy_label",
            "https_proxy_entry", "ftp_proxy_entry", "socks_proxy_entry",
            "https_proxy_port_label", "https_proxy_port_label",
            "ftp_proxy_port_label", "socks_proxy_port_label",
            "https_proxy_port",  "https_proxy_port", "ftp_proxy_port",
            "socks_proxy_port"]

        is_active = switch.get_active()

        for name in widget_names:
            w = self.ui.get_object(name)
            w.set_sensitive(not is_active)

    def setup_port_spin_buttons(self):
        spin_names = [
            "http_proxy_port", "https_proxy_port",
            "https_proxy_port", "ftp_proxy_port",
            "socks_proxy_port"]
        for name in spin_names:
            adjustment = Gtk.Adjustment(
                value=3128, lower=0, upper=65536, step_increment=1,
                page_increment=10, page_size=10)
            spin = self.ui.get_object(name)
            spin.set_adjustment(adjustment)
            spin.set_text("")

    def translate_ui(self):
        self.set_title(_("Cnchi - Internet Connection Proxy Setup"))

        label = self.ui.get_object("http_proxy_label")
        label.set_text(_("HTTP proxy server:"))
        label = self.ui.get_object("https_proxy_label")
        label.set_text(_("HTTPS proxy server:"))
        label = self.ui.get_object("ftp_proxy_label")
        label.set_text(_("FTP proxy server:"))
        label = self.ui.get_object("socks_proxy_label")
        label.set_text(_("SOCKS host server:"))
        label = self.ui.get_object("use_same_proxy_label")
        label.set_text(_("Use this proxy server for all protocols"))

        port_names = [
            "http_proxy_port_label", "https_proxy_port_label",
            "https_proxy_port_label", "ftp_proxy_port_label",
            "socks_proxy_port_label"]
        for name in port_names:
            label = self.ui.get_object(name)
            label.set_text(_("Port:"))

    def set_proxies(self, proxies):
        """ Set dialog proxies from proxies dict """
        if proxies:
            protocols = ["http", "https", "ftp", "socks"]
            for protocol in protocols:
                entry_id = protocol + "_proxy_entry"
                entry_widget = self.ui.get_object(entry_id)
                port_id = protocol + "_proxy_port"
                port_widget = self.ui.get_object(port_id)

                try:
                    proxy = proxies[protocol]
                    proxy = proxy.replace('https://', '')
                    proxy = proxy.replace('http://', '')

                    host = proxy.split(':')[0]
                    port = proxy.split(':')[1]

                    entry_widget.set_text(host)
                    port_widget.set_text(port)
                except (IndexError, KeyError) as err:
                    pass

    def get_use_same_proxy_for_all_protocols(self):
        switch = self.ui.get_object("use_same_proxy_switch")
        return switch.get_active()

    def get_proxies(self):
        """ Saves dialog proxies to proxies dict """
        proxies = {}

        protocols = ["http", "https", "ftp", "socks"]
        for protocol in protocols:
            entry_id = protocol + "_proxy_entry"
            port_id = protocol + "_proxy_port"

            entry_widget = self.ui.get_object(entry_id)
            host = entry_widget.get_text()
            port_widget = self.ui.get_object(port_id)
            port = port_widget.get_text()

            if host and port:
                if not host.startswith(protocol):
                    host = "http://" + host
                proxies[protocol] = host + ":" + port

        switch = self.ui.get_object("use_same_proxy_switch")
        if 'http' in proxies.keys():
            if switch.get_active():
                proxies['https'] = proxies['ftp'] = proxies['socks'] = proxies['http']
        else:
            switch.set_active(False)

        return proxies
