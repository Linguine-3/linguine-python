import json
import unittest

from linguine.corpus import Corpus
from linguine.ops.length_statistics import LengthStatistics


class LengthStatisticsOpTest(unittest.TestCase):

    def setUp(self):
        self.op = LengthStatistics()

    def test_run(self):
        self.test_data = [
            Corpus("0", "Test", "The quick brown fox jumped over the lazy dog. Here is another test sentence.\n")]
        results = self.op.run(self.test_data)
        print(results)
        desired_results = [{'words': {'median': 4.0, 'std': 1.6919330254585618, 'mean': 4.357142857142857},
                            'sentences': {'median': 7.0, 'std': 2.8284271247461903, 'mean': 7}}]
        self.assertEqual(json.loads(results), desired_results)


if __name__ == '__main__':
    unittest.main()
