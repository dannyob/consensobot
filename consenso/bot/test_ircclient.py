#!/usr/bin/env python
##
# consenso/bot/test_ircclient.py
###
"""consenso/bot/test_ircclient.py

"""

__author__ = "Danny O'Brien <http://www.spesh.com/danny/>"
__copyright__ = "Copyright Danny O'Brien"
__contributors__ = None
__license__ = "GPL v3"

import unittest
import os
import os.path
import signal

from consenso.bot.ircclient import IrcClient


class Ircclient(unittest.TestCase):
    def test_understands_urls(self):
        ic = IrcClient("irc://localhost:1234/#hello")
        self.assertEquals(ic.server_hostname, 'localhost')
        self.assertEquals(ic.server_port, 1234)
        self.assertIn("#hello", ic.server_groups)

    def test_creates_daemon(self):
        ic = IrcClient("irc://localhost:1234/#hello")
        if os.path.exists("/tmp/pidfile"):
            os.unlink("/tmp/pidfile")
        ic.run(pidfile="/tmp/pidfile")
        pid = int(open('/tmp/pidfile', 'r').read())
        if pid:
            os.kill(pid, signal.SIGTERM)
        self.assertGreater(pid, 0)

if __name__ == '__main__':
    import __main__
    suite = unittest.TestLoader().loadTestsFromModule(__main__)
    unittest.TextTestRunner(verbosity=1).run(suite)
