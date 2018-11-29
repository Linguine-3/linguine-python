import unittest

from linguine.corpus import Corpus
from linguine.ops.word_cloud_op import WordCloudOp
from linguine.ops.word_tokenize import WordTokenizeWhitespacePunct


class WordCloudOpTest(unittest.TestCase):

    def setUp(self):
        self.op = WordCloudOp()

    def test_run(self):
        test_data = [Corpus("0", "hello", "hello world hello hello world test")]
        WordTokenizeWhitespacePunct().run(test_data)
        desired_results = [{"term": "hello", "frequency": 3},
                           {"term": "world", "frequency": 2},
                           {"term": "test", "frequency": 1}]
        results = self.op.run(test_data)
        self.assertEqual(results["sentences"], desired_results)


if __name__ == '__main__':
    unittest.main()
