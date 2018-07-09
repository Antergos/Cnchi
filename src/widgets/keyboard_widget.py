#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# keyboard_widget.py
#
# Copyright © 2013-2017 Antergos (this GTK version)
# Copyright © 2013 Manjaro (QT version)
#
# This file is part of Cnchi.
#
# Cnchi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Cnchi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# The following additional terms are in effect as per Section 7 of the license:
#
# The preservation of all legal notices and author attributions in
# the material or in the Appropriate Legal Notices displayed
# by works containing it is required.
#
# You should have received a copy of the GNU General Public License
# along with Cnchi; If not, see <http://www.gnu.org/licenses/>.


""" Keyboard widget that shows keyboard layout and variant types to the user """

import subprocess
import math
import logging

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

import cairo

from misc.extra import raised_privileges


def unicode_to_string(raw):
    """ U+ , or +U+ ... to string """
    if raw[0:2] == "U+":
        return chr(int(raw[2:], 16))
    elif raw[0:2] == "+U":
        return chr(int(raw[3:], 16))
    return ""


class KeyboardWidget(Gtk.DrawingArea):
    """ Draws a keyboard widget """
    __gtype_name__ = 'KeyboardWidget'

    KB_104 = {
        "extended_return": False,
        "keys": [
            (0x29, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd),
            (0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x2b),
            (0x1e, 0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28),
            (0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35),
            ()]
    }

    KB_105 = {
        "extended_return": True,
        "keys": [
            (0x29, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd),
            (0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b),
            (0x1e, 0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x2b),
            (0x54, 0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35),
            ()]
    }

    KB_106 = {
        "extended_return": True,
        "keys": [
            (0x29, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd, 0xe),
            (0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b),
            (0x1e, 0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29),
            (0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36),
            ()]
    }

    def __init__(self):
        Gtk.DrawingArea.__init__(self)

        self.set_size_request(460, 130)

        self.codes = []

        self.layout = "us"
        self.variant = None
        self.font = "Helvetica"

        self.space = 6

        self.keyboard = None

    def set_layout(self, layout):
        """ Set keymap layout """
        self.layout = layout

    def set_font(self):
        """ Font depends on the keyboard layout """
        # broken: ad (Andorra), lk (Sri Lanka), brai (Braille)
        # ?!?: us:chr

        # Default
        self.font = "Helvetica"

        # Load fonts from:
        # ttf-aboriginal-sans, ttf-indic-otf, ttf-khmer, ttf-lohit-fonts, ttf-myanmar3,
        # ttf-thaana-fonts and ttf-tlwg

        fonts = {
            'Aboriginal Sans': ['chr'],
            'Akaash': ['bd'],
            'Gargi': ['np', 'in'],
            'khmerOS': ['kh'],
            'Lohit Bengali': ['ben_probhat', 'ben'],
            'Lohit Kannada': ['kan'],
            'Lohit Oriya': ['ori'],
            'Lohit Punjabi': ['guru', 'jhelum'],
            'Lohit Tamil': ['tam_keyboard_with_numerals', 'tam'],
            'Lohit Telugu': ['tel'],
            'Malayalam': ['mal', 'mal_lalitha'],
            'MVBoli': ['mv'],
            'Myanmar3': ['mm'],
            'Oriya': [
                'geo', 'urd-phonetic3', 'urd-phonetic', 'urd-winkeys',
                'af', 'ara', 'am', 'cn', 'ge', 'gr', 'gn', 'ir',
                'iq', 'ie', 'il', 'la', 'ma', 'pk', 'lk', 'sy'],
            'Padmaa': ['guj'],
            'Tlwg Mono': ['th'],
            'TSCu_Times': ['tam_TAB', 'tam_TSCII', 'tam_unicode']
        }

        for font in fonts:
            if self.layout in fonts[font] or self.variant in fonts[font]:
                self.font = font
                break

    def set_variant(self, variant):
        """ Set keymap layout variant """
        self.variant = variant
        self.load_codes()
        self.load_info()
        self.set_font()
        # Force repaint
        self.queue_draw()

    def load_info(self):
        """ Get keyboard keys based on keymap layout """
        # Most keyboards are 105 key so default to that
        if self.layout in ['us', 'th']:
            self.keyboard = self.KB_104
        elif self.layout in ['jp']:
            self.keyboard = self.KB_106
        elif self.keyboard != self.KB_105:
            self.keyboard = self.KB_105

    @staticmethod
    def rounded_rectangle(context, start_x, start_y, width, height, aspect=1.0):
        """ Draws a rectangle with rounded corners """
        corner_radius = height / 10.0
        radius = corner_radius / aspect
        degrees = math.pi / 180.0
        degrees_90 = 90 * degrees
        degrees_180 = 180 * degrees

        context.new_sub_path()
        context.arc(start_x + width - radius, start_y + radius, radius, -degrees_90, 0)
        context.arc(start_x + width - radius, start_y + height -
                    radius, radius, 0, degrees_90)
        context.arc(start_x + radius, start_y + height - radius,
                    radius, degrees_90, degrees_180)
        context.arc(start_x + radius, start_y + radius, radius, degrees_180, 270 * degrees)
        context.close_path()

        context.set_source_rgb(0.5, 0.5, 0.5)
        context.fill_preserve()
        context.set_source_rgba(0.2, 0.2, 0.2, 0.5)
        context.set_line_width(2)
        context.stroke()

    @staticmethod
    def draw_ext_return(context, point1, width1, point2, rect_x, key_width):
        """ this is some serious crap... but it has to be so
            maybe one day keyboards won't look like this...
            one can only hope """
        point_x1, point_y1 = point1
        point_x2, point_y2 = point2
        degrees = math.pi / 180.0
        degrees90 = 90 * degrees
        degrees180 = 180 * degrees

        context.new_sub_path()

        context.move_to(point_x1, point_y1 + rect_x)
        context.arc(point_x1 + rect_x, point_y1 + rect_x, rect_x,
                    degrees180, -degrees90)
        context.line_to(point_x1 + width1 - rect_x, point_y1)
        context.arc(point_x1 + width1 - rect_x, point_y1 +
                    rect_x, rect_x, -degrees90, 0)
        context.line_to(point_x1 + width1, point_y2 + key_width - rect_x)
        context.arc(point_x1 + width1 - rect_x, point_y2 + key_width - rect_x, rect_x,
                    0, degrees90)
        context.line_to(point_x2 + rect_x, point_y2 + key_width)
        context.arc(point_x2 + rect_x, point_y2 + key_width - rect_x, rect_x,
                    degrees90, degrees180)
        context.line_to(point_x2, point_y1 + key_width)
        context.line_to(point_x1 + rect_x, point_y1 + key_width)
        context.arc(point_x1 + rect_x, point_y1 + key_width - rect_x, rect_x,
                    degrees90, degrees180)

        context.close_path()

        context.set_source_rgb(0.5, 0.5, 0.5)
        context.fill_preserve()
        context.set_source_rgba(0.2, 0.2, 0.2, 0.5)
        context.set_line_width(2)
        context.stroke()

    def draw_row(self, context, row, start_x, start_y, max_width, key_width, space, last_end=False):
        """ Draw a row of the keyboard """
        my_x = start_x
        my_y = start_y
        keys = row
        rect_width = max_width - start_x
        i = 0
        for key in keys:
            rect = (my_x, my_y, key_width, key_width)

            if i == len(keys) - 1 and last_end:
                rect = (rect[0], rect[1], rect_width, rect[3])

            self.rounded_rectangle(
                context, rect[0], rect[1], rect[2], rect[3])

            point_x = rect[0] + 5
            point_y = rect[1] + rect[3] - (rect[3] / 4)

            if self.codes:
                # Draw lower character
                context.set_source_rgb(1.0, 1.0, 1.0)
                context.select_font_face(
                    self.font,
                    cairo.FONT_SLANT_NORMAL,
                    cairo.FONT_WEIGHT_BOLD)
                context.set_font_size(10)
                context.move_to(point_x, point_y)
                context.show_text(self.regular_text(key))

                point_x = rect[0] + 5
                point_y = rect[1] + (rect[3] / 3)

                # Draw upper character
                context.set_source_rgb(0.82, 0.82, 0.82)
                context.select_font_face(
                    self.font,
                    cairo.FONT_SLANT_NORMAL,
                    cairo.FONT_WEIGHT_NORMAL)
                context.set_font_size(8)
                context.move_to(point_x, point_y)
                context.show_text(self.shift_text(key))

            rect_width = rect_width - space - key_width
            my_x = my_x + space + key_width
            i += 1
        return my_x, rect_width


    def do_draw(self, context):
        """ context: current Cairo context """
        # alloc = self.get_allocation()
        # real_width = alloc.width
        # real_height = alloc.height

        if not self.keyboard:
            return

        width = 460
        height = 130

        usable_width = width - 6
        key_w = (usable_width - 14 * self.space) / 15

        # Set background color to transparent
        context.set_source_rgba(1.0, 1.0, 1.0, 0.0)
        context.paint()

        context.set_source_rgb(0.84, 0.84, 0.84)
        context.set_line_width(2)

        context.rectangle(0, 0, width, height)
        context.stroke()

        context.set_source_rgb(0.22, 0.22, 0.22)

        rect_x = 3

        space = self.space
        max_width = usable_width
        key_width = key_w

        my_x = 6
        my_y = 6

        keys = self.keyboard["keys"]
        ext_return = self.keyboard["extended_return"]

        first_key_w = 0

        rows = 4
        remaining_x = [0, 0, 0, 0]
        remaining_widths = [0, 0, 0, 0]

        for i in range(0, rows):
            if first_key_w > 0:
                first_key_w *= 1.375

                if self.keyboard == self.KB_105 and i == 3:
                    first_key_w = key_width * 1.275

                self.rounded_rectangle(context, 6, my_y, first_key_w, key_width)
                my_x = 6 + first_key_w + space
            else:
                first_key_w = key_width

            last_end = i == 1 and not ext_return
            my_x, rect_width = self.draw_row(
                context, keys[i], my_x, my_y, max_width, key_width, space, last_end)

            remaining_x[i] = my_x
            remaining_widths[i] = rect_width

            if i != 1 and i != 2:
                self.rounded_rectangle(context, my_x, my_y, rect_width, key_width)

            my_x = .5
            my_y = my_y + space + key_width

        if ext_return:
            # rect_x = rect_x * 2
            point1 = (remaining_x[1], 6 + key_width * 1 + space * 1)
            width1 = remaining_widths[1]
            point2 = (remaining_x[2], 6 + key_width * 2 + space * 2)

            self.draw_ext_return(context, point1, width1,
                                 point2, rect_x, key_width)
        else:
            my_x = remaining_x[2]
            # Changed .5 to 6 because return key was out of line
            my_y = 6 + key_width * 2 + space * 2
            self.rounded_rectangle(
                context, my_x, my_y, remaining_widths[2], key_width)

    def regular_text(self, index):
        """ Get regular key code  """
        try:
            return self.codes[index - 1][0]
        except IndexError:
            return " "

    def shift_text(self, index):
        """ Get key code when shift is pressed """
        try:
            return self.codes[index - 1][1]
        except IndexError:
            return " "

    def ctrl_text(self, index):
        """ Get key code when ctrl is pressed """
        try:
            return self.codes[index - 1][2]
        except IndexError:
            return " "

    def alt_text(self, index):
        """ Get key code when alt is pressed """
        try:
            return self.codes[index - 1][3]
        except IndexError:
            return " "

    def load_codes(self):
        """ Load keyboard codes (script ckbcomp is needed!) """

        if self.layout is None:
            return

        cmd = ["/usr/share/cnchi/scripts/ckbcomp",
               "-model", "pc106",
               "-layout", self.layout]

        if self.variant:
            cmd.extend(["-variant", self.variant])

        cmd.append("-compact")

        try:
            with raised_privileges():
                output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
                if output:
                    output = output.decode()
                    output = output.split('\n')
        except subprocess.CalledProcessError as process_error:
            msg = "Error running command %s: %s"
            logging.error(msg, process_error.cmd, process_error)
            return

        # Clear current codes
        del self.codes[:]

        for line in output:
            if line[:7] != "keycode":
                continue

            codes = line.split('=')[1].strip().split(' ')

            plain = unicode_to_string(codes[0])
            shift = unicode_to_string(codes[1])
            ctrl = unicode_to_string(codes[2])
            alt = unicode_to_string(codes[3])

            if ctrl == plain:
                ctrl = ""

            if alt == plain:
                alt = ""

            self.codes.append((plain, shift, ctrl, alt))


GObject.type_register(KeyboardWidget)
