#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# i18n_packages.py
#
# Copyright © 2013-2018 Antergos
#
# This file is part of Cnchi.
#
# Cnchi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Cnchi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cnchi; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

""" Gets specific i18n packages (for firefox, libreoffice, ...) """

import logging
import os

class I18NPackages():
    """ i18n packages helper class """

    def __init__(self, locale, data):
        """ Initialize class """

        if locale.endswith('.UTF-8'):
            locale = locale.split('.')[0]
        self.locale = locale
        self.data = data

    def get_package_i18n_codes(self, package):
        """ Get available i18n packages for package 'package'
            (firefox, libreoffice and hunspell variation packages """

        # Coded here as a failsafe, in case i18n.txt file is not found in data dir
        coded_lang_codes = {
            'firefox': [
                'ach', 'af', 'an', 'ar', 'as', 'ast', 'az', 'be', 'bg', 'bn-bd',
                'bn-in', 'br', 'bs', 'ca', 'cs', 'cy', 'da', 'de', 'dsb', 'el',
                'en-gb', 'en-us', 'en-za', 'eo', 'es-ar', 'es-cl', 'es-es',
                'es-mx', 'et', 'eu', 'fa', 'ff', 'fi', 'fr', 'fy-nl', 'ga-ie',
                'gd', 'gl', 'gu-in', 'he', 'hi-in', 'hr', 'hsb', 'hu', 'hy-am',
                'id', 'is', 'it', 'ja', 'kk', 'km', 'kn', 'ko', 'lij', 'lt', 'lv',
                'mai', 'mk', 'ml', 'mr', 'ms', 'nb-no', 'nl', 'nn-no', 'or',
                'pa-in', 'pl', 'pt-br', 'pt-pt', 'rm', 'ro', 'ru', 'si', 'sk',
                'sl', 'son', 'sq', 'sr', 'sv-se', 'ta', 'te', 'th', 'tr', 'uk',
                'uz', 'vi', 'xh', 'zh-cn', 'zh-tw'],
            'hunspell': [
                'de-frami', 'de', 'en', 'en_AU', 'en_CA', 'en_GB', 'en_US',
                'es_any', 'es_ar', 'es_bo', 'es_cl', 'es_co', 'es_cr', 'es_cu',
                'es_do', 'es_ec', 'es_es', 'es_gt', 'es_hn', 'es_mx', 'es_ni',
                'es_pa', 'es_pe', 'es_pr', 'es_py', 'es_sv', 'es_uy', 'es_ve',
                'fr', 'he', 'it', 'ro', 'el', 'hu', 'nl', 'pl'],
            'libreoffice': [
                'am', 'af', 'ar', 'as', 'ast', 'be', 'bg', 'bn', 'bn-in', 'bo',
                'br', 'brx', 'bs', 'ca', 'ca-valencia', 'cs', 'cy', 'da', 'de',
                'dgo', 'dz', 'el', 'en-gb', 'en-za', 'eo', 'es', 'et', 'eu', 'fa',
                'fi', 'fr', 'ga', 'gd', 'gl', 'gu', 'he', 'hi', 'hr', 'hu', 'id',
                'is', 'it', 'ja', 'ka', 'kk', 'km', 'kmr-latn', 'kn', 'ko', 'kok',
                'ks', 'lb', 'lo', 'lt', 'lv', 'mai', 'mk', 'ml', 'mn', 'mni', 'mr',
                'my', 'nb', 'ne', 'nl', 'nn', 'nr', 'nso', 'oc', 'om', 'or', 'pa-in',
                'pl', 'pt', 'pt-br', 'ro', 'ru', 'rw', 'sa-in', 'sat', 'sd', 'sdk',
                'si', 'sid', 'sk', 'sl', 'sq', 'sr', 'sr-latn', 'ss', 'st', 'sv',
                'sw-tz', 'ta', 'te', 'tg', 'th', 'tn', 'tr', 'ts', 'tt', 'ug', 'uk',
                'uz', 've', 'vi', 'xh', 'zh-cn', 'zh-tw', 'zu']}

        filename = "i18n-{}.txt".format(package)
        path = os.path.join(self.data, filename)
        if os.path.exists(path):
            with open(path, 'r') as lang_file:
                lang_codes = lang_file.read().split()
            return lang_codes

        # Couldn't find i18n-package.txt, use this hardcoded version then
        if package in coded_lang_codes:
            logging.debug("Could not open %s, Cnchi will use a hardcoded version.", path)
            return coded_lang_codes[package]
        return None


    def firefox(self):
        """ Add firefox language package """
        # Try to load available languages from i18n-firefox.txt (easy updating if necessary)
        lang_codes = self.get_package_i18n_codes('firefox')

        code = self.locale.replace('_', '-')

        if code not in lang_codes:
            # Try removing country part
            code = code.split('-')[0]

        if code in lang_codes:
            pkg_text = "firefox-i18n-{}".format(code)
            logging.debug("Adding firefox language package (%s)", pkg_text)
            return pkg_text

        logging.warning(
            "Firefox will be installed, but no i18n package for (%s) locale has been found.",
            self.locale)
        return None

    def hunspell(self):
        """ Adds hunspell dictionary """
        # Try to load available languages from i18n-hunspell.txt (easy updating if necessary)
        lang_codes = self.get_package_i18n_codes('hunspell')

        # Lower everything
        code = self.locale.lower()
        lang_codes = [x.lower() for x in lang_codes]

        if code not in lang_codes:
             # Try removing country part
            code = code.split('_')[0]

        if code in lang_codes:
            pkg_text = "hunspell-{}".format(code)
            logging.debug("Adding hunspell language package (%s)", pkg_text)
            return pkg_text

        logging.warning(
            "Cannot find a hunspell dictionary for (%s) locale.",
            self.locale)
        return None

    def libreoffice(self):
        """ Adds libreoffice language package """
        lang_codes = self.get_package_i18n_codes('libreoffice')
        code = self.locale.replace('_', '-')

        if code not in lang_codes:
            # Try removing country part
            code = code.split('-')[0]

        if code in lang_codes:
            pkg_text = "libreoffice-fresh-{}".format(code)
            logging.debug("Adding i18n libreoffice package (%s)", pkg_text)
            return pkg_text

        logging.warning(
            "Cannot find a i18n libreoffice package for (%s) locale.",
            self.locale)
        return None


def _prepare_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '[%(asctime)s] [%(module)s] %(levelname)s: %(message)s')
    #"%Y-%m-%d %H:%M:%S.%f")
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

def _test_i18n_packages(locale):
    """ Test if i18n packages are found """
    i18n_pkgs = I18NPackages(locale, '/usr/share/cnchi/data')
    i18n_pkgs.libreoffice()
    i18n_pkgs.hunspell()
    i18n_pkgs.firefox()


if __name__ == '__main__':
    _prepare_logger()
    _test_i18n_packages('ca_ES.UTF-8')
