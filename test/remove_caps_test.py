import unittest
import sys
from linguine.ops.remove_caps import RemoveCapsGreedy, RemoveCapsPreserveNNP
from linguine.corpus import Corpus

class RemoveCapsTest(unittest.TestCase):

    def setUp(self):
        self.op = RemoveCapsGreedy()

    def test_run_greedy(self):
        self.op = RemoveCapsGreedy()
        test_data = [Corpus("0", "", '''Removes all non-proper-noun capitals from a given text. Removes capital letters from text, even for Bill Clinton. Accepts as input a non-tokenized string.''')]
        desired_results = {"0": '''removes all non-proper-noun capitals from a given text. removes capital letters from text, even for bill clinton. accepts as input a non-tokenized string.'''}
        results = self.op.run(test_data)
        self.assertIsNotNone(results)
        for corpus in results:
            self.assertEqual(corpus.contents, desired_results[corpus.id])

    def test_run_preserve_nnp(self):
        self.op = RemoveCapsPreserveNNP()
        test_data = [Corpus("0", "", '''Removes all non-proper-noun capitals from a given text. Removes capital letters from text, even for Bill Clinton. Accepts as input a non-tokenized string.''')]
        desired_results = {"0": '''removes all non-proper-noun capitals from a given text. removes capital letters from text, even for Bill Clinton. accepts as input a non-tokenized string.'''}
        results = self.op.run(test_data)
        self.assertIsNotNone(results)
        for corpus in results:
            self.assertEqual(corpus.contents, desired_results[corpus.id])

if __name__ == '__main__':
    unittest.main()
