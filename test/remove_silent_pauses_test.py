import unittest

from linguine.corpus import Corpus
from linguine.ops.remove_silent_pauses import RemoveSilence


class RemoveSilentPausesTest(unittest.TestCase):

    def setUp(self):
        self.op = RemoveSilence()

    def test_run(self):
        test_data = [Corpus("0", "", "The quick brown fox {sl} jumped over the lazy dog.\n")]
        desired_results = {"0": "The quick brown fox jumped over the lazy dog.\n"}
        results = self.op.run(test_data)
        self.assertIsNotNone(results)
        for corpus in results:
            self.assertEqual(corpus.contents, desired_results[corpus.id])


if __name__ == '__main__':
    unittest.main()
