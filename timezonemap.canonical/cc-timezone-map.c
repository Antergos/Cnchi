/*
 * Copyright (C) 2010 Intel, Inc
 * Copyright (C) 2011 Canonical Ltd.
 *
 * Portions from Ubiquity, Copyright (C) 2009 Canonical Ltd.
 * Written by Evan Dandrea <ev@ubuntu.com>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc., 
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 *
 * Author: Thomas Wood <thomas.wood@intel.com>
 *
 */

#include "cc-timezone-map.h"
#include "cc-timezone-location.h"
#include <math.h>
#include "tz.h"

G_DEFINE_TYPE (CcTimezoneMap, cc_timezone_map, GTK_TYPE_WIDGET)

#define TIMEZONE_MAP_PRIVATE(o) \
  (G_TYPE_INSTANCE_GET_PRIVATE ((o), CC_TYPE_TIMEZONE_MAP, CcTimezoneMapPrivate))


typedef struct
{
  gdouble offset;
  guchar red;
  guchar green;
  guchar blue;
  guchar alpha;
} CcTimezoneMapOffset;

struct _CcTimezoneMapPrivate
{
  GdkPixbuf *orig_background;
  GdkPixbuf *orig_color_map;

  GdkPixbuf *background;
  GdkPixbuf *color_map;
  GdkPixbuf *olsen_map;

  guchar *visible_map_pixels;
  gint visible_map_rowstride;

  gint olsen_map_channels;
  guchar *olsen_map_pixels;
  gint olsen_map_rowstride;

  gdouble selected_offset;
  gboolean show_offset;

  gchar *watermark;

  TzDB *tzdb;
  CcTimezoneLocation *location;
  GHashTable *alias_db;
  GList *distances;

  gint previous_x;
  gint previous_y;
};

enum
{
  LOCATION_CHANGED,
  LAST_SIGNAL
};

enum {
  PROP_0,
  PROP_SELECTED_OFFSET,
};

static guint signals[LAST_SIGNAL];


static CcTimezoneMapOffset color_codes[] =
{
    {-11.0, 43, 0, 0, 255 },
    {-10.0, 85, 0, 0, 255 },
    {-9.5, 102, 255, 0, 255 },
    {-9.0, 128, 0, 0, 255 },
    {-8.0, 170, 0, 0, 255 },
    {-7.0, 212, 0, 0, 255 },
    {-6.0, 255, 0, 1, 255 }, // north
    {-6.0, 255, 0, 0, 255 }, // south
    {-5.0, 255, 42, 42, 255 },
    {-4.5, 192, 255, 0, 255 },
    {-4.0, 255, 85, 85, 255 },
    {-3.5, 0, 255, 0, 255 },
    {-3.0, 255, 128, 128, 255 },
    {-2.0, 255, 170, 170, 255 },
    {-1.0, 255, 213, 213, 255 },
    {0.0, 43, 17, 0, 255 },
    {1.0, 85, 34, 0, 255 },
    {2.0, 128, 51, 0, 255 },
    {3.0, 170, 68, 0, 255 },
    {3.5, 0, 255, 102, 255 },
    {4.0, 212, 85, 0, 255 },
    {4.5, 0, 204, 255, 255 },
    {5.0, 255, 102, 0, 255 },
    {5.5, 0, 102, 255, 255 },
    {5.75, 0, 238, 207, 247 },
    {6.0, 255, 127, 42, 255 },
    {6.5, 204, 0, 254, 254 },
    {7.0, 255, 153, 85, 255 },
    {8.0, 255, 179, 128, 255 },
    {9.0, 255, 204, 170, 255 },
    {9.5, 170, 0, 68, 250 },
    {10.0, 255, 230, 213, 255 },
    {10.5, 212, 124, 21, 250 },
    {11.0, 212, 170, 0, 255 },
    {11.5, 249, 25, 87, 253 },
    {12.0, 255, 204, 0, 255 },
    {12.75, 254, 74, 100, 248 },
    {13.0, 255, 85, 153, 250 },
    {-100, 0, 0, 0, 0 }
};

