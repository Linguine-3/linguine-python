"""
Returns: A list of strings produced by tokenizing the given data
Given: A string containing a bunch of text.
"""
from nltk.tokenize import sent_tokenize


class SentenceTokenize:
    def __init__(self):
        pass

    def run(self, data):
        results = []
        for corpus in data:
            results.append({'corpus_id': corpus.id, 'sentences': sent_tokenize(corpus.contents)})
        return results
