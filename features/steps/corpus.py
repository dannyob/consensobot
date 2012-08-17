#!/usr/bin/env python
##
# corpus.py
###
"""corpus.py

"""

from consenso.corpus import Corpus
from behave import given, then

@given(u'an empty set of texts in the corpus')
def step(context):
    corpus = Corpus()
    corpus.clear_text()
    assert (len(corpus.texts) == 0)

@then(u'there should be {num:d} text in the corpus')
def step(context, num=0):
    corpus = Corpus()
    assert (len(corpus.texts) == num)
