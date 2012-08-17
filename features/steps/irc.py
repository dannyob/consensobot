#!/usr/bin/env python
##
# irc.py
###
"""irc.py

"""

from time import sleep

from behave import given

@given(u'a mock IRC server on localhost:4567')
def step(context):
    assert('Running on port 4567, localhost' in context.ircserver.output())

@then(u"the mock IRC server should output '{output}' within {timeout} seconds")
def step(context, output, timeout):
    sleep(float(timeout))
    assert(output in context.ircserver.output())

@then(u"the mock IRC server should not output '{output}' within {timeout} seconds")
def step(context, output, timeout):
    sleep(float(timeout))
    assert(not (output in context.ircserver.output()))
