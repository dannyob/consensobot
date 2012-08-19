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
        if channel not in self.factory.channels:
            self.factory.channels.append(channel)

    def left(self, channel):
        print("Left %s." % (channel,))
        if channel in self.factory.channels:
            self.factory.channels.remove(channel)

    def privmsg(self, user, channel, msg):
        print(msg)


class ConsensoBotFactory(protocol.ClientFactory):
    protocol = ConsensoBot

    def __init__(self, channel=None, nickname='consensobot'):
        self.channels = [channel]
        self.nickname = nickname
        self.client = []
        self.deferUntilSignedOn = defer.Deferred()
        self.signedOn = False
        self.join(channel)

    def clientConnectionLost(self, connector, reason):
        print("Lost connection (%s), reconnecting." % (reason,))
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print("Could not connect: %s" % (reason,))

    def _pass_onto_client(self, client_func, *args, **kwargs):
        if not self.signedOn:
            def defer_me(s):
                if s is None:
                    log.err("Something broke the chain of returned values in this deferral")
                    raise TypeError
                log.msg("Deferring {}".format(s))
                client_func(s, *args, **kwargs)
                return s
            self.deferUntilSignedOn.addCallback(defer_me)
            self.deferUntilSignedOn.addErrback(lambda s: log.err(s))
            return
        for c in self.client:
            client_func(c, *args, **kwargs)

    def join(self, channel):
        self._pass_onto_client(ConsensoBot.join, channel)

    def leave(self, channel):
        self._pass_onto_client(ConsensoBot.leave, channel)

    def announce(self, message):
        for i in self.channels:
            log.msg("I am saying {} on {}".format(message, i))
            self._pass_onto_client(ConsensoBot.say, i, message, 80)
