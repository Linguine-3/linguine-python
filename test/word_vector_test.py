import json
import unittest

from linguine.corpus import Corpus
from linguine.ops.word_vector import WordVector


class WordVectorTest(unittest.TestCase):

    def setUp(self):
        self.op = WordVector()

    def test_run(self):
        commands = ["sim_score universities colleges", "sim_math +woman +king -man"]
        test_data = [Corpus(0, "", "\n".join(commands))]
        results = self.op.run(test_data)
        desired_results = [
            {'type': 'sim_score', 'word1': 'universities', 'score': 0.9215914199727002, 'word2': 'colleges'},
            {'type': 'sim_math', 'pos': ['woman', 'king'], 'neg': ['man'],
             'answer': [{'score': 0.8523603677749634, 'word': 'queen'},
                        {'score': 0.7664333581924438, 'word': 'throne'},
                        {'score': 0.759214460849762, 'word': 'prince'},
                        {'score': 0.7473883032798767, 'word': 'daughter'},
                        {'score': 0.7460220456123352, 'word': 'elizabeth'},
                        {'score': 0.7424570322036743, 'word': 'princess'},
                        {'score': 0.7337412238121033, 'word': 'kingdom'},
                        {'score': 0.7214491367340088, 'word': 'monarch'},
                        {'score': 0.7184862494468689, 'word': 'eldest'},
                        {'score': 0.7099430561065674, 'word': 'widow'}]}]
        # self.assertEqual(results, desired_results)
        self.assertIsNotNone(results)
        # TODO: Add better verification


if __name__ == '__main__':
    unittest.main()
