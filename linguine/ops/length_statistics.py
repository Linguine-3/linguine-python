import json
import re
import statistics
from itertools import chain


class LengthStatistics:
    def run(self, data):
        results = []

        for corpus in data:
            corpus.contents = corpus.contents.strip()
            sentences = [re.sub(r"[.,:;!?()[\]{\}]", "", sentence.strip()) for sentence in
                         re.split(r'[.?!]', corpus.contents) if sentence]
            words_by_sentence = [re.split(r'\s+', sentence) for sentence in sentences]
            words = list(chain.from_iterable(words_by_sentence))
            sentence_lengths = [len(sentence) for sentence in words_by_sentence]
            word_lengths = [len(word) for word in words]
            results.append({'sentences': self.get_stats(sentence_lengths), 'words': self.get_stats(word_lengths)})

        return results

    def get_stats(self, lengths):
        results = {
            'mean': statistics.mean(lengths),
            'median': statistics.median(lengths),
            'std': statistics.stdev(lengths) if len(lengths) > 1 else None
        }
        return results
