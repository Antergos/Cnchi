# This is used in PANEL_CFLAGS
cappletname = datetime

SUBDIRS = po-timezones

icons16dir = $(datadir)/icons/hicolor/16x16/apps
dist_icons16_DATA = icons/16x16/preferences-system-time.png
icons22dir = $(datadir)/icons/hicolor/22x22/apps
dist_icons22_DATA = icons/22x22/preferences-system-time.png
icons32dir = $(datadir)/icons/hicolor/32x32/apps
dist_icons32_DATA = icons/32x32/preferences-system-time.png
icons48dir = $(datadir)/icons/hicolor/48x48/apps
dist_icons48_DATA = icons/48x48/preferences-system-time.png
icons256dir = $(datadir)/icons/hicolor/256x256/apps
dist_icons256_DATA = icons/256x256/preferences-system-time.png
iconsscalabledir = $(datadir)/icons/hicolor/scalable/apps
dist_iconsscalable_DATA = icons/scalable/preferences-system-time.svg

tzdatadir = $(pkgdatadir)/datetime
dist_tzdata_DATA = backward

AM_CPPFLAGS =						\
	$(PANEL_CFLAGS)					\
	$(DATETIME_PANEL_CFLAGS)			\
	-DGNOMELOCALEDIR="\"$(datadir)/locale\""	\
	-DGNOMECC_DATA_DIR="\"$(pkgdatadir)\""		\
	$(NULL)

noinst_PROGRAMS = test-timezone-gfx test-endianess test-timezone

test_timezone_SOURCES = test-timezone.c cc-timezone-map.h cc-timezone-map.c tz.c tz.h
test_timezone_LDADD = $(DATETIME_PANEL_LIBS)
test_timezone_CFLAGS = $(DATETIME_PANEL_CFLAGS)

test_timezone_gfx_SOURCES = test-timezone-gfx.c tz.c tz.h
test_timezone_gfx_LDADD = $(DATETIME_PANEL_LIBS)
test_timezone_gfx_CFLAGS = $(DATETIME_PANEL_CFLAGS)

test_endianess_SOURCES = test-endianess.c date-endian.c date-endian.h
test_endianess_LDADD = $(DATETIME_PANEL_LIBS)
test_endianess_CFLAGS = $(DATETIME_PANEL_CFLAGS)

all-local: check-local

check-local: test-timezone-gfx test-endianess test-timezone
	$(builddir)/test-timezone-gfx $(srcdir)/data
	$(builddir)/test-endianess
#	$(builddir)/test-timezone

noinst_LTLIBRARIES = libdate_time.la


# This requires running d-bus session and accessible timedate1 daemon
# FIXME: need to find a way how to filter out unnecessary d-bus stuff (introspectable, properties)
#timedated1-interface.xml:
#	gdbus introspect					\
#		--xml						\
#		--system					\
#		--dest org.freedesktop.timedate1		\
#		--object-path /org/freedesktop/timedate1	\
#		 > timedated1-interface.xml

dbus_built_sources = timedated.c timedated.h
timedated.c: timedated.h
timedated.h: Makefile.am timedated1-interface.xml
	gdbus-codegen						\
		--interface-prefix org.freedesktop.		\
		--generate-c-code timedated			\
		$(srcdir)/timedated1-interface.xml


resource_files = $(shell glib-compile-resources --sourcedir=$(srcdir) --generate-dependencies $(srcdir)/datetime.gresource.xml)
cc-datetime-resources.c: datetime.gresource.xml $(resource_files)
	$(AM_V_GEN) glib-compile-resources --target=$@ --sourcedir=$(srcdir) --generate-source --c-name cc_datetime $<
cc-datetime-resources.h: datetime.gresource.xml $(resource_files)
	$(AM_V_GEN) glib-compile-resources --target=$@ --sourcedir=$(srcdir) --generate-header --c-name cc_datetime $<

BUILT_SOURCES = 		\
	$(dbus_built_sources)	\
	cc-datetime-resources.h	\
	cc-datetime-resources.c

libdate_time_la_SOURCES =	\
	$(BUILT_SOURCES)	\
	cc-datetime-panel.c	\
	cc-datetime-panel.h	\
	cc-timezone-map.c	\
	cc-timezone-map.h	\
	date-endian.c		\
	date-endian.h		\
	tz.c tz.h		\
	$(NULL)

libdate_time_la_LIBADD = $(PANEL_LIBS) $(DATETIME_PANEL_LIBS)

polkitdir = $(datadir)/polkit-1/actions
polkit_in_files = org.gnome.controlcenter.datetime.policy.in

@INTLTOOL_POLICY_RULE@
polkit_DATA = $(polkit_in_files:.policy.in=.policy)


@INTLTOOL_DESKTOP_RULE@

desktopdir = $(datadir)/applications
desktop_in_files = gnome-datetime-panel.desktop.in
desktop_DATA = $(desktop_in_files:.desktop.in=.desktop)

CLEANFILES =					\
	$(desktop_in_files)			\
	$(desktop_DATA)				\
	$(BUILT_SOURCES)			\
	org.gnome.controlcenter.datetime.policy

EXTRA_DIST =				\
	timedated1-interface.xml	\
	$(polkit_in_files)		\
	$(resource_files)		\
	datetime.gresource.xml

-include $(top_srcdir)/git.mk
