#include <gtk/gtk.h>
#include "cc-timezone-map.h"

#define TZ_DIR "/usr/share/zoneinfo/"

static GList *
get_timezone_list (GList *tzs,
		   const char *top_path,
		   const char *subpath)
{
	GDir *dir;
	char *fullpath;
	const char *name;

	if (subpath == NULL)
		fullpath = g_strdup (top_path);
	else
		fullpath = g_build_filename (top_path, subpath, NULL);
	dir = g_dir_open (fullpath, 0, NULL);
	if (dir == NULL) {
		g_warning ("Could not open %s", fullpath);
		return NULL;
	}
	while ((name = g_dir_read_name (dir)) != NULL) {
		char *path;

		if (g_str_has_suffix (name, ".tab"))
			continue;

		if (subpath != NULL)
			path = g_build_filename (top_path, subpath, name, NULL);
		else
			path = g_build_filename (top_path, name, NULL);
		if (g_file_test (path, G_FILE_TEST_IS_DIR)) {
			if (subpath == NULL) {
				tzs = get_timezone_list (tzs, top_path, name);
			} else {
				char *new_subpath;
				new_subpath = g_strdup_printf ("%s/%s", subpath, name);
				tzs = get_timezone_list (tzs, top_path, new_subpath);
				g_free (new_subpath);
			}
		} else if (g_file_test (path, G_FILE_TEST_IS_REGULAR)) {
			if (subpath == NULL)
				tzs = g_list_prepend (tzs, g_strdup (name));
			else {
				char *tz;
				tz = g_strdup_printf ("%s/%s", subpath, name);
				tzs = g_list_prepend (tzs, tz);
			}
		}
		g_free (path);
	}
	g_dir_close (dir);

	return tzs;
}

int main (int argc, char **argv)
{
	CcTimezoneMap *map;
	TzDB *tz_db;
	GList *tzs, *l;
	GHashTable *ht;
	int ret = 0;

	gtk_init (&argc, &argv);

	ht = g_hash_table_new_full (g_str_hash, g_str_equal, g_free, NULL);
	map = cc_timezone_map_new ();
	tz_db = tz_load_db ();
	tzs = get_timezone_list (NULL, TZ_DIR, NULL);
	for (l = tzs; l != NULL; l = l->next) {
		char *timezone = l->data;
		char *clean_tz;

		clean_tz = tz_info_get_clean_name (tz_db, timezone);

		if (cc_timezone_map_set_timezone (map, clean_tz) == FALSE) {
			if (g_hash_table_lookup (ht, clean_tz) == NULL) {
				if (g_strcmp0 (clean_tz, timezone) == 0)
					g_print ("Failed to locate timezone '%s'\n", timezone);
				else
					g_print ("Failed to locate timezone '%s' (original name: '%s')\n", clean_tz, timezone);
				g_hash_table_insert (ht, g_strdup (clean_tz), GINT_TO_POINTER (TRUE));
			}
			/* We don't warn for those two, we'll just fallback
			 * in the panel code */
			if (!g_str_equal (clean_tz, "posixrules") &&
			    !g_str_equal (clean_tz, "Factory"))
				ret = 1;
		}
		g_free (timezone);
		g_free (clean_tz);
	}
	g_list_free (tzs);
	tz_db_free (tz_db);
	g_hash_table_destroy (ht);

	return ret;
}
