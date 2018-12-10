"""
Removes all hashtag tokens, #, from a text.
Returns the text as a single string separated by spaces.
"""

import re


class RemoveHashtags:
    def run(self, data):
        results = []
        for corpus in data:
            temp_corpus = re.sub(r'#', '', corpus.contents)
            corpus.contents = temp_corpus
            results.append(corpus)
        return results
