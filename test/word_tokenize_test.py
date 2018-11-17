import unittest

from linguine.corpus import Corpus
from linguine.ops.word_tokenize import WordTokenizeSpaces


class WordTokenizeTest(unittest.TestCase):

    def setUp(self):
        self.op = WordTokenizeSpaces()

    def test_run(self):
        test_data = [Corpus("0", "hello", "hello world"), Corpus("1", "goodbye", "goodbye world")]
        results = self.op.run(test_data)
        desired_results = {"0": ["hello", "world"],
                           "1": ["goodbye", "world"]}
        self.assertIsNotNone(results)
        for corpus in results:
            self.assertEqual(corpus.tokenized_contents, desired_results[corpus.id])


if __name__ == '__main__':
    unittest.main()
