import json
import unittest

from linguine.corpus import Corpus
from linguine.ops.char_ngrams import CharNgrams


class CharNgramsOpTest(unittest.TestCase):

    def setUp(self):
        self.op = CharNgrams()

    def test_run(self):
        self.test_data = [Corpus("0", "Test", "The quick brown fox jumped over the lazy dog.\n")]
        results = self.op.run(self.test_data)
        desired_results = [{"corpus_id": "0",
                            "unigrams": {"_": 8, "a": 1, "b": 1, "c": 1, "d": 2, "e": 4, "f": 1, "g": 1, "h": 2, "i": 1,
                                         "j": 1, "k": 1, "l": 1, "m": 1, "n": 1, "o": 4, "p": 1, "q": 1, "r": 2, "t": 2,
                                         "u": 2, "v": 1, "w": 1, "x": 1, "y": 1, "z": 1},
                            "bigrams": {"_b": 1, "_d": 1, "_f": 1, "_j": 1, "_l": 1, "_o": 1, "_q": 1, "_t": 1, "az": 1,
                                        "br": 1, "ck": 1, "d_": 1, "do": 1, "e_": 2, "ed": 1, "er": 1, "fo": 1, "he": 2,
                                        "ic": 1, "ju": 1, "k_": 1, "la": 1, "mp": 1, "n_": 1, "og": 1, "ov": 1, "ow": 1,
                                        "ox": 1, "pe": 1, "qu": 1, "r_": 1, "ro": 1, "th": 2, "ui": 1, "um": 1, "ve": 1,
                                        "wn": 1, "x_": 1, "y_": 1, "zy": 1},
                            "trigrams": {"_br": 1, "_do": 1, "_fo": 1, "_ju": 1, "_la": 1, "_ov": 1, "_qu": 1, "_th": 1,
                                         "azy": 1, "bro": 1, "ck_": 1, "d_o": 1, "dog": 1, "e_l": 1, "e_q": 1, "ed_": 1,
                                         "er_": 1, "fox": 1, "he_": 2, "ick": 1, "jum": 1, "k_b": 1, "laz": 1, "mpe": 1,
                                         "n_f": 1, "ove": 1, "own": 1, "ox_": 1, "ped": 1, "qui": 1, "r_t": 1, "row": 1,
                                         "the": 2, "uic": 1, "ump": 1, "ver": 1, "wn_": 1, "x_j": 1, "y_d": 1,
                                         "zy_": 1}}]
        self.assertEqual(results, desired_results)


if __name__ == '__main__':
    unittest.main()
