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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <json-glib/json-glib.h>
#include <gdk/gdk.h>
#include <gdk/gdkkeysyms.h>
#include <glib/gi18n.h>
#include "timezone-completion.h"
#include "tz.h"

enum {
  LAST_SIGNAL
};

/* static guint signals[LAST_SIGNAL] = { }; */

struct _CcTimezoneCompletionPrivate
{
  GtkTreeModel * initial_model;
  GtkEntry *     entry;
  guint          queued_request;
  guint          changed_id;
  guint          keypress_id;
  GCancellable * cancel;
  gchar *        request_text;
  GHashTable *   request_table;
};

#define GEONAME_URL "http://geoname-lookup.ubuntu.com/?query=%s&release=%s&lang=%s"

/* Prototypes */
static void cc_timezone_completion_class_init (CcTimezoneCompletionClass *klass);
static void cc_timezone_completion_init       (CcTimezoneCompletion *self);
static void cc_timezone_completion_dispose    (GObject *object);
static void cc_timezone_completion_finalize   (GObject *object);

G_DEFINE_TYPE (CcTimezoneCompletion, cc_timezone_completion, GTK_TYPE_ENTRY_COMPLETION);

static gboolean
match_func (GtkEntryCompletion *completion, const gchar *key,
            GtkTreeIter *iter, gpointer user_data)
{
  // geonames does the work for us
  return TRUE;
}

static void
save_and_use_model (CcTimezoneCompletion * completion, GtkTreeModel * model)
{
  CcTimezoneCompletionPrivate * priv = completion->priv;

  g_hash_table_insert (priv->request_table, g_strdup (priv->request_text), g_object_ref_sink (model));

  if (model == priv->initial_model)
    gtk_entry_completion_set_match_func (GTK_ENTRY_COMPLETION (completion), NULL, NULL, NULL);
  else
    gtk_entry_completion_set_match_func (GTK_ENTRY_COMPLETION (completion), match_func, NULL, NULL);

  gtk_entry_completion_set_model (GTK_ENTRY_COMPLETION (completion), model);

  if (priv->entry != NULL) {
    gtk_entry_completion_complete (GTK_ENTRY_COMPLETION (completion));

    /* By this time, the changed signal has come and gone.  We didn't give a
       model to use, so no popup appeared for user.  Poke the entry again to show
       popup in 300ms. */
    g_signal_emit_by_name (priv->entry, "changed");
  }
}

static gint
sort_zone (GtkTreeModel *model, GtkTreeIter *a, GtkTreeIter *b,
           gpointer user_data)
{
  /* Anything that has text as a prefix goes first, in mostly sorted order.
     Then everything else goes after, in mostly sorted order. */
  const gchar *casefolded_text = (const gchar *)user_data;

  const gchar *namea = NULL, *nameb = NULL;
  gtk_tree_model_get (model, a, CC_TIMEZONE_COMPLETION_NAME, &namea, -1);
  gtk_tree_model_get (model, b, CC_TIMEZONE_COMPLETION_NAME, &nameb, -1);

  gchar *casefolded_namea = NULL, *casefolded_nameb = NULL;
  casefolded_namea = g_utf8_casefold (namea, -1);
  casefolded_nameb = g_utf8_casefold (nameb, -1);

  gboolean amatches = FALSE, bmatches = FALSE;
  amatches = strncmp (casefolded_text, casefolded_namea, strlen(casefolded_text)) == 0;
  bmatches = strncmp (casefolded_text, casefolded_nameb, strlen(casefolded_text)) == 0;

  gint rv;
  if (amatches && !bmatches)
    rv = -1;
  else if (bmatches && !amatches)
    rv = 1;
  else
    rv = g_utf8_collate (casefolded_namea, casefolded_nameb);

  g_free (casefolded_namea);
  g_free (casefolded_nameb);
  return rv;
}

