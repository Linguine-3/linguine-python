import json
import unittest

from linguine.corpus import Corpus
from linguine.ops.unsupervised_morphology import UnsupervisedMorphology


class UnsupervisedMorphologyTest(unittest.TestCase):

    def setUp(self):
        self.op = UnsupervisedMorphology()

    def test_run(self):
        test_data = [Corpus("0", "", open('brown.txt', 'r').read())]
        results = self.op.run(test_data)
        results = json.loads(results)
        self.assertIsNotNone(results)
        # TODO: Add better verification


if __name__ == '__main__':
    unittest.main()
