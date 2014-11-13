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
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
 */

#include "cc-timezone-location.h"

G_DEFINE_TYPE (CcTimezoneLocation, cc_timezone_location, G_TYPE_OBJECT)

#define TIMEZONE_LOCATION_PRIVATE(o) \
  (G_TYPE_INSTANCE_GET_PRIVATE ((o), CC_TYPE_TIMEZONE_LOCATION, CcTimezoneLocationPrivate))

struct _CcTimezoneLocationPrivate
{
    gchar *country;
    gchar *full_country;
    gchar *en_name;
    gchar *state;
    gdouble latitude;
    gdouble longitude;
    gchar *zone;
    gchar *comment;

    gdouble dist; /* distance to clicked point for comparison */
};

enum {
  PROP_0,
  PROP_COUNTRY,
  PROP_FULL_COUNTRY,
  PROP_EN_NAME,
  PROP_STATE,
  PROP_LATITUDE,
  PROP_LONGITUDE,
  PROP_ZONE,
  PROP_COMMENT,
  PROP_DIST,
};

static void
cc_timezone_location_get_property (GObject    *object,
                              guint       property_id,
                              GValue     *value,
                              GParamSpec *pspec)
{
  CcTimezoneLocationPrivate *priv = CC_TIMEZONE_LOCATION (object)->priv;
  switch (property_id) {
    case PROP_COUNTRY:
      g_value_set_string (value, priv->country);
      break;
    case PROP_FULL_COUNTRY:
      g_value_set_string (value, priv->full_country);
      break;
    case PROP_EN_NAME:
      g_value_set_string (value, priv->en_name);
      break;
    case PROP_STATE:
      g_value_set_string (value, priv->state);
      break;
    case PROP_LATITUDE:
      g_value_set_double (value, priv->latitude);
      break;
    case PROP_LONGITUDE:
      g_value_set_double (value, priv->longitude);
      break;
    case PROP_ZONE:
      g_value_set_string (value, priv->zone);
      break;
    case PROP_COMMENT:
      g_value_set_string (value, priv->comment);
      break;
    case PROP_DIST:
      g_value_set_double (value, priv->dist);
      break;
    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, property_id, pspec);
    }
}

static void
cc_timezone_location_set_property (GObject      *object,
                              guint         property_id,
                              const GValue *value,
                              GParamSpec   *pspec)
{
  CcTimezoneLocation *loc = CC_TIMEZONE_LOCATION(object);
  switch (property_id) {
    case PROP_COUNTRY:
      cc_timezone_location_set_country(loc, g_value_get_string(value));
      break;
    case PROP_FULL_COUNTRY:
      cc_timezone_location_set_full_country(loc, g_value_get_string(value));
      break;
    case PROP_EN_NAME:
      cc_timezone_location_set_en_name(loc, g_value_get_string(value));
      break;
    case PROP_STATE:
      cc_timezone_location_set_state(loc, g_value_get_string(value));
      break;
    case PROP_LATITUDE:
      cc_timezone_location_set_latitude(loc, g_value_get_double(value));
      break;
    case PROP_LONGITUDE:
      cc_timezone_location_set_longitude(loc, g_value_get_double(value));
      break;
    case PROP_ZONE:
      cc_timezone_location_set_zone(loc, g_value_get_string(value));
      break;
    case PROP_COMMENT:
      cc_timezone_location_set_comment(loc, g_value_get_string(value));
      break;
    case PROP_DIST:
      cc_timezone_location_set_dist(loc, g_value_get_double(value));
      break;
    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, property_id, pspec);
    }
}

static void
cc_timezone_location_dispose (GObject *object)
{
  CcTimezoneLocationPrivate *priv = CC_TIMEZONE_LOCATION (object)->priv;

  if (priv->country) 
    {
      g_free (priv->country);
      priv->country = NULL;
    }

  if (priv->full_country) 
    {
      g_free (priv->full_country);
      priv->full_country = NULL;
    }

  if (priv->en_name)
    {
      g_free (priv->en_name);
      priv->en_name = NULL;
    }

  if (priv->state) 
    {
      g_free (priv->state);
      priv->state = NULL;
    }

  if (priv->zone) 
    {
      g_free (priv->zone);
      priv->zone = NULL;
    }

  if (priv->comment) 
    {
      g_free (priv->comment);
      priv->comment = NULL;
    }

  G_OBJECT_CLASS (cc_timezone_location_parent_class)->dispose (object);
}

static void
cc_timezone_location_finalize (GObject *object)
{
  CcTimezoneLocationPrivate *priv = CC_TIMEZONE_LOCATION (object)->priv;
  G_OBJECT_CLASS (cc_timezone_location_parent_class)->finalize (object);
}

