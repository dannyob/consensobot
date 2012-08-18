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


class IRCAddress(object):
    def __init__(self, hostname, port, channel):
        self.hostname = hostname
        self.port = port
        self.channel = channel

    def __repr__(self):
        return "{} on {}:{}".format(self.channel, self.hostname, self.port)


class ConsensoControl(object):
    def __init__(self, app):
        self._app = app
        self._factories = {}

    @staticmethod
    def _factory_key(address):
        return '{}:{}'.format(address.hostname, address.port)

    def join(self, address):
        key = self._factory_key(address)
        if key not in self._factories:
            f = ConsensoBotFactory(address.channel)
            self._factories[key] = f
            s = internet.TCPClient(address.hostname, address.port, f, 20)
            s.setServiceParent(self._app)
            f.join(address.channel)
        else:
            f = self._factories[key]
            f.join(address.channel)

    def leave(self, address):
        key = self._factory_key(address)
        if key not in self._factories:
            return
        else:
            f = self._factories[key]
            f.leave(address.channel)


class RemoteControl(Referenceable):
    """ Main object to remotely manage the long-running Consenso process.
    """
    @staticmethod
    def parse_irc_uri(url):
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
        return IRCAddress(server_hostname, server_port, server_channel)

    def __init__(self, app):
        self._control = ConsensoControl(app)

    def remote_join(self, url):
        address = self.parse_irc_uri(url)
        print "I am trying to join {}".format(address)
        self._control.join(address)

    def remote_leave(self, url):
        address = self.parse_irc_uri(url)
        print "I am trying to leave {}".format(address)
        self._control.leave(address)


def get_tub(application):
    myserver = RemoteControl(application)
    tub = Tub(certFile=os.path.join(consenso.directories.foolscap_dir, "pb2server.pem"))
    tub.listenOn("tcp:12345")
    tub.setLocation("localhost:12345")
    tub.registerReference(myserver, "remote-control", furlFile=furlfile)
    return tub

application = service.Application("Consenso Twisted Application")
get_tub(application).setServiceParent(application)
