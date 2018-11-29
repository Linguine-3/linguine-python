import unittest

from linguine.corpus import Corpus
from linguine.ops.remove_stopwords import RemoveStopwords
from linguine.ops.word_tokenize import WordTokenizeWhitespacePunct


class RemoveStopwordsTest(unittest.TestCase):

    def setUp(self):
        self.op = RemoveStopwords()

    def test_run(self):
        test_data = [Corpus("0", "", "the quick brown fox jumps over the lazy dog")]
        test_data = WordTokenizeWhitespacePunct().run(test_data)
        desired_results = {"0": "quick brown fox jumps lazy dog"}
        results = self.op.run(test_data)
        self.assertIsNotNone(results)
        for corpus in results:
            self.assertEqual(corpus.contents, desired_results[corpus.id])


if __name__ == '__main__':
    unittest.main()