static void
cc_timezone_location_class_init (CcTimezoneLocationClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  g_type_class_add_private (klass, sizeof (CcTimezoneLocationPrivate));

  object_class->get_property = cc_timezone_location_get_property;
  object_class->set_property = cc_timezone_location_set_property;
  object_class->dispose = cc_timezone_location_dispose;
  object_class->finalize = cc_timezone_location_finalize;

  g_object_class_install_property(object_class,
                                  PROP_COUNTRY,
                                  g_param_spec_string ("country",
                                          "Country",
                                          "The country for the location",
                                          "",
                                          G_PARAM_READWRITE));
  g_object_class_install_property(object_class,
                                  PROP_FULL_COUNTRY,
                                  g_param_spec_string ("full_country",
                                          "Country (full name)",
                                          "The full country name",
                                          "",
                                          G_PARAM_READWRITE));
  g_object_class_install_property(object_class,
                                  PROP_EN_NAME,
                                  g_param_spec_string ("en_name",
                                          "English Name",
                                          "The name of the location",
                                          "",
                                          G_PARAM_READWRITE));
  g_object_class_install_property(object_class,
                                  PROP_STATE,
                                  g_param_spec_string ("state",
                                          "State",
                                          "The state for the location",
                                          "",
                                          G_PARAM_READWRITE));
  g_object_class_install_property(object_class,
                                  PROP_LATITUDE,
                                  g_param_spec_double ("latitude",
                                          "Latitude",
                                          "The latitude for the location",
                                          -90.0,
                                          90.0,
                                          0.0,
                                          G_PARAM_READWRITE));
  g_object_class_install_property(object_class,
                                  PROP_LONGITUDE,
                                  g_param_spec_double ("longitude",
                                          "Longitude",
                                          "The longitude for the location",
                                          -180.0,
                                          180.0,
                                          0.0,
                                          G_PARAM_READWRITE));
  g_object_class_install_property(object_class,
                                  PROP_ZONE,
                                  g_param_spec_string ("zone",
                                          "Zone",
                                          "The time zone for the location",
                                          "",
                                          G_PARAM_READWRITE));
  g_object_class_install_property(object_class,
                                  PROP_COMMENT,
                                  g_param_spec_string ("Comment",
                                          "Comment",
                                          "A comment for the location",
                                          "",
                                          G_PARAM_READWRITE));
  g_object_class_install_property(object_class,
                                  PROP_DIST,
                                  g_param_spec_double ("dist",
                                          "Distance",
                                          "The distance for the location",
                                          0.0,
                                          DBL_MAX,
                                          0.0,
                                          G_PARAM_READWRITE));
}

static void
cc_timezone_location_init (CcTimezoneLocation *self) {
  CcTimezoneLocationPrivate *priv;
  priv = self->priv = TIMEZONE_LOCATION_PRIVATE (self);
}

CcTimezoneLocation *
cc_timezone_location_new (void)
{
  return g_object_new (CC_TYPE_TIMEZONE_LOCATION, NULL);
}

const gchar *cc_timezone_location_get_country(CcTimezoneLocation *loc)
{
    return loc->priv->country;
}

void cc_timezone_location_set_country(CcTimezoneLocation *loc, const gchar *country)
{
    g_free(loc->priv->country);
    loc->priv->country = g_strdup(country);

    g_object_notify(G_OBJECT(loc), "country");
}

const gchar *cc_timezone_location_get_full_country(CcTimezoneLocation *loc)
{
    return loc->priv->full_country;
}

void cc_timezone_location_set_full_country(CcTimezoneLocation *loc, const gchar *full_country)
{
    g_free(loc->priv->full_country);
    loc->priv->full_country = g_strdup(full_country);

    g_object_notify(G_OBJECT(loc), "full_country");
}

const gchar *cc_timezone_location_get_en_name(CcTimezoneLocation *loc)
{
    return loc->priv->en_name;
}

void cc_timezone_location_set_en_name(CcTimezoneLocation *loc, const gchar *en_name)
{
    g_free(loc->priv->en_name);
    loc->priv->en_name = g_strdup(en_name);

    g_object_notify(G_OBJECT(loc), "en_name");
}

const gchar *cc_timezone_location_get_state(CcTimezoneLocation *loc)
{
    return loc->priv->state;
}

void cc_timezone_location_set_state(CcTimezoneLocation *loc, const gchar *state)
{
    g_free(loc->priv->state);
    loc->priv->state = g_strdup(state);

    g_object_notify(G_OBJECT(loc), "state");
}

gdouble cc_timezone_location_get_latitude(CcTimezoneLocation *loc)
{
    return loc->priv->latitude;
}

void cc_timezone_location_set_latitude(CcTimezoneLocation *loc, gdouble lat)
{
    loc->priv->latitude = lat;
    g_object_notify(G_OBJECT(loc), "latitude");
}

gdouble cc_timezone_location_get_longitude(CcTimezoneLocation *loc)
{
    return loc->priv->longitude;
}

void cc_timezone_location_set_longitude(CcTimezoneLocation *loc, gdouble lng)
{
    loc->priv->longitude = lng;
    g_object_notify(G_OBJECT(loc), "longitude");
}

const gchar *cc_timezone_location_get_zone(CcTimezoneLocation *loc)
{
    return loc->priv->zone;
}

void cc_timezone_location_set_zone(CcTimezoneLocation *loc, const gchar *zone)
{
    g_free(loc->priv->zone);
    loc->priv->zone = g_strdup(zone);

    g_object_notify(G_OBJECT(loc), "zone");
}

const gchar *cc_timezone_location_get_comment(CcTimezoneLocation *loc)
{
    return loc->priv->comment;
}

void cc_timezone_location_set_comment(CcTimezoneLocation *loc, const gchar *comment)
{
    g_free(loc->priv->comment);
    loc->priv->comment = g_strdup(comment);

    g_object_notify(G_OBJECT(loc), "Comment");
}

gdouble cc_timezone_location_get_dist(CcTimezoneLocation *loc)
{
    return loc->priv->dist;
}

void cc_timezone_location_set_dist(CcTimezoneLocation *loc, gdouble dist)
{
    loc->priv->dist = dist;
    g_object_notify(G_OBJECT(loc), "dist");
}
