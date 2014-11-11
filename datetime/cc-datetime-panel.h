/*
 * Copyright (C) 2010 Intel, Inc
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
 * along with this program; if not, see <http://www.gnu.org/licenses/>.
 *
 * Author: Thomas Wood <thomas.wood@intel.com>
 *
 */


#ifndef _CC_DATE_TIME_PANEL_H
#define _CC_DATE_TIME_PANEL_H

#include <shell/cc-panel.h>

G_BEGIN_DECLS

#define CC_TYPE_DATE_TIME_PANEL cc_date_time_panel_get_type()

#define CC_DATE_TIME_PANEL(obj) \
  (G_TYPE_CHECK_INSTANCE_CAST ((obj), \
  CC_TYPE_DATE_TIME_PANEL, CcDateTimePanel))

#define CC_DATE_TIME_PANEL_CLASS(klass) \
  (G_TYPE_CHECK_CLASS_CAST ((klass), \
  CC_TYPE_DATE_TIME_PANEL, CcDateTimePanelClass))

#define CC_IS_DATE_TIME_PANEL(obj) \
  (G_TYPE_CHECK_INSTANCE_TYPE ((obj), \
  CC_TYPE_DATE_TIME_PANEL))

#define CC_IS_DATE_TIME_PANEL_CLASS(klass) \
  (G_TYPE_CHECK_CLASS_TYPE ((klass), \
  CC_TYPE_DATE_TIME_PANEL))

#define CC_DATE_TIME_PANEL_GET_CLASS(obj) \
  (G_TYPE_INSTANCE_GET_CLASS ((obj), \
  CC_TYPE_DATE_TIME_PANEL, CcDateTimePanelClass))

typedef struct _CcDateTimePanel CcDateTimePanel;
typedef struct _CcDateTimePanelClass CcDateTimePanelClass;
typedef struct _CcDateTimePanelPrivate CcDateTimePanelPrivate;

struct _CcDateTimePanel
{
  CcPanel parent;

  CcDateTimePanelPrivate *priv;
};

struct _CcDateTimePanelClass
{
  CcPanelClass parent_class;
};

GType cc_date_time_panel_get_type (void) G_GNUC_CONST;

G_END_DECLS

#endif /* _CC_DATE_TIME_PANEL_H */
