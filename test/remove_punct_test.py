import unittest

from linguine.corpus import Corpus
from linguine.ops.remove_punct import RemovePunct


class RemovePunctTest(unittest.TestCase):

    def setUp(self):
        self.op = RemovePunct()

    def test_run(self):
        test_data = [Corpus("0", "", "He said,\"that's it.\" *u* Hello, World. O'Rourke is rockin'.")]
        desired_results = {"0": "He said that s it Hello World O Rourke is rockin"}
        results = self.op.run(test_data)
        self.assertIsNotNone(results)
        for corpus in results:
            self.assertEqual(corpus.contents, desired_results[corpus.id])


if __name__ == '__main__':
    unittest.main()
