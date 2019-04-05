import unittest

from linguine.corpus import Corpus
from linguine.ops.stanford_core_nlp import StanfordCoreNLP


class StanfordCoreNLPTest(unittest.TestCase):

    def setUp(self):
        self.op = StanfordCoreNLP([])
        self.test_data = [Corpus('0', 'Test', 'The quick brown fox jumped over the lazy dog.\n')]

    def test_run_pos(self):
        self.op.analysis_type = 'pos'
        results = self.op.run(self.test_data)
        desired_results = {
            'sentences': [{
                'tokens': [{'token': 'The'},
                           {'token': 'quick'},
                           {'token': 'brown'},
                           {'token': 'fox'},
                           {'token': 'jumped'},
                           {'token': 'over'},
                           {'token': 'the'},
                           {'token': 'lazy'},
                           {'token': 'dog'},
                           {'token': '.'}],
                'tree_json': [{'id': 1, 'tag': '', 'head': 0, 'value': 'S'},
                              {'id': 2, 'tag': '', 'head': 1, 'value': 'NP'},
                              {'id': 3, 'tag': '', 'head': 2, 'value': 'DT'},
                              {'id': 4, 'tag': '', 'head': 3, 'value': 'The'},
                              {'id': 5, 'tag': '', 'head': 2, 'value': 'JJ'},
                              {'id': 6, 'tag': '', 'head': 5, 'value': 'quick'},
                              {'id': 7, 'tag': '', 'head': 2, 'value': 'JJ'},
                              {'id': 8, 'tag': '', 'head': 7, 'value': 'brown'},
                              {'id': 9, 'tag': '', 'head': 2, 'value': 'NN'},
                              {'id': 10, 'tag': '', 'head': 9, 'value': 'fox'},
                              {'id': 11, 'tag': '', 'head': 1, 'value': 'VP'},
                              {'id': 12, 'tag': '', 'head': 11, 'value': 'VBD'},
                              {'id': 13, 'tag': '', 'head': 12, 'value': 'jumped'},
                              {'id': 14, 'tag': '', 'head': 11, 'value': 'PP'},
                              {'id': 15, 'tag': '', 'head': 14, 'value': 'IN'},
                              {'id': 16, 'tag': '', 'head': 15, 'value': 'over'},
                              {'id': 17, 'tag': '', 'head': 14, 'value': 'NP'},
                              {'id': 18, 'tag': '', 'head': 17, 'value': 'DT'},
                              {'id': 19, 'tag': '', 'head': 18, 'value': 'the'},
                              {'id': 20, 'tag': '', 'head': 17, 'value': 'JJ'},
                              {'id': 21, 'tag': '', 'head': 20, 'value': 'lazy'},
                              {'id': 22, 'tag': '', 'head': 17, 'value': 'NN'},
                              {'id': 23, 'tag': '', 'head': 22, 'value': 'dog'},
                              {'id': 24, 'tag': '', 'head': 1, 'value': '.'},
                              {'id': 25, 'tag': '', 'head': 24, 'value': '.'}]}]}
        self.assertEqual(results, desired_results)

    def test_run_ner(self):
        self.op.analysis_type = 'ner'
        results = self.op.run(self.test_data)
        desired_results = {
            'sentences': [{
                'tokens': [{'token': 'The', 'ner': 'O'},
                           {'token': 'quick', 'ner': 'O'},
                           {'token': 'brown', 'ner': 'O'},
                           {'token': 'fox', 'ner': 'O'},
                           {'token': 'jumped', 'ner': 'O'},
                           {'token': 'over', 'ner': 'O'},
                           {'token': 'the', 'ner': 'O'},
                           {'token': 'lazy', 'ner': 'O'},
                           {'token': 'dog', 'ner': 'O'},
                           {'token': '.', 'ner': 'O'}]}]}
        self.assertEqual(results, desired_results)

    def test_run_sentiment(self):
        self.op.analysis_type = 'sentiment'
        results = self.op.run(self.test_data)
        desired_results = {
            'sentences': [{
                'tokens': [{'token': 'The', 'sentiment': 'Neutral'},
                           {'token': 'quick', 'sentiment': 'Neutral'},
                           {'token': 'brown', 'sentiment': 'Neutral'},
                           {'token': 'fox', 'sentiment': 'Neutral'},
                           {'token': 'jumped', 'sentiment': 'Neutral'},
                           {'token': 'over', 'sentiment': 'Neutral'},
                           {'token': 'the', 'sentiment': 'Neutral'},
                           {'token': 'lazy', 'sentiment': 'Negative'},
                           {'token': 'dog', 'sentiment': 'Positive'},
                           {'token': '.', 'sentiment': 'Neutral'}],
                'sentiment': 'Negative',
                'sentimentValue': 1,
                'tree_json': [{'id': 1, 'tag': 1, 'head': 0, 'value': 'ROOT'},
                              {'id': 2, 'tag': 2, 'head': 1, 'value': 'NP'},
                              {'id': 3, 'tag': 2, 'head': 2, 'value': 'DT'},
                              {'id': 4, 'tag': '', 'head': 3, 'value': 'The'},
                              {'id': 5, 'tag': 2, 'head': 2, 'value': '@NP'},
                              {'id': 6, 'tag': 2, 'head': 5, 'value': 'JJ'},
                              {'id': 7, 'tag': '', 'head': 6, 'value': 'quick'},
                              {'id': 8, 'tag': 2, 'head': 5, 'value': '@NP'},
                              {'id': 9, 'tag': 2, 'head': 8, 'value': 'JJ'},
                              {'id': 10, 'tag': '', 'head': 9, 'value': 'brown'},
                              {'id': 11, 'tag': 2, 'head': 8, 'value': 'NN'},
                              {'id': 12, 'tag': '', 'head': 11, 'value': 'fox'},
                              {'id': 13, 'tag': 1, 'head': 1, 'value': '@S'},
                              {'id': 14, 'tag': 2, 'head': 13, 'value': 'VP'},
                              {'id': 15, 'tag': 2, 'head': 14, 'value': 'VBD'},
                              {'id': 16, 'tag': '', 'head': 15, 'value': 'jumped'},
                              {'id': 17, 'tag': 2, 'head': 14, 'value': 'PP'},
                              {'id': 18, 'tag': 2, 'head': 17, 'value': 'IN'},
                              {'id': 19, 'tag': '', 'head': 18, 'value': 'over'},
                              {'id': 20, 'tag': 2, 'head': 17, 'value': 'NP'},
                              {'id': 21, 'tag': 2, 'head': 20, 'value': 'DT'},
                              {'id': 22, 'tag': '', 'head': 21, 'value': 'the'},
                              {'id': 23, 'tag': 1, 'head': 20, 'value': '@NP'},
                              {'id': 24, 'tag': 1, 'head': 23, 'value': 'JJ'},
                              {'id': 25, 'tag': '', 'head': 24, 'value': 'lazy'},
                              {'id': 26, 'tag': 3, 'head': 23, 'value': 'NN'},
                              {'id': 27, 'tag': '', 'head': 26, 'value': 'dog'},
                              {'id': 28, 'tag': 2, 'head': 13, 'value': '.'},
                              {'id': 29, 'tag': '', 'head': 28, 'value': '.'}],
                'parse': '(ROOT (S (NP (DT The) (JJ quick) (JJ brown) (NN fox)) (VP (VBD jumped) (PP (IN over) (NP (DT the) (JJ lazy) (NN dog)))) (. .)))'
            }]}
        self.assertEqual(results, desired_results)

    def test_run_coref(self):
        self.op.analysis_type = 'coref'
        results = self.op.run(self.test_data)
        desired_results = {
            'sentences': [{
                'tokens': [{'token': 'The'},
                           {'token': 'quick'},
                           {'token': 'brown'},
                           {'token': 'fox'},
                           {'token': 'jumped'},
                           {'token': 'over'},
                           {'token': 'the'},
                           {'token': 'lazy'},
                           {'token': 'dog'},
                           {'token': '.'}]}],
            'entities': [
                {'entityid': 1, 'mentions': [
                    {'gender': 'MALE', 'representative': True, 'sentence': 0, 'mentiontype': 'NOMINAL',
                     'animacy': 'ANIMATE', 'mentionid': 1, 'tokspan_in_sentence': [0, 4],
                     'number': 'SINGULAR', 'head': 3}]},
                {'entityid': 2, 'mentions': [
                    {'gender': 'UNKNOWN', 'representative': True, 'sentence': 0, 'mentiontype': 'NOMINAL',
                     'animacy': 'ANIMATE', 'mentionid': 2, 'tokspan_in_sentence': [6, 9],
                     'number': 'SINGULAR', 'head': 8}]}],
        }
        self.assertEqual(results, desired_results)

    def test_run_relation(self):
        self.op.analysis_type = 'relation'
        results = self.op.run(self.test_data)
        desired_results = {
            'sentences': [{
                'tokens': [{'token': 'The'},
                           {'token': 'quick'},
                           {'token': 'brown'},
                           {'token': 'fox'},
                           {'token': 'jumped'},
                           {'token': 'over'},
                           {'token': 'the'},
                           {'token': 'lazy'},
                           {'token': 'dog'},
                           {'token': '.'}],
                'parse': '(ROOT (S (NP (DT The) (JJ quick) (JJ brown) (NN fox)) (VP (VBD jumped) (PP (IN over) (NP (DT the) (JJ lazy) (NN dog)))) (. .)))',
                'relations': [
                    {'subject': {'lemma': 'quick brown fox', 'start': 1, 'end': 4},
                     'relation': {'lemma': 'jumped over', 'start': 4, 'end': 6},
                     'object': {'lemma': 'lazy dog', 'start': 7, 'end': 9}},
                    {'subject': {'lemma': 'fox', 'start': 3, 'end': 4},
                     'relation': {'lemma': 'jumped over', 'start': 4, 'end': 6},
                     'object': {'lemma': 'dog', 'start': 8, 'end': 9}},
                    {'subject': {'lemma': 'quick fox', 'start': 1, 'end': 4},
                     'relation': {'lemma': 'jumped over', 'start': 4, 'end': 6},
                     'object': {'lemma': 'dog', 'start': 8, 'end': 9}},
                    {'subject': {'lemma': 'quick brown fox', 'start': 1, 'end': 4},
                     'relation': {'lemma': 'jumped over', 'start': 4, 'end': 6},
                     'object': {'lemma': 'dog', 'start': 8, 'end': 9}},
                    {'subject': {'lemma': 'brown fox', 'start': 2, 'end': 4},
                     'relation': {'lemma': 'jumped over', 'start': 4, 'end': 6},
                     'object': {'lemma': 'lazy dog', 'start': 7, 'end': 9}},
                    {'subject': {'lemma': 'brown fox', 'start': 2, 'end': 4},
                     'relation': {'lemma': 'jumped over', 'start': 4, 'end': 6},
                     'object': {'lemma': 'dog', 'start': 8, 'end': 9}},
                    {'subject': {'lemma': 'quick fox', 'start': 1, 'end': 4},
                     'relation': {'lemma': 'jumped over', 'start': 4, 'end': 6},
                     'object': {'lemma': 'lazy dog', 'start': 7, 'end': 9}},
                    {'subject': {'lemma': 'fox', 'start': 3, 'end': 4},
                     'relation': {'lemma': 'jumped over', 'start': 4, 'end': 6},
                     'object': {'lemma': 'lazy dog', 'start': 7, 'end': 9}}]
            }]}
        self.assertEqual(results, desired_results)


if __name__ == '__main__':
    unittest.main()
