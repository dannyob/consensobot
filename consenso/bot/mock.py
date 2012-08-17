#!/usr/bin/env python
##
# consenso/bot/mock.py
###
"""consenso/bot/mock.py

"""

import subprocess
import fcntl
import os
import os.path


this_dir = os.path.split(__file__)[0]


class Ircserver(object):
    @staticmethod
    def _non_block_read(output):
        """Fiddles with fd so that it will be non-blocking.

        Used with stdout and stderr"""
        fd = output.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        try:
            return output.read()
        except:
            return ""

    def __init__(self):
        self._process = None
        self._results = ""

    def run(self):
        self._process = subprocess.Popen(
                os.path.join(this_dir, "mock_ircserver.py"),
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def output(self):
        self._results += self._non_block_read(self._process.stdout) \
                + self._non_block_read(self._process.stderr)
        return self._results

    def kill(self):
        self._process.kill()
