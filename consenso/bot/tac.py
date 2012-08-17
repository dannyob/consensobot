#!/usr/bin/env python
##
# tac.py
###
"""tac.py

Twisted Application .tac file for the Consenso process.

See <http://twistedmatrix.com/documents/current/core/howto/application.html>
"""

import os
import urlparse

from twisted.application import service, internet
from foolscap.api import Referenceable, Tub

import consenso.directories
from consenso.bot.ircclient import ConsensoBotFactory

furlfile = os.path.join(consenso.directories.foolscap_dir, "root.furl")


class RemoteControl(Referenceable):
    def remote_join(self, url):
        components = urlparse.urlparse(url, scheme='irc')
        if components.port:
            server_port = components.port
        else:
            server_port = 6667
        if components.hostname:
            server_hostname = components.hostname
        else:
            server_hostname = 'localhost'
        server_channel = components.path.strip('/')
        print "I am trying to join {} on {}:{}".format(server_channel, server_hostname, server_port)
        f = ConsensoBotFactory(server_channel)
        s = internet.TCPClient(server_hostname, server_port, f, 20)
        s.setServiceParent(application)


def get_tub():
    myserver = RemoteControl()
    tub = Tub(certFile=os.path.join(consenso.directories.foolscap_dir, "pb2server.pem"))
    tub.listenOn("tcp:12345")
    tub.setLocation("localhost:12345")
    tub.registerReference(myserver, "remote-control", furlFile=furlfile)
    return tub

application = service.Application("Consenso Twisted Application")
get_tub().setServiceParent(application)
