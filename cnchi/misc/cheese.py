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

from gi.repository import GtkClutter
GtkClutter.init([])

from gi.repository import Clutter, GObject, Gtk, Gst, GLib

from gi.repository import Cheese


class VideoBox(Gtk.Widget):
    __gtype_name__ = 'VideoBox'

    # __gsignals__ = {'location-changed': (GObject.SignalFlags.RUN_LAST, None, (object,))}

    def __init__(self, width=400, height=400):
        Gtk.Widget.__init__(self)

        self.set_size_request(width, height)

        self.stage = Clutter.Stage()
        self.stage.set_size(width, height)

        self.layout_manager = Clutter.BoxLayout()
        self.textures_box = Clutter.Actor(layout_manager=self.layout_manager)
        self.stage.add_actor(self.textures_box)

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
            Cheese.Camera.setup(self.camera, None)
        except GLib.GError as error:
            logging.warning(error)
            return

        Cheese.Camera.play(self.camera)

        def added(signal, data):
            uuid=data.get_uuid()
            node=data.get_device_node()
            print("uuid is ", str(uuid))
            print("node is ", str(node))
            self.camera.set_device_by_device_node(node)
            self.camera.switch_camera_device()

        device_monitor = Cheese.CameraDeviceMonitor.new()
        device_monitor.connect("added", added)
        device_monitor.coldplug()

        # self.stage.show()
        # Clutter.main()

if __name__ == "__main__":
    # Gst.init(None)
    # Clutter.init(sys.argv)
    # app = VideoBox()

    # GtkClutter.init(ref args);

    win = Gtk.Window()
    video_box = VideoBox()
    win.add(video_box)
    win.show_all()

    import signal    # enable Ctrl-C since there is no menu to quit
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()





'''
from gi.repository import GtkClutter
GtkClutter.init([])
from gi.repository import Clutter, Gtk, Gdk

GtkClutter.init([])

class MyCanvas(GtkClutter.Embed):
    __gtype_name__ = 'MyCanvas'

    def __init__(self):
        super(MyCanvas, self).__init__()

        self.stage = self.get_stage()

        self.rect = MyRect()
        self.stage.connect('key-press-event', self.key_press) # This Works!
        self.stage.add_actor(self.rect)
        self.rect.set_position(10, 10)

        self.show_all()

    def key_press(self, widget, event):
        print widget, event


class MyRect(Clutter.Rectangle):
    __gtype_name__ = 'MyRect'

    def __init__(self):
        super(MyRect, self).__init__()
        self.set_color(Clutter.Color.new(255, 255, 255, 0))
        self.set_border_color(Clutter.Color.new(255, 255, 255, 255))
        self.set_border_width(1)
        self.set_size(200, 200)

        self.set_reactive(True)

    # None of the following callbacks work
    # Not even if I explicitly connect signals like 
    # self.connect('button-press-event', self.on_button_press)

    def do_button_press_event(self, event):
        print event

    def do_motion_event(self, event):
        print event


class MyWindow(Gtk.Window):
    __gtype_name__ = 'MyWindow'

    def __init__(self):
        super(MyWindow, self).__init__()
        self.canvas = AnnotateCanvas()
        self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON1_MOTION_MASK)
        self.set_size_request(500, 500)

        vbox_main = Gtk.VBox()
        scrolledwin = Gtk.ScrolledWindow()
        scrolledwin.add_with_viewport(self.canvas)
        vbox_main.pack_end(scrolledwin, True, True, 0)
        self.add(vbox_main)

    def run(self):
        self.show_all()
        self.loop = GObject.MainLoop()
        self.loop.run()


app = MyWindow()
app.run()'''