static void
json_parse_ready (GObject *object, GAsyncResult *res, gpointer user_data)
{
  CcTimezoneCompletion * completion = CC_TIMEZONE_COMPLETION (user_data);
  CcTimezoneCompletionPrivate * priv = completion->priv;
  GError * error = NULL;
  const gchar * prev_name = NULL;
  const gchar * prev_admin1 = NULL;
  const gchar * prev_country = NULL;

  json_parser_load_from_stream_finish (JSON_PARSER (object), res, &error);

  if (!g_error_matches (error, G_IO_ERROR, G_IO_ERROR_CANCELLED) && priv->cancel) {
    g_cancellable_reset (priv->cancel);
  }

  if (error != NULL) 
    {
      if (!g_error_matches (error, G_IO_ERROR, G_IO_ERROR_CANCELLED))
        save_and_use_model (completion, priv->initial_model);
      g_warning ("Could not parse geoname JSON data: %s", error->message);
      g_error_free (error);
      return;
    }

  GtkListStore * store = gtk_list_store_new (CC_TIMEZONE_COMPLETION_LAST,
                                             G_TYPE_STRING,
                                             G_TYPE_STRING,
                                             G_TYPE_STRING,
                                             G_TYPE_STRING,
                                             G_TYPE_STRING,
                                             G_TYPE_STRING);

  JsonReader * reader = json_reader_new (json_parser_get_root (JSON_PARSER (object)));

  if (!json_reader_is_array (reader)) 
    {
      g_warning ("Could not parse geoname JSON data");
      save_and_use_model (completion, priv->initial_model);
      g_object_unref (G_OBJECT (reader));
      return;
    }

  gint i, count = json_reader_count_elements (reader);
  for (i = 0; i < count; ++i) 
    {
      if (!json_reader_read_element (reader, i))
        continue;

      if (json_reader_is_object (reader)) 
        {
          const gchar * name = NULL;
          const gchar * admin1 = NULL;
          const gchar * country = NULL;
          const gchar * longitude = NULL;
          const gchar * latitude = NULL;
          gboolean skip = FALSE;
          if (json_reader_read_member (reader, "name"))
            {
              name = json_reader_get_string_value (reader);
              json_reader_end_member (reader);
            }
          if (json_reader_read_member (reader, "admin1"))
            {
              admin1 = json_reader_get_string_value (reader);
              json_reader_end_member (reader);
            }
          if (json_reader_read_member (reader, "country"))
            {
              country = json_reader_get_string_value (reader);
              json_reader_end_member (reader);
            }
          if (json_reader_read_member (reader, "longitude"))
            {
              longitude = json_reader_get_string_value (reader);
              json_reader_end_member (reader);
            }
          if (json_reader_read_member (reader, "latitude"))
            {
              latitude = json_reader_get_string_value (reader);
              json_reader_end_member (reader);
            }

      if (g_strcmp0(name, prev_name) == 0 &&
          g_strcmp0(admin1, prev_admin1) == 0 &&
          g_strcmp0(country, prev_country) == 0)
        {
          // Sometimes the data will have duplicate entries that only differ
          // in longitude and latitude.  e.g. "rio de janeiro", "wellington"
          skip = TRUE;
        }

      if (!skip) 
        {
          GtkTreeIter iter;
          gtk_list_store_append (store, &iter);
          gtk_list_store_set (store, &iter,
                              CC_TIMEZONE_COMPLETION_ZONE, NULL,
                              CC_TIMEZONE_COMPLETION_NAME, name,
                              CC_TIMEZONE_COMPLETION_ADMIN1, admin1,
                              CC_TIMEZONE_COMPLETION_COUNTRY, country,
                              CC_TIMEZONE_COMPLETION_LONGITUDE, longitude,
                              CC_TIMEZONE_COMPLETION_LATITUDE, latitude,
                              -1);
          gtk_tree_sortable_set_sort_func (GTK_TREE_SORTABLE (store),
                                           CC_TIMEZONE_COMPLETION_NAME,
                                           sort_zone,
                                           g_utf8_casefold(priv->request_text,
                                             -1),
                                           g_free);
          gtk_tree_sortable_set_sort_column_id (GTK_TREE_SORTABLE (store),
                                                CC_TIMEZONE_COMPLETION_NAME,
                                                GTK_SORT_ASCENDING);
        }

      prev_name = name;
      prev_admin1 = admin1;
      prev_country = country;
    }

    json_reader_end_element (reader);
  }

  if (strlen (priv->request_text) < 4)
    {
      gchar * lower_text = g_ascii_strdown (priv->request_text, -1);
      if (g_strcmp0 (lower_text, "ut") == 0 ||
          g_strcmp0 (lower_text, "utc") == 0)
        {
           GtkTreeIter iter;
           gtk_list_store_append (store, &iter);
           gtk_list_store_set (store, &iter,
                               CC_TIMEZONE_COMPLETION_ZONE, "UTC",
                                CC_TIMEZONE_COMPLETION_NAME, "UTC",
                               -1);
        }
      g_free (lower_text);
    }

  save_and_use_model (completion, GTK_TREE_MODEL (store));
  g_object_unref (G_OBJECT (reader));
}

