#!/usr/bin/env python3
# Nagios Varnish Backend Check
# v1.3
# URL: www.admingeekz.com
# Contact: sales@admingeekz.com
#
#
# Copyright (c) 2013, AdminGeekZ Ltd
# All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2, as
# published by the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
#
#   13 Apr 2016 - Jeoffrey BAUVIN
#   Migrate to Varnish 4.1
#
#   21 Feb 2022 - Dennis Ullrich
#   Migrate to Python 3
#              Varnish 6.2
#   Improved output

import sys
import optparse
import subprocess


def runcommand(command, exit_on_fail=True):
    try:
        process = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE)
        output, unused_err = process.communicate()
        return output

    except OSError as e:
        nexit(2, f"Error: Executing command failed: {e}")


def nexit(exitCode, message):
    exitCodes = ('OK', 'WARNING', 'CRITICAL', 'UNKNOWN')
    print(f"{exitCodes[exitCode]}: {message}")
    sys.exit(exitCode)


def main(argv):
    o = optparse.OptionParser(
        conflict_handler="resolve",
        description="Nagios plugin to check varnish backend health.")
    o.add_option('-H', '--host',
                 action='store', type='string', dest='host',
                 default='127.0.0.1',
                 help='The ip varnishadm is listening on')
    o.add_option('-P', '--port',
                 action='store', type='int', dest='port',
                 default=6082,
                 help='The port varnishadm is listening on')
    o.add_option('-s', '--secret',
                 action='store', type='string', dest='secret',
                 default='/etc/varnish/secret',
                 help='The path to the secret file')
    o.add_option('-p', '--path',
                 action='store', type='string', dest='path',
                 default='/usr/bin/varnishadm',
                 help='The path to the varnishadm binary')

    options = o.parse_args()[0]
    command = runcommand(f"{options.path} -S {options.secret} "
                         f"-T {options.host}:{options.port} backend.list")
    backends = str(command.decode("utf-8")).split("\n")
    backends_healthy, backends_sick = [], []
    for line in backends:
        if line.startswith("boot") and line.find("test") == -1:
            if line.find("ealthy") != -1:
                backends_healthy.append(line.split(" ")[0])
            else:
                backends_sick.append(line.split(" ")[0])

    if backends_sick:
        totalBackends = len(backends_healthy) + len(backends_sick)
        nexit(2, f"{len(backends_sick)}/{totalBackends} backends are down: "
                 f"{', '.join(backends_sick)}")

    if not backends_sick and not backends_healthy:
        child_ok = False
        command = runcommand(f"{options.path} -S {options.secret} "
                             f"-T {options.host}:{options.port} status")
        response = str(command.decode("utf-8")).split("/n")
        for line in response:
            if line.startswith("Child in state running"):
                child_ok = True
                break

        if child_ok:
            nexit(0, "Child in state running")
        else:
            nexit(1, "No backends detected. "
                     "If this is an error, see readme.txt")

    nexit(0, f"{len(backends_healthy)} backends are healthy.")


if __name__ == "__main__":
    main(sys.argv[1:])
