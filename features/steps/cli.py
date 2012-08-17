#!/usr/bin/env python
##
# cli.py
###
"""cli.py

Steps for the command line

"""

import os
import subprocess
import shlex

from behave import when, then


@when(u"I type 'consensobot {args}'")
def step(context, args=None):
    command = [os.path.join(os.path.split(__file__)[0], "../../scripts/consensobot")]
    command += shlex.split(args)
    print command
    context.consensobot_output = subprocess.check_output(command)


@then(u"the CLI should output '{result}'")
def step2(context, result=None):
    assert result in context.consensobot_output
