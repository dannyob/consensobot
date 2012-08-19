#!/usr/bin/env python
##
# bot.py
###
"""consensobot

Runs a consensobot on your choice of IRC network.
"""

import argparse
import sys

from distutils2.database import get_distribution

from twisted.internet import reactor
from foolscap.api import Tub

from consenso.corpus import Corpus
from consenso.bot.client import ConsensoProcess


program_name = 'consensobot'
metadata = get_distribution(program_name).metadata


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


def do_remote_command(command, *args, **kwargs):
    client = ConsensoProcess()
    client.start()
    furl = client.furl()
    tub = Tub()
    tub.startService()

    def got_error(err):
        print "Error while calling command remotely", err
        reactor.stop()

    def got_result(res):
        print(res)

    def got_remote(remote):
        d = remote.callRemote(command, *args, **kwargs)
        d.addCallback(got_result)
        d.addCallback(lambda res: reactor.stop())
        d.addErrback(got_error)
        return d

    d = tub.getReference(furl)
    d.addCallback(got_remote)
    d.addErrback(got_error)
    reactor.run()


def command_irc_join(parsed_args):
    do_remote_command("join", parsed_args.url)


def command_irc_leave(parsed_args):
    do_remote_command("leave", parsed_args.url)


def command_irc_announce(parsed_args):
    do_remote_command("announce", parsed_args.message)


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

    parser_irc_join_text = subparsers.add_parser('irc_join',
            help='irc_join an IRC channel')
    parser_irc_join_text.add_argument('url', type=str)
    parser_irc_join_text.set_defaults(func=command_irc_join)

    parser_irc_leave_text = subparsers.add_parser('irc_leave',
            help='Leave an IRC channel')
    parser_irc_leave_text.add_argument('url', type=str)
    parser_irc_leave_text.set_defaults(func=command_irc_leave)

    parser_irc_announce_text = subparsers.add_parser('irc_announce',
            help='Say something on all IRC channels')
    parser_irc_announce_text.add_argument('message', type=str)
    parser_irc_announce_text.set_defaults(func=command_irc_announce)

    parsed_args = parser.parse_args(args)
    parsed_args.func(parsed_args)
