#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import io, sys, os, json

from Baubles.Colours import Colours
from Baubles.Logger import Logger
from Perdy.pretty import prettyPrintLn, Style
from Perdy.parser import doParse
from Argumental.Argue import Argue

logger = Logger()
args = Argue()

@args.command(single=True)
class Warbeler(object):
	
	@logger.debug
	@args.property(short='c', flag=True, help='output in colour')
	def colour(self): 
		return False	
	
	def __init__(self, colour=False):
		self.colour = colour
	
	@logger.info
	@args.operation
	@args.parameter(name='files', short='f', nargs='*', metavar='file')
	def sing(self, files=[]):
		'''
		coloured file name outpu
		'''
		self.colours = Colours(colour=self.colour)
		for file in files:
			off = self.colours.Off
			colour = off
			if os.path.isfile(file):
				colour = self.colours.Orange
			if os.path.isdir(file):
				colour = self.colours.Blue
			if os.path.islink(file):
				colour = self.colours.Green
			sys.stdout.write(f'{colour}{file}{off}\n')
		del self.colours
		return files
		
	@args.operation
	@args.parameter(name='file')
	def song(self, file):
		'''
		stat the file
		'''
		print(os.stat(file))
		
if __name__ == '__main__': args.execute()



