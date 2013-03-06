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

from config import installer_settings

import logging
import queue

_show_event_queue_messages = True

def fatal_error(message):
    # Remove /tmp/.setup-running
    p = "/tmp/.setup-running"
    if os.path.exists(p):
        os.remove(p)
    error(message)
    sys.exit(1)

def error(message):
    print(message)
    logging.error(message)
    msg_dialog = Gtk.MessageDialog(None,\
        Gtk.DialogFlags.MODAL,\
        Gtk.MessageType.ERROR,\
        Gtk.ButtonsType.CLOSE,\
        _("Cinnarch Installer - Error"))
    msg_dialog.format_secondary_text(message)
    msg_dialog.run()
    msg_dialog.destroy()

def warning(message):
    print(message)
    logging.error(message)
    msg_dialog = Gtk.MessageDialog(None,\
        Gtk.DialogFlags.MODAL,\
        Gtk.MessageType.WARNING,\
        Gtk.ButtonsType.CLOSE,\
        _("Cinnarch Installer - Warning"))
    msg_dialog.format_secondary_text(message)
    msg_dialog.run()
    msg_dialog.destroy()

def message(message):
    print(message)
    logging.info(message)
    msg_dialog = Gtk.MessageDialog(None,\
        Gtk.DialogFlags.MODAL,\
        Gtk.MessageType.INFO,\
        Gtk.ButtonsType.YES_NO,\
        _("Cinnarch Installer - Information"))
    msg_dialog.format_secondary_text(message)
    msg_dialog.run()
    msg_dialog.destroy()

def question(message):
    print(message)
    logging.info(message)
    msg_dialog = Gtk.MessageDialog(None,\
        Gtk.DialogFlags.MODAL,\
        Gtk.MessageType.QUESTION,\
        Gtk.ButtonsType.YES_NO,\
        _("Cinnarch Installer - Question"))
    msg_dialog.format_secondary_text(message)
    response = msg_dialog.run()
    msg_dialog.destroy()
    return response

def event_from_callback_queue(event_queue):
    if _show_event_queue_messages:
        try:
            event = event_queue.get_nowait()
        except queue.Empty:
            event = ()
        
        if len(event) > 0:
            queue_event(event)
        return True
    else:
        return False

def queue_event(event):
    install_ok = _("Installation finished!")

    if len(event) > 0:
        if event[0] == "debug":
            print(event[1])
            logging.info(event[1])
        elif event[0] == "info":
            print(event[1])
            logging.info(event[1])
        elif event[0] == "warning":
            print(event[1])
            logging.info(event[1])
        elif event[0] == "action":
            print(event[1])
            logging.info(event[1])
        elif event[0] == "icon":
            print(event[1])
            logging.info(event[1])
        elif event[0] == "target":
            print(event[1])
            logging.info(event[1])
        elif event[0] == "percent":
            # do not log percent
            pass
            #print(event[1])
            #logging.info(event[1])
        elif event[0] == "finished":
            logging.info(install_ok)
            print(install_ok)
        elif event[0] == "error":
            logging.error(event[1])
            fatal_error(event[1])
            return False
    
    return True
