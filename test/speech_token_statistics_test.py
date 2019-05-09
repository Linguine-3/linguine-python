import unittest

from linguine.corpus import Corpus
from linguine.ops.speech_token_statistics import SpeechTokenStatistics


class SpeechTokenStatisticsTest(unittest.TestCase):

    def setUp(self):
        self.op = SpeechTokenStatistics()

    def test_run(self):
        test_data_contents = '[{"start":10,"filler":false,"end":90,"word":"i"},' \
                             '{"start":100,"filler":false,"end":360,"word":"know"},' \
                             '{"start":370,"filler":false,"end":470,"word":"i"},' \
                             '{"start":480,"filler":false,"end":730,"word":"just"},' \
                             '{"start":740,"filler":false,"end":950,"word":"as"},' \
                             '{"start":960,"filler":true,"end":980,"word":"<sil>"},' \
                             '{"start":990,"filler":false,"end":1070,"word":"you"},' \
                             '{"start":1080,"filler":false,"end":1320,"word":"this"},' \
                             '{"start":1490,"filler":true,"end":1600,"word":"<sil>"}]'
        test_data = [Corpus('0', '', test_data_contents)]
        results = self.op.run(test_data)
        desired_results = [{'transcript': 'i know i just as <sil> you this <sil>',
                            'base_stats': {'num_fillers': 2,
                                           'num_words': 7,
                                           'filler_time': 0.13,
                                           'word_time': 1.22,
                                           'total_time': 1.6,
                                           'words_per_minute': 262.5},
                            'longest_tokens': [{'word': 'know', 'length': 0.26},
                                               {'word': 'just', 'length': 0.25},
                                               {'word': 'this', 'length': 0.24},
                                               {'word': 'as', 'length': 0.21},
                                               {'word': 'i', 'length': 0.1},
                                               {'word': 'i', 'length': 0.08},
                                               {'word': 'you', 'length': 0.08}]}]
        self.assertEqual(results, desired_results)


if __name__ == '__main__':
    unittest.main()
