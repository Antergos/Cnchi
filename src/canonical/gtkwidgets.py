#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# Copyright (C) 2012 Canonical Ltd.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import cairo
from gi.repository import Gtk, Gdk, GObject, Pango
import canonical.misc as misc

def refresh():
    while Gtk.events_pending():
        Gtk.main_iteration()

def draw_round_rect(c, r, x, y, w, h):
    c.move_to(x + r, y)
    c.line_to(x + w - r, y)
    c.curve_to(x + w, y, x + w, y, x + w, y + r)
    c.line_to(x + w, y + h - r)
    c.curve_to(x + w, y + h, x + w, y + h, x + w - r, y + h)
    c.line_to(x + r, y + h)
    c.curve_to(x, y + h, x, y + h, x, y + h - r)
    c.line_to(x, y + r)
    c.curve_to(x, y, x, y, x + r, y)
    c.close_path()


def gtk_to_cairo_color(c):
    color = Gdk.color_parse(c)
    s = 1.0 / 65535.0
    r = color.red * s
    g = color.green * s
    b = color.blue * s
    return r, g, b


class StylizedFrame(Gtk.Alignment):
    __gtype_name__ = 'StylizedFrame'
    __gproperties__ = {
        'radius': (
            GObject.TYPE_INT, 'Radius', 'The radius of the rounded corners.',
            0, GObject.G_MAXINT, 10, GObject.PARAM_READWRITE),
        'width': (
            GObject.TYPE_INT, 'Width', 'The width of the outline.',
            0, GObject.G_MAXINT, 1, GObject.PARAM_READWRITE),
    }

    def __init__(self):
        Gtk.Alignment.__init__(self)
        self.radius = 10
        self.width = 1

    def do_get_property(self, prop):
        if prop.name in ('radius', 'width'):
            return getattr(self, prop.name)
        else:
            return Gtk.Alignment.do_get_property(self, prop)

    def do_set_property(self, prop, value):
        if prop.name in ('radius', 'width'):
            setattr(self, prop.name, value)
            self.queue_draw()
        else:
            Gtk.Alignment.do_set_property(self, prop, value)

    def paint_background(self, c):
        c.set_source_rgb(*gtk_to_cairo_color('#fbfbfb'))
        alloc = self.get_allocation()
        draw_round_rect(c, self.radius,
                        self.width / 2, self.width / 2,
                        alloc.width - self.width,
                        alloc.height - self.width)
        c.fill_preserve()

    def do_draw(self, c):
        # Background
        self.paint_background(c)
        # Edge
        c.set_source_rgb(*gtk_to_cairo_color('#c7c7c6'))
        c.set_line_width(self.width)
        c.stroke()
        if self.get_child():
            top, bottom, left, right = self.get_padding()
            c.translate(left, top)
            self.get_child().draw(c)

GObject.type_register(StylizedFrame)


