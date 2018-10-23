import json

from gensim.models import Word2Vec


class WordVector:
    def __init__(self):
        self.model = Word2Vec.load_word2vec_format('linguine/ops/glove.6B.50d.w2vformat.txt', binary=False)

    def run(self, data):
        results = []
        for corpus in data:
            for line in corpus.contents.strip().split("\n"):
                result = {}
                tokens = line.split()
                if tokens[0] == "sim_score":
                    result["type"] = "sim_score"
                    result["word1"] = tokens[1]
                    result["word2"] = tokens[2]
                    result["score"] = self.get_similarity(result["word1"], result["word2"])
                elif tokens[0] == "sim_math":
                    result["type"] = "sim_math"
                    result["pos"] = [word[1:] for word in tokens[1:] if word.startswith("+")]
                    result["neg"] = [word[1:] for word in tokens[1:] if word.startswith("-")]
                    result["answer"] = [{"word": word, "score": score} for word, score in
                                        self.get_most_similar(result["pos"], result["neg"])]
                results.append(result)
        return json.dumps(results)

    def get_similarity(self, word1, word2):
        return self.model.similarity(word1, word2)

    def get_most_similar(self, positive=None, negative=None):
        if positive is None:
            positive = []
        if negative is None:
            negative = []

        return self.model.most_similar(positive=positive, negative=negative)
