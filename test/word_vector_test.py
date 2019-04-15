import unittest

from linguine.corpus import Corpus
from linguine.ops.word_vector import WordVector
from test.test_utils import round_json_floats


class WordVectorTest(unittest.TestCase):

    def setUp(self):
        self.op = WordVector()

    def test_run(self):
        commands = ['doesnt_match breakfast cereal dinner lunch', 'most_sim python', 'sim_math +woman +king -man', '',
                    'sim_score universities colleges', 'never_will_work test1 test2 ']
        test_data = [Corpus(0, '', '\r\n'.join(commands))]
        results = self.op.run(test_data)
        print(results)
        desired_results = [
            {'type': 'doesnt_match', 'words': ['breakfast', 'cereal', 'dinner', 'lunch'], 'answer': 'cereal'},
            {'type': 'most_sim', 'word': 'python',
             'answer': [{'word': 'reticulated', 'score': 0.6916365027427673},
                        {'word': 'spamalot', 'score': 0.6635736227035522},
                        {'word': 'php', 'score': 0.6414496898651123},
                        {'word': 'owl', 'score': 0.6301496028900146},
                        {'word': 'mouse', 'score': 0.6275478005409241},
                        {'word': 'reticulatus', 'score': 0.6274471282958984},
                        {'word': 'perl', 'score': 0.6267576217651367},
                        {'word': 'monkey', 'score': 0.6207212209701538},
                        {'word': 'monty', 'score': 0.6079354286193848},
                        {'word': 'scripting', 'score': 0.6041731834411621}]},
            {'type': 'sim_math', 'pos': ['woman', 'king'], 'neg': ['man'],
             'answer': [{'word': 'queen', 'score': 0.8523603677749634},
                        {'word': 'throne', 'score': 0.7664333581924438},
                        {'word': 'prince', 'score': 0.759214460849762},
                        {'word': 'daughter', 'score': 0.7473883032798767},
                        {'word': 'elizabeth', 'score': 0.7460220456123352},
                        {'word': 'princess', 'score': 0.7424570322036743},
                        {'word': 'kingdom', 'score': 0.7337412238121033},
                        {'word': 'monarch', 'score': 0.7214491367340088},
                        {'word': 'eldest', 'score': 0.7184862494468689},
                        {'word': 'widow', 'score': 0.7099430561065674}]},
            {'type': 'sim_score', 'word1': 'universities', 'score': 0.9215914199727002, 'word2': 'colleges'},
            {'type': 'error', 'command': 'never_will_work test1 test2'}]
        self.assertEqual(round_json_floats(results, 4), round_json_floats(desired_results, 4))


if __name__ == '__main__':
    unittest.main()
