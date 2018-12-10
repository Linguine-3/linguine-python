"""
Removes all silent pause tokens, {SL}, from a text.
Returns the text as a single string separated by spaces.
"""

import re


class RemoveSilence:
    def run(self, data):
        results = []
        for corpus in data:
            split_string = corpus.contents.split(" ")
            print(split_string)
            temp_corpus = list(filter(("{SL}").__ne__, split_string))
            temp_corpus = list(filter(("{sl}").__ne__, temp_corpus))
            temp_corpus = " ".join(temp_corpus)
            print(temp_corpus)
            temp_corpus = re.sub(r'\{SL\}\.', '.', temp_corpus)
            temp_corpus = re.sub(r'\{sl\}\.', '.', temp_corpus)
            temp_corpus = re.sub(r' +', ' ', temp_corpus)
            temp_corpus = temp_corpus.split(" ")
            print(temp_corpus)
            temp_corpus = list(filter((" ").__ne__, temp_corpus))
            temp_corpus = list(filter((".").__ne__, temp_corpus))
            temp_corpus = " ".join(temp_corpus)
            print(temp_corpus)
            corpus.contents = temp_corpus
            results.append(corpus)
        return results