static const gchar * olsen_map_timezones[] = {
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
    "Pacific/Wallis"
};

static void
cc_timezone_map_get_property (GObject    *object,
                              guint       property_id,
                              GValue     *value,
                              GParamSpec *pspec)
{
  CcTimezoneMap *map = CC_TIMEZONE_MAP(object);
  switch (property_id)
    {
    case PROP_SELECTED_OFFSET:
      g_value_set_double(value, map->priv->selected_offset);
      break;
    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, property_id, pspec);
    }
}

static void
cc_timezone_map_set_property (GObject      *object,
                              guint         property_id,
                              const GValue *value,
                              GParamSpec   *pspec)
{
  CcTimezoneMap *map = CC_TIMEZONE_MAP(object);
  switch (property_id)
    {
    case PROP_SELECTED_OFFSET:
      cc_timezone_map_set_selected_offset(map, g_value_get_double(value));
      break;
    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, property_id, pspec);
    }
}

static void
cc_timezone_map_dispose (GObject *object)
{
  CcTimezoneMapPrivate *priv = CC_TIMEZONE_MAP (object)->priv;

  if (priv->orig_background)
    {
      g_object_unref (priv->orig_background);
      priv->orig_background = NULL;
    }

  if (priv->orig_color_map)
    {
      g_object_unref (priv->orig_color_map);
      priv->orig_color_map = NULL;
    }

  if (priv->olsen_map)
    {
      g_object_unref (priv->olsen_map);
      priv->olsen_map = NULL;

      priv->olsen_map_channels = 0;
      priv->olsen_map_pixels = NULL;
      priv->olsen_map_rowstride = 0;
    }

  if (priv->background)
    {
      g_object_unref (priv->background);
      priv->background = NULL;
    }

  if (priv->color_map)
    {
      g_object_unref (priv->color_map);
      priv->color_map = NULL;

      priv->visible_map_pixels = NULL;
      priv->visible_map_rowstride = 0;
    }

  if (priv->alias_db)
    {
      g_hash_table_destroy (priv->alias_db);
      priv->alias_db = NULL;
    }
  if (priv->distances)
    {
      g_list_free (priv->distances);
      priv->distances = NULL;
    }

  if (priv->watermark)
    {
      g_free (priv->watermark);
      priv->watermark = NULL;
    }

  G_OBJECT_CLASS (cc_timezone_map_parent_class)->dispose (object);
}

static void
cc_timezone_map_finalize (GObject *object)
{
  CcTimezoneMapPrivate *priv = CC_TIMEZONE_MAP (object)->priv;

  if (priv->tzdb)
    {
      tz_db_free (priv->tzdb);
      priv->tzdb = NULL;
    }


  G_OBJECT_CLASS (cc_timezone_map_parent_class)->finalize (object);
}

/* GtkWidget functions */
static void
cc_timezone_map_get_preferred_width (GtkWidget *widget,
                                     gint      *minimum,
                                     gint      *natural)
{
  /* choose a minimum size small enough to prevent the window
   * from growing horizontally
   */
  if (minimum != NULL)
    *minimum = 300;
  if (natural != NULL)
    *natural = 300;
}

static void
cc_timezone_map_get_preferred_height (GtkWidget *widget,
                                      gint      *minimum,
                                      gint      *natural)
{
  CcTimezoneMapPrivate *priv = CC_TIMEZONE_MAP (widget)->priv;
  gint size;

  /* The + 20 here is a slight tweak to make the map fill the
   * panel better without causing horizontal growing
   */
  size = 300 * gdk_pixbuf_get_height (priv->orig_background) / gdk_pixbuf_get_width (priv->orig_background) + 20;
  if (minimum != NULL)
    *minimum = size;
  if (natural != NULL)
    *natural = size;
}

