/* -*- Mode: C; tab-width: 8; indent-tabs-mode: t; c-basic-offset: 8 -*- */
/* Timezone location information
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
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
 */

#ifndef _CC_TIMEZONE_LOCATION_H
#define _CC_TIMEZONE_LOCATION_H

#include <glib.h>
#include <glib-object.h>

G_BEGIN_DECLS

#define CC_TYPE_TIMEZONE_LOCATION cc_timezone_location_get_type()

#define CC_TIMEZONE_LOCATION(obj) \
  (G_TYPE_CHECK_INSTANCE_CAST ((obj), \
  CC_TYPE_TIMEZONE_LOCATION, CcTimezoneLocation))

#define CC_TIMEZONE_LOCATION_CLASS(klass) \
  (G_TYPE_CHECK_CLASS_CAST ((klass), \
  CC_TYPE_TIMEZONE_LOCATION, CcTimezoneLocationClass))

#define CC_IS_TIMEZONE_LOCATION(obj) \
  (G_TYPE_CHECK_INSTANCE_TYPE ((obj), \
  CC_TYPE_TIMEZONE_LOCATION))

#define CC_IS_TIMEZONE_LOCATION_CLASS(klass) \
  (G_TYPE_CHECK_CLASS_TYPE ((klass), \
  CC_TYPE_TIMEZONE_LOCATION))

#define CC_TIMEZONE_LOCATION_GET_CLASS(obj) \
  (G_TYPE_INSTANCE_GET_CLASS ((obj), \
  CC_TYPE_TIMEZONE_LOCATION, CcTimezoneLocationClass))

typedef struct _CcTimezoneLocation CcTimezoneLocation;
typedef struct _CcTimezoneLocationClass CcTimezoneLocationClass;
typedef struct _CcTimezoneLocationPrivate CcTimezoneLocationPrivate;

struct _CcTimezoneLocation
{
  GObject parent;
  CcTimezoneLocationPrivate *priv;
};

struct _CcTimezoneLocationClass
{
  GObjectClass parent_class;
};

GType cc_timezone_location_get_type (void) G_GNUC_CONST;

CcTimezoneLocation *cc_timezone_location_new (void);

const gchar *cc_timezone_location_get_country(CcTimezoneLocation *loc);
void cc_timezone_location_set_country(CcTimezoneLocation *loc, const gchar *country);
const gchar *cc_timezone_location_get_full_country(CcTimezoneLocation *loc);
void cc_timezone_location_set_full_country(CcTimezoneLocation *loc, const gchar *full_country);
const gchar *cc_timezone_location_get_en_name(CcTimezoneLocation *loc);
void cc_timezone_location_set_en_name(CcTimezoneLocation *loc, const gchar *en_name);
const gchar *cc_timezone_location_get_state(CcTimezoneLocation *loc);
void cc_timezone_location_set_state(CcTimezoneLocation *loc, const gchar *state);
gdouble cc_timezone_location_get_latitude(CcTimezoneLocation *loc);
void cc_timezone_location_set_latitude(CcTimezoneLocation *loc, gdouble lat);
gdouble cc_timezone_location_get_longitude(CcTimezoneLocation *loc);
void cc_timezone_location_set_longitude(CcTimezoneLocation *loc, gdouble lng);
const gchar *cc_timezone_location_get_zone(CcTimezoneLocation *loc);
void cc_timezone_location_set_zone(CcTimezoneLocation *loc, const gchar *zone);
const gchar *cc_timezone_location_get_comment(CcTimezoneLocation *loc);
void cc_timezone_location_set_comment(CcTimezoneLocation *loc, const gchar *comment);
gdouble cc_timezone_location_get_dist(CcTimezoneLocation *loc);
void cc_timezone_location_set_dist(CcTimezoneLocation *loc, gdouble dist);

G_END_DECLS

#endif /* _CC_TIMEZONE_LOCATION_H */
