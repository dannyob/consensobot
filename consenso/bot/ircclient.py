#!/usr/bin/env python
##
# consenso/bot/ircclient.py
###
"""consenso/bot/ircclient.py

"""

__author__ = "Danny O'Brien <http://www.spesh.com/danny/>"
__copyright__ = "Copyright Danny O'Brien"
__contributors__ = None
__license__ = "GPL v3"

import urlparse
import subprocess
import os.path
import tempfile
import os
import signal


class BotError(Exception):
    pass


class ProcessError(BotError):
    pass


class IrcClient(object):
    def __init__(self, url):
        components = urlparse.urlparse(url, scheme='irc')
        self.url = url
        self.server_port = components.port
        self.server_hostname = components.hostname
        self.server_groups = [components.path.strip('/')]

    def run(self, pidfile=None):
        this_dir = os.path.split(__file__)[0]
        command = ['twistd', '--python={}'.format(os.path.join(this_dir, 'ConsensoBotTac.py'))]
        if not pidfile:
            (f, pidfile) = tempfile.NamedTemporaryFile(
                    prefix="consensobot", suffix="pid", delete=False)
            f.close()
        command.append("--pidfile={}".format(pidfile))
        self.pidfile = pidfile
        status = subprocess.call(command)
        if status != 0:
            raise ProcessError(status)
        while (1):  # FIXME shouldn't buzz around a loop, should use select
            try:
                pid = int(file(self.pidfile, "r").read())
            except (IOError, ValueError):
                pid = 0
            if pid > 0:
                break
        self.pid = int(file(self.pidfile, "r").read())

    def kill(self):
        self.pid = int(file(self.pidfile, "r").read())
        os.kill(self.pid, signal.SIGTERM)
        os.unlink(self.pidfile)
