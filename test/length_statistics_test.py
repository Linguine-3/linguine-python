import unittest

from linguine.corpus import Corpus
from linguine.ops.length_statistics import LengthStatistics
from test.test_utils import round_json_floats


class LengthStatisticsOpTest(unittest.TestCase):

    def setUp(self):
        self.op = LengthStatistics()

    def test_run(self):
        self.test_data = [
            Corpus("0", "Test", "The quick brown fox jumped over the lazy dog. Here is another test sentence.\n")]
        results = self.op.run(self.test_data)
        desired_results = [{'words': {'median': 4.0, 'std': 1.6919330254585618, 'mean': 4.357142857142857},
                            'sentences': {'median': 7.0, 'std': 2.8284271247461903, 'mean': 7}}]
        self.assertEqual(round_json_floats(results), round_json_floats(desired_results))


if __name__ == '__main__':
    unittest.main()
