#!/usr/bin/env python
"""
Removes all hashtag tokens, #, from a text.
Returns the text as a single string separated by spaces.
"""

import re


class RemoveQuotes:
    def run(self, data):
        results = []
        for corpus in data:
            temp_corpus = re.sub(r'["“”]', '', corpus.contents)
            temp_corpus = re.sub(r'[‘’]', "'", temp_corpus)
            temp_corpus = re.sub(r"( '\w|\w' )", '', temp_corpus)
            corpus.contents = temp_corpus
            results.append(corpus)
        return results