class ResizeWidget(Gtk.HPaned):
    __gtype_name__ = 'ResizeWidget'
    __gproperties__ = {
        'part_size': (
            GObject.TYPE_UINT64, 'Partition size',
            'The size of the partition being resized',
            1, GObject.G_MAXUINT64, 100, GObject.PARAM_READWRITE),
        'min_size': (
            GObject.TYPE_UINT64, 'Minimum size',
            'The minimum size that the existing partition can be resized to',
            0, GObject.G_MAXUINT64, 0, GObject.PARAM_READWRITE),
        'max_size': (
            GObject.TYPE_UINT64, 'Maximum size',
            'The maximum size that the existing partition can be resized to',
            1, GObject.G_MAXUINT64, 100, GObject.PARAM_READWRITE)
    }

    def do_get_property(self, prop):
        return getattr(self, prop.name.replace('-', '_'))

    def do_set_property(self, prop, value):
        setattr(self, prop.name.replace('-', '_'), value)

    def __init__(self, part_size=100, min_size=0, max_size=100,
                 existing_part=None, new_part=None):
        Gtk.HPaned.__init__(self)
        assert min_size <= max_size <= part_size
        assert part_size > 0
        # The size (b) of the existing partition.
        self.part_size = part_size
        # The min size (b) that the existing partition can be resized to.
        self.min_size = min_size
        # The max size (b) that the existing partition can be resized to.
        self.max_size = max_size

        # FIXME: Why do we still need these event boxes to get proper bounds
        # for the linear gradient?
        self.existing_part = existing_part or PartitionBox()
        eb = Gtk.EventBox()
        eb.add(self.existing_part)
        self.pack1(eb, resize=False, shrink=False)
        self.new_part = new_part or PartitionBox()
        eb = Gtk.EventBox()
        eb.add(self.new_part)
        self.pack2(eb, resize=False, shrink=False)
        self.show_all()
        # FIXME hideous, but do_realize fails inexplicably.
        self.connect('realize', self.realize)

    def realize(self, w):
        # TEST: Make sure the value of the minimum size and maximum size
        # equal the value of the widget when pushed to the min/max.
        total = (self.new_part.get_allocation().width +
                 self.existing_part.get_allocation().width)
        tmp = float(self.min_size) / self.part_size
        pixels = int(tmp * total)
        self.existing_part.set_size_request(pixels, -1)

        tmp = ((float(self.part_size) - self.max_size) / self.part_size)
        pixels = int(tmp * total)
        self.new_part.set_size_request(pixels, -1)

    def do_draw(self, cr):
        s1 = self.existing_part.get_allocation().width
        s2 = self.new_part.get_allocation().width
        total = s1 + s2

        percent = (float(s1) / float(total))
        self.existing_part.set_size(percent * self.part_size)
        percent = (float(s2) / float(total))
        self.new_part.set_size(percent * self.part_size)

    def set_pref_size(self, size):
        s1 = self.existing_part.get_allocation().width
        s2 = self.new_part.get_allocation().width
        total = s1 + s2

        percent = (float(size) / float(self.part_size))
        val = percent * total
        self.set_position(int(val))

    def get_size(self):
        '''Returns the size of the old partition,
           clipped to the minimum and maximum sizes.
        '''
        s1 = self.existing_part.get_allocation().width
        s2 = self.new_part.get_allocation().width
        totalwidth = s1 + s2
        size = int(float(s1) * self.part_size / float(totalwidth))
        if size < self.min_size:
            return self.min_size
        elif size > self.max_size:
            return self.max_size
        else:
            return size

GObject.type_register(ResizeWidget)


class DiskBox(Gtk.Box):
    __gtype_name__ = 'DiskBox'

    def add(self, partition, size):
        Gtk.Box.add(self, partition, expand=False)
        partition.set_size_request(size, -1)

    def clear(self):
        self.forall(lambda x: self.remove(x))

GObject.type_register(DiskBox)