static void
cc_timezone_map_size_allocate (GtkWidget     *widget,
                               GtkAllocation *allocation)
{
  CcTimezoneMapPrivate *priv = CC_TIMEZONE_MAP (widget)->priv;

  if (priv->background)
    g_object_unref (priv->background);

  priv->background = gdk_pixbuf_scale_simple (priv->orig_background,
                                              allocation->width,
                                              allocation->height,
                                              GDK_INTERP_BILINEAR);

  if (priv->color_map)
    g_object_unref (priv->color_map);

  priv->color_map = gdk_pixbuf_scale_simple (priv->orig_color_map,
                                             allocation->width,
                                             allocation->height,
                                             GDK_INTERP_BILINEAR);

  priv->visible_map_pixels = gdk_pixbuf_get_pixels (priv->color_map);
  priv->visible_map_rowstride = gdk_pixbuf_get_rowstride (priv->color_map);

  GTK_WIDGET_CLASS (cc_timezone_map_parent_class)->size_allocate (widget,
                                                                  allocation);
}

static void
cc_timezone_map_realize (GtkWidget *widget)
{
  GdkWindowAttr attr = { 0, };
  GtkAllocation allocation;
  GdkCursor *cursor;
  GdkWindow *window;

  gtk_widget_get_allocation (widget, &allocation);

  gtk_widget_set_realized (widget, TRUE);

  attr.window_type = GDK_WINDOW_CHILD;
  attr.wclass = GDK_INPUT_OUTPUT;
  attr.width = allocation.width;
  attr.height = allocation.height;
  attr.x = allocation.x;
  attr.y = allocation.y;
  attr.event_mask = gtk_widget_get_events (widget)
                                 | GDK_EXPOSURE_MASK | GDK_BUTTON_PRESS_MASK;

  window = gdk_window_new (gtk_widget_get_parent_window (widget), &attr,
                           GDK_WA_X | GDK_WA_Y);

  gdk_window_set_user_data (window, widget);

  cursor = gdk_cursor_new (GDK_HAND2);
  gdk_window_set_cursor (window, cursor);

  gtk_widget_set_window (widget, window);
}


static gdouble
convert_longtitude_to_x (gdouble longitude, gint map_width)
{
  const gdouble xdeg_offset = -6;
  gdouble x;

  x = (map_width * (180.0 + longitude) / 360.0)
    + (map_width * xdeg_offset / 180.0);

  return x;
}

static gdouble
radians (gdouble degrees)
{
  return (degrees / 360.0) * G_PI * 2;
}

static gdouble
convert_latitude_to_y (gdouble latitude, gdouble map_height)
{
  gdouble bottom_lat = -59;
  gdouble top_lat = 81;
  gdouble top_per, y, full_range, top_offset, map_range;

  top_per = top_lat / 180.0;
  y = 1.25 * log (tan (G_PI_4 + 0.4 * radians (latitude)));
  full_range = 4.6068250867599998;
  top_offset = full_range * top_per;
  map_range = fabs (1.25 * log (tan (G_PI_4 + 0.4 * radians (bottom_lat))) - top_offset);
  y = fabs (y - top_offset);
  y = y / map_range;
  y = y * map_height;
  return y;
}


