#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  logging_resources.py
#
#  Copyright © 2013-2018 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
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
#  along with Cnchi; If not, see <http://www.gnu.org/licenses/>.

""" Logging handler to log resources (for debugging purposes only) """

import logging
import resource
import time

class ResourcesFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None):
        """ Init base class """
        logging.Formatter.__init__(fmt, datefmt)

        self.resources = [
            ('ru_utime', 'User time'),
            ('ru_stime', 'System time'),
            ('ru_maxrss', 'Max. Resident Set Size'),
            ('ru_ixrss', 'Shared Memory Size'),
            ('ru_idrss', 'Unshared Memory Size'),
            ('ru_isrss', 'Stack Size'),
            ('ru_inblock', 'Block inputs'),
            ('ru_oublock', 'Block outputs')]

    def format(self, record):
        """ Ignore record and log resources usage """
        
        usage = resource.getrusage(resource.RUSAGE_SELF)

        msg = []
        template = "{0} {1} = {2}"
        for name, desc in self.resources:
            msg.append(template.format(desc, name, getattr(usage, name)))
        return "\n".join(msg)