class PartitionBox(StylizedFrame):
    __gtype_name__ = 'PartitionBox'
    __gproperties__ = {
        'title': (
            GObject.TYPE_STRING, 'Title', None, 'Title',
            GObject.PARAM_READWRITE),
        'icon-name': (
            GObject.TYPE_STRING, 'Icon Name', None, 'distributor-logo',
            GObject.PARAM_READWRITE),
        'extra': (
            GObject.TYPE_STRING, 'Extra Text', None, '',
            GObject.PARAM_READWRITE),
    }

    def do_get_property(self, prop):
        if prop.name == 'title':
            return self.ostitle.get_text()
        elif prop.name == 'icon-name':
            return self.logo.get_icon_name()
        elif prop.name == 'extra':
            return self.extra.get_text()
        return getattr(self, prop.name)

    def do_set_property(self, prop, value):
        if prop.name == 'title':
            self.ostitle.set_markup('<b>%s</b>' % value)
            return
        elif prop.name == 'icon-name':
            self.logo.set_from_icon_name(value, Gtk.IconSize.DIALOG)
            return
        elif prop.name == 'extra':
            self.extra.set_markup('<small>%s</small>' %
                                  (value and value or ' '))
            return
        setattr(self, prop.name, value)

    def __init__(self, title='', extra='', icon_name='distributor-logo'):
        # 10 px above the topmost element
        # 6 px between the icon and the title
        # 4 px between the title and the extra heading
        # 5 px between the extra heading and the size
        # 12 px below the bottom-most element
        StylizedFrame.__init__(self)
        vbox = Gtk.Box()
        vbox.set_orientation(Gtk.Orientation.VERTICAL)
        self.logo = Gtk.Image.new_from_icon_name(icon_name,
                                                 Gtk.IconSize.DIALOG)
        align = Gtk.Alignment.new(0.5, 0.5, 0.5, 0.5)
        align.set_padding(10, 0, 0, 0)
        align.add(self.logo)
        vbox.pack_start(align, False, True, 0)

        self.ostitle = Gtk.Label()
        self.ostitle.set_ellipsize(Pango.EllipsizeMode.END)
        align = Gtk.Alignment.new(0.5, 0.5, 0.5, 0.5)
        align.set_padding(6, 0, 0, 0)
        align.add(self.ostitle)
        vbox.pack_start(align, False, True, 0)

        self.extra = Gtk.Label()
        self.extra.set_ellipsize(Pango.EllipsizeMode.END)
        align = Gtk.Alignment.new(0.5, 0.5, 0.5, 0.5)
        align.set_padding(4, 0, 0, 0)
        align.add(self.extra)
        vbox.pack_start(align, False, True, 0)

        self.size = Gtk.Label()
        self.size.set_ellipsize(Pango.EllipsizeMode.END)
        align = Gtk.Alignment.new(0.5, 0.5, 0.5, 0.5)
        align.set_padding(5, 12, 0, 0)
        align.add(self.size)
        vbox.pack_start(align, False, True, 0)
        self.add(vbox)

        self.ostitle.set_markup('<b>%s</b>' % title)
        # Take up the space that would otherwise be used to create symmetry.
        self.extra.set_markup('<small>%s</small>' % extra and extra or ' ')
        self.show_all()

    def set_size(self, size):
        size = misc.format_size(size)
        self.size.set_markup('<span size="x-large">%s</span>' % size)

    def render_dots(self):
        # FIXME: Dots are rendered over the frame.
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 2, 2)
        cr = cairo.Context(s)
        cr.set_source_rgb(*gtk_to_cairo_color('#b6b0a9'))
        cr.rectangle(1, 1, 1, 1)
        cr.fill()
        pattern = cairo.SurfacePattern(s)
        return pattern

    def paint_background(self, c):
        StylizedFrame.paint_background(self, c)
        a = self.get_allocation()
        pattern = self.render_dots()
        pattern.set_extend(cairo.EXTEND_REPEAT)
        c.set_source(pattern)
        c.fill_preserve()

        g = cairo.RadialGradient(a.width / 2, a.height / 2, 0, a.width / 2,
                                 a.height / 2,
                                 a.width > a.height and a.width or a.height)
        g.add_color_stop_rgba(0.00, 1, 1, 1, 1.00)
        g.add_color_stop_rgba(0.25, 1, 1, 1, 0.75)
        g.add_color_stop_rgba(0.40, 1, 1, 1, 0.00)
        c.set_source(g)
        c.fill_preserve()

GObject.type_register(PartitionBox)


class StateBox(StylizedFrame):
    __gtype_name__ = 'StateBox'
    __gproperties__ = {
        'label': (
            GObject.TYPE_STRING, 'Label', None, 'label',
            GObject.PARAM_READWRITE),
    }

    def do_get_property(self, prop):
        if prop.name == 'label':
            return self.label.get_text()
        return getattr(self, prop.name)

    def do_set_property(self, prop, value):
        if prop.name == 'label':
            self.label.set_text(value)
            return
        setattr(self, prop.name, value)

    def __init__(self, text=''):
        StylizedFrame.__init__(self)
        alignment = Gtk.Alignment()
        alignment.set_padding(7, 7, 15, 15)
        hbox = Gtk.Box()
        hbox.set_spacing(10)
        self.image = Gtk.Image()
        self.image.set_from_stock(Gtk.STOCK_YES, Gtk.IconSize.LARGE_TOOLBAR)
        self.label = Gtk.Label(label=text)

        self.label.set_alignment(0, 0.5)
        hbox.pack_start(self.image, False, True, 0)
        hbox.pack_start(self.label, True, True, 0)
        alignment.add(hbox)
        self.add(alignment)
        self.show_all()

        self.status = True

    def set_state(self, state):
        self.status = state
        if state:
            self.image.set_from_stock(Gtk.STOCK_YES,
                                      Gtk.IconSize.LARGE_TOOLBAR)
        else:
            self.image.set_from_stock(Gtk.STOCK_NO,
                                      Gtk.IconSize.LARGE_TOOLBAR)

    def get_state(self):
        return self.status

    def show(self):
        super().show()
    
    def hide(self):
        super().hide()

GObject.type_register(StateBox)

# GtkBuilder should have .get_object_ids() method
class Builder(Gtk.Builder):
    def __init__(self):
        self._widget_ids = set()
        super().__init__()

    def add_from_file(self, filename):
        import xml.etree.cElementTree as ET
        tree = ET.parse(filename)
        root = tree.getroot()
        for widgets in root.iter('object'):
            self._widget_ids.add(widgets.attrib['id'])
        return super().add_from_file(filename)

    def get_object_ids(self):
        return self._widget_ids
