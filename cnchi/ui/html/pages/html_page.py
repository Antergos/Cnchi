#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  _html_page.py
#
#  Copyright © 2016 Antergos
#
#  This file is part of The Antergos Build Server, (AntBS).
#
#  AntBS is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  AntBS is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  The following additional terms are in effect as per Section 7 of the license:
#
#  The preservation of all legal notices and author attributions in
#  the material or in the Appropriate Legal Notices displayed
#  by works containing it is required.
#
#  You should have received a copy of the GNU General Public License
#  along with AntBS; If not, see <http://www.gnu.org/licenses/>.

# Standard Lib
from _base_object import (
    os
)

# 3rd-party Libs
from ui.base_widgets import (
    Gtk,
    GLib
)

from jinja2 import (
    Environment,
    FileSystemLoader,
    PrefixLoader
)

# This application
from ui.base_widgets import (
    bg_thread,
    DataObject,
    Page,
    SharedData,
    Singleton,
)


class HTMLPage(Page, metaclass=Singleton):
    """
    Base class for HTML UI pages.

    Class Attributes:
        _tpl (SharedData): Descriptor object that handles access to Jinja2 template environment.
        Also see `Page.__doc__`

    """

    _tpl = SharedData('_tpl')
    _tpl_setup_ran = SharedData('_tpl_setup_running')
    _top_level_tabs = SharedData('_top_level_tabs')

    def __init__(self, name='HTMLPage', tpl_engine='jinja', *args, **kwargs):
        """
        Attributes:
            _tpl (Environment): The Jinja2 template environment.
            Also see `Page.__doc__`.

        Args:
            name (str): A name for this widget.

        """

        super().__init__(name=name, tpl_engine=tpl_engine, *args, **kwargs)

        self.signals = []
        self.tabs = []
        self.can_go_to_next_page = False

        if self._tpl is None and self._tpl_setup_ran is None:
            self._tpl_setup_ran = True
            self._initialize_template_engine()
            self._create_and_connect_special_signals()

        if self._pages_data is None:
            self.logger.debug('creating data object in _pages_data for %s..', name)
            self._pages_data = DataObject()
            self._pages_data.has_data = False

        if self._top_level_tabs is None:
            self.logger.debug('Generating main navigation tabs list..')
            self._generate_tabs_list()


    def _create_and_connect_signals(self):
        """
        Creates the page's signals and connects them to their callbacks (handlers).
        Signals should be appended to `self.signals` prior to calling this method.

        A corresponding result signal will be created for each signal and added to the
        allowed signals list automatically. Signal names will have 'do-' prepended to them.
        Their corresponding result signal will have '-result' appended to it.

        The name of the callback method that will be registered for each signal will be the
        signal name as it appears in `self.signals` at the time of calling this method with
        hyphens replaced by underscores and should end with '_cb'.

        Signal names that start with two hyphens are ignored by this method.

        Example:
            >>> self.signals = ['some-action', 'some-other-action', '--private-action']
            >>> self._create_and_connect_signals()
            >>> self.signals
                ['do-some-action', 'some-action-result', 'do-other-action',
                 'other-action-result', '_private_action']

            With the above, these callback methods would have been registered (they must exist):
                'do-some-action':  `self.some_action_cb`
                'do-other-action': `self.other_action_cb`

        """

        __signals = []

        for _signal in self.signals:
            if _signal.startswith('--'):
                __signals.append(_signal)
                continue

            cb_name = '{}_cb'.format(_signal.replace('-', '_'))
            callback = getattr(self, cb_name)
            result_signal = '{}-result'.format(_signal)
            _signal = 'do-{}'.format(_signal)

            for __signal in [_signal, result_signal]:
                if __signal not in self._allowed_signals:
                    self._allowed_signals.append(__signal)
                    self._main_window.create_custom_signal(__signal)
                    __signals.append(__signal)

            self._main_window.connect(_signal, callback)

        self.signals = __signals

    def _create_and_connect_special_signals(self):
        # TODO: This is garbage. Come up with something better.
        for _signal, callback in [('go-to-next-page', self.go_to_next_page), ('trigger_event', '')]:
            if _signal not in self._allowed_signals:
                self._allowed_signals.append(_signal)
                self._main_window.create_custom_signal(_signal)
                if '' != callback:
                    self._main_window.connect(_signal, callback)

    def _generate_tabs_list(self):
        tabs = self._pages_helper.get_page_names()
        excluded = ['language', 'welcome']
        self._top_level_tabs = [(t, False) for t in tabs if t not in excluded]

    def _get_default_template_vars(self):
        return {'page_name': self.name, 'top_level_tabs': self._top_level_tabs}

    def _initialize_template_engine(self):
        resources_path = 'cnchi://{}'.format(os.path.join(self.PAGES_DIR, 'resources'))
        tpl_map = {
            pdir: FileSystemLoader(os.path.join(self.PAGES_DIR, pdir)) for pdir in self._page_dirs
        }
        tpl_map['pages'] = FileSystemLoader(self.PAGES_DIR)
        self._tpl = Environment(loader=PrefixLoader(tpl_map), lstrip_blocks=True, trim_blocks=True)
        self._tpl.globals['RESOURCES_DIR'] = resources_path
        self._tpl.add_extension('jinja2.ext.do')
        self._tpl.add_extension('jinja2.ext.i18n')
        self._tpl.install_null_translations(newstyle=True)

    def _set_active_tab(self):
        self._top_level_tabs = [(t, self.name == t) for t in self._top_level_tabs]

    def emit_js(self, name, *args):
        """ See `Controller.emit_js.__doc__` """
        self._controller.emit_js(name, *args)

    def get_next_page_index(self):
        return self._pages_helper.page_names.index(self.name) + 1

    def get_previous_page_index(self):
        return self._pages.helper.page_names.index(self.name) - 1

    def go_to_next_page(self, obj=None, next_plus=0):
        if self.name != self._controller.current_page:
            return

        if not next_plus:
            next_plus = 0

        self.store_values()
        self._controller.set_current_page(self.get_next_page_index() + next_plus)

        return True

    def prepare(self):
        """ This must be implemented by subclasses """
        pass

    def render_template(self, name=None, tpl_vars=None):
        name = name if name is not None else self.template
        default_tpl_vars = self._get_default_template_vars()
        tpl = self._tpl.get_template(name)

        if tpl_vars is not None:
            tpl_vars = tpl_vars.update(default_tpl_vars)
        else:
            tpl_vars = default_tpl_vars

        return tpl.render(tpl_vars)

    def render_template_as_bytes(self, name=None, tpl_vars=None):
        tpl = self.render_template(name=name, tpl_vars=tpl_vars)
        return tpl.encode('UTF-8')

    def store_values(self):
        """ This must be implemented by subclasses """
        self._pages_data.has_data = True
