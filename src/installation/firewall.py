#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  firewall.py
#
#  Copyright © 2013,2014 Antergos
#  Based on parts of ufw code © 2012 Canonical
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

""" Manage ufw setup """

import logging
from installation import chroot

try:
    import ufw
    _UFW = True
except ImportError as err:
    _UFW = False

def run(params):
    cmd = ["ufw"]
    cmd.extend(params)

    if not _UFW:
        # Call ufw command directly
        chroot.run(cmd, DEST_DIR)
        return

    app_action = False
    pr = None

    # Remember, will have to take --force into account if we use it with 'app'
    idx = 1
    if len(cmd) > 1 and cmd[1].lower() == "--dry-run":
        idx += 1

    if len(cmd) > idx and cmd[idx].lower() == "app":
        app_action = True

    try:
        pr = ufw.frontend.parse_command(sys.argv)
        ui = ufw.frontend.UFWFrontend(pr.dryrun)
        if app_action and 'type' in pr.data and pr.data['type'] == 'app':
            res = ui.do_application_action(pr.action, pr.data['name'])
        else:
            bailout = False
            if pr.action == "enable" and not pr.force and \
               not ui.continue_under_ssh():
                res = _("Aborted")
                bailout = True

            if not bailout:
                if 'rule' in pr.data:
                    res = ui.do_action(
                        pr.action,
                        pr.data['rule'],
                        pr.data['iptype'],
                        pr.force)
                else:
                    res = ui.do_action(
                        pr.action,
                        "",
                        "",
                        pr.force)
    except (ValueError, UFWError) as err:
        logging.warning(err)
        # Call ufw command directly
        chroot.run(cmd, DEST_DIR)
