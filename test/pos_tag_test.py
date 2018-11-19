import unittest
import sys

from linguine.ops.pos_tag import PosTag
from linguine.corpus import Corpus

class PosTagTest(unittest.TestCase):

    def setUp(self):
        self.op = PosTag()

    def test_run(self):
        test_data = [Corpus("0", "", "the old man the boat. john ate an old sandwich, unfortunately.")]
        desired_results = {"0": [('the', 'DT'), ('old', 'JJ'), ('man', 'NN'), ('the', 'DT'), \
         ('boat', 'NN'), ('john', 'NN'), ('ate', 'VBD'), ('an', 'DT'),\
         ('old', 'JJ'), ('sandwich', 'NN'), ('unfortunately', 'RB')]}
        results = self.op.run(test_data)
        self.assertIsNotNone(results)
        for result in results:
            self.assertEqual(result['tags'], desired_results[result['corpus_id']])

if __name__ == '__main__':
    unittest.main()
