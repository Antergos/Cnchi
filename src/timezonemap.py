#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  timezonemap.py
#
#  Portions from Ubiquity, Copyright (C) 2009 Canonical Ltd.
#  Written in C by Evan Dandrea <evand@ubuntu.com>
#  Python code Copyright © 2013,2014 Antergos
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

""" Custom widget to show world time zones """

from gi.repository import GObject, Gdk, Gtk, GdkPixbuf, cairo, Pango, PangoCairo
import canonical.tz as tz

import os
import math
import sys

PIN_HOT_POINT_X = 8
PIN_HOT_POINT_Y = 15
LOCATION_CHANGED = 0

G_PI_4 = 0.78539816339744830961566084581987572104929234984378

TIMEZONEMAP_IMAGES_PATH = "/usr/share/cnchi/data/images/timezonemap"

# color_codes is (offset, red, green, blue, alpha)
color_codes = [
    (-11.0, 43, 0, 0, 255),
    (-10.0, 85, 0, 0, 255),
    (-9.5, 102, 255, 0, 255),
    (-9.0, 128, 0, 0, 255),
    (-8.0, 170, 0, 0, 255),
    (-7.0, 212, 0, 0, 255),
    (-6.0, 255, 0, 1, 255), # north
    (-6.0, 255, 0, 0, 255), # south
    (-5.0, 255, 42, 42, 255),
    (-4.5, 192, 255, 0, 255),
    (-4.0, 255, 85, 85, 255),
    (-3.5, 0, 255, 0, 255),
    (-3.0, 255, 128, 128, 255),
    (-2.0, 255, 170, 170, 255),
    (-1.0, 255, 213, 213, 255),
    (0.0, 43, 17, 0, 255),
    (1.0, 85, 34, 0, 255),
    (2.0, 128, 51, 0, 255),
    (3.0, 170, 68, 0, 255),
    (3.5, 0, 255, 102, 255),
    (4.0, 212, 85, 0, 255),
    (4.5, 0, 204, 255, 255),
    (5.0, 255, 102, 0, 255),
    (5.5, 0, 102, 255, 255),
    (5.75, 0, 238, 207, 247),
    (6.0, 255, 127, 42, 255),
    (6.5, 204, 0, 254, 254),
    (7.0, 255, 153, 85, 255),
    (8.0, 255, 179, 128, 255),
    (9.0, 255, 204, 170, 255),
    (9.5, 170, 0, 68, 250),
    (10.0, 255, 230, 213, 255),
    (10.5, 212, 124, 21, 250),
    (11.0, 212, 170, 0, 255),
    (11.5, 249, 25, 87, 253),
    (12.0, 255, 204, 0, 255),
    (12.75, 254, 74, 100, 248),
    (13.0, 255, 85, 153, 250)]

def radians(degrees):
    return (degrees / 360.0) * math.pi * 2

def convert_longitude_to_x(longitude, map_width):
    xdeg_offset = -6
    return (map_width * (180.0 + longitude) / 360.0) + (map_width * xdeg_offset / 180.0)

def convert_latitude_to_y(latitude, map_height):
    bottom_lat = -59;
    top_lat = 81;

    top_per = top_lat / 180.0;
    y = 1.25 * math.log(math.tan(G_PI_4 + 0.4 * radians(latitude)))
    full_range = 4.6068250867599998
    top_offset = full_range * top_per
    map_range = math.fabs(1.25 * math.log(math.tan(G_PI_4 + 0.4 * radians(bottom_lat))) - top_offset)
    y = math.fabs(y - top_offset)
    y = y / map_range
    y = y * map_height
    return y

def clamp(x, min_value, max_value):
    if x < min_value:
        x = min_value
    elif x > max_value:
        x = max_value
    return x

# TODO: Add signal location-changed
# TODO: add set_timezone function
# TODO: add get_timezone_at_coords function

