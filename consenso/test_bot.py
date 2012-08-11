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
import bot
import os
import os.path

import StringIO as s


class Configuration_directory(unittest.TestCase):
    def test_contains_sensible_name(self):
        self.assertIn('consensobot', bot.data_dir)

    def test_is_writeable(self):
        fname = os.path.join(bot.data_dir, 'foo.txt')
        f = open(fname, 'w')    # throws exception if not writeable
        f.close()
        os.unlink(fname)
        self.assert_(True)


class Corpus_class(unittest.TestCase):
    def test_can_add_a_work(self):
        i = bot.Corpus()
        i.clear_text()
        i.add_text(s.StringIO("I am spartacus"))
        self.assertEquals(len(i.texts), 1)

    def test_can_add_two_works(self):
        i = bot.Corpus()
        i.clear_text()
        i.add_text(s.StringIO("I am spartacus"))
        i.add_text(s.StringIO("No I am spartacus"))
        self.assertEquals(len(i.texts), 2)

    def test_can_translate_unnamed_stream_into_fname(self):
        i = bot.Corpus()
        i.clear_text()
        i.add_text(s.StringIO("I am spartacus"))
        self.assertEquals(i.texts['Untitled'], 'I am spartacus')

    def test_can_put_numbers_at_end_of_fname_to_prevent_doubles(self):
        i = bot.Corpus()
        i.clear_text()
        i.add_text(s.StringIO("I am spartacus"))
        i.add_text(s.StringIO("No I am spartacus"))
        self.assertEquals(i.texts['Untitled(1)'], 'No I am spartacus')

    def test_can_generate_markov_triplet(self):
        i = bot.Corpus()
        i.clear_text()
        i.add_text(s.StringIO("I am spartacus loosely"))
        i.add_text(s.StringIO("No I am spartacus splendidly"))
        triplet = i.get_triplet("am", "spartacus")
        self.assertIn('loosely', triplet)
        self.assertIn('splendidly', triplet)

    def test_can_generate_markov_triplet_from_file(self):
        i = bot.Corpus()
        i.clear_text()
        i.add_text(file('test_data/test_corpus.txt', 'r'))
        triplet = i.get_triplet("Pontefract", "Miserabilis")
        self.assertIn('--', triplet)


    def test_can_generate_markov_sentence(self):
        i = bot.Corpus()
        i.clear_text()
        i.add_text(s.StringIO("I am spartacus loosely."))
        i.add_text(s.StringIO("No I am spartacus splendidly."))
        markov = i.markov(max_sentences=1)
        self.assert_(markov.endswith('.'))


if __name__ == '__main__':
    import __main__
    suite = unittest.TestLoader().loadTestsFromModule(__main__)
    unittest.TextTestRunner(verbosity=1).run(suite)
