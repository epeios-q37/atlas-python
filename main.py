#!/usr/bin/python3
# coding: utf-8

# All files under MIT license
# Copyright (c) 2019 Claude SIMON (https://q37.info/s/rmnmqd49)
# See  'LICENSE' file.

# For 'Repl.it'.

import os,sys

try:
	input = raw_input
except NameError:
	pass

loop = True

DEMOS = (
	"Blank",
	"Hello",
	"Chatroom",
	"Notes",
	"TodoMVC",
	"Hangman",
	"15-puzzle",
	"Contacts",
	"Widgets",
	"Chatrooms",
	"Reversi",
	"MatPlotLib"
)

DEMOS_AMOUNT = len(DEMOS)

def normalize(item):
	if ( isinstance(item,str) ):
		return item, 0
	else:
		return item

while loop:
	
	for id in range(0,DEMOS_AMOUNT):
		label, amount = normalize(DEMOS[id])
		letter = chr(id + ord('a'))

		if amount:
			print(letter, 0, ", ", letter, 1, ", …, ", letter, amount, ": ", label, " (tutorial)", sep='')
		else:
			print(letter, ": ", label, sep='')

	entry = input("Select one of above demo: ").lower()
   
	try:
		id = int(ord(entry[:1]) - ord('a'))
		label, amount = normalize(DEMOS[id])

		affix = "tutorials" if amount else "examples"

		if ( amount ):
			number = int(entry[1:])

			if ( ( number < 0 ) or ( number > amount ) ):
				raise

		# Needed by Repl.it
		suffix = "part" + entry[1:] if amount else 'main'

		sample = affix + "." + label + "." + suffix
		sys.argv[0]=affix + '/' + label + "/"

		if True:  # Simplifies debugging when set to False
			try:
				__import__(sample)
			except ImportError:
				print("\tERROR: could not launch '" + sys.argv[0] + suffix + ".py'!")
				loop = False
			except:
				loop = False
		else:
			__import__(sample)
	except:
		print("'" + entry + "' is not a valid sample id. Please retry.\n")
