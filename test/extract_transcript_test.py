import unittest

from linguine.corpus import Corpus
from linguine.ops.extract_transcript import ExtractTranscript


class ExtractTranscriptTest(unittest.TestCase):

    def setUp(self):
        self.op = ExtractTranscript()

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
        desired_results = {'0': 'i know i just as you this'}
        results = self.op.run(test_data)
        self.assertIsNotNone(results)
        for corpus in results:
            self.assertEqual(corpus.contents, desired_results[corpus.id])


if __name__ == '__main__':
    unittest.main()
