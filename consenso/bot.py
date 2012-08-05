#!/usr/bin/env python
##
# bot.py
###
"""consensobot

Runs a consensobot on your choice of IRC network.
"""

__author__ = "Danny O'Brien <http://www.spesh.com/danny/>"
__copyright__ = "Copyright Danny O'Brien"
__contributors__ = None
__license__ = "GPL v3"

import argparse
from distutils2.database import get_distribution
metadata = get_distribution('consensobot').metadata


def main():
    parser = argparse.ArgumentParser(description=metadata.get('summary'),
            epilog="Mail {} <{}> with bugs and features.".format(metadata.get('maintainer'),
                metadata.get('maintainer_email')))
    parser.parse_args()
