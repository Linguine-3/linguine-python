import unittest
import sys
sys.path.append('../src')
sys.path.append('../src/ops')

from remove_punct import remove_punct

class tfidf_test(unittest.TestCase):

	def setUp(self):
		self.op = remove_punct()
	
	def test_run(self):
		self.op = remove_punct()
		self.test_data = '''He said,"that's it." *u* Hello, World. O'Rourke is rockin'.'''
		self.assertEqual(self.op.run(self.test_data), '''He said that s it Hello World O Rourke is rockin''')

if __name__ == '__main__':
	unittest.main()