static gboolean
cc_timezone_map_draw (GtkWidget *widget,
                      cairo_t   *cr)
{
  CcTimezoneMapPrivate *priv = CC_TIMEZONE_MAP (widget)->priv;
  GdkPixbuf *hilight, *orig_hilight, *pin;
  GtkAllocation alloc;
  gchar *file;
  GError *err = NULL;
  gdouble pointx, pointy;
  gdouble alpha = 1.0;
  GtkStyle *style;
  char buf[16];

  gtk_widget_get_allocation (widget, &alloc);

  style = gtk_widget_get_style (widget);

  /* Check if insensitive */
  if (gtk_widget_get_state (widget) == GTK_STATE_INSENSITIVE)
    alpha = 0.5;

  /* paint background */
  gdk_cairo_set_source_color (cr, &style->bg[gtk_widget_get_state (widget)]);
  cairo_paint (cr);
  gdk_cairo_set_source_pixbuf (cr, priv->background, 0, 0);
  cairo_paint_with_alpha (cr, alpha);

  /* paint watermark */
  if (priv->watermark) {
    cairo_text_extents_t extent;
    cairo_select_font_face(cr, "Sans", CAIRO_FONT_SLANT_NORMAL, CAIRO_FONT_WEIGHT_NORMAL);
    cairo_set_font_size(cr, 12.0);
    cairo_set_source_rgba(cr, 1, 1, 1, 0.5);
    cairo_text_extents(cr, priv->watermark, &extent);
    cairo_move_to(cr, alloc.width - extent.x_advance + extent.x_bearing - 5,
                      alloc.height - extent.height - extent.y_bearing - 5);
    cairo_show_text(cr, priv->watermark);
    cairo_stroke(cr);
  }

  if (!priv->show_offset) {
    return TRUE;
  }

  /* paint hilight */
  file = g_strdup_printf (DATADIR "/timezone_%s.png",
                          g_ascii_formatd (buf, sizeof (buf),
                                           "%g", priv->selected_offset));
  orig_hilight = gdk_pixbuf_new_from_file (file, &err);
  g_free (file);
  file = NULL;

  if (!orig_hilight)
    {
      g_warning ("Could not load hilight: %s",
                 (err) ? err->message : "Unknown Error");
      if (err)
        g_clear_error (&err);
    }
  else
    {

      hilight = gdk_pixbuf_scale_simple (orig_hilight, alloc.width,
                                         alloc.height, GDK_INTERP_BILINEAR);
      gdk_cairo_set_source_pixbuf (cr, hilight, 0, 0);

      cairo_paint_with_alpha (cr, alpha);
      g_object_unref (hilight);
      g_object_unref (orig_hilight);
    }

  if (!priv->location) {
    return TRUE;
  }

  /* load pin icon */
  pin = gdk_pixbuf_new_from_file (DATADIR "/pin.png", &err);

  if (err)
    {
      g_warning ("Could not load pin icon: %s", err->message);
      g_clear_error (&err);
    }

  pointx = convert_longtitude_to_x (
          cc_timezone_location_get_longitude(priv->location), alloc.width);
  pointy = convert_latitude_to_y (
          cc_timezone_location_get_latitude(priv->location), alloc.height);

  if (pointy > alloc.height)
    pointy = alloc.height;

  if (pin)
    {
      gdk_cairo_set_source_pixbuf (cr, pin, pointx - 8, pointy - 14);
      cairo_paint_with_alpha (cr, alpha);
      g_object_unref (pin);
    }

  return TRUE;
}

static void
cc_timezone_map_class_init (CcTimezoneMapClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  g_type_class_add_private (klass, sizeof (CcTimezoneMapPrivate));

  object_class->get_property = cc_timezone_map_get_property;
  object_class->set_property = cc_timezone_map_set_property;
  object_class->dispose = cc_timezone_map_dispose;
  object_class->finalize = cc_timezone_map_finalize;

  widget_class->get_preferred_width = cc_timezone_map_get_preferred_width;
  widget_class->get_preferred_height = cc_timezone_map_get_preferred_height;
  widget_class->size_allocate = cc_timezone_map_size_allocate;
  widget_class->realize = cc_timezone_map_realize;
  widget_class->draw = cc_timezone_map_draw;

  g_object_class_install_property(G_OBJECT_CLASS(klass),
                                  PROP_SELECTED_OFFSET,
                                  g_param_spec_string ("selected-offset",
                                      "Selected offset",
                                      "The selected offset from GMT in hours",
                                      "",
                                      G_PARAM_READWRITE));

  signals[LOCATION_CHANGED] = g_signal_new ("location-changed",
                                            CC_TYPE_TIMEZONE_MAP,
                                            G_SIGNAL_RUN_FIRST,
                                            0,
                                            NULL,
                                            NULL,
                                            g_cclosure_marshal_VOID__OBJECT,
                                            G_TYPE_NONE, 1,
                                            CC_TYPE_TIMEZONE_LOCATION);
}


