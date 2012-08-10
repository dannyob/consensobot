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
import appdirs
import os.path
import os
import datetime
import errno
import shutil


program_name = 'consensobot'

metadata = get_distribution(program_name).metadata

def mkdir_if_not_there(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise

data_dir = appdirs.user_data_dir(program_name, metadata.get('organization'))
mkdir_if_not_there(data_dir)

class Corpus():
    def __init__(self, location=None):
        self.storage_dir = os.path.join(data_dir, 'corpus')
        mkdir_if_not_there(self.storage_dir)
        self.texts = {i: open( os.path.join(self.storage_dir, i), 'r').read() for i in os.listdir(self.storage_dir)}
        return

    def clear(self):
        for fname in self.texts:
            os.unlink( os.path.join(self.storage_dir, fname) )
        self.texts = {}

    def _corpus_text_fname(self, fileobj):
        try:
            new_filename = None
            new_filename = os.path.split(fileobj.name)[1]
            if new_filename.startswith('<') and new_filename.endswith('>'):  # ie <stdin>
                new_filename = new_filename[1:-1]
        except AttributeError:
            new_filename = "Untitled"

        name, ext = os.path.splitext(new_filename)
        make_fn = lambda i: os.path.join(self.storage_dir, '%s(%d)%s' % (name, i, ext))
        for i in xrange(2, sys.maxint):
            uni_fn = make_fn(i)
            if not os.path.exists(uni_fn):
                return uni_fn

    def add_text(self, fileobj):
        new_path = self._corpus_text_fname(fileobj)
        shutil.copyfileobj(fileobj, open(new_path, 'w'))
        self.texts[new_path] = [] 


def command_add_text(parsed_args):
    corpus = Corpus()
    corpus.add_text(parsed_args.location)
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
