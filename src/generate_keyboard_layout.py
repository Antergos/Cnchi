#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  generate_keyboard_layout.py

from gi.repository import Gtk, Gdk
import cairo
import subprocess
import sys
import math

#U+ , or +U+ ... to string
def fromUnicodeString(raw):
    if raw[0:2] == "U+":
        return chr(int(raw[2:], 16))
    elif raw[0:2] == "+U":
        return chr(int(raw[3:], 16))
    return ""


class Keyboard(Gtk.DrawingArea):

    kb_104 = {
        "extended_return": False,
        "keys": [
        (0x29, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd),
        (0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x2b),
        (0x1e, 0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28),
        (0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35),
        ()]
    }

    kb_105 = {
        "extended_return": True,
        "keys": [
        (0x29, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd),
        (0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b),
        (0x1e, 0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x2b),
        (0x54, 0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35),
        ()]
    }

    kb_106 = {
        "extended_return": True,
        "keys": [
        (0x29, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd, 0xe),
        (0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b),
        (0x1e, 0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29),
        (0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36),
        ()]
    }

    #lowerFont = "Helvetica SemiBold 10"
    #upperFont = "Helvetica 8"

    def __init__(self, parent=None):
        Gtk.DrawingArea.__init__(self)
        
        self.set_size_request(430, 130)
        
        self.codes = []

        self.layout = "us"
        self.variant = ""
        
        self.kb = None
        
        self.connect('draw', self.do_draw_cb)
        self.connect('configure-event', self.configure_event_cb)
        

    def setLayout(self, layout):
        self.layout = layout

    def setVariant(self, variant):
        self.variant = variant
        self.loadCodes()
        self.loadInfo()
        #self.repaint()
        self.configure_event_cb(None, None)
        self.queue_draw()

    def loadInfo(self):
        kbl_104 = ["us", "th"]
        kbl_106 = ["jp"]

        # Most keyboards are 105 key so default to that
        if self.layout in kbl_104:
            self.kb = self.kb_104
        elif self.layout in kbl_106:
            self.kb = self.kb_106
        elif self.kb != self.kb_105:
            self.kb = self.kb_105

    def rounded_rectangle(self, cr, x, y, width, height, aspect=1.0):
        corner_radius = height / 10.0
        radius = corner_radius / aspect;
        degrees = math.pi / 180.0;
        
        cr.new_sub_path()
        cr.arc(x + width - radius, y + radius, radius, -90 * degrees, 0 * degrees)
        cr.arc(x + width - radius, y + height - radius, radius, 0 * degrees, 90 * degrees)
        cr.arc(x + radius, y + height - radius, radius, 90 * degrees, 180 * degrees)
        cr.arc(x + radius, y + radius, radius, 180 * degrees, 270 * degrees)
        cr.close_path()

        cr.set_source_rgb(0.5, 0.5, 0.5)
        cr.fill_preserve()
        cr.set_source_rgba(0.2, 0.2, 0.2, 0.5)
        cr.set_line_width(2)
        cr.stroke()

    def configure_event_cb(self, widget, event):
        self.space = 6
                
        width = self.get_allocated_width()
        height = self.get_allocated_height()

        print("************************************ width: ", width)
        print("************************************ height: ", height)
        
        #(width, height) = self.get_size_request()
        #print("************************************ width: ", width)
        #print("************************************ height: ", height)

        self.usable_width = width - 6
        self.key_w = (self.usable_width - 14 * self.space) / 15

        #(width, height) = self.get_size_request()
        #max_height = self.key_w * 4 + self.space * 5
        
        return False
    
    def do_draw_cb(self, widget, cr):
        ''' The do_draw_cb is called when the widget is asked to draw itself
            with the 'draw' as opposed to old function 'expose event' 
            Remember that this will be called a lot of times, so it's usually
            a good idea to write this code as optimized as it can be, don't
            create any resources in here.
            the 'cr' variable is the current Cairo context '''
            
        # Set background color to transparent
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.0)
        cr.paint()
        
        # d6d6d6
        cr.set_source_rgb(0.84, 0.84, 0.84)
        cr.set_line_width(2)
        
        cr.rectangle(0, 0, 640, 640)
        cr.stroke()
                
        # 585858
        cr.set_source_rgb(0.22, 0.22, 0.22)

        rx = 3

        space = self.space
        w = self.usable_width
        kw = self.key_w

        def drawRow(row, sx, sy, last_end=False):
            x = sx
            y = sy
            keys = row
            rw = w - sx
            i = 0
            for k in keys:
                rect = (x, y, kw, kw)

                if i == len(keys) - 1 and last_end:
                    rect[2] = rect[0] + rw

                self.rounded_rectangle(cr, rect[0], rect[1], rect[2], rect[3])

                px = rect[0] + 5
                py = rect[1] + rect[3] - (rect[3] / 4)

                # lower
                cr.set_source_rgb(1.0, 1.0, 1.0)
                cr.select_font_face("Helvetica", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD);
                cr.set_font_size(10)
                cr.move_to(px, py)
                cr.show_text(self.regular_text(k))

                px = rect[0] + 5
                py = rect[1] + (rect[3] / 3)
                
                # upper
                cr.set_source_rgb(0.82, 0.82, 0.82)
                cr.select_font_face("Helvetica", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL);
                cr.set_font_size(8)
                cr.move_to(px, py)
                cr.show_text(self.shift_text(k))

                rw = rw - space - kw
                x = x + space + kw
                i = i + 1
            return (x, rw)

        x = 6
        y = 6

        keys = self.kb["keys"]
        ext_return = self.kb["extended_return"]

        first_key_w = 0

        rows = 4
        remaining_x = [0, 0, 0, 0]
        remaining_widths = [0, 0, 0, 0]

        for i in range(0, rows):
            if first_key_w > 0:
                first_key_w = first_key_w * 1.375

                if self.kb == self.kb_105 and i == 3:
                    first_key_w = kw * 1.275

                self.rounded_rectangle(cr, 6, y, first_key_w, kw)
                x = 6 + first_key_w + space
            else:
                first_key_w = kw

            x, rw = drawRow(keys[i], x, y, i == 1 and not ext_return)

            remaining_x[i] = x
            remaining_widths[i] = rw

            if i != 1 and i != 2:
                self.rounded_rectangle(cr, x, y, rw, kw)

            x = .5
            y = y + space + kw
        
        if ext_return:
            #rx = rx * 2
            x1 = remaining_x[1]
            y1 = 6 + kw * 1 + space * 1
            w1 = remaining_widths[1]
            x2 = remaining_x[2]
            y2 = 6 + kw * 2 + space * 2

            # this is some serious crap... but it has to be so
            # maybe one day keyboards won't look like this...
            # one can only hope
            #pp = QPainterPath()
            degrees = math.pi / 180.0;
            cr.new_sub_path()
            
            cr.move_to(x1, y1 + rx)
            cr.arc(x1 + rx, y1 + rx, rx, 180 * degrees, -90 * degrees)
            cr.line_to(x1 + w1 - rx, y1)
            cr.arc(x1 + w1 - rx, y1 + rx, rx, -90 * degrees, 0)
            cr.line_to(x1 + w1, y2 + kw - rx)
            cr.arc(x1 + w1 - rx, y2 + kw - rx, rx, 0 * degrees, 90 * degrees)           
            cr.line_to(x2 + rx, y2 + kw)
            cr.arc(x2 + rx, y2 + kw - rx, rx, 90 * degrees, 180 * degrees)
            cr.line_to(x2, y1 + kw)
            cr.line_to(x1 + rx, y1 + kw)
            cr.arc(x1 + rx, y1 + kw - rx, rx, 90 * degrees, 180 * degrees)
            
            cr.close_path()
            cr.set_source_rgb(0.5, 0.5, 0.5)
            cr.fill_preserve()
            cr.set_source_rgba(0.2, 0.2, 0.2, 0.5)
            cr.set_line_width(2)
            cr.stroke()
        else:
            x = remaining_x[2]
            # Changed .5 to 6 because return key was out of line
            y = 6 + kw * 2 + space * 2
            #rect = QRectF(x, y, remaining_widths[2], kw)
            #p.drawRoundedRect(rect, rx, rx)
            self.rounded_rectangle(cr, x, y, remaining_widths[2], kw)


        #QWidget.paintEvent(self, pe)
        

    def regular_text(self, index):
        return self.codes[index - 1][0]

    def shift_text(self, index):
        return self.codes[index - 1][1]

    def ctrl_text(self, index):
        return self.codes[index - 1][2]

    def alt_text(self, index):
        return self.codes[index - 1][3]

    def loadCodes(self):
        if self.layout is None:
            return

        variantParam = ""
        if self.variant:
            variantParam = "-variant %s" % self.variant

        cmd = "/usr/share/cnchi/scripts/ckbcomp -model pc106 -layout %s %s -compact" % (self.layout, variantParam)
        #print cmd

        pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=None)
        cfile = pipe.communicate()[0].decode("utf-8").split('\n')

        #clear the current codes
        del self.codes[:]

        for line in cfile:
            if line[:7] != "keycode":
                continue

            codes = line.split('=')[1].strip().split(' ')

            plain = fromUnicodeString(codes[0])
            shift = fromUnicodeString(codes[1])
            ctrl = fromUnicodeString(codes[2])
            alt = fromUnicodeString(codes[3])

            if ctrl == plain:
                ctrl = ""

            if alt == plain:
                alt = ""

            self.codes.append((plain, shift, ctrl, alt))

## testing

def destroy(window):
    Gtk.main_quit()

if __name__ == "__main__":
    window = Gtk.Window()
    window.set_title ("Hello World")
    box = Gtk.Box('Vertical',5)

    kb1 = Keyboard()
    
    kb1.setLayout("jp")
    kb1.setVariant("")
        
    window.add(kb1)
                       
    window.connect_after('destroy', destroy)
    window.show_all()
    Gtk.main()
