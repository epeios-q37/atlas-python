""" 
MIT License

Copyright (c) 2018 Claude SIMON (https://q37.info/s/rmnmqd49)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
 """

import XDHq, XDHqSHRD
from threading import Thread
import threading
import inspect

import signal, sys, os

if sys.version_info[0] == 2:
	import __builtin__ as builtins
else:
	import builtins

# Overriding some functions for the Dev environment.
if XDHqSHRD.isDev():
	if "openpyxl" in sys.modules :
		defaultXLFunction = sys.modules['openpyxl'].load_workbook
		sys.modules['openpyxl'].load_workbook = lambda filename, **kwargs: defaultXLFunction(XDHq.get_asset_filename(filename), **kwargs)
	
	defaultBuiltinsFunction = builtins.open
	builtins.open = lambda filename, *args, **kwargs: defaultBuiltinsFunction(XDHq.get_asset_filename(filename), *args, **kwargs)

def signal_handler(sig, frame):
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def create_XML(root_tag):
	return XDHq.XML(root_tag)

createXML = create_XML	


def create_HTML(root_tag=""):	# If 'root_tag' is empty, there will be no root tag in the tree.
	return XDHq.XML(root_tag)

createHTML = create_HTML

broadcast_action = XDHq.broadcastAction


def _call(func, userObject, dom, id, action):
	amount = len(inspect.getargspec(func).args)
	args = []

	if ( not(userObject)) :
		amount += 1

	if ( amount == 4 ):
		args.insert(0,action)

	if( amount >= 3 ):
		args.insert(0,id)

	if( amount >= 2 ):
		args.insert(0,dom)

	if( userObject and (amount >= 1 )):
		args.insert(0,userObject)

	return func(*args)


def worker(userCallback,dom,callbacks):
	args=[]
	userObject = None

	if ( userCallback != None ):
		if ( not(inspect.isclass(userCallback)) and len(inspect.getargspec(userCallback).args) == 1 ):
			args.append(dom)

		userObject = userCallback(*args)
	
	while True:
		[action,id] = dom.getAction()

		if dom.isQuitting():
			break

		if action=="" or not "_PreProcess" in callbacks or _call(callbacks["_PreProcess"],userObject, dom, id, action):
			if ( action in callbacks ):
				if _call(callbacks[action], userObject, dom, id, action ) and "_PostProcess" in callbacks:
					_call(callbacks["_PostProcess"],userObject, dom, id, action)
			else:
				dom.alert("\tDEV ERROR: missing callback for '" + action + "' action!") 

	# print("Quitting thread !")

def callback(userCallback,callbacks,instance):
	thread = threading.Thread(target=worker, args=(userCallback, XDHq.DOM(instance), callbacks))
	thread.daemon = True
	thread.start()
	return thread

def launch(callbacks, userCallback = None, headContent = ""):
	XDHq.launch(callback,userCallback,callbacks,headContent)

