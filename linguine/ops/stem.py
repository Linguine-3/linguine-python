"""
Returns: A list of words that have been stemmed using the chosen method
Given: A list of strings representing a tokenized collection of words.
There is one stemming algorithm available: The Porter stemmer.
"""
from nltk.stem.porter import PorterStemmer


class StemmerPorter:
    def __init__(self):
        pass

    def run(self, data):
        porter = PorterStemmer()
        for corpus in data:
            corpus_string = ""
            corpus.tokenized_contents = [porter.stem(word) for word in corpus.tokenized_contents]
            for index, word in enumerate(corpus.tokenized_contents):
                corpus_string += corpus.tokenized_contents[index] + " "

            corpus.contents = corpus_string

        return data
