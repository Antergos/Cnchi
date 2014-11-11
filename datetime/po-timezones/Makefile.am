PO_LINGUAS = $(subst .po,,$(wildcard *.po))

USER_LINGUAS = $(filter $(LINGUAS),$(PO_LINGUAS))

USE_LINGUAS = $(shell if test -n "$(USER_LINGUAS)" -o -n "$(LINGUAS)"; then LLINGUAS="$(USER_LINGUAS)"; else LLINGUAS="$(PO_LINGUAS)"; fi; for lang in $$LLINGUAS; do printf "$$lang "; done)

ALL_CATALOGS = $(patsubst %.po,%.mo,$(wildcard *.po))

CATALOGS = $(USE_LINGUAS:%=%.mo)

all: $(CATALOGS)

NLSPACKAGE = $(GETTEXT_PACKAGE)-timezones

%.mo: %.po
	$(AM_V_GEN) msgfmt -o $@ $<

install: $(CATALOGS)
	@mkdir -p $(DESTDIR)$(localedir)
	for n in $(CATALOGS); do \
		l=`basename $$n .mo`; \
		$(INSTALL) -m 755 -d $(DESTDIR)$(localedir)/$$l; \
		$(INSTALL) -m 755 -d $(DESTDIR)$(localedir)/$$l/LC_MESSAGES; \
		if [ -f $$n ]; then \
			$(INSTALL) -m 644 $$n $(DESTDIR)$(localedir)/$$l/LC_MESSAGES/$(NLSPACKAGE).mo; \
		fi; \
	done

EXTRA_DIST=$(wildcard *.po)

CLEANFILES = $(ALL_CATALOGS)

-include $(top_srcdir)/git.mk
