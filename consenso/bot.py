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
        self._dirty_markov_tables()
        return

    def clear_text(self):
        for fname in self.texts:
            os.unlink(os.path.join(self.storage_dir, fname))
        self.texts = {}
        self._dirty_markov_tables()

    def add_text(self, fileobj):
        self._dirty_markov_tables()
        new_path = self._corpus_text_fname(fileobj)
        shutil.copyfileobj(fileobj, open(new_path, 'w'))
        self.texts[os.path.split(new_path)[1]] = firstline_of_file(new_path)

    def delete_text(self, text_to_delete):
        self._dirty_markov_tables()
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

    def _dirty_markov_tables(self):
        self._table = None
        self._start_words = None

    def _create_markov_tables(self):
        if self._table:
            return
        nonword = '\n'
        w1 = nonword
        w2 = nonword
        table = {}
        start_words = []
        for f in self.texts:
            for l in open(os.path.join(self.storage_dir, f), 'r'):
                for word in l.split():
                    table.setdefault((w1, w2), []).append(word)
                    if w1[0].isupper():
                        start_words.append((w1, w2))
                    w1, w2 = w2, word
        self._table = table
        self._start_words = start_words

    def get_triplet(self, trip1, trip2):
        self._create_markov_tables()
        return self._table[(trip1, trip2)]

    def get_startwords(self):
        self._create_markov_tables()
        return random.choice(self._start_words)

    def markov(self, max_sentences=1):
        """ Extracts markov sentences -- text beginning with an uppercase letter,
        and ending with a full stop."""
        self._create_markov_tables()
        word1, word2 = self.get_startwords()
        result = [word1, word2]
        sentences_to_go = max_sentences
        while sentences_to_go:
            next_word = random.choice(self.get_triplet(result[-2], result[-1]))
            result.append(next_word)
            if next_word.endswith('.') and sentences_to_go:
                sentences_to_go -= 1
                if sentences_to_go == 0:
                    break
        return ' '.join(result)


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
