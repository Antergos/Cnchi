#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
#  Copyright (C) 2012 Canonical Ltd.
#  Written by Colin Watson <cjwatson@ubuntu.com>.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""Parse the output of kbdnames-maker."""

from collections import defaultdict
import gzip
import io

# TODO: fix this as it's not clean to have a full path here
# _default_filename = "/usr/lib/ubiquity/console-setup/kbdnames.gz"
# _default_filename = "data/kbdnames.gz"
_default_filename = '/usr/share/cnchi/data/kbdnames.gz'


class KeyboardNames:
    def __init__(self, filename):
        self._current_lang = None
        self._filename = filename
        self._clear()

    def _clear(self):
        self._layout_by_id = {}
        self.layout_by_human = {}
        self._variant_by_id = defaultdict(dict)
        self.variant_by_human = defaultdict(dict)

    def _load_file(self, lang, kbdnames):
        # TODO cjwatson 2012-07-19: Work around
        # http://bugs.python.org/issue10791 in Python 3.2.  When we can rely
        # on 3.3, this should be:
        #   for line in kbdnames:
        #       line = line.rstrip("\n")

        for line in kbdnames.read().splitlines():
            got_lang, element, name, value = line.split("*", 3)
            if got_lang != lang:
                continue

            if element == "layout":
                self._layout_by_id[name] = value
                self.layout_by_human[value] = name
            elif element == "variant":
                variantname, variantdesc = value.split("*", 1)
                self._variant_by_id[name][variantname] = variantdesc
                self.variant_by_human[name][variantdesc] = variantname

    def load(self, lang):
        if lang == self._current_lang:
            return

        # Saving memory is more important than parsing time in the
        # relatively rare case of changing languages, so we only keep data
        # around for a single language.
        self._clear()

        raw = gzip.open(self._filename)
        try:
            with io.TextIOWrapper(raw, encoding='utf-8') as kbdnames:
                self._load_file(lang, kbdnames)
        finally:
            raw.close()
        self._current_lang = lang

    def has_language(self, lang):
        self.load(lang)
        return bool(self._layout_by_id)

    def has_layout(self, lang, name):
        self.load(lang)
        return name in self._layout_by_id

    def layout_human(self, lang, name):
        self.load(lang)
        return self._layout_by_id[name]

    def layout_id(self, lang, value):
        self.load(lang)
        return self.layout_by_human[value]

    def has_variants(self, lang, layout):
        self.load(lang)
        return layout in self._variant_by_id

    def has_variant(self, lang, layout, name):
        self.load(lang)
        return (layout in self._variant_by_id and
                name in self._variant_by_id[layout])

    def variant_human(self, lang, layout, name):
        self.load(lang)
        return self._variant_by_id[layout][name]

    def variant_id(self, lang, layout, value):
        self.load(lang)
        return self.variant_by_human[layout][value]


_keyboard_names = None


def _get_keyboard_names():
    """Return a singleton KeyboardNames instance."""
    global _keyboard_names
    if _keyboard_names is None:
        _keyboard_names = KeyboardNames(filename=_default_filename)
    return _keyboard_names


def has_language(lang):
    """Are there any keyboard names for this language?"""
    kn = _get_keyboard_names()
    return kn.has_language(lang)


def has_layout(lang, name):
    """Does this layout ID exist for this language?"""
    kn = _get_keyboard_names()
    return kn.has_layout(lang, name)


def layout_human(lang, name):
    """Return a human layout name given a layout ID."""
    kn = _get_keyboard_names()
    return kn.layout_human(lang, name)


def layout_id(lang, value):
    """Return a layout ID given a human layout name."""
    kn = _get_keyboard_names()
    return kn.layout_id(lang, value)


def has_variants(lang, layout):
    """Are there any variants for this language and layout ID?"""
    kn = _get_keyboard_names()
    return kn.has_variants(lang, layout)


def has_variant(lang, layout, name):
    """Does this variant ID exist for this language and layout ID?"""
    kn = _get_keyboard_names()
    return kn.has_variant(lang, layout, name)


def variant_human(lang, layout, name):
    """Return a human variant name given layout and variant IDs."""
    kn = _get_keyboard_names()
    return kn.variant_human(lang, layout, name)


def variant_id(lang, layout, value):
    """Return a variant ID given a layout ID and a human variant name."""
    kn = _get_keyboard_names()
    return kn.variant_id(lang, layout, value)
