#!/usr/bin/python3

import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gst, Gtk

# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
gi.require_version('GstVideo', '1.0')
from gi.repository import GdkX11, GstVideo


class WebcamWidget(Gtk.DrawingArea):
    __gtype_name__ = 'WebcamWidget'
    def __init__(self, width=160, height=90):

        Gtk.DrawingArea.__init__(self)

        self.set_size_request(width, height)

        Gst.init(None)

        # Create GStreamer pipeline
        self.pipeline = Gst.Pipeline()

        # Create bus to get events from GStreamer pipeline
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::error', self.on_error)

        # This is needed to make the video output in our DrawingArea:
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message::element', self.on_sync_message)

        # Create GStreamer elements
        # gconfvideosrc
        self.src = Gst.ElementFactory.make('autovideosrc', None)
        self.sink = Gst.ElementFactory.make('autovideosink', None)

        fmt_str = 'video/x-raw, format=(string)YV12, '
        fmt_str += 'width=(int){0}, height=(int){1}, '.format(width, height)
        fmt_str += 'pixel-aspect-ratio=(fraction)1/1, '
        fmt_str += 'interlace-mode=(string)progressive, '
        fmt_str += 'framerate=(fraction){ 30/1, 24/1, 20/1, 15/1, 10/1, 15/2, 5/1 }'
        caps = Gst.caps_from_string(fmt_str)

        # Add elements to the pipeline
        self.pipeline.add(self.src)
        self.pipeline.add(self.sink)

        self.src.link_filtered(self.sink, caps)

        self.connect('destroy', self.on_destroy)

    def show_all(self):
        # You need to get the XID after window.show_all().  You shouldn't get it
        # in the on_sync_message() handler because threading issues will cause
        # segfaults there.
        self.xid = self.get_property('window').get_xid()
        self.pipeline.set_state(Gst.State.PLAYING)

    def on_destroy(self, data):
        self.pipeline.set_state(Gst.State.NULL)
        self.destroy()

    def on_sync_message(self, bus, msg):
        if msg.get_structure().get_name() == 'prepare-window-handle':
            # print('prepare-window-handle')
            msg.src.set_property('force-aspect-ratio', True)
            msg.src.set_window_handle(self.xid)

    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())


GObject.type_register(WebcamWidget)

if __name__ == '__main__':
    GObject.threads_init()
    Gst.init(None)
    window = Gtk.Window()
    webcam = WebcamWidget()
    window.add(webcam)
    webcam.run()
    Gtk.main()
