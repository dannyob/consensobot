#!/usr/bin/env python
##
# cli.py
###
"""cli.py

Steps for the command line

"""

__author__ = "Danny O'Brien <http://www.spesh.com/danny/>"
__copyright__ = "Copyright Danny O'Brien"
__contributors__ = None
__license__ = "GPL v3"

from behave import when, then
from consenso.bot import cli
import shlex


@when(u"I type 'consensobot {args}'")
def step(context, args=None):
    cli.main(shlex.split(args))


@then(u"the CLI should output '{result}'")
def step2(context, result=None):
    assert result in context.stdout_capture.getvalue()
