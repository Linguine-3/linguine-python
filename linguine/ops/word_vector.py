import gensim.downloader as api


class WordVector:
    model = None

    def __init__(self):
        if WordVector.model is None:
            WordVector.model = api.load('glove-wiki-gigaword-50')

    def run(self, data):
        results = []
        for corpus in data:
            for line in corpus.contents.strip().splitlines():
                result = {}
                tokens = line.split()
                if not tokens:  # Ignore blank lines
                    continue
                elif tokens[0] == 'doesnt_match' and len(tokens) > 1:
                    result['type'] = 'doesnt_match'
                    result['words'] = tokens[1:]
                    result['answer'] = self.get_doesnt_match(result['words'])
                elif tokens[0] == 'most_sim' and len(tokens) == 2:
                    result['type'] = 'most_sim'
                    result['word'] = tokens[1]
                    result['answer'] = self.get_most_similar(result['word'])
                elif tokens[0] == 'sim_math' and len(tokens) > 1 and all(
                        t[0] in ['+', '-'] and len(t) > 1 for t in tokens[1:]):
                    result['type'] = 'sim_math'
                    result['pos'] = [word[1:] for word in tokens[1:] if word.startswith('+')]
                    result['neg'] = [word[1:] for word in tokens[1:] if word.startswith('-')]
                    result['answer'] = self.get_most_similar(result['pos'], result['neg'])
                elif tokens[0] == 'sim_score' and len(tokens) == 3:
                    result['type'] = 'sim_score'
                    result['word1'] = tokens[1]
                    result['word2'] = tokens[2]
                    result['score'] = self.get_similarity(result['word1'], result['word2'])
                else:
                    result['type'] = 'error'
                    result['command'] = line.strip()
                results.append(result)
        return results

    def get_doesnt_match(self, words):
        return WordVector.model.doesnt_match(words)

    def get_most_similar(self, positive=None, negative=None):
        if positive is None:
            positive = []
        if negative is None:
            negative = []

        results = WordVector.model.most_similar(positive=positive, negative=negative)
        formatted = [{'word': word, 'score': score} for word, score in results]

        return formatted

    def get_similarity(self, word1, word2):
        return float(WordVector.model.similarity(word1, word2))
