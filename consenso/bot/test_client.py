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

#import unittest
import os
import os.path
import signal

from consenso.bot.client import BotClient
import twisted.trial.unittest as unittest


class Test_BotClient(unittest.TestCase):
    def setUp(self):
        self.ic = BotClient()

    def test_creates_daemon(self):
        if os.path.exists("/tmp/pidfile"):
            os.unlink("/tmp/pidfile")
        self.ic.run(pidfile="/tmp/pidfile")
        pid = int(open('/tmp/pidfile', 'r').read())
        if pid:
            os.kill(pid, signal.SIGTERM)
        self.assertGreater(pid, 0)

    def test_got_pid(self):
        if os.path.exists("/tmp/pidfile"):
            os.unlink("/tmp/pidfile")
        self.ic.run(pidfile="/tmp/pidfile")
        pid = int(open('/tmp/pidfile', 'r').read())
        self.assertEqual(pid, self.ic.pid)

    def tearDown(self):
        self.ic.kill()

if __name__ == '__main__':
    import __main__
    suite = unittest.TestLoader().loadTestsFromModule(__main__)
    unittest.TextTestRunner(verbosity=1).run(suite)
