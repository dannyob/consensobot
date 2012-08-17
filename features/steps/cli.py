#!/usr/bin/env python
##
# cli.py
###
"""cli.py

Steps for the command line

"""

from behave import when, then
from consenso.bot import cli
import shlex


@when(u"I type 'consensobot {args}'")
def step(context, args=None):
    cli.main(shlex.split(args))


@then(u"the CLI should output '{result}'")
def step2(context, result=None):
    assert result in context.stdout_capture.getvalue()
