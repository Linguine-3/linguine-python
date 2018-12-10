"""
Returns: The corpus list, with tokenized contents generated
Given: Data containing a list of corpora to tokenize
Uses the Penn Treebank corpus for the WordTokenizeTreebank tokenization.
Uses the Stanford Tokenizer for WordTokenizeStanford.
WordTokenizeWhitespacePunct splits the text on whitespace and punctuation marks.
"""
from nltk.tokenize import TreebankWordTokenizer, wordpunct_tokenize
from nltk.tokenize.stanford import StanfordTokenizer


class WordTokenizeTreebank:
    def __init__(self):
        pass

    def run(self, data):
        for corpus in data:
            corpus.tokenized_contents = TreebankWordTokenizer().tokenize(corpus.contents)
        return data


class WordTokenizeWhitespacePunct:
    def __init__(self):
        pass

    def run(self, data):
        for corpus in data:
            corpus.tokenized_contents = wordpunct_tokenize(corpus.contents)
        return data


class WordTokenizeStanford:
    def __init__(self):
        pass

    def run(self, data):
        for corpus in data:
            corpus.tokenized_contents = StanfordTokenizer().tokenize(corpus.contents)
        return data
