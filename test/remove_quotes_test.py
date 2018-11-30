import unittest

from linguine.corpus import Corpus
from linguine.ops.remove_quotes import RemoveQuotes


class RemoveQuotesTest(unittest.TestCase):

    def setUp(self):
        self.op = RemoveQuotes()

    def test_run(self):
        test_data = [Corpus("0", "", 'I said, "The quick brown fox jumped over the lazy dog."')]
        desired_results = {"0": 'I said, The quick brown fox jumped over the lazy dog.'}
        results = self.op.run(test_data)
        self.assertIsNotNone(results)
        for corpus in results:
            self.assertEqual(corpus.contents, desired_results[corpus.id])


if __name__ == '__main__':
    unittest.main()
