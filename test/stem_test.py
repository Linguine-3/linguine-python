import unittest

from linguine.corpus import Corpus
from linguine.ops.stem import StemmerPorter
from linguine.ops.word_tokenize import WordTokenizeWhitespacePunct


class StemTest(unittest.TestCase):

    def setUp(self):
        self.op = StemmerPorter()

    def test_porter(self):
        test_data = [Corpus("0", "", ' '.join(
            ['strange', 'women', 'lying', 'ponds', 'distributing', 'swords', 'no', 'basis', 'system', 'government']))]
        test_data = WordTokenizeWhitespacePunct().run(test_data)
        desired_results = {
            "0": ['strang', 'women', 'lie', 'pond', 'distribut', 'sword', 'no', 'basi', 'system', 'govern']}
        results = self.op.run(test_data)
        self.assertIsNotNone(results)
        for corpus in results:
            self.assertEqual(corpus.tokenized_contents, desired_results[corpus.id])


if __name__ == '__main__':
    unittest.main()
