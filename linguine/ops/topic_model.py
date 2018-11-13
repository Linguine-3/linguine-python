"""
Returns: A list of topics, where each topic lists pairs of words-probabilities
that fit the topic
Given: A list of Corpora, where each corpus is a string
Uses the Gensim Topic Modeling library to find the most relevant topics

TODO: define JSON format such that user can define num_topics, passes
"""
import json

from gensim.corpora import Dictionary
from gensim.models import LdaModel
from nltk.corpus import stopwords

from linguine.corpus import Corpus
from linguine.ops.remove_punct import RemovePunct


class TopicModel:
    def __init__(self, num_topics=30):
        self.num_topics = num_topics

    def run(self, data):
        corpora = []
        for corpus in data:
            sentences = [Corpus(str(i), "", sentence.strip()) for i, sentence in
                         enumerate(corpus.contents.split('\n\n')) if sentence]
            corpora += sentences

        print('Num corpora = {}'.format(len(corpora)))
        corpora = RemovePunct().run(corpora)
        return self.execute(corpora)

    def test_run(self, data):
        """Because LdaModel is resource intensive, this method is used for unit testing.
        It's identical to run, except that the passes attribute is a smaller number for shorter
        runtime.
        """
        return self.execute(data, passes=10)

    def execute(self, data, passes=10):
        wordlists = [corpus.contents.lower().split() for corpus in data]

        stoplist = stopwords.words('english')

        dictionary = Dictionary(wordlists)

        # Remove stop words and words that appear too much or too little
        stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
        dictionary.filter_tokens(stop_ids)
        dictionary.filter_extremes(no_below=2, no_above=0.2)

        bags_of_words = [dictionary.doc2bow(t) for t in wordlists]

        # This can take a while to run:
        lda = LdaModel(bags_of_words, id2word=dictionary, num_topics=self.num_topics, passes=passes)

        results = self.assemble_topics(lda)
        return results

    def assemble_topics(self, lda_model):
        """Print LDA model topics into a human-interpretable data structure

        Example:
        [
            #Topic 1:
            [
                (prob1, word1)
                (prob2, word2)
                ...
            ]
            #Topic 2:
            [
                (prob1, word1)
                ...
            ]
            ...
        ]
        Args:
            lda_model: Gensim LDA model
        Returns:
            A list of topics, with each topic listing the word-prob pairs
        """
        topics = dict()
        for n, topic in lda_model.show_topics(num_topics=self.num_topics, formatted=False):
            topics[str(n)] = list()
            for word, prob in topic:
                topics[str(n)].append({'probability': prob, 'word': word})
        return topics
