from linguine.ops.char_ngrams import CharNgrams


class BigramArray:
    def run(self, data):
        ngram_results = CharNgrams().run(data)

        results = []
        for ngram_result in ngram_results:
            result = {}

            unigrams = sorted(ngram_result['unigrams'].keys())
            result['chars'] = unigrams

            result['array'] = {}
            for unigram in unigrams:
                result['array'][unigram] = {k: 0 for k in unigrams}

            for bigram, count in ngram_result['bigrams'].items():
                result['array'][bigram[0]][bigram[1]] = count

            results.append(result)

        return results
