import json
import unittest

from linguine.corpus import Corpus
from linguine.ops.splat import SplatComplexity, SplatDisfluency, SplatNGrams, SplatPOSFrequencies, SplatPronouns, \
    SplatSyllables
from test.test_utils import round_json_floats


class SplatTest(unittest.TestCase):

    def test_run_disfluency(self):
        self.op = SplatDisfluency()
        self.test_data = [
            Corpus("0", "Test", "The quick brown fox {sl} jumped over the lazy dog.\nI uh saw it happen.")]
        results = json.loads(self.op.run(self.test_data))
        print(results)
        desired_results = [{'corpus_id': '0',
                            'sentences': {
                                'uh saw it happen.':
                                    {'SILENT PAUSE': 0, 'HM': 0, 'BREAK': 0, 'UH': 1, 'UM': 0, 'AH': 0, 'REPETITION': 0,
                                     'ER': 0},
                                'The quick brown fox {sl} jumped over the lazy dog.I':
                                    {'SILENT PAUSE': 1, 'HM': 0, 'BREAK': 0, 'UH': 0, 'UM': 0, 'AH': 0, 'REPETITION': 0,
                                     'ER': 0}},
                            'average_disfluencies_per_sentence': 1.0,
                            'total_disfluencies':
                                {'SILENT PAUSE': 1, 'HM': 0, 'BREAK': 0, 'TOTAL': 2, 'UM': 0, 'AH': 0, 'UH': 1,
                                 'REPETITION': 0, 'ER': 0}
                            }]

        self.assertEqual(results, desired_results)

    def test_run_ngrams(self):
        self.op = SplatNGrams()
        self.test_data = [Corpus("0", "Test", "The quick brown fox jumped over the lazy dog.\n")]
        results = json.loads(self.op.run(self.test_data))
        desired_results = [{"corpus_id": "0",
                            "unigrams": {"dog": 1, "the": 2, "fox": 1, "jumped": 1, "over": 1, "lazy": 1, "brown": 1,
                                         "quick": 1},
                            "bigrams": {"the quick": 1, "quick brown": 1, "lazy dog": 1, "brown fox": 1,
                                        "fox jumped": 1,
                                        "jumped over": 1, "over the": 1, "the lazy": 1},
                            "trigrams": {"the quick brown": 1, "quick brown fox": 1, "the lazy dog": 1,
                                         "jumped over the": 1,
                                         "over the lazy": 1, "brown fox jumped": 1, "fox jumped over": 1}}]
        self.assertEqual(results, desired_results)

    def test_run_complexity(self):
        self.op = SplatComplexity()
        self.test_data = [Corpus("0", "Test", "The quick brown fox jumped over the lazy dog.\nI saw it happen.")]
        results = json.loads(self.op.run(self.test_data))
        desired_results = [{'corpus_id': '0',
                            'content_density': [2.0, 2.0, 2.0],
                            'idea_density': 0.5,
                            'flesch_score': 96.1,
                            'kincaid_score': 1.5,
                            'types': 12,
                            'tokens': 13,
                            'type_token_ratio': 0.9230769230769231}]
        self.assertEqual(round_json_floats(results), round_json_floats(desired_results))

    def test_run_pos_frequencies(self):
        self.op = SplatPOSFrequencies()
        self.test_data = [Corpus("0", "Test", "The very quick brown fox jumped over the lazy dog.\nI saw it happen.")]
        results = json.loads(self.op.run(self.test_data))
        desired_results = [{"corpus_id": "0",
                            "pos_tags": {"DT": ["The", "the"], "JJ": ["very"], "IN": ["over"], "VBD": ["jumped", "saw"],
                                         "VB": ["happen"], "PRP": ["I", "it"],
                                         "NN": ["quick", "brown", "fox", "lazy", "dog"], ".": ["."]},
                            "pos_counts": {"DT": 2, "JJ": 1, "IN": 1, "VBD": 2, "VB": 1, "PRP": 2, "NN": 5, ".": 2}
                            }]
        self.assertEqual(results, desired_results)

    def test_run_syllables(self):
        self.op = SplatSyllables()
        self.test_data = [Corpus("0", "Test", "The very quick brown fox jumped over the lazy dog.\nI saw it happen.")]
        results = json.loads(self.op.run(self.test_data))
        desired_results = [{'corpus_id': '0',
                            'syllables': {'1': ['the', 'quick', 'brown', 'fox', 'jumped', 'dog', 'i', 'saw', 'it'],
                                          '2': ['very', 'over', 'lazy', 'happen']}}]
        self.assertEqual(results, desired_results)

    def test_run_pronouns(self):
        self.op = SplatPronouns()
        self.test_data = [Corpus("0", "Test", "He and she jumped over my fence.\nI saw them do so, and I told you.")]
        results = json.loads(self.op.run(self.test_data))
        print(results)
        desired_results = [{'corpus_id': '0',
                            'first-person': {'MYSELF': [0, '1st-Person', 'Reflexive', 'Singular'],
                                             'OURSELVES': [0, '1st-Person', 'Reflexive', 'Plural'],
                                             'WE': [0, '1st-Person', 'Personal', 'Plural'],
                                             'ME': [0, '1st-Person', 'Personal', 'Singular'],
                                             'OUR': [0, '1st-Person', 'Possessive', 'Plural'],
                                             'MY': [1, '1st-Person', 'Possessive', 'Singular'],
                                             'MINE': [0, '1st-Person', 'Possessive', 'Singular'],
                                             'US': [0, '1st-Person', 'Personal', 'Plural'],
                                             'I': [2, '1st-Person', 'Personal', 'Singular'],
                                             'OURS': [0, '1st-Person', 'Possessive', 'Plural']},
                            'second-person': {'YOU': [1, '2nd-Person', 'Personal', 'Singular/Plural'],
                                              'YOURSELVES': [0, '2nd-Person', 'Reflexive', 'Plural'],
                                              'YOURS': [0, '2nd-Person', 'Possessive', 'Singular/Plural'],
                                              'YOUR': [0, '2nd-Person', 'Possessive', 'Singular/Plural'],
                                              'YOURSELF': [0, '2nd-Person', 'Reflexive', 'Singular']},
                            'third-person': {'THEY': [0, '3rd-Person', 'Personal', 'Plural'],
                                             'ITSELF': [0, '3rd-Person', 'Reflexive', 'Singular'],
                                             'HERS': [0, '3rd-Person', 'Possessive', 'Singular'],
                                             'HIM': [0, '3rd-Person', 'Personal', 'Singular'],
                                             'SHE': [1, '3rd-Person', 'Personal', 'Singular'],
                                             'HERSELF': [0, '3rd-Person', 'Reflexive', 'Singular'],
                                             'ITS': [0, '3rd-Person', 'Possessive', 'Singular'],
                                             'HIMSELF': [0, '3rd-Person', 'Reflexive', 'Singular'],
                                             'THEIRS': [0, '3rd-Person', 'Possessive', 'Plural'],
                                             'THEIR': [0, '3rd-Person', 'Possessive', 'Plural'],
                                             'HIS': [0, '3rd-Person', 'Possessive', 'Singular'],
                                             'IT': [0, '3rd-Person', 'Personal', 'Singular'],
                                             'HE': [1, '3rd-Person', 'Personal', 'Singular'],
                                             'HER': [0, '3rd-Person', 'Personal/Possessive', 'Singular/Plural'],
                                             'THEMSELVES': [0, '3rd-Person', 'Reflexive', 'Plural'],
                                             'THEM': [1, '3rd-Person', 'Personal', 'Plural']},
                            'sentences': ['He and she jumped over my fence.', 'I saw them do so, and I told you.']}]
        self.assertEqual(results, desired_results)


if __name__ == '__main__':
    unittest.main()
