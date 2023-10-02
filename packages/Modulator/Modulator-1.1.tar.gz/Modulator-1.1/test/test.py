#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import io, sys, os, logging, unittest

sys.path.insert(0, '..')
	
from Modulated.Warbeler import Warbeler

class WarbelerTest(unittest.TestCase):
	
	def setUp(self):
		sys.stdout.write('setUp\n')
		
	def tearDown(self):
		sys.stdout.write('tearDown\n')
		
	def test_sing_method(self):
		warbler = Warbeler(colour=True)
		files = os.listdir()+['../bin']
		result = warbler.sing(files=files)
		self.assertEqual(result, files)


if __name__ == '__main__':
	level = logging.INFO
	#level = logging.DEBUG
	logging.basicConfig(level=level)
	unittest.main(exit=True)
