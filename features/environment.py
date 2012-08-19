#!/usr/bin/env python
##
# features/environment.py
###
"""features/environment.py

"""

from consenso.bot.mock import Ircserver
from consenso.bot.client import NewConsensoProcess, ExistingConsensoProcess


def before_tag(context, tag):
    if tag == 'ircserver':
        context.ircserver = Ircserver()
        context.ircserver.run()
        while (1):
            output = context.ircserver.output()
            if 'Running' in output:
                break
    if tag == 'consensoserver':
        NewConsensoProcess()


def after_tag(context, tag):
    if tag == 'ircserver':
        if context.ircserver:
            context.ircserver.kill()
    if tag == 'consensoserver':
        ExistingConsensoProcess().shutdown()
