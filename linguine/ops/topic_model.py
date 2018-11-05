"""
Returns: A list of topics, where each topic lists pairs of words-probabilities
that fit the topic
Given: A list of Corpora, where each corpus is a string
Uses the Gensim Topic Modeling library to find the most relevant topics

TODO: define JSON format such that user can define num_topics, passes
"""
import json
import re

from gensim.corpora import Dictionary
from gensim.models import LdaModel
from nltk.corpus import stopwords

from linguine.corpus import Corpus
from linguine.ops.remove_punct import RemovePunct


class TopicModel:
    def __init__(self):
        self.remove_punct = RemovePunct()

    def run(self, data):
        corpora = []
        for corpus in data:
            sentences = [Corpus("0", "", sentence.strip()) for sentence in re.split(r'[.?!]', corpus.contents) if
                         sentence]
            corpora += sentences

        corpora = self.remove_punct.run(corpora)
        return self.execute(corpora)

    def test_run(self, data):
        """Because LdaModel is resource intensive, this method is used for unit testing.
        It's identical to run, except that the passes attribute is a smaller number for shorter
        runtime.
        """
        return self.execute(data, passes=10)

    def execute(self, data, num_topics=30, passes=10):
        wordlists = [corpus.contents.lower().split() for corpus in data]

        stoplist = stopwords.words('english')

        dictionary = Dictionary(wordlists)

        # Remove stop words
        stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
        # once_ids = [token_id for token_id, doc_freq in dictionary.dfs.items() if doc_freq == 1]
        dictionary.filter_tokens(stop_ids)
        dictionary.compactify()

        # dictionary.filter_extremes(no_above=0.5)
        bags_of_words = [dictionary.doc2bow(t) for t in wordlists]

        # This can take a while to run:
        lda = LdaModel(bags_of_words, id2word=dictionary, num_topics=num_topics, passes=passes)

        results = self.assemble_topics(lda, num_topics)
        return json.dumps(results)

    @staticmethod
    def assemble_topics(lda_model, num_topics):
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
            num_topics: number of topics
        Returns:
            A list of topics, with each topic listing the word-prob pairs
        """
        topics = dict()
        for n, topic in lda_model.show_topics(num_topics=num_topics, formatted=False):
            topics[str(n)] = list()
            for word, prob in topic:
                topics[str(n)].append({'probability': prob, 'word': word})
        return topics
