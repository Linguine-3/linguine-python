import unittest

from linguine.corpus import Corpus
from linguine.ops.lemmatize import LemmatizerWordNet
from linguine.ops.word_tokenize import WordTokenizeWhitespacePunct


class LemmatizeTest(unittest.TestCase):

    def setUp(self):
        self.op = LemmatizerWordNet()

    def test_run(self):
        test_data = [
            Corpus("0", "", "strange women lying in ponds distributing swords is no basis for a system of government")]
        test_data = WordTokenizeWhitespacePunct().run(test_data)
        desired_results = {"0": "strange woman lie in pond distribute sword be no basis for a system of government"}
        results = self.op.run(test_data)
        self.assertIsNotNone(results)
        for corpus in results:
            self.assertEqual(corpus.contents, desired_results[corpus.id])


if __name__ == '__main__':
    unittest.main()
