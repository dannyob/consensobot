#!/usr/bin/env python
##
# bot.py
###
"""consensobot

Runs a consensobot on your choice of IRC network.
"""

import argparse
import errno
import os
import os.path
import random
import shutil
import sys

import appdirs
from distutils2.database import get_distribution


program_name = 'consensobot'
org_name = 'noisebridge'
metadata = get_distribution(program_name).metadata

# establish default storage directories
data_dir = appdirs.user_data_dir(program_name, org_name)
storage_dir = os.path.join(data_dir, 'corpus')


def mkdir_if_not_there(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise


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
    """A permanent store of texts for Consenso to use in markov chains.

    """
    def __init__(self, location=storage_dir):
        """Creates a corpus, with texts stored in location.
        Args:
            location: a directory, containing only text files.
        """
        self.storage_dir = location
        mkdir_if_not_there(self.storage_dir)
        self.texts = {i: firstline_of_file(os.path.join(self.storage_dir, i))
                      for i in os.listdir(self.storage_dir)}
        self._dirty_markov_tables()
        return

    def clear_text(self):
        """Removes all texts from the corpus store."""
        for fname in self.texts:
            os.unlink(os.path.join(self.storage_dir, fname))
        self.texts = {}
        self._dirty_markov_tables()

    def add_text(self, fileobj):
        """Add a text to the corpus.

        Args:
            fileobj: a file-like object, open for reading, which
                will be copied into the corpus.
        """
        self._dirty_markov_tables()
        new_path = self._corpus_text_fname(fileobj)
        shutil.copyfileobj(fileobj, open(new_path, 'w'))
        self.texts[os.path.split(new_path)[1]] = firstline_of_file(new_path)

    def delete_text(self, text_to_delete):
        """Delete a specific text from the corpus.

        Args:
            text_to_delete: name of text to delete. This is the same as the
            filename storing the text in the corpus directory.
        """
        self._dirty_markov_tables()
        path_to_delete = os.path.join(self.storage_dir, text_to_delete)
        os.unlink(path_to_delete)
        print("I have forgotten {}".format(text_to_delete))

    def _corpus_text_fname(self, fileobj):
        """Create unique corpus name from fileobj.

        Args:
            fileobj: readable file-like object, like an open file, or stdin.
        """
        # get name from file-like object
        try:
            new_filename = None
            new_filename = os.path.split(fileobj.name)[1]
            if new_filename.startswith('<') and new_filename.endswith('>'):
                new_filename = new_filename[1:-1]   # ie <stdin>
        except AttributeError:
            new_filename = "Untitled"

        # ensure the name is unique, and add digits until it is
        name, ext = os.path.splitext(new_filename)
        make_fn = lambda i: os.path.join(self.storage_dir,
                '%s(%d)%s' % (name, i, ext) if i else new_filename)
        for i in xrange(0, sys.maxint):
            uni_fn = make_fn(i)
            if not os.path.exists(uni_fn):
                return uni_fn

    def _dirty_markov_tables(self):
        """Mark internal markov tables as out of date."""
        self._triplets = None
        self._start_words = None

    def _create_markov_tables(self):
        """Create new markov tables from scratch."""
        if self._triplets:
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
        self._triplets = table
        self._start_words = start_words

    def get_triplet(self, trip1, trip2):
        """ A markov triplet from the corpus.

        Args:
            trip1, trip2: two consecutive words found in the corpus.

        Returns:
            A list of words that follow the two words. If a word follows the
            two words more than once, it appears in the list more than once.
            E.g.:
                get_triplet('I', 'am') == ['Spartacus', 'Spartacus', 'Frank']
        """
        self._create_markov_tables()
        return self._triplets[(trip1, trip2)]

    def get_startwords(self, start_word=None):
        """ Provides a starter word set for beginning a markov chain.

        Args:
            start_word: word known to be in the corpus

        Returns:
            Tuple, with the first item the start_word, and second a
            consecutive word that can be used as the arguments for
            `get_triplet`.

        If start_word is None or omitted, a random valid tuple is returned.
        Currently, because we assume markov chains are going to intended to be
        full sentences, only startwords that begin with an uppercase letter are
        stored.
        """
        self._create_markov_tables()
        if start_word is None:
            return random.choice(self._start_words)
        else:
            find_word = [(w1, w2)
                    for (w1, w2) in self._start_words if w1 == start_word]
            if find_word:
                return find_word[0]
            else:
                raise KeyError

    def markov_sentence(self, sentences=1, start_word=None):
        """ Extracts markov sentences from corpus.

        Args:
            sentences: number of sentences to return.
            start_word: optional word to start. Must have uppercase initial
                letter, and must be in the corpus.
        Returns:
            Markovian sentences, where a sentence wil begin with an uppercase
                letter, and end with a full stop."""
        self._create_markov_tables()
        word1, word2 = self.get_startwords(start_word)
        result = [word1, word2]
        sentences_to_go = sentences
        while sentences_to_go > 0:
            next_word = random.choice(self.get_triplet(result[-2], result[-1]))
            result.append(next_word)
            if next_word.endswith('.') and sentences_to_go:
                sentences_to_go -= 1
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


def command_markov_text(parsed_args):
    corpus = Corpus()
    markov = corpus.markov_sentence(sentences=parsed_args.sentences,
            start_word=parsed_args.start_word)
    print(markov)


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description=metadata.get('summary'),
            epilog="Mail {} <{}> with bugs and feature requests."
            .format(metadata.get('maintainer'),
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

    parser_markov_text = subparsers.add_parser('markov',
            help='Generate markov sentence(s).')
    parser_markov_text.add_argument('sentences', type=int, default=1)
    parser_markov_text.add_argument('--start-word', type=str, default=None)
    parser_markov_text.set_defaults(func=command_markov_text)

    parsed_args = parser.parse_args(args)
    parsed_args.func(parsed_args)
