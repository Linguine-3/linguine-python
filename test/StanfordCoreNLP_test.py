import unittest

from linguine.ops.StanfordCoreNLP import StanfordCoreNLP
from linguine.corpus import Corpus


class StanfordCoreNLPTest(unittest.TestCase):

    def setUp(self):
        self.op = StanfordCoreNLP([])
        self.test_data = [Corpus("0", "Test", "The quick brown fox jumped over the lazy dog.\n")]

    def test_run(self):
        self.op.analysisType = ['pos']
        self.op.run(self.test_data)


if __name__ == '__main__':
    unittest.main()