static gint
sort_locations (CcTimezoneLocation *a,
                CcTimezoneLocation *b)
{
  gdouble dist_a, dist_b;
  dist_a = cc_timezone_location_get_dist(a);
  dist_b = cc_timezone_location_get_dist(b);
  if (dist_a > dist_b)
    return 1;

  if (dist_a < dist_b)
    return -1;

  return 0;
}

static void
set_location (CcTimezoneMap *map,
              CcTimezoneLocation    *location)
{
  CcTimezoneMapPrivate *priv = map->priv;
  TzInfo *info;

  priv->location = location;

  if (priv->location)
  {
    info = tz_info_from_location (priv->location);
    priv->selected_offset = tz_location_get_utc_offset (priv->location)
        / (60.0*60.0) + ((info->daylight) ? -1.0 : 0.0);
    priv->show_offset = TRUE;
    tz_info_free (info);
  }
  else
  {
    priv->show_offset = FALSE;
    priv->selected_offset = 0.0;
  }

  g_signal_emit (map, signals[LOCATION_CHANGED], 0, priv->location);

}

static CcTimezoneLocation *
get_loc_for_xy (GtkWidget * widget, gint x, gint y)
{
  CcTimezoneMapPrivate *priv = CC_TIMEZONE_MAP (widget)->priv;
  guchar r, g, b, a;
  guchar *pixels;
  gint rowstride;
  gint i;

  const GPtrArray *array;
  gint width, height;
  GtkAllocation alloc;
  CcTimezoneLocation* location;

  rowstride = priv->visible_map_rowstride;
  pixels = priv->visible_map_pixels;

  r = pixels[(rowstride * y + x * 4)];
  g = pixels[(rowstride * y + x * 4) + 1];
  b = pixels[(rowstride * y + x * 4) + 2];
  a = pixels[(rowstride * y + x * 4) + 3];


  if ((x - priv->previous_x < 5 && x - priv->previous_x > -5) &&
      (y - priv->previous_y < 5 && y - priv->previous_y > -5)) {
    x = priv->previous_x;
    y = priv->previous_y;
  }
  for (i = 0; color_codes[i].offset != -100; i++)
    {
       if (color_codes[i].red == r && color_codes[i].green == g
           && color_codes[i].blue == b && color_codes[i].alpha == a)
         {
           priv->selected_offset = color_codes[i].offset;
         }
    }

  gtk_widget_queue_draw (widget);

  /* work out the co-ordinates */

  array = tz_get_locations (priv->tzdb);

  gtk_widget_get_allocation (widget, &alloc);
  width = alloc.width;
  height = alloc.height;

  if (x == priv->previous_x && y == priv->previous_y) 
    {
      priv->distances = g_list_next (priv->distances);
      location = (CcTimezoneLocation*) priv->distances->data;
    } else {
      g_list_free (priv->distances);
      priv->distances = NULL;
      for (i = 0; i < array->len; i++)
        {
          gdouble pointx, pointy, dx, dy;
          CcTimezoneLocation *loc = array->pdata[i];

          pointx = convert_longtitude_to_x (cc_timezone_location_get_longitude(loc), width);
          pointy = convert_latitude_to_y (cc_timezone_location_get_latitude(loc), height);

          dx = pointx - x;
          dy = pointy - y;

          cc_timezone_location_set_dist(loc, (gdouble) dx * dx + dy * dy);
          priv->distances = g_list_prepend (priv->distances, loc);
        }
      priv->distances = g_list_sort (priv->distances, (GCompareFunc) sort_locations);
      location = (CcTimezoneLocation*) priv->distances->data;
      priv->previous_x = x;
      priv->previous_y = y;
    }

    return location;
}

static gboolean
button_press_event (GtkWidget      *widget,
                    GdkEventButton *event)
{
  CcTimezoneLocation * loc = get_loc_for_xy (widget, event->x, event->y);
  set_location (CC_TIMEZONE_MAP (widget), loc);
  return TRUE;
}

static void
state_flags_changed (GtkWidget *widget)
{
  // To catch sensitivity changes
  gtk_widget_queue_draw (widget);
}

