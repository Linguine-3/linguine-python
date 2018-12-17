from nltk.corpus import stopwords

from linguine.untokenize import untokenize


class RemoveStopwords:
    def __init__(self):
        pass

    def run(self, data):
        stopset = set(stopwords.words('english'))
        for corpus in data:
            corpus.tokenized_contents = [w for w in corpus.tokenized_contents if w not in stopset]
            corpus.contents = untokenize(corpus.tokenized_contents)
        return data
