#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cheese.py
#
#  Based on code by Christian Schaller
#  Copyright © 2013-2015 Antergos
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

import sys
import logging

import gi
gi.require_version('Gst', '1.0')

from gi.repository import GtkClutter
from gi.repository import Clutter, GObject, Gtk, Gst, GLib
from gi.repository import Cheese


def camera_box_init():
    Gst.init(None)
    GtkClutter.init([])

class CameraBox(GtkClutter.Embed):
    __gtype_name__ = 'VideoBox'

    # __gsignals__ = {'location-changed': (GObject.SignalFlags.RUN_LAST, None, (object,))}

    def __init__(self, width=400, height=400):
        GtkClutter.Embed.__init__(self)

        self.set_size_request(width, height)

        self.stage = self.get_stage()
        self.stage.set_size(width, height)

        self.layout_manager = Clutter.BoxLayout()
        self.container = Clutter.Actor(layout_manager=self.layout_manager)
        self.stage.add_actor(self.container)

        self.video_texture = Clutter.Texture.new()
        self.video_texture.set_keep_aspect_ratio(True)
        self.video_texture.set_size(width, height)
        
        self.layout_manager.pack(
            self.video_texture,
            expand=False,
            x_fill=False,
            y_fill=False,
            x_align=Clutter.BoxAlignment.CENTER,
            y_align=Clutter.BoxAlignment.CENTER)

        self.camera = Cheese.Camera.new(self.video_texture, None, 100, 100)
        
        try:
            self.camera.setup()
            self.camera_found = True
        except GLib.GError as error:
            logging.warning(error)
            self.camera_found = False
            return

    def on(self):
        if self.camera_found:
            self.camera.play()

            def added(signal, data):
                uuid = data.get_uuid()
                node = data.get_device_node()
                logging.debug("Camera uuid is %s", str(uuid))
                logging.debug("Camera node is %s", str(node))
                self.camera.set_device_by_device_node(node)
                self.camera.switch_camera_device()

            device_monitor = Cheese.CameraDeviceMonitor.new()
            device_monitor.connect("added", added)
            device_monitor.coldplug()

            self.stage.show()
    
    def stop(self):
        if self.camera_found:
            self.camera.stop()

    #def take_photo(self):
    #return self.camera.take_photo()


if __name__ == "__main__":
    camera_box_init()

    win = Gtk.Window()
    camera_box = CameraBox()
    win.add(camera_box)
    win.show_all()

    def exit_button(widget, data=None):
        sys.exit(0)

    win.connect('delete-event', exit_button)
    
    camera_box.on()

    import signal    # enable Ctrl-C since there is no menu to quit
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    Gtk.main()