static void
load_backward_tz (CcTimezoneMap *self)
{
  GError *error = NULL;
  char **lines, *contents;
  guint i;

  self->priv->alias_db = g_hash_table_new_full (g_str_hash, g_str_equal, g_free, g_free);

  if (g_file_get_contents (GNOMECC_DATA_DIR "/backward", &contents, NULL, &error) == FALSE)
    {
      g_warning ("Failed to load 'backward' file: %s", error->message);
      return;
    }
  lines = g_strsplit (contents, "\n", -1);
  g_free (contents);
  for (i = 0; lines[i] != NULL; i++)
    {
      char **items;
      guint j;
      char *real, *alias;

      if (g_ascii_strncasecmp (lines[i], "Link\t", 5) != 0)
        continue;

      items = g_strsplit (lines[i], "\t", -1);
      real = NULL;
      alias = NULL;
      /* Skip the "Link<tab>" part */
      for (j = 1; items[j] != NULL; j++)
        {
          if (items[j][0] == '\0')
            continue;
          if (real == NULL)
            {
              real = items[j];
              continue;
            }
          alias = items[j];
          break;
        }

      if (real == NULL || alias == NULL)
        g_warning ("Could not parse line: %s", lines[i]);

      g_hash_table_insert (self->priv->alias_db, g_strdup (alias), g_strdup (real));
      g_strfreev (items);
    }
  g_strfreev (lines);
}

static void
cc_timezone_map_init (CcTimezoneMap *self)
{
  CcTimezoneMapPrivate *priv;
  GError *err = NULL;

  priv = self->priv = TIMEZONE_MAP_PRIVATE (self);

  priv->previous_x = -1;
  priv->previous_y = -1;

  priv->orig_background = gdk_pixbuf_new_from_file (DATADIR "/bg.png",
                                                    &err);

  if (!priv->orig_background)
    {
      g_warning ("Could not load background image: %s",
                 (err) ? err->message : "Unknown error");
      g_clear_error (&err);
    }

  priv->orig_color_map = gdk_pixbuf_new_from_file (DATADIR "/cc.png",
                                                   &err);
  if (!priv->orig_color_map)
    {
      g_warning ("Could not load background image: %s",
                 (err) ? err->message : "Unknown error");
      g_clear_error (&err);
    }

  priv->olsen_map = gdk_pixbuf_new_from_file (DATADIR "/olsen_map.png",
                                              &err);
  if (!priv->olsen_map)
    {
      g_warning ("Could not load olsen map: %s",
                 (err) ? err->message : "Unknown error");
      g_clear_error (&err);
    }
  priv->olsen_map_channels = gdk_pixbuf_get_n_channels (priv->olsen_map);
  priv->olsen_map_pixels = gdk_pixbuf_get_pixels (priv->olsen_map);
  priv->olsen_map_rowstride = gdk_pixbuf_get_rowstride (priv->olsen_map);

  priv->selected_offset = 0.0;
  priv->show_offset = FALSE;

  priv->tzdb = tz_load_db ();

  g_signal_connect (self, "button-press-event", G_CALLBACK (button_press_event),
                    NULL);
  g_signal_connect (self, "state-flags-changed", G_CALLBACK (state_flags_changed),
                    NULL);

  load_backward_tz (self);
}

CcTimezoneMap *
cc_timezone_map_new (void)
{
  return g_object_new (CC_TYPE_TIMEZONE_MAP, NULL);
}

void
cc_timezone_map_set_timezone (CcTimezoneMap *map,
                              const gchar   *timezone)
{
  GPtrArray *locations;
  guint i;
  char *real_tz;

  real_tz = g_hash_table_lookup (map->priv->alias_db, timezone);

  locations = tz_get_locations (map->priv->tzdb);

  for (i = 0; i < locations->len; i++)
    {
      CcTimezoneLocation *loc = locations->pdata[i];

      if (!g_strcmp0 (cc_timezone_location_get_zone(loc), real_tz ? real_tz : timezone))
        {
          set_location (map, loc);
          break;
        }
    }

  gtk_widget_queue_draw (GTK_WIDGET (map));
}

