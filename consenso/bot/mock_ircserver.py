#!/usr/bin/env python
##
# mock_ircserver.py
###
"""mock_ircserver.py

"""

from twisted.words.service import InMemoryWordsRealm, IRCFactory, IRCUser, Group
from twisted.cred import checkers, portal, credentials
from twisted.internet import reactor, defer, task
from zope.interface import implements


class MockIRCServer (IRCUser):

    def irc_NICK(self, prefix, params):
        """Only changed slightly from superclass to allow
        /nick with no password"""
        try:
            nickname = params[0].decode(self.encoding)
        except UnicodeDecodeError:
            self.privmsg(
                "Nickserv",
                nickname,
                'Your nickname is cannot be decoded.  Please use ASCII or UTF-8.')
            self.transport.loseConnection()
            return

        if self.password is None:
            self.password = 'anonymous'

        password = self.password

        self.password = None
        self.logInAs(nickname, password)
        print(nickname, "appeared.")
        pass

    def userJoined(self, group, user):
        print(user.name, "joined", group.name)

    def userLeft(self, group, user, reason=None):
        print(user.name, "left", group.name)


class MockIRCFactory(IRCFactory):
    protocol = MockIRCServer


class MockCredChecker:
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (credentials.IAnonymous,
                            credentials.IUsernamePassword,
                            credentials.IUsernameHashedPassword)

    def requestAvatarId(self, credentials):
        return defer.succeed(credentials.username)


class MockIRCRealm(InMemoryWordsRealm):

    def __init__(self, *a, **kw):
        super(MockIRCRealm, self).__init__(*a, **kw)
        self.createGroupOnRequest = True

    def groupFactory(self, name):
        group = Group(name)
        self.groups[name] = group
        return group


if __name__ == '__main__':
    import os
    root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    realm = MockIRCRealm('mock_irc')
    checker = MockCredChecker()
    portal = portal.Portal(realm, [checker])
    factory = MockIRCFactory(realm, portal)
    reactor.listenTCP(4567, factory)

    def end_me():
        reactor.stop()
    d = task.deferLater(reactor, 5, end_me)  # kill myself after 5 seconds
    print "Running on port 4567, localhost"
    reactor.run()
