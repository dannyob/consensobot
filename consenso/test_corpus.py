#!/usr/bin/env python
##
# consenso/test_bot.py
###
"""consenso/test_bot.py

"""

__author__ = "Danny O'Brien <http://www.spesh.com/danny/>"
__copyright__ = "Copyright Danny O'Brien"
__contributors__ = None
__license__ = "GPL v3"

import unittest
from consenso.corpus import Corpus
from consenso.directories import corpus_dir
import os
import os.path
import tempfile

import StringIO as s


class Configuration_directory(unittest.TestCase):
    def test_contains_sensible_name(self):
        self.assertIn('consensobot', corpus_dir)

    def test_is_writeable(self):
        fname = os.path.join(corpus_dir, 'foo.txt')
        f = open(fname, 'w')    # throws exception if not writeable
        f.close()
        os.unlink(fname)
        self.assert_(True)


class Corpus_class(unittest.TestCase):
    def setUp(self):
        self.corpus_location = os.path.join(tempfile.gettempdir(), 'temp_corpus')
        os.mkdir(self.corpus_location)
        self.corpus = Corpus(location=self.corpus_location)
        self.corpus.clear_text()

    def tearDown(self):
        self.corpus.clear_text()
        os.rmdir(self.corpus_location)

    def test_can_add_a_work(self):
        self.corpus.add_text(s.StringIO("I am spartacus"))
        self.assertEquals(len(self.corpus.texts), 1)

    def test_can_add_two_works(self):
        self.corpus.add_text(s.StringIO("I am spartacus"))
        self.corpus.add_text(s.StringIO("No I am spartacus"))
        self.assertEquals(len(self.corpus.texts), 2)

    def test_can_translate_unnamed_stream_into_fname(self):
        self.corpus.add_text(s.StringIO("I am spartacus"))
        self.assertEquals(self.corpus.texts['Untitled'], 'I am spartacus')

    def test_can_put_numbers_at_end_of_fname_to_prevent_doubles(self):
        self.corpus.add_text(s.StringIO("I am spartacus"))
        self.corpus.add_text(s.StringIO("No I am spartacus"))
        self.assertEquals(self.corpus.texts['Untitled(1)'], 'No I am spartacus')

    def test_can_generate_markov_triplet(self):
        self.corpus.add_text(s.StringIO("I am spartacus loosely"))
        self.corpus.add_text(s.StringIO("No I am spartacus splendidly"))
        triplet = self.corpus.get_triplet("am", "spartacus")
        self.assertIn('loosely', triplet)
        self.assertIn('splendidly', triplet)

    def test_can_generate_markov_triplet_from_file(self):
        self.corpus.add_text(file('test_data/test_corpus.txt', 'r'))
        triplet = self.corpus.get_triplet("Pontefract", "Miserabilis")
        self.assertIn('--', triplet)

    def test_can_generate_markov_sentence_from_file(self):
        self.corpus.add_text(file('test_data/test_corpus.txt', 'r'))
        markov = self.corpus.markov_sentence(sentences=1, start_word='Pontefract')
        self.assertIn('Miserabilis', markov)

    def test_can_generate_markov_sentence(self):
        self.corpus.add_text(s.StringIO("I am spartacus loosely."))
        self.corpus.add_text(s.StringIO("No I am spartacus splendidly."))
        markov = self.corpus.markov_sentence(sentences=1)
        self.assert_(markov.endswith('.'))


if __name__ == '__main__':
    import __main__
    suite = unittest.TestLoader().loadTestsFromModule(__main__)
    unittest.TextTestRunner(verbosity=1).run(suite)