static void
geonames_data_ready (GObject *object, GAsyncResult *res, gpointer user_data)
{
  CcTimezoneCompletion * completion = CC_TIMEZONE_COMPLETION (user_data);
  CcTimezoneCompletionPrivate * priv = completion->priv;
  GError * error = NULL;
  GFileInputStream * stream;

  stream = g_file_read_finish (G_FILE (object), res, &error);

  if (!g_error_matches (error, G_IO_ERROR, G_IO_ERROR_CANCELLED) && priv->cancel)
    {
      g_cancellable_reset (priv->cancel);
    }

  if (error != NULL)
    {
      if (!g_error_matches (error, G_IO_ERROR, G_IO_ERROR_CANCELLED))
        save_and_use_model (completion, priv->initial_model);
      g_warning ("Could not connect to geoname lookup server: %s",
          error->message);
      g_error_free (error);
      return;
    }

  JsonParser * parser = json_parser_new ();
  json_parser_load_from_stream_async (parser, G_INPUT_STREAM (stream), priv->cancel,
                                      json_parse_ready, user_data);
}

/* Returns message locale, with possible country info too like en_US */
static gchar *
get_locale (void)
{
  /* Check LANGUAGE, LC_ALL, LC_MESSAGES, and LANG, treat as colon-separated */
  const gchar *env_names[] = {"LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG", NULL};
  const gchar *env = NULL;
  gint i;

  for (i = 0; env_names[i]; i++)
    {
      env = g_getenv (env_names[i]);
      if (env != NULL && env[0] != 0)
        break;
    }

  if (env == NULL)
    return NULL;

  /* Now, we split on colons as expected, but also on . and @ to filter out
     extra pieces of locale we don't care about as we only use first chunk. */
  gchar **split = g_strsplit_set (env, ":.@", 2);
  if (split == NULL)
    return NULL;

  if (split[0] == NULL)
    {
      g_strfreev (split);
      return NULL;
    }

  gchar *locale = g_strdup (split[0]);
  g_strfreev (split);
  return locale;
}

static gchar *
get_version (void)
{
  static gchar *version = NULL;

  if (version == NULL)
    {
      gchar *stdout = NULL;
      g_spawn_command_line_sync ("lsb_release -rs", &stdout, NULL, NULL, NULL);

      if (stdout != NULL)
        version = g_strstrip (stdout);
      else
        version = g_strdup("");
    }

  return version;
}

static gboolean
request_zones (CcTimezoneCompletion * completion)
{
  CcTimezoneCompletionPrivate * priv = completion->priv;

  priv->queued_request = 0;

  if (priv->entry == NULL)
    {
      return FALSE;
    }

  /* Cancel any ongoing request */
  if (priv->cancel)
    {
      g_cancellable_cancel (priv->cancel);
      g_cancellable_reset (priv->cancel);
    }
  g_free (priv->request_text);

  const gchar * text = gtk_entry_get_text (priv->entry);
  priv->request_text = g_strdup (text);

  gchar * escaped = g_uri_escape_string (text, NULL, FALSE);
  gchar * version = get_version ();
  gchar * locale = get_locale ();
  gchar * url = g_strdup_printf (GEONAME_URL, escaped, version, locale);
  g_free (locale);
  g_free (escaped);

  GFile * file =  g_file_new_for_uri (url);
  g_free (url);

  g_file_read_async (file, G_PRIORITY_DEFAULT, priv->cancel,
                     geonames_data_ready, completion);

  return FALSE;
}