void
cc_timezone_map_set_location (CcTimezoneMap *map,
			      gdouble lon,
			      gdouble lat)
{
  GtkAllocation alloc;
  gtk_widget_get_allocation (GTK_WIDGET(map), &alloc);
  gdouble x = convert_longtitude_to_x(lon, alloc.width);
  gdouble y = convert_latitude_to_y(lat, alloc.height);
  CcTimezoneLocation * loc = get_loc_for_xy (GTK_WIDGET(map), x, y);
  set_location (map, loc);
}

void
cc_timezone_map_set_coords (CcTimezoneMap *map, gdouble lon, gdouble lat)
{
  const gchar * zone = cc_timezone_map_get_timezone_at_coords (map, lon, lat);
  cc_timezone_map_set_timezone (map, zone);
}

const gchar *
cc_timezone_map_get_timezone_at_coords (CcTimezoneMap *map, gdouble lon, gdouble lat)
{
  gint x = (int)(2048.0 / 360.0 * (180.0 + lon));
  gint y = (int)(1024.0 / 180.0 * (90.0 - lat));
  gint offset = map->priv->olsen_map_rowstride * y + x * map->priv->olsen_map_channels;
  guchar color0 = map->priv->olsen_map_pixels[offset];
  guchar color1 = map->priv->olsen_map_pixels[offset + 1];
  gint zone = ((color0 & 248) << 1) + ((color1 >>4) & 15);

  const gchar * city = NULL;
  if (zone < G_N_ELEMENTS(olsen_map_timezones))
    city = olsen_map_timezones[zone];

  if (city != NULL)
    {
      return city;
    } else {
      GtkAllocation alloc;
      GValue val_zone = {0};
      g_value_init (&val_zone, G_TYPE_STRING);
      gtk_widget_get_allocation (GTK_WIDGET (map), &alloc);
      x = convert_longtitude_to_x(lon, alloc.width);
      y = convert_latitude_to_y(lat, alloc.height);
      CcTimezoneLocation * loc = get_loc_for_xy(GTK_WIDGET (map), x, y);
      g_value_unset (&val_zone);
      return g_value_get_string(&val_zone);
    }
}

void
cc_timezone_map_set_watermark (CcTimezoneMap *map, const gchar * watermark)
{
  if (map->priv->watermark)
    g_free (map->priv->watermark);

  map->priv->watermark = g_strdup (watermark);
  gtk_widget_queue_draw (GTK_WIDGET (map));
}

/**
 * cc_timezone_map_get_location:
 * @map: A #CcTimezoneMap
 *
 * Returns the current location set for the map.
 *
 * Returns: (transfer none): the map location.
 */
CcTimezoneLocation *
cc_timezone_map_get_location (CcTimezoneMap *map)
{
  return map->priv->location;
}

/**
 * cc_timezone_map_clear_location:
 * @map: A #CcTimezoneMap
 *
 * Clear the location currently set for the #CcTimezoneMap. This will remove
 * the highlight and reset the map to its original state.
 *
 */
void
cc_timezone_map_clear_location (CcTimezoneMap *map)
{
  set_location(map, NULL);
  gtk_widget_queue_draw (GTK_WIDGET (map));
}

/**
 * cc_timezone_map_get_selected_offset:
 * @map: A #CcTimezoneMap
 *
 * Returns the currently selected offset in hours from GMT.
 *
 * Returns: The selected offset.
 *
 */
gdouble cc_timezone_map_get_selected_offset(CcTimezoneMap *map)
{
  return map->priv->selected_offset;
}

/**
 * cc_timezone_map_set_selected_offset:
 * @map: A #CcTimezoneMap
 * @offset: The offset from GMT in hours
 *
 * Set the currently selected offset for the map and redraw the highlighted
 * time zone.
 */
void cc_timezone_map_set_selected_offset (CcTimezoneMap *map, gdouble offset)
{
  map->priv->selected_offset = offset;
  map->priv->show_offset = TRUE;
  g_object_notify(G_OBJECT(map), "selected-offset");
  gtk_widget_queue_draw (GTK_WIDGET (map));
}
