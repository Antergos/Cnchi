#include <config.h>
#include <locale.h>

#include "tz.h"

int main (int argc, char **argv)
{
	TzDB *db;
	GPtrArray *locs;
	guint i;
	char *pixmap_dir;
	int retval = 0;

        setlocale (LC_ALL, "");

	if (argc == 2) {
		pixmap_dir = g_strdup (argv[1]);
	} else if (argc == 1) {
		pixmap_dir = g_strdup ("data/");
	} else {
		g_message ("Usage: %s [PIXMAP DIRECTORY]", argv[0]);
		return 1;
	}

	db = tz_load_db ();
	locs = tz_get_locations (db);
	for (i = 0; i < locs->len ; i++) {
		TzLocation *loc = locs->pdata[i];
		TzInfo *info;
		char *filename, *path;
		gdouble selected_offset;
                char buf[16];

		info = tz_info_from_location (loc);
		selected_offset = tz_location_get_utc_offset (loc)
			/ (60.0*60.0) + ((info->daylight) ? -1.0 : 0.0);

		filename = g_strdup_printf ("timezone_%s.png",
                                            g_ascii_formatd (buf, sizeof (buf),
                                                             "%g", selected_offset));
		path = g_build_filename (pixmap_dir, filename, NULL);

		if (g_file_test (path, G_FILE_TEST_IS_REGULAR) == FALSE) {
			g_message ("File '%s' missing for zone '%s'", filename, loc->zone);
			retval = 1;
		}

		g_free (filename);
		g_free (path);
	}
	tz_db_free (db);
	g_free (pixmap_dir);

	return retval;
}
