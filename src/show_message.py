#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  show_message.py
#
#  Copyright © 2013,2014 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

from gi.repository import Gtk

import sys
import os
import queue
import logging
import canonical.misc as misc
import multiprocessing

_show_event_queue_messages = True

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message): return message

def fatal_error(parent, message):
    # Remove /tmp/.setup-running
    p = "/tmp/.setup-running"
    if os.path.exists(p):
        os.remove(p)

    multiprocessing.active_children()

    error(parent, message)
    sys.exit(1)

def error(parent, message):
    message = str(message)
    logging.error(message)
    msg_dialog = Gtk.MessageDialog(transient_for=parent,
                                   modal=True,
                                   destroy_with_parent=True,
                                   message_type=Gtk.MessageType.ERROR,
                                   buttons=Gtk.ButtonsType.CLOSE,
                                   text=_("Antergos Installer - Error"))
    msg_dialog.format_secondary_text(message)
    msg_dialog.run()
    msg_dialog.destroy()

def warning(parent, message):
    message = str(message)
    logging.warning(message)
    msg_dialog = Gtk.MessageDialog(transient_for=parent,
                                   modal=True,
                                   destroy_with_parent=True,
                                   message_type=Gtk.MessageType.WARNING,
                                   buttons=Gtk.ButtonsType.CLOSE,
                                   text=_("Antergos Installer - Warning"))
    msg_dialog.format_secondary_text(message)
    msg_dialog.run()
    msg_dialog.destroy()

def message(parent, message):
    message = str(message)
    logging.info(message)
    msg_dialog = Gtk.MessageDialog(transient_for=parent,
                                   modal=True,
                                   destroy_with_parent=True,
                                   message_type=Gtk.MessageType.INFO,
                                   buttons=Gtk.ButtonsType.CLOSE,
                                   text=_("Antergos Installer - Information"))
    msg_dialog.format_secondary_text(message)
    msg_dialog.run()
    msg_dialog.destroy()

def question(parent, message):
    message = str(message)
    logging.info(message)
    msg_dialog = Gtk.MessageDialog(transient_for=parent,
                                   modal=True,
                                   destroy_with_parent=True,
                                   message_type=Gtk.MessageType.QUESTION,
                                   buttons=Gtk.ButtonsType.YES_NO,
                                   text=_("Antergos Installer - Confirmation"))
    msg_dialog.format_secondary_text(message)
    response = msg_dialog.run()
    msg_dialog.destroy()
    return response
