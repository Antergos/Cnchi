/* -*- Mode: C; coding: utf-8; indent-tabs-mode: nil; tab-width: 2 -*-

Copyright 2011 Canonical Ltd.

Authors:
    Michael Terry <michael.terry@canonical.com>

This program is free software: you can redistribute it and/or modify it 
under the terms of the GNU General Public License version 3, as published 
by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranties of 
MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along 
with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#ifndef __CC_TIMEZONE_COMPLETION_H__
#define __CC_TIMEZONE_COMPLETION_H__

#include <glib.h>
#include <glib-object.h>
#include <gtk/gtk.h>

G_BEGIN_DECLS

#define CC_TIMEZONE_COMPLETION_TYPE            (cc_timezone_completion_get_type ())
#define CC_TIMEZONE_COMPLETION(obj)            (G_TYPE_CHECK_INSTANCE_CAST ((obj), CC_TIMEZONE_COMPLETION_TYPE, CcTimezoneCompletion))
#define CC_TIMEZONE_COMPLETION_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST ((klass), CC_TIMEZONE_COMPLETION_TYPE, CcTimezoneCompletionClass))
#define IS_CC_TIMEZONE_COMPLETION(obj)         (G_TYPE_CHECK_INSTANCE_TYPE ((obj), CC_TIMEZONE_COMPLETION_TYPE))
#define IS_CC_TIMEZONE_COMPLETION_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE ((klass), CC_TIMEZONE_COMPLETION_TYPE))
#define CC_TIMEZONE_COMPLETION_GET_CLASS(obj)  (G_TYPE_INSTANCE_GET_CLASS ((obj), CC_TIMEZONE_COMPLETION_TYPE, CcTimezoneCompletionClass))

typedef struct _CcTimezoneCompletion             CcTimezoneCompletion;
typedef struct _CcTimezoneCompletionPrivate      CcTimezoneCompletionPrivate;
typedef struct _CcTimezoneCompletionClass        CcTimezoneCompletionClass;

struct _CcTimezoneCompletion {
  GtkEntryCompletion parent;

  CcTimezoneCompletionPrivate *priv;
};

struct _CcTimezoneCompletionClass {
  GtkEntryCompletionClass parent_class;
};

#define CC_TIMEZONE_COMPLETION_ZONE      0
#define CC_TIMEZONE_COMPLETION_NAME      1
#define CC_TIMEZONE_COMPLETION_ADMIN1    2
#define CC_TIMEZONE_COMPLETION_COUNTRY   3
#define CC_TIMEZONE_COMPLETION_LONGITUDE 4
#define CC_TIMEZONE_COMPLETION_LATITUDE  5
#define CC_TIMEZONE_COMPLETION_LAST      6

GType cc_timezone_completion_get_type (void) G_GNUC_CONST;
CcTimezoneCompletion * cc_timezone_completion_new ();
void cc_timezone_completion_watch_entry (CcTimezoneCompletion * completion, GtkEntry * entry);

G_END_DECLS

#endif /* __CC_TIMEZONE_COMPLETION_H__ */

