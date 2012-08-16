#!/usr/bin/env python
##
# tac.py
###
"""tac.py

Twisted Application .tac file for the Consenso process.

See <http://twistedmatrix.com/documents/current/core/howto/application.html>
"""

__author__ = "Danny O'Brien <http://www.spesh.com/danny/>"
__copyright__ = "Copyright Danny O'Brien"
__contributors__ = None
__license__ = "GPL v3"

import os

from twisted.application import service
from foolscap.api import Referenceable, Tub

import consenso.directories


class RemoteControl(Referenceable):
    def remote_irc_joint(self, host, port, group=None, nick=None):
        print "I am trying to join {} on {}:{} as {}".format(group, host, port, nick)

myserver = RemoteControl()
tub = Tub(certFile=os.path.join(consenso.directories.foolscap_dir, "pb2server.pem"))
tub.listenOn("tcp:12345")
tub.setLocation("localhost:12345")
url = tub.registerReference(myserver, "remote-control")
print("pid ", os.getpid())
print("furl ", url)

application = service.Application("Consenso Twisted Application")
tub.setServiceParent(application)
