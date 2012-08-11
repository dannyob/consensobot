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

def mkdir_if_not_there(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise

program_name = 'consensobot'
metadata = get_distribution(program_name).metadata

data_dir = appdirs.user_data_dir(program_name, metadata.get('organization'))
mkdir_if_not_there(data_dir)
storage_dir = os.path.join(data_dir, 'corpus')
mkdir_if_not_there(storage_dir)


def firstline_of_file(path):
    f = open(path, 'r')
    l = f.readline().strip()
    try:
        while l == "":
            l = f.readline().strip
    except EOFError:
        return "Empty"
    return l


class Corpus():
    def __init__(self, location=storage_dir):
        self.storage_dir = location
        self.texts = {i: firstline_of_file(os.path.join(self.storage_dir, i))
                for i in os.listdir(self.storage_dir)}
        return

    def clear_text(self):
        for fname in self.texts:
            os.unlink(os.path.join(self.storage_dir, fname))
        self.texts = {}

    def add_text(self, fileobj):
        new_path = self._corpus_text_fname(fileobj)
        shutil.copyfileobj(fileobj, open(new_path, 'w'))
        self.texts[os.path.split(new_path)[1]] = firstline_of_file(new_path)

    def delete_text(self, text_to_delete):
        path_to_delete = os.path.join(self.storage_dir, text_to_delete)
        os.unlink(path_to_delete)
        print("I have forgotten {}".format(text_to_delete))

    def _corpus_text_fname(self, fileobj):
        try:
            new_filename = None
            new_filename = os.path.split(fileobj.name)[1]
            if new_filename.startswith('<') and new_filename.endswith('>'):  # ie <stdin>
                new_filename = new_filename[1:-1]
        except AttributeError:
            new_filename = "Untitled"

        name, ext = os.path.splitext(new_filename)
        make_fn = lambda i: os.path.join(self.storage_dir, '%s(%d)%s' % (name, i, ext) if i else new_filename)
        for i in xrange(0, sys.maxint):
            uni_fn = make_fn(i)
            if not os.path.exists(uni_fn):
                return uni_fn


def command_add_text(parsed_args):
    corpus = Corpus()
    corpus.add_text(parsed_args.location)
    print("I have learned {}".format(parsed_args.location.name))


def command_list_text(parsed_args):
    corpus = Corpus()
    print("Texts learned")
    for path in corpus.texts:
        print('{} "{}"'.format(path, corpus.texts[path]))


def command_delete_text(parsed_args):
    corpus = Corpus()
    corpus.delete_text(parsed_args.text_name)


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description=metadata.get('summary'),
            epilog="Mail {} <{}> with bugs and features.".format(metadata.get('maintainer'),
                metadata.get('maintainer_email')))
    subparsers = parser.add_subparsers()

    parser_add_text = subparsers.add_parser('add_text',
            help='Adds a text file to corpus of Consenso markov knowledge.')
    parser_add_text.add_argument('location', type=argparse.FileType())
    parser_add_text.set_defaults(func=command_add_text)

    parser_list_text = subparsers.add_parser('list_text',
            help='Lists texts in the Consenso markov knowledge database.')
    parser_list_text.set_defaults(func=command_list_text)

    parser_delete_text = subparsers.add_parser('delete_text',
            help='Deletes text in the Consenso markov knowledge database.')
    parser_delete_text.add_argument('text_name', type=str)
    parser_delete_text.set_defaults(func=command_delete_text)

    parsed_args = parser.parse_args(args)
    parsed_args.func(parsed_args)
