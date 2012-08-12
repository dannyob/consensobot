#!/usr/bin/env python
##
# irc.py
###
"""irc.py

"""

__author__ = "Danny O'Brien <http://www.spesh.com/danny/>"
__copyright__ = "Copyright Danny O'Brien"
__contributors__ = None
__license__ = "GPL v3"

from behave import given

@given(u'a mock IRC server on localhost:4567')
def step(context):
    assert('Running on port 4567, localhost' in context.ircserver.output())

@then(u"the mock IRC server should output '{output}'")
def step(context, output):
    assert(output in context.ircserver.output())

@then(u"the mock IRC server should not output '{output}'")
def step(context, output):
    assert(not (output in context.ircserver.output()))
