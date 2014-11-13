/* -*- Mode: C; tab-width: 8; indent-tabs-mode: t; c-basic-offset: 8 -*- */
/* Generic timezone utilities.
 *
 * Copyright (C) 2000-2001 Ximian, Inc.
 *
 * Authors: Hans Petter Jansson <hpj@ximian.com>
 * 
 * Largely based on Michael Fulbright's work on Anaconda.
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
 */


#ifndef _E_TZ_H
#define _E_TZ_H

#include <glib.h>

#include "cc-timezone-location.h"

#ifndef __sun
#  define TZ_DATA_FILE "/usr/share/libtimezonemap/ui/cities15000.txt"
#else
#  define TZ_DATA_FILE "/usr/share/lib/zoneinfo/tab/zone_sun.tab"
#endif

# define ADMIN1_FILE "/usr/share/libtimezonemap/ui/admin1Codes.txt"
# define COUNTRY_FILE "/usr/share/libtimezonemap/ui/countryInfo.txt"

G_BEGIN_DECLS

typedef struct _TzDB TzDB;
typedef struct _TzInfo TzInfo;

struct _TzDB
{
	GPtrArray *locations;
};


/* see the glibc info page information on time zone information */
/*  tzname_normal    is the default name for the timezone */
/*  tzname_daylight  is the name of the zone when in daylight savings */
/*  utc_offset       is offset in seconds from utc */
/*  daylight         if non-zero then location obeys daylight savings */

struct _TzInfo
{
	gchar *tzname_normal;
	gchar *tzname_daylight;
	glong utc_offset;
	gint daylight;
};


TzDB      *tz_load_db                 (void);
void       tz_db_free                 (TzDB *db);
GPtrArray *tz_get_locations           (TzDB *db);
glong      tz_location_get_utc_offset (CcTimezoneLocation *loc);
gint       tz_location_set_locally    (CcTimezoneLocation *loc);
TzInfo    *tz_info_from_location      (CcTimezoneLocation *loc);
void       tz_info_free               (TzInfo *tz_info);

G_END_DECLS

#endif
