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

import sys
import argparse
from distutils2.database import get_distribution
metadata = get_distribution('consensobot').metadata


class Corpus():
    def __init__(self, location=None):
        self.texts = []
        return

    def clear(self):
        self.texts = []


def command_add_text(parsed_args):
    print("I have learned {}".format(parsed_args.location.name))


def main(args=sys.argv):
    parser = argparse.ArgumentParser(description=metadata.get('summary'),
            epilog="Mail {} <{}> with bugs and features.".format(metadata.get('maintainer'),
                metadata.get('maintainer_email')))
    subparsers = parser.add_subparsers()
    parser_add_text = subparsers.add_parser('add_text',
            help='Adds a text file to corpus of Consenso markov knowledge.')
    parser_add_text.add_argument('location', type=argparse.FileType())
    parser_add_text.set_defaults(func=command_add_text)
    parsed_args = parser.parse_args(args)
    parsed_args.func(parsed_args)
