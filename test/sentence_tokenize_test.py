import unittest

from linguine.corpus import Corpus
from linguine.ops.sentence_tokenize import SentenceTokenize


class SentenceTokenizeTest(unittest.TestCase):

    def setUp(self):
        self.op = SentenceTokenize()

    def test_run(self):
        test_data = [Corpus("0", "", "hello world. Will you say goodbye, world? I'll say hello.")]
        desired_results = {"0": ["hello world.", "Will you say goodbye, world?", "I'll say hello."]}
        results = self.op.run(test_data)
        self.assertIsNotNone(results)
        for result in results:
            self.assertEqual(result['sentences'], desired_results[result['corpus_id']])


if __name__ == '__main__':
    unittest.main()
