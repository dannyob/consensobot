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

import os
import os.path


from consenso.bot.client import ConsensoProcess
import twisted.trial.unittest as unittest


class Test_ConsensoProcess(unittest.TestCase):
    def setUp(self):
        if os.path.exists("/tmp/pidfile"):
            os.unlink("/tmp/pidfile")
        self.ic = ConsensoProcess(pidfile="/tmp/pidfile")
        self.ic.start()

    def test_creates_daemon(self):
        pid = int(open('/tmp/pidfile', 'r').read())
        self.assertGreater(pid, 0)

    def test_got_pid(self):
        pid = int(open('/tmp/pidfile', 'r').read())
        self.assertEqual(pid, self.ic.pid)

    def test_got_furl(self):
        self.assert_(self.ic.furl())

    def tearDown(self):
        self.ic.shutdown()

if __name__ == '__main__':
    import __main__
    suite = unittest.TestLoader().loadTestsFromModule(__main__)
    unittest.TextTestRunner(verbosity=1).run(suite)
