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
import sys

from distutils2.database import get_distribution
from consenso.corpus import Corpus

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


def firstline_of_file(path):
    f = open(path, 'r')
    l = f.readline().strip()
    try:
        while l == "":
            l = f.readline().strip
    except EOFError:
        return "Empty"
    return l

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
