#!/usr/bin/env python
##
# consenso/bot/client
###
"""consenso/bot/client

"""

__author__ = "Danny O'Brien <http://www.spesh.com/danny/>"
__copyright__ = "Copyright Danny O'Brien"
__contributors__ = None
__license__ = "GPL v3"

import subprocess
import os.path
import tempfile
import os
import signal

import consenso.directories


class ConsensoProcess(object):

    furlfile = os.path.join(consenso.directories.foolscap_dir, "root.furl")

    def __init__(self, pidfile=None, logfile=None):
        self.pid = None
        self._furl = None
        if not pidfile:
            (f, pidfile) = tempfile.NamedTemporaryFile(
                    prefix="consensobot", suffix="pid", delete=False)
            f.close()
        if not logfile:
            logfile = os.path.join(consenso.directories.log_dir, 'client.log')
        self._pidfile = pidfile
        self._logfile = logfile

    def start(self):
        this_dir = os.path.split(__file__)[0]
        command = ['twistd', '--python={}'.format(os.path.join(this_dir, 'tac.py'))]
        command.append("--pidfile={}".format(self._pidfile))
        command.append("--logfile={}".format(self._logfile))
        if os.path.exists(self.furlfile):
            os.unlink(self.furlfile)
        subprocess.call(command, stderr=subprocess.STDOUT)
        pid = 0
        furl = ""
        while (pid == 0 or furl == ""):  # FIXME shouldn't buzz around a loop, should use select
            try:
                pid = int(file(self._pidfile, "r").read())
            except (IOError, ValueError):
                pid = 0
            try:
                furl = file(self.furlfile, "r").read()
            except:
                furl = ""
        self.pid = pid
        self._furl = furl

    def furl(self):
        if not self._furl:
            try:
                furl = file(self.furlfile, "r").read()
            except IOError:
                furl = None
            self._furl = furl
        return self._furl

    def shutdown(self):
        if self.pid:
            os.kill(self.pid, signal.SIGTERM)
        if self._pidfile:
            os.unlink(self._pidfile)
        if self.furlfile:
            os.unlink(self.furlfile)
