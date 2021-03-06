#!/usr/bin/env python
##
# consenso/bot/test_ircclient.py
###
"""consenso/bot/test_ircclient.py

"""

import os
import os.path


from consenso.bot.client import AnyConsensoProcess
import twisted.trial.unittest as unittest


class Test_ConsensoProcess(unittest.TestCase):
    def setUp(self):
        if os.path.exists("/tmp/pidfile"):
            os.unlink("/tmp/pidfile")
        self.ic = AnyConsensoProcess(pidfile="/tmp/pidfile")
        self.ic.start()

    def test_creates_daemon(self):
        pid = int(open('/tmp/pidfile', 'r').read())
        self.assertGreater(pid, 0)

    def test_got_pid(self):
        pid = int(open('/tmp/pidfile', 'r').read())
        self.assertEqual(pid, self.ic.pid)

    def test_got_furl(self):
        self.assert_(self.ic.furl())

    def test_second_process(self):
        """ Should just return with the pid and furl of previous one """
        second_ic = AnyConsensoProcess(pidfile="/tmp/pidfile")
        self.assertEquals(second_ic.pid, self.ic.pid)
        self.assertEquals(second_ic.furl(), self.ic.furl())

    def tearDown(self):
        self.ic.shutdown()

if __name__ == '__main__':
    import __main__
    suite = unittest.TestLoader().loadTestsFromModule(__main__)
    unittest.TextTestRunner(verbosity=1).run(suite)
