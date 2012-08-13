#!/usr/bin/env python
##
# ircbot.tac
###
"""ircbot.tac

Twisted Application .tac file
See <http://twistedmatrix.com/documents/current/core/howto/application.html>
"""

__author__ = "Danny O'Brien <http://www.spesh.com/danny/>"
__copyright__ = "Copyright Danny O'Brien"
__contributors__ = None
__license__ = "GPL v3"

from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.application import service, internet


class ConsensoBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, channel, msg):
        print msg


class ConsensoBotFactory(protocol.ClientFactory):
    protocol = ConsensoBot

    def __init__(self, channel, nickname='ConsensoSimple'):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

application = service.Application("Consenso Twisted Application")