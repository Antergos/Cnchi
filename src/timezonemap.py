#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  timezonemap.py
#
#  Author: Thomas Wood <thomas.wood@intel.com>
#
#  Portions from Ubiquity, Copyright (C) 2009 Canonical Ltd.
#  Written in C by Evan Dandrea <evand@ubuntu.com>
#  Python port Copyright © 2013,2014 Antergos
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

BUBBLE_TEXT_FONT = "Sans 9"

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
    (1.0, 85, 34, 0, 255), # eastern Europe
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

# This info is duplicated in timezones.xml
olsen_map_timezones = [
    "Africa/Abidjan",
    "Africa/Accra",
    "Africa/Addis_Ababa",
    "Africa/Algiers",
    "Africa/Asmara",
    "Africa/Bamako",
    "Africa/Bangui",
    "Africa/Banjul",
    "Africa/Bissau",
    "Africa/Blantyre",
    "Africa/Brazzaville",
    "Africa/Bujumbura",
    "Africa/Cairo",
    "Africa/Casablanca",
    "Africa/Conakry",
    "Africa/Dakar",
    "Africa/Dar_es_Salaam",
    "Africa/Djibouti",
    "Africa/Douala",
    "Africa/El_Aaiun",
    "Africa/Freetown",
    "Africa/Gaborone",
    "Africa/Harare",
    "Africa/Johannesburg",
    "Africa/Kampala",
    "Africa/Khartoum",
    "Africa/Kigali",
    "Africa/Kinshasa",
    "Africa/Lagos",
    "Africa/Libreville",
    "Africa/Lome",
    "Africa/Luanda",
    "Africa/Lubumbashi",
    "Africa/Lusaka",
    "Africa/Malabo",
    "Africa/Maputo",
    "Africa/Maseru",
    "Africa/Mbabane",
    "Africa/Mogadishu",
    "Africa/Monrovia",
    "Africa/Nairobi",
    "Africa/Ndjamena",
    "Africa/Niamey",
    "Africa/Nouakchott",
    "Africa/Ouagadougou",
    "Africa/Porto-Novo",
    "Africa/Sao_Tome",
    "Africa/Tripoli",
    "Africa/Tunis",
    "Africa/Windhoek",
    "America/Adak",
    "America/Anguilla",
    "America/Antigua",
    "America/Araguaina",
    "America/Argentina/Buenos_Aires",
    "America/Argentina/Catamarca",
    "America/Argentina/Cordoba",
    "America/Argentina/Jujuy",
    "America/Argentina/La_Rioja",
    "America/Argentina/Mendoza",
    "America/Argentina/Rio_Gallegos",
    "America/Argentina/San_Juan",
    "America/Argentina/San_Luis",
    "America/Argentina/Tucuman",
    "America/Argentina/Ushuaia",
    "America/Aruba",
    "America/Asuncion",
    "America/Atikokan",
    "America/Bahia",
    "America/Barbados",
    "America/Belem",
    "America/Belize",
    "America/Blanc-Sablon",
    "America/Boa_Vista",
    "America/Bogota",
    "America/Boise",
    "America/Cambridge_Bay",
    "America/Campo_Grande",
    "America/Cancun",
    "America/Caracas",
    "America/Cayenne",
    "America/Cayman",
    "America/Chicago",
    "America/Chihuahua",
    "America/Coral_Harbour",
    "America/Costa_Rica",
    "America/Cuiaba",
    "America/Curacao",
    "America/Dawson",
    "America/Dawson_Creek",
    "America/Denver",
    "America/Dominica",
    "America/Edmonton",
    "America/Eirunepe",
    "America/El_Salvador",
    "America/Fortaleza",
    "America/Glace_Bay",
    "America/Goose_Bay",
    "America/Grand_Turk",
    "America/Grenada",
    "America/Guadeloupe",
    "America/Guatemala",
    "America/Guayaquil",
    "America/Guyana",
    "America/Halifax",
    "America/Havana",
    "America/Hermosillo",
    "America/Indiana/Indianapolis",
    "America/Indiana/Knox",
    "America/Indiana/Marengo",
    "America/Indiana/Petersburg",
    "America/Indiana/Vevay",
    "America/Indiana/Vincennes",
    "America/Indiana/Winamac",
    "America/Inuvik",
    "America/Iqaluit",
    "America/Jamaica",
    "America/Juneau",
    "America/Kentucky/Louisville",
    "America/Kentucky/Monticello",
    "America/La_Paz",
    "America/Lima",
    "America/Los_Angeles",
    "America/Maceio",
    "America/Managua",
    "America/Manaus",
    "America/Marigot",
    "America/Martinique",
    "America/Mazatlan",
    "America/Menominee",
    "America/Merida",
    "America/Mexico_City",
    "America/Miquelon",
    "America/Moncton",
    "America/Monterrey",
    "America/Montevideo",
    "America/Montreal",
    "America/Montserrat",
    "America/Nassau",
    "America/New_York",
    "America/Nipigon",
    "America/Noronha",
    "America/North_Dakota/Center",
    "America/North_Dakota/Salem",
    "America/Panama",
    "America/Pangnirtung",
    "America/Paramaribo",
    "America/Phoenix",
    "America/Port-au-Prince",
    "America/Port_of_Spain",
    "America/Porto_Velho",
    "America/Puerto_Rico",
    "America/Rainy_River",
    "America/Rankin_Inlet",
    "America/Recife",
    "America/Regina",
    "America/Resolute",
    "America/Rio_Branco",
    "America/Santarem",
    "America/Santiago",
    "America/Santo_Domingo",
    "America/Sao_Paulo",
    "America/St_Barthelemy",
    "America/St_Johns",
    "America/St_Kitts",
    "America/St_Lucia",
    "America/St_Thomas",
    "America/St_Vincent",
    "America/Tegucigalpa",
    "America/Thunder_Bay",
    "America/Tijuana",
    "America/Toronto",
    "America/Tortola",
    "America/Vancouver",
    "America/Whitehorse",
    "America/Winnipeg",
    "America/Yellowknife",
    "Ameriica/Swift_Current",
    "Arctic/Longyearbyen",
    "Asia/Aden",
    "Asia/Almaty",
    "Asia/Amman",
    "Asia/Anadyr",
    "Asia/Aqtau",
    "Asia/Aqtobe",
    "Asia/Ashgabat",
    "Asia/Baghdad",
    "Asia/Bahrain",
    "Asia/Baku",
    "Asia/Bangkok",
    "Asia/Beirut",
    "Asia/Bishkek",
    "Asia/Brunei",
    "Asia/Choibalsan",
    "Asia/Chongqing",
    "Asia/Colombo",
    "Asia/Damascus",
    "Asia/Dhaka",
    "Asia/Dili",
    "Asia/Dubai",
    "Asia/Dushanbe",
    "Asia/Gaza",
    "Asia/Harbin",
    "Asia/Ho_Chi_Minh",
    "Asia/Hong_Kong",
    "Asia/Hovd",
    "Asia/Irkutsk",
    "Asia/Jakarta",
    "Asia/Jayapura",
    "Asia/Jerusalem",
    "Asia/Kabul",
    "Asia/Kamchatka",
    "Asia/Karachi",
    "Asia/Kashgar",
    "Asia/Katmandu",
    "Asia/Kolkata",
    "Asia/Krasnoyarsk",
    "Asia/Kuala_Lumpur",
    "Asia/Kuching",
    "Asia/Kuwait",
    "Asia/Macau",
    "Asia/Magadan",
    "Asia/Makassar",
    "Asia/Manila",
    "Asia/Muscat",
    "Asia/Nicosia",
    "Asia/Novosibirsk",
    "Asia/Omsk",
    "Asia/Oral",
    "Asia/Phnom_Penh",
    "Asia/Pontianak",
    "Asia/Pyongyang",
    "Asia/Qatar",
    "Asia/Qyzylorda",
    "Asia/Rangoon",
    "Asia/Riyadh",
    "Asia/Sakhalin",
    "Asia/Samarkand",
    "Asia/Seoul",
    "Asia/Shanghai",
    "Asia/Singapore",
    "Asia/Taipei",
    "Asia/Tashkent",
    "Asia/Tbilisi",
    "Asia/Tehran",
    "Asia/Thimphu",
    "Asia/Tokyo",
    "Asia/Ulaanbaatar",
    "Asia/Urumqi",
    "Asia/Vientiane",
    "Asia/Vladivostok",
    "Asia/Yakutsk",
    "Asia/Yekaterinburg",
    "Asia/Yerevan",
    "Atlantic/Azores",
    "Atlantic/Bermuda",
    "Atlantic/Canary",
    "Atlantic/Cape_Verde",
    "Atlantic/Faroe",
    "Atlantic/Madeira",
    "Atlantic/Reykjavik",
    "Atlantic/South_Georgia",
    "Atlantic/St_Helena",
    "Atlantic/Stanley",
    "Australia/Adelaide",
    "Australia/Brisbane",
    "Australia/Broken_Hill",
    "Australia/Currie",
    "Australia/Darwin",
    "Australia/Eucla",
    "Australia/Hobart",
    "Australia/Lindeman",
    "Australia/Lord_Howe",
    "Australia/Melbourne",
    "Australia/Perth",
    "Australia/Sydney",
    "Europe/Amsterdam",
    "Europe/Andorra",
    "Europe/Athens",
    "Europe/Belgrade",
    "Europe/Berlin",
    "Europe/Bratislava",
    "Europe/Brussels",
    "Europe/Bucharest",
    "Europe/Budapest",
    "Europe/Chisinau",
    "Europe/Copenhagen",
    "Europe/Dublin",
    "Europe/Gibraltar",
    "Europe/Guernsey",
    "Europe/Helsinki",
    "Europe/Isle_of_Man",
    "Europe/Istanbul",
    "Europe/Jersey",
    "Europe/Kaliningrad",
    "Europe/Kiev",
    "Europe/Lisbon",
    "Europe/Ljubljana",
    "Europe/London",
    "Europe/Luxembourg",
    "Europe/Madrid",
    "Europe/Malta",
    "Europe/Marienhamn",
    "Europe/Minsk",
    "Europe/Monaco",
    "Europe/Moscow",
    "Europe/Oslo",
    "Europe/Paris",
    "Europe/Podgorica",
    "Europe/Prague",
    "Europe/Riga",
    "Europe/Rome",
    "Europe/Samara",
    "Europe/San_Marino",
    "Europe/Sarajevo",
    "Europe/Simferopol",
    "Europe/Skopje",
    "Europe/Sofia",
    "Europe/Stockholm",
    "Europe/Tallinn",
    "Europe/Tirane",
    "Europe/Uzhgorod",
    "Europe/Vaduz",
    "Europe/Vatican",
    "Europe/Vienna",
    "Europe/Vilnius",
    "Europe/Volgograd",
    "Europe/Warsaw",
    "Europe/Zagreb",
    "Europe/Zaporozhye",
    "Europe/Zurich",
    "Indian/Antananarivo",
    "Indian/Chagos",
    "Indian/Christmas",
    "Indian/Cocos",
    "Indian/Comoro",
    "Indian/Kerguelen",
    "Indian/Mahe",
    "Indian/Maldives",
    "Indian/Mauritius",
    "Indian/Mayotte",
    "Indian/Reunion",
    "Pacific/Apia",
    "Pacific/Auckland",
    "Pacific/Chatham",
    "Pacific/Easter",
    "Pacific/Efate",
    "Pacific/Enderbury",
    "Pacific/Fakaofo",
    "Pacific/Fiji",
    "Pacific/Funafuti",
    "Pacific/Galapagos",
    "Pacific/Gambier",
    "Pacific/Guadalcanal",
    "Pacific/Guam",
    "Pacific/Honolulu",
    "Pacific/Johnston",
    "Pacific/Kiritimati",
    "Pacific/Kosrae",
    "Pacific/Kwajalein",
    "Pacific/Majuro",
    "Pacific/Marquesas",
    "Pacific/Midway",
    "Pacific/Nauru",
    "Pacific/Niue",
    "Pacific/Norfolk",
    "Pacific/Noumea",
    "Pacific/Pago_Pago",
    "Pacific/Palau",
    "Pacific/Pitcairn",
    "Pacific/Ponape",
    "Pacific/Port_Moresby",
    "Pacific/Rarotonga",
    "Pacific/Saipan",
    "Pacific/Tahiti",
    "Pacific/Tarawa",
    "Pacific/Tongatapu",
    "Pacific/Truk",
    "Pacific/Wake",
    "Pacific/Wallis"]

