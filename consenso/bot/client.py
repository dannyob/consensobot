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
import os
import signal
import errno

import consenso.directories


class NoGoodFurl(Exception):
    pass


class ConsensoProcess(object):

    furlfile = os.path.join(consenso.directories.foolscap_dir, "root.furl")
    default_pidfile = os.path.join(consenso.directories.foolscap_dir, "pid")

    def __init__(self, pidfile=None, logfile=None):
        self.pid = None
        self._furl = None
        if not pidfile:
            pidfile = self.default_pidfile
        if not logfile:
            logfile = os.path.join(consenso.directories.log_dir, 'client.log')
        self._pidfile = pidfile
        self._logfile = logfile
        try:
            pid = int(file(self._pidfile, "r").read())
        except (IOError, ValueError):
            return
        try:
            os.kill(pid, 0)
        except (IOError, OSError) as e:
            if e.errno in (errno.ENOENT, errno.ESRCH):
                return
            raise
        self.pid = pid
        try:
            self.furl()
        except NoGoodFurl:
            print "I found a running ConsensoProcess but not a valid furl"
            raise

    def start(self):
        if self.pid:
            return
        this_dir = os.path.split(__file__)[0]
        command = ['twistd', '--python={}'.format(os.path.join(this_dir, 'tac.py'))]
        command.append("--pidfile={}".format(self._pidfile))
        command.append("--logfile={}".format(self._logfile))
        if os.path.exists(self.furlfile):
            os.unlink(self.furlfile)
        subprocess.check_call(command, stderr=subprocess.STDOUT)
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
            except IOError as e:
                print e
                print "Have you remembered to start() the ConsensoProcess?"
                raise NoGoodFurl
            self._furl = furl
        return self._furl

    def shutdown(self):
        if self.pid:
            os.kill(self.pid, signal.SIGTERM)
        if self._pidfile:
            os.unlink(self._pidfile)
        if self.furlfile:
            os.unlink(self.furlfile)