static void
entry_changed (GtkEntry * entry, CcTimezoneCompletion * completion)
{
  CcTimezoneCompletionPrivate * priv = completion->priv;

  if (priv->queued_request)
    {
      g_source_remove (priv->queued_request);
      priv->queued_request = 0;
    }

  /* See if we've already got this one */
  const gchar * text = gtk_entry_get_text (priv->entry);
  gpointer data;
  if (g_hash_table_lookup_extended (priv->request_table, text, NULL, &data))
    {
      gtk_entry_completion_set_model (GTK_ENTRY_COMPLETION (completion),
          GTK_TREE_MODEL (data));
    }
  else 
    {
      priv->queued_request = g_timeout_add (300, (GSourceFunc)request_zones,
          completion);
      gtk_entry_completion_set_model (GTK_ENTRY_COMPLETION (completion), NULL);
    }
  gtk_entry_completion_complete (GTK_ENTRY_COMPLETION (completion));
}

static GtkWidget *
get_descendent (GtkWidget * parent, GType type)
{
  if (g_type_is_a (G_OBJECT_TYPE (parent), type))
    return parent;

  if (GTK_IS_CONTAINER (parent))
    {
      GList * children = gtk_container_get_children (GTK_CONTAINER (parent));
      GList * iter;
      for (iter = children; iter; iter = iter->next)
        {
          GtkWidget * found = get_descendent (GTK_WIDGET (iter->data), type);
          if (found)
            {
              g_list_free (children);
              return found;
            }
        }
      g_list_free (children);
    }

  return NULL;
}

/*
 * The popup window and its GtkTreeView are private to our parent completion
 * object.  We can't get access to discover if there is a highlighted item or
 * even if the window is showing right now.  So this is a super hack to find
 * it by looking through our toplevel's window group and finding a window with
 * a GtkTreeView that points at our model.  There should be only one ever, so
 * we'll use the first one we find.
 */
static GtkTreeView *
find_popup_treeview (GtkWidget * widget, GtkTreeModel * model)
{
  GtkWidget * toplevel = gtk_widget_get_toplevel (widget);
  if (!GTK_IS_WINDOW (toplevel))
    return NULL;

  GtkWindowGroup * group = gtk_window_get_group (GTK_WINDOW (toplevel)); 
  GList * windows = gtk_window_group_list_windows (group);
  GList * iter;
  for (iter = windows; iter; iter = iter->next)
    {
      if (iter->data == toplevel)
        continue; // Skip our own window, we don't have it
      GtkWidget * view = get_descendent (GTK_WIDGET (iter->data),
          GTK_TYPE_TREE_VIEW);
       if (view != NULL)
         {
          GtkTreeModel * tree_model =
            gtk_tree_view_get_model (GTK_TREE_VIEW (view));
          if (GTK_IS_TREE_MODEL_FILTER (tree_model))
            tree_model = gtk_tree_model_filter_get_model (
                GTK_TREE_MODEL_FILTER (tree_model));
          if (tree_model == model)
            {
              g_list_free (windows);
              return GTK_TREE_VIEW (view);
            }
        }
    }
  g_list_free (windows);

  return NULL;
}

static gboolean
entry_keypress (GtkEntry * entry, GdkEventKey  *event, CcTimezoneCompletion * completion)
{
  if (event->keyval == GDK_KEY_ISO_Enter ||
      event->keyval == GDK_KEY_KP_Enter ||
      event->keyval == GDK_KEY_Return)
    {
      /* Make sure that user has a selection to choose, otherwise ignore */
      GtkTreeModel * model = gtk_entry_completion_get_model (
          GTK_ENTRY_COMPLETION (completion));
      GtkTreeView * view = find_popup_treeview (GTK_WIDGET (entry), model);
      if (view == NULL)
       {
         // Just beep if popup hasn't appeared yet.
         gtk_widget_error_bell (GTK_WIDGET (entry));
         return TRUE;
       }

      GtkTreeSelection * sel = gtk_tree_view_get_selection (view);
      GtkTreeModel * sel_model = NULL;
      if (!gtk_tree_selection_get_selected (sel, &sel_model, NULL))
        {
          // No selection, we should help them out and select first item in list
          GtkTreeIter iter;
          if (gtk_tree_model_get_iter_first (sel_model, &iter))
            gtk_tree_selection_select_iter (sel, &iter);
          // And fall through to normal handler code
        }
    }

  return FALSE;
}

