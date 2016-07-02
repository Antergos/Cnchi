#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ui_controller.py
#
# Copyright © 2013-2016 Antergos
#
# This file is part of Cnchi.
#
# Cnchi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Cnchi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# The following additional terms are in effect as per Section 7 of the license:
#
# The preservation of all legal notices and author attributions in
# the material or in the Appropriate Legal Notices displayed
# by works containing it is required.
#
# You should have received a copy of the GNU General Public License
# along with Cnchi; If not, see <http://www.gnu.org/licenses/>.

""" UI Controller Module """

import json
import logging

from .base_widgets import BaseObject, WebKit2


class Controller(BaseObject):
    """
    UI Controller

    Class Attributes:
        _emit_js_tpl (str): Javascript string used to emit signals in web_view.
        See also `BaseWidget.__doc__`

    """

    _emit_js_tpl = 'window.cnchi._emit(%s)'

    def __init__(self, name='controller', parent=None,
                 tpl_engine='jinja', logger=None, *args, **kwargs):

        super().__init__(
            name=name, parent=parent, tpl_engine=tpl_engine, logger=logger, *args, **kwargs
        )

    def decide_policy_cb(self, view, decision, decision_type):
        if decision_type == WebKit2.PolicyDecisionType.NAVIGATION_ACTION:
            # grab the requested URI
            uri = decision.get_request().get_uri()
            pass

    def emit_js(self, name, *args):
        msg = json.dumps([name] + list(args))
        self._web_view.run_javascript(self._emit_js_tpl.format(msg))

    def load_changed_cb(self, view, event):
        pass

    def title_changed_cb(self, view, event):
        incoming_data = view.get_title()

        # check for "_BR::" prefix to determine we're crossing the python/JS bridge
        if not incoming_data or not incoming_data.startswith('_BR::'):
            return

        try:
            incoming_data = json.loads(incoming_data[5:])

            name = incoming_data.setdefault('name', '')
            args = incoming_data.setdefault('args', [])

            # emit our python/js bridge signal
            self._cnchi_app.emit('on-js', name, args)

        except Exception as err:
            logging.exception(err)

    def uri_resource_cb(self, request):
        pass
        # path = o = request.get_uri().split('?')[0]
        #
        # if path == 'app:///':
        #     path = self._uri_app_base + 'app.html'
        #
        # else:
        #     path = path.replace('app://', self._uri_app_base)
        #
        #     # variable substitution
        #     path = path.replace('$backend', 'gtk3')
        #
        # logger.debug('Loading app resource: {0} ({1})'.format(o, path))
        #
        # if os.path.exists(path):
        #     request.finish(Gio.File.new_for_path(path).read(None), -1,
        #                    Gio.content_type_guess(path, None)[0])
        #
        # else:
        #     raise Exception('App resource path not found: {0}'.format(path))

