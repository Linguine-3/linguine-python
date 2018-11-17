import unittest

from linguine.corpus import Corpus
from linguine.ops.topic_model import TopicModel


class TopicModelTest(unittest.TestCase):

    def setUp(self):
        self.num_topics = 10
        self.op = TopicModel(self.num_topics)

    def test_run(self):
        test_data = [Corpus(str(num), "", line) for num, line in enumerate(open('brown.txt', 'r'))]
        test_data = test_data[:100]
        results = self.op.run(test_data)
        self.assertIsNotNone(results)  # Result is returned
        self.assertEqual(len(results), self.num_topics)  # Correct number of topics returned
        for topic in results.values():
            self.assertEqual(len(topic), 10)  # Each topic has 10 words


if __name__ == '__main__':
    unittest.main()
