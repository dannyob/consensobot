#!/usr/bin/env python
##
# consenso/bot/client
###
"""consenso/bot/client

"""

import subprocess
import os.path
import os
import signal
import errno

import consenso.directories


class NoGoodFurl(Exception):
    """ Raised if we cannot use an old foolscap URL, found in an old furlfile, or else
    we expected to find a furl in a furlfile, but it wasn't there."""
    pass


class CannotChangeConsensoLogfile(Exception):
    """ ConsensoProcess can find an old process and operate it, but it can't
    tell it to change logfile. If a new logfile is specified when creating a new
    ConsensoProcess, and we find an old process, we raise this error."""
    pass


def delete_file_if_exists(fname):
    if fname is None:
        return
    if os.path.exists(fname):
        os.unlink(fname)


class ConsensoProcess(object):
    """ Encapsulates an external consenso long-running process.

    ConsensoProcess will start a new process if necessary, but tries to find an
    old process that's already running to talk to first.

    Args:
        pidfile: file to store (or look for) the pid
        logfile: file to store logs

    """

    default_furlfile = os.path.join(consenso.directories.foolscap_dir, "root.furl")
    default_pidfile = os.path.join(consenso.directories.foolscap_dir, "pid")

    def _process_exists(self, pid):
        try:
            os.kill(pid, 0)
        except (IOError, OSError) as e:
            if e.errno in (errno.ENOENT, errno.ESRCH):
                return False
            raise
        return True

    def __init__(self, pidfile=None, logfile=None):
        self.pid = None
        self._furl = None
        self._furlfile = self.default_furlfile
        if not pidfile:
            pidfile = self.default_pidfile
        self._pidfile = pidfile
        if not logfile:
            self._logfile = os.path.join(consenso.directories.log_dir, 'client.log')
        else:
            self._logfile = logfile
        try:
            pid = int(file(self._pidfile, "r").read())
        except (IOError, ValueError):
            return
        if self._process_exists(pid):
            self.pid = pid
            if logfile is not None:
                raise CannotChangeConsensoLogfile

    def start(self):
        if self.pid:
            return
        this_dir = os.path.split(__file__)[0]
        command = ['twistd', '--python={}'.format(os.path.join(this_dir, 'tac.py'))]
        command.append("--pidfile={}".format(self._pidfile))
        command.append("--logfile={}".format(self._logfile))
        delete_file_if_exists(self._furlfile)
        subprocess.check_call(command, stderr=subprocess.STDOUT)
        pid = 0
        furl = ""
        while (pid == 0 or furl == ""):  # FIXME shouldn't buzz around a loop, should use select
            try:
                pid = int(file(self._pidfile, "r").read())
            except (IOError, ValueError):
                pid = 0
            try:
                furl = file(self._furlfile, "r").read()
            except:
                furl = ""
        self.pid = pid
        self._furl = furl

    def furl(self):
        if not self._furl:
            try:
                furl = file(self._furlfile, "r").read()
            except IOError as e:
                print e
                if self.pid is None:
                    print "Have you remembered to start() the ConsensoProcess?"
                else:
                    print "Process is running, but cannot find valid furlfile", self._furlfile
                raise NoGoodFurl
            self._furl = furl
        return self._furl

    def shutdown(self):
        if self.pid:
            os.kill(self.pid, signal.SIGTERM)
        delete_file_if_exists(self._pidfile)
        delete_file_if_exists(self._furlfile)
