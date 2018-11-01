import json
import unittest

from linguine.corpus import Corpus
from linguine.ops.topic_model import TopicModel


class TopicModelTest(unittest.TestCase):

    def setUp(self):
        self.op = TopicModel()

    def test_run(self):
        test_data = [Corpus(str(num), "", line) for num, line in enumerate(open('brown.txt', 'r'))]
        test_data = test_data[:100]
        results = self.op.run(test_data)
        results = json.loads(results)
        self.assertIsNotNone(results)
        # TODO: Add better verification


if __name__ == '__main__':
    unittest.main()
