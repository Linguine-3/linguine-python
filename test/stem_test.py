import unittest

from linguine.corpus import Corpus
from linguine.ops.stem import StemmerLancaster, StemmerPorter, StemmerSnowball
from linguine.ops.word_tokenize import WordTokenizeSpaces


class StemTest(unittest.TestCase):

    def test_lancaster(self):
        self.op = StemmerLancaster()
        test_data = [Corpus("0", "", ' '.join(
            ['strange', 'women', 'lying', 'ponds', 'distributing', 'swords', 'no', 'basis', 'system', 'government']))]
        test_data = WordTokenizeSpaces().run(test_data)
        desired_results = {
            "0": ['strange', 'wom', 'lying', 'pond', 'distribut', 'sword', 'no', 'bas', 'system', 'govern']}
        results = self.op.run(test_data)
        self.assertIsNotNone(results)
        for corpus in results:
            self.assertEqual(corpus.tokenized_contents, desired_results[corpus.id])

    def test_porter(self):
        self.op = StemmerPorter()
        test_data = [Corpus("0", "", ' '.join(
            ['strange', 'women', 'lying', 'ponds', 'distributing', 'swords', 'no', 'basis', 'system', 'government']))]
        test_data = WordTokenizeSpaces().run(test_data)
        desired_results = {
            "0": ['strang', 'women', 'lie', 'pond', 'distribut', 'sword', 'no', 'basi', 'system', 'govern']}
        results = self.op.run(test_data)
        self.assertIsNotNone(results)
        for corpus in results:
            self.assertEqual(corpus.tokenized_contents, desired_results[corpus.id])

    def test_snowball(self):
        self.op = StemmerSnowball()
        test_data = [Corpus("0", "", ' '.join(
            ['strange', 'women', 'lying', 'ponds', 'distributing', 'swords', 'no', 'basis', 'system', 'government']))]
        test_data = WordTokenizeSpaces().run(test_data)
        desired_results = {
            "0": ['strang', 'women', 'lie', 'pond', 'distribut', 'sword', 'no', 'basi', 'system', 'govern']}
        results = self.op.run(test_data)
        self.assertIsNotNone(results)
        for corpus in results:
            self.assertEqual(corpus.tokenized_contents, desired_results[corpus.id])


if __name__ == '__main__':
    unittest.main()
