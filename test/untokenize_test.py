import unittest

from linguine.untokenize import untokenize


class UntokenizeTest(unittest.TestCase):

    def test_run(self):
        test_data = ['This', 'is', 'a', 'test', 'sentence', '.', 'Why', 'is', 'it', 'so', 'hard', 'to', 'make', '?',
                     'I', 'don\'t', 'know', '.']
        desired_results = 'This is a test sentence. Why is it so hard to make? I don\'t know.'
        results = untokenize(test_data)
        self.assertEqual(results, desired_results)


if __name__ == '__main__':
    unittest.main()
