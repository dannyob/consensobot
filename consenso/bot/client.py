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

import consenso.directories

furlfile = os.path.join(consenso.directories.foolscap_dir, "root.furl")


class BotClient(object):
    def __init__(self):
        self.pid = None
        self.furl = None
        self.pidfile = None

    def run(self, pidfile=None, logfile=None):
        this_dir = os.path.split(__file__)[0]
        command = ['twistd', '--python={}'.format(os.path.join(this_dir, 'tac.py'))]
        if not pidfile:
            (f, pidfile) = tempfile.NamedTemporaryFile(
                    prefix="consensobot", suffix="pid", delete=False)
            f.close()
        if not logfile:
            logfile = os.path.join(consenso.directories.log_dir, 'client.log')
        self.pidfile = pidfile
        command.append("--pidfile={}".format(pidfile))
        self.logfile = logfile
        command.append("--logfile={}".format(logfile))
        if os.path.exists(furlfile):
            os.unlink(furlfile)
        subprocess.call(command, stderr=subprocess.STDOUT)
        pid = 0
        furl = ""
        while (pid == 0 or furl == ""):  # FIXME shouldn't buzz around a loop, should use select
            try:
                pid = int(file(self.pidfile, "r").read())
            except (IOError, ValueError):
                pid = 0
            try:
                furl = file(furlfile, "r").read()
            except:
                furl = ""
        self.pid = pid
        self.furl = furl

    def join(self, url):
        components = urlparse.urlparse(url, scheme='irc')
        self.url = url
        self.server_port = components.port
        self.server_hostname = components.hostname
        self.server_groups = [components.path.strip('/')]

    def kill(self):
        if self.pid:
            os.kill(self.pid, signal.SIGTERM)
        if self.pidfile:
            os.unlink(self.pidfile)
        if furlfile:
            os.unlink(furlfile)
