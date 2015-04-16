









# Code by Christian Schaller

import sys
from gi.repository import Gtk
from gi.repository import Cheese
from gi.repository import Clutter
from gi.repository import Gst
Gst.init(None)
Clutter.init(sys.argv)

class VideoBox():
   def __init__(self):
    self.stage = Clutter.Stage()
    self.stage.set_size(400, 400)
    self.layout_manager = Clutter.BoxLayout()
    self.textures_box = Clutter.Actor(layout_manager=self.layout_manager)
    self.stage.add_actor(self.textures_box)

    self.video_texture = Clutter.Texture.new()

    self.video_texture.set_keep_aspect_ratio(True)
    self.video_texture.set_size(400,400)
    self.layout_manager.pack(self.video_texture, expand=False, x_fill=False, y_fill=False, x_align=Clutter.BoxAlignment.CENTER, y_align=Clutter.BoxAlignment.CENTER)

    self.camera = Cheese.Camera.new(self.video_texture, None, 100, 100)
    Cheese.Camera.setup(self.camera, None)
    Cheese.Camera.play(self.camera)

    def added(signal, data):
        uuid=data.get_uuid()
        node=data.get_device_node()
        print "uuid is " +str(uuid)
        print "node is " +str(node)
        self.camera.set_device_by_device_node(node)
        self.camera.switch_camera_device()

    device_monitor=Cheese.CameraDeviceMonitor.new()
    device_monitor.connect("added", added)
    device_monitor.coldplug()

    self.stage.show()
    Clutter.main()
if __name__ == "__main__":
    app = VideoBox()