void
cc_timezone_completion_watch_entry (CcTimezoneCompletion * completion, GtkEntry * entry)
{
  CcTimezoneCompletionPrivate * priv = completion->priv;

  if (priv->queued_request)
    {
      g_source_remove (priv->queued_request);
      priv->queued_request = 0;
    }
  if (priv->entry)
    {
      g_signal_handler_disconnect (priv->entry, priv->changed_id);
      priv->changed_id = 0;
      g_signal_handler_disconnect (priv->entry, priv->keypress_id);
      priv->keypress_id = 0;
      g_object_remove_weak_pointer (G_OBJECT (priv->entry), (gpointer *)&priv->entry);
      gtk_entry_set_completion (priv->entry, NULL);
    }

  priv->entry = entry;

  if (entry)
    {
      guint id = g_signal_connect (entry, "changed",
          G_CALLBACK (entry_changed), completion);
      priv->changed_id = id;

      id = g_signal_connect (entry, "key-press-event",
          G_CALLBACK (entry_keypress), completion);
      priv->keypress_id = id;

      g_object_add_weak_pointer (G_OBJECT (entry), (gpointer *)&priv->entry);

      gtk_entry_set_completion (entry, GTK_ENTRY_COMPLETION (completion));
    }
}

static GtkListStore *
get_initial_model (void)
{
  TzDB * db = tz_load_db ();
  GPtrArray * locations = tz_get_locations (db);

  GtkListStore * store = gtk_list_store_new (CC_TIMEZONE_COMPLETION_LAST,
                                             G_TYPE_STRING,
                                             G_TYPE_STRING,
                                             G_TYPE_STRING,
                                             G_TYPE_STRING,
                                             G_TYPE_STRING,
                                             G_TYPE_STRING);

  gint i;
  for (i = 0; i < locations->len; ++i)
    {
      CcTimezoneLocation * loc = g_ptr_array_index (locations, i);
      GtkTreeIter iter;
      gtk_list_store_append (store, &iter);

      gchar * zone;
      gchar * country;
      gchar * en_name; // FIXME: need something better for non-English locales 
      gdouble longitude;
      gdouble latitude;
      g_object_get (loc, "zone", &zone, "country", &country, "en_name", &en_name,
                    "longitude", &longitude, "latitude", &latitude,
                    NULL);

      gchar * longitude_s = g_strdup_printf ("%f", longitude);
      gchar * latitude_s=  g_strdup_printf ("%f", latitude);

      gtk_list_store_set (store, &iter,
                          CC_TIMEZONE_COMPLETION_ZONE, NULL,
                          CC_TIMEZONE_COMPLETION_NAME, en_name,
                          CC_TIMEZONE_COMPLETION_COUNTRY, country,
                          CC_TIMEZONE_COMPLETION_LONGITUDE, longitude_s,
                          CC_TIMEZONE_COMPLETION_LATITUDE, latitude_s,
                          -1);

      g_free (latitude_s);
      g_free (longitude_s);
      g_free (en_name);
      g_free (country);
      g_free (zone);
    }

  GtkTreeIter iter;
  gtk_list_store_append (store, &iter);
  gtk_list_store_set (store, &iter,
                      CC_TIMEZONE_COMPLETION_ZONE, "UTC",
                      CC_TIMEZONE_COMPLETION_NAME, "UTC",
                      -1);

  tz_db_free (db);
  return store;
}

