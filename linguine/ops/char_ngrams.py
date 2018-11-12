import json
import re

from linguine.ops.splat import SplatNGrams


class CharNgrams:
    def run(self, data):
        splat_ngrams = SplatNGrams()

        for corpus in data:
            corpus.contents = corpus.contents.strip()
            corpus.contents = re.sub(r'\s+', '_', corpus.contents)
            corpus.contents = re.sub(r"[.,:;!?()[\]{\}]", "", corpus.contents)  # Can be removed once SPLAT bug is fixed
            corpus.contents = ' '.join(corpus.contents)

        results = json.loads(splat_ngrams.run(data))
        for result in results:
            result['bigrams'] = {word.replace(' ', ''): count for word, count in result['bigrams'].items()}
            result['trigrams'] = {word.replace(' ', ''): count for word, count in result['trigrams'].items()}

        return results
