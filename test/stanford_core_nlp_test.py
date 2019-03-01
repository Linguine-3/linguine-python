import unittest

from linguine.corpus import Corpus
from linguine.ops.stanford_core_nlp import StanfordCoreNLP


class StanfordCoreNLPTest(unittest.TestCase):

    def setUp(self):
        self.op = StanfordCoreNLP([])
        self.test_data = [Corpus("0", "Test", "The quick brown fox jumped over the lazy dog.\n")]

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
                'tree_json': [{'id': 1, 'tag': 'S', 'head': 0, 'value': 'S'},
                              {'id': 2, 'tag': 'NP', 'head': 1, 'value': 'NP'},
                              {'id': 3, 'tag': 'VP', 'head': 1, 'value': 'VP'},
                              {'id': 4, 'tag': '.', 'head': 1, 'value': '.'},
                              {'id': 5, 'tag': 'DT', 'head': 2, 'value': 'DT'},
                              {'id': 6, 'tag': 'JJ', 'head': 2, 'value': 'JJ'},
                              {'id': 7, 'tag': 'JJ', 'head': 2, 'value': 'JJ'},
                              {'id': 8, 'tag': 'NN', 'head': 2, 'value': 'NN'},
                              {'id': 9, 'tag': '', 'head': 5, 'value': 'The'},
                              {'id': 10, 'tag': '', 'head': 6, 'value': 'quick'},
                              {'id': 11, 'tag': '', 'head': 7, 'value': 'brown'},
                              {'id': 12, 'tag': '', 'head': 8, 'value': 'fox'},
                              {'id': 13, 'tag': 'VBD', 'head': 3, 'value': 'VBD'},
                              {'id': 14, 'tag': 'PP', 'head': 3, 'value': 'PP'},
                              {'id': 15, 'tag': '', 'head': 13, 'value': 'jumped'},
                              {'id': 16, 'tag': 'IN', 'head': 14, 'value': 'IN'},
                              {'id': 17, 'tag': 'NP', 'head': 14, 'value': 'NP'},
                              {'id': 18, 'tag': '', 'head': 16, 'value': 'over'},
                              {'id': 19, 'tag': 'DT', 'head': 17, 'value': 'DT'},
                              {'id': 20, 'tag': 'JJ', 'head': 17, 'value': 'JJ'},
                              {'id': 21, 'tag': 'NN', 'head': 17, 'value': 'NN'},
                              {'id': 22, 'tag': '', 'head': 19, 'value': 'the'},
                              {'id': 23, 'tag': '', 'head': 20, 'value': 'lazy'},
                              {'id': 24, 'tag': '', 'head': 21, 'value': 'dog'},
                              {'id': 25, 'tag': '', 'head': 4, 'value': '.'}]}]}
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
                'sentiment': 'Negative',
                'sentimentValue': 1,
                'parse': '(ROOT (S (NP (DT The) (JJ quick) (JJ brown) (NN fox)) (VP (VBD jumped) (PP (IN over) (NP (DT the) (JJ lazy) (NN dog)))) (. .)))',
                'tree_json': [{'value': 'ROOT', 'head': 0, 'tag': 1, 'id': 1},
                              {'value': 'NP', 'head': 1, 'tag': 2, 'id': 2},
                              {'value': '@S', 'head': 1, 'tag': 1, 'id': 3},
                              {'value': 'DT', 'head': 2, 'tag': 2, 'id': 4},
                              {'value': '@NP', 'head': 2, 'tag': 2, 'id': 5},
                              {'value': 'The', 'head': 4, 'tag': '', 'id': 6},
                              {'value': 'JJ', 'head': 5, 'tag': 2, 'id': 7},
                              {'value': '@NP', 'head': 5, 'tag': 2, 'id': 8},
                              {'value': 'quick', 'head': 7, 'tag': '', 'id': 9},
                              {'value': 'JJ', 'head': 8, 'tag': 2, 'id': 10},
                              {'value': 'NN', 'head': 8, 'tag': 2, 'id': 11},
                              {'value': 'brown', 'head': 10, 'tag': '', 'id': 12},
                              {'value': 'fox', 'head': 11, 'tag': '', 'id': 13},
                              {'value': 'VP', 'head': 3, 'tag': 2, 'id': 14},
                              {'value': '.', 'head': 3, 'tag': 2, 'id': 15},
                              {'value': 'VBD', 'head': 14, 'tag': 2, 'id': 16},
                              {'value': 'PP', 'head': 14, 'tag': 2, 'id': 17},
                              {'value': 'jumped', 'head': 16, 'tag': '', 'id': 18},
                              {'value': 'IN', 'head': 17, 'tag': 2, 'id': 19},
                              {'value': 'NP', 'head': 17, 'tag': 2, 'id': 20},
                              {'value': 'over', 'head': 19, 'tag': '', 'id': 21},
                              {'value': 'DT', 'head': 20, 'tag': 2, 'id': 22},
                              {'value': '@NP', 'head': 20, 'tag': 1, 'id': 23},
                              {'value': 'the', 'head': 22, 'tag': '', 'id': 24},
                              {'value': 'JJ', 'head': 23, 'tag': 1, 'id': 25},
                              {'value': 'NN', 'head': 23, 'tag': 3, 'id': 26},
                              {'value': 'lazy', 'head': 25, 'tag': '', 'id': 27},
                              {'value': 'dog', 'head': 26, 'tag': '', 'id': 28},
                              {'value': '.', 'head': 15, 'tag': '', 'id': 29}],
                'tokens': [{'sentiment': 'Neutral', 'token': 'The'},
                           {'sentiment': 'Neutral', 'token': 'quick'},
                           {'sentiment': 'Neutral', 'token': 'brown'},
                           {'sentiment': 'Neutral', 'token': 'fox'},
                           {'sentiment': 'Neutral', 'token': 'jumped'},
                           {'sentiment': 'Neutral', 'token': 'over'},
                           {'sentiment': 'Neutral', 'token': 'the'},
                           {'sentiment': 'Negative', 'token': 'lazy'},
                           {'sentiment': 'Positive', 'token': 'dog'},
                           {'sentiment': 'Neutral', 'token': '.'}]}]}
        self.assertEqual(results, desired_results)

    def test_run_coref(self):
        self.op.analysis_type = 'coref'
        results = self.op.run(self.test_data)
        desired_results = {
            'sentences': [{
                'tokens': [{'token': 'The'}, {'token': 'quick'}, {'token': 'brown'},
                           {'token': 'fox'}, {'token': 'jumped'}, {'token': 'over'},
                           {'token': 'the'}, {'token': 'lazy'}, {'token': 'dog'},
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
                'tokens': [{'token': 'The'}, {'token': 'quick'}, {'token': 'brown'},
                           {'token': 'fox'}, {'token': 'jumped'}, {'token': 'over'},
                           {'token': 'the'}, {'token': 'lazy'}, {'token': 'dog'},
                           {'token': '.'}],
                'relations': [
                    {'object': {'end': 9, 'start': 7, 'lemma': 'lazy dog'},
                     'relation': {'end': 6, 'start': 4, 'lemma': 'jump over'},
                     'subject': {'end': 4, 'start': 1, 'lemma': 'quick brown fox'}},
                    {'object': {'end': 9, 'start': 8, 'lemma': 'dog'},
                     'relation': {'end': 6, 'start': 4, 'lemma': 'jump over'},
                     'subject': {'end': 4, 'start': 3, 'lemma': 'fox'}},
                    {'object': {'end': 9, 'start': 8, 'lemma': 'dog'},
                     'relation': {'end': 6, 'start': 4, 'lemma': 'jump over'},
                     'subject': {'end': 4, 'start': 1, 'lemma': 'quick fox'}},
                    {'object': {'end': 9, 'start': 8, 'lemma': 'dog'},
                     'relation': {'end': 6, 'start': 4, 'lemma': 'jump over'},
                     'subject': {'end': 4, 'start': 1, 'lemma': 'quick brown fox'}},
                    {'object': {'end': 9, 'start': 7, 'lemma': 'lazy dog'},
                     'relation': {'end': 6, 'start': 4, 'lemma': 'jump over'},
                     'subject': {'end': 4, 'start': 2, 'lemma': 'brown fox'}},
                    {'object': {'end': 9, 'start': 8, 'lemma': 'dog'},
                     'relation': {'end': 6, 'start': 4, 'lemma': 'jump over'},
                     'subject': {'end': 4, 'start': 2, 'lemma': 'brown fox'}},
                    {'object': {'end': 9, 'start': 7, 'lemma': 'lazy dog'},
                     'relation': {'end': 6, 'start': 4, 'lemma': 'jump over'},
                     'subject': {'end': 4, 'start': 1, 'lemma': 'quick fox'}},
                    {'object': {'end': 9, 'start': 7, 'lemma': 'lazy dog'},
                     'relation': {'end': 6, 'start': 4, 'lemma': 'jump over'},
                     'subject': {'end': 4, 'start': 3, 'lemma': 'fox'}}],
                'parse': '(ROOT (S (NP (DT The) (JJ quick) (JJ brown) (NN fox)) (VP (VBD jumped) (PP (IN over) (NP (DT the) (JJ lazy) (NN dog)))) (. .)))'}]}
        self.assertEqual(results, desired_results)


if __name__ == '__main__':
    unittest.main()