class Timezonemap(Gtk.Widget):
    __gtype_name__ = 'Timezonemap'

    __gsignals__ = { 'location-changed' : (GObject.SignalFlags.RUN_LAST, None, (object,)) }
    
    def __init__(self):
        #super().__init__(self)
        Gtk.Widget.__init__(self)

        self.set_size_request(40, 40)

        self._background = None
        self._color_map = None
        self._visible_map_pixels = None
        self._visible_map_rowstride = None
        self._selected_offset = 0

        self._tz_location = None

        self._bubble_text = "This is a test!"

        try:
            self._orig_background = GdkPixbuf.Pixbuf.new_from_file(
                os.path.join(TIMEZONEMAP_IMAGES_PATH, "bg.png"))

            self._orig_background_dim = GdkPixbuf.Pixbuf.new_from_file(
                os.path.join(TIMEZONEMAP_IMAGES_PATH, "bg_dim.png"))

            self._orig_color_map = GdkPixbuf.Pixbuf.new_from_file(
                os.path.join(TIMEZONEMAP_IMAGES_PATH, "cc.png"))

            self._pin = GdkPixbuf.Pixbuf.new_from_file(
                os.path.join(TIMEZONEMAP_IMAGES_PATH, "pin.png"))
        except Exception as err:
            print(err)
            sys.exit(1)

        self._tzdb = tz.Database()
        

    def do_get_preferred_width(self):
        """ Retrieves a widget’s initial minimum and natural width. """
        width = self._orig_background.get_width()
        return (width, width)

    def do_get_preferred_height(self):
        """ Retrieves a widget’s initial minimum and natural height. """
        height = self._orig_background.get_height()
        return (height, height)

    def do_size_allocate(self, allocation):
        """ The do_size_allocate is called by when the actual size is known
         and the widget is told how much space could actually be allocated """
        self.set_allocation(allocation)

        if self._background is not None:
            del self._background
            self._background = None

        if self.is_sensitive():
            self._background = self._orig_background.scale_simple(
                allocation.width,
                allocation.height,
                GdkPixbuf.InterpType.BILINEAR)
        else:
            self._background = self._orig_background_dim.scale_simple(
                allocation.width,
                allocation.height,
                GdkPixbuf.InterpType.BILINEAR)

        if self._color_map is not None:
            del self._color_map
            self._color_map = None

        self._color_map = self._orig_color_map.scale_simple(
            allocation.width,
            allocation.height,
            GdkPixbuf.InterpType.BILINEAR)

        self._visible_map_pixels = self._color_map.get_pixels()
        self._visible_map_rowstride = self._color_map.get_rowstride()

        if self.get_realized():
            self.get_window().move_resize(
            allocation.x,
            allocation.y,
            allocation.width,
            allocation.height)

    def do_realize(self):
        """ Called when the widget should create all of its
        windowing resources.  We will create our window here """
        self.set_realized(True)
        allocation = self.get_allocation()
        attr = Gdk.WindowAttr()
        attr.window_type = Gdk.WindowType.CHILD
        # GDK_INPUT_OUTPUT
        attr.wclass = Gdk.WindowWindowClass.INPUT_OUTPUT
        attr.width = allocation.width
        attr.height = allocation.height
        attr.x = allocation.x
        attr.y = allocation.y
        attr.visual = self.get_visual()
        attr.event_mask = self.get_events() | Gdk.EventMask.EXPOSURE_MASK | Gdk.EventMask.BUTTON_PRESS_MASK
        wat = Gdk.WindowAttributesType
        mask = wat.X | wat.Y | wat.VISUAL
        window = Gdk.Window(self.get_parent_window(), attr, mask)
        # Associate the gdk.Window with ourselves,
        # Gtk+ needs a reference between the widget and the gdk window
        window.set_user_data(self)
        self.set_window(window)

    # http://lotsofexpression.blogspot.com.es/2012/04/python-gtk-3-pango-cairo-example.html
    def draw_text_bubble(self, cr, pointx, pointy):
        corner_radius = 9.0
        margin_top = 12.0
        margin_bottom = 12.0
        margin_left = 24.0
        margin_right = 24.0

        if len(self._bubble_text) <= 0:
            return

        alloc = self.get_allocation()

        layout = PangoCairo.create_layout(cr)

        layout.set_alignment(Pango.Alignment.CENTER)
        layout.set_spacing(3)
        layout.set_markup(self._bubble_text)
        (ink_rect, logical_rect) = layout.get_pixel_extents()

        # Calculate the bubble size based on the text layout size
        width = logical_rect.width + margin_left + margin_right
        height = logical_rect.height + margin_top + margin_bottom

        if pointx < alloc.width / 2:
            x = pointx + 25
        else:
            x = pointx - width - 25

        y = pointy - height / 2

        # Make sure it fits in the visible area
        x = clamp(x, 0, alloc.width - width)
        y = clamp(y, 0, alloc.height - height)

        cr.save()
        cr.translate(x, y)

        # Draw the bubble
        cr.new_sub_path()
        cr.arc(width - corner_radius, corner_radius, corner_radius, radians(-90), radians(0))
        cr.arc(width - corner_radius, height - corner_radius, corner_radius, radians(0), radians(90))
        cr.arc(corner_radius, height - corner_radius, corner_radius, radians(90), radians(180))
        cr.arc(corner_radius, corner_radius, corner_radius, radians(180), radians(270))

        cr.close_path()

        cr.set_source_rgba(0.2, 0.2, 0.2, 0.7)
        cr.fill()

        # And finally draw the text
        cr.set_source_rgb(1, 1, 1)
        cr.move_to(margin_left, margin_top)
        PangoCairo.show_layout(cr, layout)
        cr.restore()

    def do_draw(self, cr):
        alloc = self.get_allocation()

        # Paint background
        if self._background is not None:
            Gdk.cairo_set_source_pixbuf(cr, self._background, 0, 0)
            cr.paint()

        # Paint hilight
        if self.is_sensitive():
            filename = "timezone_%g.png" % self._selected_offset
        else:
            filename = "timezone_%g_dim.png" % self._selected_offset
        
        print(filename)

        try:
            path = os.path.join(TIMEZONEMAP_IMAGES_PATH, filename)
            orig_hilight = GdkPixbuf.Pixbuf.new_from_file(path)
        except Exception as err:
            print("Can't load %s image file" % path)
            return

        hilight = orig_hilight.scale_simple(
            alloc.width,
            alloc.height,
            GdkPixbuf.InterpType.BILINEAR)

        Gdk.cairo_set_source_pixbuf(cr, hilight, 0, 0)
        cr.paint()

        del hilight
        del orig_hilight

        if self._tz_location:
            longitude = self._tz_location.get_longitude()
            latitude = self._tz_location.get_latitude()

            pointx = convert_longitude_to_x(longitude, alloc.width)
            pointy = convert_latitude_to_y(latitude, alloc.height)

            pointx = clamp(math.floor(pointx), 0, alloc.width)
            pointy = clamp(math.floor(pointy), 0, alloc.height)

            self.draw_text_bubble(cr, pointx, pointy)

            if self._pin is not None:
                Gdk.cairo_set_source_pixbuf(
                    cr,
                    self._pin,
                    pointx - PIN_HOT_POINT_X,
                    pointy - PIN_HOT_POINT_Y)
                cr.paint()

    def set_location(self, tz_location):
        if tz_location is not None:
            self._tz_location = tz_location
            
            info = self._tz_location.get_info()

            if info.get_daylight():
                daylight = -1.0
            else:
                daylight = 0.0

            self._selected_offset = tz_location.get_utc_offset().total_seconds() / (60.0 * 60.0) + daylight

            self.emit("location-changed", self._tz_location)

    def do_button_press_event(self, event):
        """ The button press event virtual method """

        # Make sure it was the first button
        if event.button == 1:
            x = event.x
            y = event.y
            rowstride = self._visible_map_rowstride
            pixels = self._visible_map_pixels
            my_red = pixels[int(rowstride * y + x * 4)]
            my_green = pixels[int(rowstride * y + x * 4) + 1]
            my_blue = pixels[int(rowstride * y + x * 4) + 2]
            my_alpha = pixels[int(rowstride * y + x * 4) + 3]

            for color_code in color_codes:
                (offset, red, green, blue, alpha) = color_code
                if red == my_red and green == my_green and blue == my_blue and alpha == my_alpha:
                    self._selected_offset = offset
                    break
            
            self.queue_draw()
            
            # work out the co-ordinates
            allocation = self.get_allocation()
            
            distances = []
            
            nearest_tz_location = None
            small_dist = 100

            for tz_location in self._tzdb.get_locations():
                longitude = tz_location.get_longitude()
                latitude = tz_location.get_latitude()

                pointx = convert_longitude_to_x(longitude, allocation.width)
                pointy = convert_latitude_to_y(latitude, allocation.height)

                dx = pointx - x;
                dy = pointy - y;
                
                dist = dx * dx + dy * dy
                
                if dist < small_dist:
                    nearest_tz_location = tz_location
                    small_dist = dist
            
            self.set_location(nearest_tz_location)

        return True

    def set_timezone(self, timezone):
        real_tz = self._tzdb.get_loc(timezone)
        
        if len(real_tz) > 0:
            tz_to_compare = real_tz
        else:
            tz_to_compare = timezone

        ret = False

        for tz_location in self._tzdb.get_locations():
            if tz_location.get_zone() == tz_to_compare:
                self.set_location(tz_location)
                ret = True
                break
        
        if ret is True:
            self.queue_draw()
        
        return ret

    def set_bubble_text(self, text):
        self.bubble_text = text
        Gtk.Widget.queue_draw(self)
    
    def get_location(self):
        return self._tz_location

if __name__ == '__main__':
    win = Gtk.Window()
    win.add(Timezonemap())
    win.show_all()
    import signal    # enable Ctrl-C since there is no menu to quit
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()
