import unittest

from linguine.corpus import Corpus
from linguine.ops.remove_hashtags import RemoveHashtags


class RemoveHashtagsTest(unittest.TestCase):

    def setUp(self):
        self.op = RemoveHashtags()

    def test_run(self):
        test_data = [Corpus("0", "", "This tweet is great! #Hashtags")]
        desired_results = {"0": "This tweet is great! Hashtags"}
        results = self.op.run(test_data)
        self.assertIsNotNone(results)
        for corpus in results:
            self.assertEqual(corpus.contents, desired_results[corpus.id])


if __name__ == '__main__':
    unittest.main()
