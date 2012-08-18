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


class ConsensoControl(object):
    def __init__(self, app):
        self._app = app
        self._factories = {}

    def join(self, channel, hostname, port):
        key = '{}:{}'.format(hostname, port)
        if key not in self._factories:
            f = ConsensoBotFactory(channel)
            self._factories[key] = f
            s = internet.TCPClient(hostname, port, f, 20)
            s.setServiceParent(self._app)
            f.join(channel)
            return
        else:
            f = self._factories[key]
            f.join(channel)


class RemoteControl(Referenceable):
    """ Main object to remotely manage the long-running Consenso process.
    """
    def __init__(self, app):
        self._control = ConsensoControl(app)

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
        self._control.join(server_channel, server_hostname, server_port)


def get_tub(application):
    myserver = RemoteControl(application)
    tub = Tub(certFile=os.path.join(consenso.directories.foolscap_dir, "pb2server.pem"))
    tub.listenOn("tcp:12345")
    tub.setLocation("localhost:12345")
    tub.registerReference(myserver, "remote-control", furlFile=furlfile)
    return tub

application = service.Application("Consenso Twisted Application")
get_tub(application).setServiceParent(application)
