#!/usr/bin/env python
##
# consenso/bot/ircclient.py
###
"""consenso/bot/ircclient.py

"""

from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet import defer
from twisted.python import log


class ConsensoBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.factory.client.append(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        if self in self.factory.client:
            self.factory.client.remove(self)
        self.factory.signedOn = False

    def signedOn(self):
        print("Signed on as %s." % (self.nickname,))
        self.factory.signedOn = True
        self.factory.deferUntilSignedOn.callback(self)

    def joined(self, channel):
        print("Joined %s." % (channel,))

    def privmsg(self, user, channel, msg):
        print(msg)


class ConsensoBotFactory(protocol.ClientFactory):
    protocol = ConsensoBot

    def __init__(self, channel, nickname='consensobot'):
        self.channel = channel
        self.nickname = nickname
        self.client = []
        self.deferUntilSignedOn = defer.Deferred()
        self.signedOn = False

    def clientConnectionLost(self, connector, reason):
        print("Lost connection (%s), reconnecting." % (reason,))
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print("Could not connect: %s" % (reason,))

    def join(self, channel):
        if not self.signedOn:
            def defer_join(s):
                log.msg("I am joining {} via {} (deferred)".format(channel, s))
                s.join(channel)
            self.deferUntilSignedOn.addCallback(defer_join)
            self.deferUntilSignedOn.addErrback(lambda s: log.err(s))
            return
        for c in self.client:
            log.msg("I am joining {} via {}".format(channel, c))
            c.join(channel)

    def leave(self, channel):
        if not self.signedOn:
            def defer_leave(s):
                log.msg("I am leaving {} via {} (deferred)".format(channel, s))
                s.leave(channel)
            self.deferUntilSignedOn.addCallback(defer_leave)
            self.deferUntilSignedOn.addErrback(lambda s: log.err(s))
        for c in self.client:
            log.msg("I am leaving {} via {}".format(channel, c))
            c.leave(channel)