def convert_longitude_to_x(longitude, map_width):
    xdeg_offset = -6.0
    return (map_width * (180.0 + longitude) / 360.0) + (map_width * xdeg_offset / 180.0)

def convert_latitude_to_y(latitude, map_height):
    bottom_lat = -59.0
    top_lat = 81.0

    top_per = top_lat / 180.0

    y = 1.25 * math.log(math.tan(G_PI_4 + 0.4 * math.radians(latitude)))

    full_range = 4.6068250867599998
    top_offset = full_range * top_per
    map_range = math.fabs(1.25 * math.log(math.tan(G_PI_4 + 0.4 * math.radians(bottom_lat))) - top_offset)
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

class TimezoneMap(Gtk.Widget):
    __gtype_name__ = 'TimezoneMap'

    __gsignals__ = { 'location-changed' : (GObject.SignalFlags.RUN_LAST, None, (object,)) }
    
    def __init__(self):
        Gtk.Widget.__init__(self)

        self.set_size_request(40, 40)

        self._background = None
        self._color_map = None
        self._olsen_map = None
        
        self._selected_offset = 0.0
        self._show_offset = False

        self._tz_location = None

        self._bubble_text = ""

        try:
            self._orig_background = GdkPixbuf.Pixbuf.new_from_file(
                os.path.join(TIMEZONEMAP_IMAGES_PATH, "bg.png"))

            self._orig_background_dim = GdkPixbuf.Pixbuf.new_from_file(
                os.path.join(TIMEZONEMAP_IMAGES_PATH, "bg_dim.png"))

            self._orig_color_map = GdkPixbuf.Pixbuf.new_from_file(
                os.path.join(TIMEZONEMAP_IMAGES_PATH, "cc.png"))

            self._olsen_map = GdkPixbuf.Pixbuf.new_from_file(
                os.path.join(TIMEZONEMAP_IMAGES_PATH, "olsen_map.png"))

            self._pin = GdkPixbuf.Pixbuf.new_from_file(
                os.path.join(TIMEZONEMAP_IMAGES_PATH, "pin.png"))
        except Exception as err:
            print(err)
            sys.exit(1)

        self._tzdb = tz.Database()

    def do_get_preferred_width(self):
        """ Retrieves a widget’s initial minimum and natural width. """
        width = self._orig_background.get_width()
        return (width / 2, width)

    def do_get_preferred_height(self):
        """ Retrieves a widget’s initial minimum and natural height. """
        height = self._orig_background.get_height()
        return (height / 2, height)

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

        #self._visible_map_pixels = self._color_map.get_pixels()
        #self._visible_map_rowstride = self._color_map.get_rowstride()

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

        cursor = Gdk.Cursor(Gdk.CursorType.HAND2)
        window.set_cursor(cursor)
        
        self.set_window(window)

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
        
        font_description = Pango.font_description_from_string(BUBBLE_TEXT_FONT)
        layout.set_font_description(font_description)

        layout.set_alignment(Pango.Alignment.CENTER)
        layout.set_spacing(3)
        layout.set_markup(self._bubble_text)
        (ink_rect, logical_rect) = layout.get_pixel_extents()

        # Calculate the bubble size based on the text layout size
        width = logical_rect.width + margin_left + margin_right
        height = logical_rect.height + margin_top + margin_bottom

        if pointx < alloc.width / 2:
            x = pointx + 20
        else:
            x = pointx - width - 20

        y = pointy - height / 2

        # Make sure it fits in the visible area
        x = clamp(x, 0, alloc.width - width)
        y = clamp(y, 0, alloc.height - height)

        cr.save()
        cr.translate(x, y)

        # Draw the bubble
        cr.new_sub_path()
        cr.arc(width - corner_radius, corner_radius, corner_radius, math.radians(-90), math.radians(0))
        cr.arc(width - corner_radius, height - corner_radius, corner_radius, math.radians(0), math.radians(90))
        cr.arc(corner_radius, height - corner_radius, corner_radius, math.radians(90), math.radians(180))
        cr.arc(corner_radius, corner_radius, corner_radius, math.radians(180), math.radians(270))

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

        if not self._show_offset:
            return
            
        # Paint hilight
        offset = self._selected_offset

        if self.is_sensitive():
            filename = "timezone_%g.png" % offset
        else:
            filename = "timezone_%g_dim.png" % offset

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
            longitude = self._tz_location.get_property('longitude')
            latitude = self._tz_location.get_property('latitude')

            pointx = convert_longitude_to_x(longitude, alloc.width)
            pointy = convert_latitude_to_y(latitude, alloc.height)

            #pointx = clamp(math.floor(pointx), 0, alloc.width)
            #pointy = clamp(math.floor(pointy), 0, alloc.height)
            
            if pointy > alloc.height:
                pointy = alloc.height

            # Draw text bubble
            self.draw_text_bubble(cr, pointx, pointy)

            # Draw pin
            if self._pin is not None:
                Gdk.cairo_set_source_pixbuf(
                    cr,
                    self._pin,
                    pointx - PIN_HOT_POINT_X,
                    pointy - PIN_HOT_POINT_Y)
                cr.paint()

    def set_location(self, tz_location):
        self._tz_location = tz_location
            
        if tz_location is not None:
            info = self._tz_location.get_info()

            daylight_offset = 0

            if self._tz_location.is_dst():
                if info.get_daylight() == 1:
                    daylight_offset = -1.0

            self._selected_offset = tz_location.get_utc_offset().total_seconds() / (60.0 * 60.0) + daylight_offset
            
            self.emit("location-changed", self._tz_location)
            
            self._show_offset = True
        else:
            self._show_offset = False
            self._selected_offset = 0.0

    def get_loc_for_xy(self, x, y):
        rowstride = self._color_map.get_rowstride()
        pixels = self._color_map.get_pixels()
        
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
        
        # Work out the co-ordinates
        allocation = self.get_allocation()
        width = allocation.width
        height = allocation.height
        
        nearest_tz_location = None
                
        # Impossible distance
        small_dist =  -1

        for tz_location in self._tzdb.get_locations():
            longitude = tz_location.get_property('longitude')
            latitude = tz_location.get_property('latitude')

            pointx = convert_longitude_to_x(longitude, width)
            pointy = convert_latitude_to_y(latitude, height)

            dx = pointx - x;
            dy = pointy - y;
            
            dist = dx * dx + dy * dy

            if small_dist == -1 or dist < small_dist:
                nearest_tz_location = tz_location
                small_dist = dist
        
        return nearest_tz_location
        
        
    def do_button_press_event(self, event):
        """ The button press event virtual method """

        # Make sure it was the first button
        if event.button == 1:
            x = int(event.x)
            y = int(event.y)

            nearest_tz_location = self.get_loc_for_xy(x, y)

            if nearest_tz_location is not None:
                self.set_bubble_text(nearest_tz_location)
                self.set_location(nearest_tz_location)
                self.queue_draw()

        return True

    def set_timezone(self, timezone):
        real_tz = self._tzdb.get_loc(timezone)
        
        if real_tz is not None:
            tz_to_compare = real_tz
        else:
            tz_to_compare = timezone

        ret = False

        for tz_location in self._tzdb.get_locations():
            if tz_location.get_property('zone') == tz_to_compare.get_property('zone'):
                self.set_bubble_text(tz_location)
                self.set_location(tz_location)
                ret = True
                break
        
        if ret is True:
            self.queue_draw()
        
        return ret

    def set_bubble_text(self, location):
        city_name = location.get_info().tzname("").split("/")[1]
        city_name = city_name.replace("_", " ")
        country_name = location.get_property('human_country')
        self._bubble_text = "%s, %s" % (city_name, country_name)
        self.queue_draw()
    
    def get_location(self):
        return self._tz_location

    def get_timezone_at_coords(self, longitude, latitude):
        x = int(2048.0 / 360.0 * (180.0 + longitude))
        y = int(1024.0 / 180.0 * (90.0 - latitude))

        olsen_map_channels = self._olsen_map.get_n_channels()
        olsen_map_rowstride = self._olsen_map.get_rowstride()
        olsen_map_pixels = self._olsen_map.get_pixels()

        zone = -1
        offset = olsen_map_rowstride * y + x * olsen_map_channels
        
        if offset < len(olsen_map_pixels):
            color0 = olsen_map_pixels[offset]
            color1 = olsen_map_pixels[offset + 1]
            zone = ((color0 & 248) << 1) + ((color1 >> 4) & 15)

        if zone >= 0 and zone < len(olsen_map_timezones):
            city = olsen_map_timezones[zone]
            return city
        else:
            alloc = self.get_allocation()
            x = convert_longitude_to_x(longitude, alloc.width)
            y = convert_latitude_to_y(latitude, alloc.height)
            location = get_loc_for_xy(x, y)
            zone = location.get_property('zone')
            return zone

'''
      GtkAllocation alloc;
      GValue val_zone = {0};
      g_value_init (&val_zone, G_TYPE_STRING);
      gtk_widget_get_allocation (GTK_WIDGET (map), &alloc);
      x = convert_longtitude_to_x(lon, alloc.width);
      y = convert_latitude_to_y(lat, alloc.height);
      CcTimezoneLocation * loc = get_loc_for_xy(GTK_WIDGET (map), x, y);
      g_value_unset (&val_zone);
      return g_value_get_string(&val_zone);
'''


if __name__ == '__main__':
    win = Gtk.Window()
    tzmap = TimezoneMap()
    win.add(tzmap)
    win.show_all()
    # "Europe/London" +513030-0000731
    timezone = tzmap.get_timezone_at_coords(latitude=51.3030, longitude=-0.00731)
    tzmap.set_timezone(timezone)
    import signal    # enable Ctrl-C since there is no menu to quit
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()
