#!/usr/bin/env python
##
# features/environment.py
###
"""features/environment.py

"""

import os
from consenso.bot.mock import Ircserver

def before_tag(context, tag):
    if tag == 'ircserver':
        context.ircserver = Ircserver()
        context.ircserver.run()
    while (1):
        output = context.ircserver.output()
        if 'Running' in output:
            break


def after_tag(context, tag):
    if tag == 'ircserver':
        if context.ircserver:
            context.ircserver.kill()
