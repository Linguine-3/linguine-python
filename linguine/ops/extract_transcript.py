import json


class ExtractTranscript:
    def run(self, data):
        results = []
        for corpus in data:
            tokens = json.loads(corpus.contents)
            words = list(token['word'] for token in tokens if not token['filler'])
            corpus.contents = ' '.join(words)
            results.append(corpus)
        return results