static void
data_func (GtkCellLayout *cell_layout, GtkCellRenderer *cell,
           GtkTreeModel *tree_model, GtkTreeIter *iter, gpointer user_data)
{
  const gchar * name, * admin1, * country;

  gtk_tree_model_get (GTK_TREE_MODEL (tree_model), iter,
                      CC_TIMEZONE_COMPLETION_NAME, &name,
                      CC_TIMEZONE_COMPLETION_ADMIN1, &admin1,
                      CC_TIMEZONE_COMPLETION_COUNTRY, &country,
                      -1);

  gchar * user_name;
  if (country == NULL || country[0] == 0)
    {
      user_name = g_strdup (name);
    } else if (admin1 == NULL || admin1[0] == 0) {
      user_name = g_strdup_printf ("%s <small>(%s)</small>", name, country);
    } else {
      user_name = g_strdup_printf ("%s <small>(%s, %s)</small>", name, admin1, country);
    }

  g_object_set (G_OBJECT (cell), "markup", user_name, NULL);
}

static void
cc_timezone_completion_class_init (CcTimezoneCompletionClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);

  g_type_class_add_private (klass, sizeof (CcTimezoneCompletionPrivate));

  object_class->dispose = cc_timezone_completion_dispose;
  object_class->finalize = cc_timezone_completion_finalize;

  return;
}

static void
cc_timezone_completion_init (CcTimezoneCompletion * self)
{
  CcTimezoneCompletionPrivate *priv;

  self->priv = G_TYPE_INSTANCE_GET_PRIVATE (self,
                                            CC_TIMEZONE_COMPLETION_TYPE,
                                            CcTimezoneCompletionPrivate);
  priv = self->priv;

  priv->initial_model = GTK_TREE_MODEL (get_initial_model ());

  g_object_set (G_OBJECT (self),
                "text-column", CC_TIMEZONE_COMPLETION_NAME,
                "popup-set-width", FALSE,
                NULL);

  priv->cancel = g_cancellable_new ();

  priv->request_table = g_hash_table_new_full (g_str_hash, g_str_equal, g_free, g_object_unref);

  GtkCellRenderer * cell = gtk_cell_renderer_text_new ();
  gtk_cell_layout_pack_start (GTK_CELL_LAYOUT (self), cell, TRUE);
  gtk_cell_layout_set_cell_data_func (GTK_CELL_LAYOUT (self), cell, data_func, NULL, NULL);

  return;
}

static void
cc_timezone_completion_dispose (GObject * object)
{
  G_OBJECT_CLASS (cc_timezone_completion_parent_class)->dispose (object);

  CcTimezoneCompletion * completion = CC_TIMEZONE_COMPLETION (object);
  CcTimezoneCompletionPrivate * priv = completion->priv;

  if (priv->changed_id)
    {
      if (priv->entry)
        g_signal_handler_disconnect (priv->entry, priv->changed_id);
      priv->changed_id = 0;
    }

  if (priv->keypress_id)
    {
      if (priv->entry)
        g_signal_handler_disconnect (priv->entry, priv->keypress_id);
      priv->keypress_id = 0;
    }

  if (priv->entry != NULL)
    {
      gtk_entry_set_completion (priv->entry, NULL);
      g_object_remove_weak_pointer (G_OBJECT (priv->entry), (gpointer *)&priv->entry);
      priv->entry = NULL;
    }

  if (priv->initial_model != NULL)
    {
      g_object_unref (G_OBJECT (priv->initial_model));
      priv->initial_model = NULL;
    }

  if (priv->queued_request)
    {
      g_source_remove (priv->queued_request);
      priv->queued_request = 0;
    }

  if (priv->cancel != NULL)
    {
      g_cancellable_cancel (priv->cancel);
      g_object_unref (priv->cancel);
      priv->cancel = NULL;
    }

  if (priv->request_text != NULL)
    {
      g_free (priv->request_text);
      priv->request_text = NULL;
    }

  if (priv->request_table != NULL)
    {
      g_hash_table_destroy (priv->request_table);
      priv->request_table = NULL;
    }

  return;
}

static void
cc_timezone_completion_finalize (GObject * object)
{
  G_OBJECT_CLASS (cc_timezone_completion_parent_class)->finalize (object);
  return;
}

CcTimezoneCompletion *
cc_timezone_completion_new ()
{
  CcTimezoneCompletion * self = g_object_new (CC_TIMEZONE_COMPLETION_TYPE, NULL);
  return self;
}

