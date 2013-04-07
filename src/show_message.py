#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  installation_advanced.py
#  
#  Copyright 2013 Cinnarch
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
#  
#  Cinnarch Team:
#   Alex Filgueira (faidoc) <alexfilgueira.cinnarch.com>
#   Raúl Granados (pollitux) <raulgranados.cinnarch.com>
#   Gustau Castells (karasu) <karasu.cinnarch.com>
#   Kirill Omelchenko (omelcheck) <omelchek.cinnarch.com>
#   Marc Miralles (arcnexus) <arcnexus.cinnarch.com>
#   Alex Skinner (skinner) <skinner.cinnarch.com>

from gi.repository import Gtk

import sys
import os
import queue
import log
import misc

_show_event_queue_messages = True

@misc.raise_privileges
def fatal_error(message):
    # Remove /tmp/.setup-running
    p = "/tmp/.setup-running"
    if os.path.exists(p):
        os.remove(p)
    error(message)
    sys.exit(1)

def error(message):
    log.debug(message)
    msg_dialog = Gtk.MessageDialog(None,\
        Gtk.DialogFlags.MODAL,\
        Gtk.MessageType.ERROR,\
        Gtk.ButtonsType.CLOSE,\
        _("Cinnarch Installer - Error"))
    msg_dialog.format_secondary_text(message)
    msg_dialog.run()
    msg_dialog.destroy()

def warning(message):
    log.debug(message)
    msg_dialog = Gtk.MessageDialog(None,\
        Gtk.DialogFlags.MODAL,\
        Gtk.MessageType.WARNING,\
        Gtk.ButtonsType.CLOSE,\
        _("Cinnarch Installer - Warning"))
    msg_dialog.format_secondary_text(message)
    msg_dialog.run()
    msg_dialog.destroy()

def message(message):
    log.debug(message)
    msg_dialog = Gtk.MessageDialog(None,\
        Gtk.DialogFlags.MODAL,\
        Gtk.MessageType.INFO,\
        Gtk.ButtonsType.CLOSE,\
        _("Cinnarch Installer - Information"))
    msg_dialog.format_secondary_text(message)
    msg_dialog.run()

def question(message):
    log.debug(message)
    msg_dialog = Gtk.MessageDialog(None,\
        Gtk.DialogFlags.MODAL,\
        Gtk.MessageType.QUESTION,\
        Gtk.ButtonsType.YES_NO,\
        _("Cinnarch Installer - Question"))
    msg_dialog.format_secondary_text(message)
    response = msg_dialog.run()
    msg_dialog.destroy()
    return response
