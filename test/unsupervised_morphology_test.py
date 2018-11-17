import unittest

from linguine.corpus import Corpus
from linguine.ops.unsupervised_morphology import UnsupervisedMorphology


class UnsupervisedMorphologyTest(unittest.TestCase):

    def setUp(self):
        self.op = UnsupervisedMorphology()

    def test_run(self):
        test_data = [Corpus("0", "", open('brown.txt', 'r').read())]
        results = self.op.run(test_data)
        self.assertIsNotNone(results)
        for result in results:
            self.assertTrue(result)
            for sigs_stems in result:
                self.assertTrue(sigs_stems['affixes'])
                self.assertLessEqual(len(sigs_stems['roots']), 15)


if __name__ == '__main__':
    unittest.main()
