import unittest

from linguine.corpus import Corpus
from linguine.ops.no_op import NoOp


class NoOpTest(unittest.TestCase):

    def setUp(self):
        self.op = NoOp()

    def test_run_has_data(self):
        self.test_data = [Corpus("0", "Test", "The quick brown fox jumped over the lazy dog.\n")]
        results = self.op.run(self.test_data)
        print(results)
        desired_results = {'title': 'Test', 'tags': [], 'id': '0',
                           'contents': 'The quick brown fox jumped over the lazy dog.\n', 'tokenized_contents': None}
        self.assertEqual(results, desired_results)

    def test_run_no_data(self):
        self.test_data = []
        results = self.op.run(self.test_data)
        print(results)
        desired_results = ''
        self.assertEqual(results, desired_results)


if __name__ == '__main__':
    unittest.main()
