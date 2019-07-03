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

import XDHq
from threading import Thread
import threading
import inspect
from XDHq import readAsset

def createXML(rootTag):
	return XDHq.XML(rootTag)

def createHTML(rootTag=""):	# If 'rootTag' is empty, there will be no root tag in the tree.
	return XDHq.XML(rootTag)

def _call(func, userObject, dom, id, action):
	amount = len(inspect.getargspec(func).args)
	args = []

	if ( amount == 4 ):
		args.insert(0,action)

	if( amount >= 3 ):
		args.insert(0,id)

	if( amount >= 2 ):
		args.insert(0,dom)

	if( amount >= 1 ):
		args.insert(0,userObject)

	return func(*args)


def worker(userCallback,dom,callbacks):
	userObject = userCallback()
	while True:
		[action,id] = dom.getAction()
		if action=="" or not "_PreProcess" in callbacks or _call(callbacks["_PreProcess"],userObject, dom, id, action):
			if _call(callbacks[action], userObject, dom, id, action ) and "_PostProcess" in callbacks:
				_call(callbacks["_PostProcess"],userObject, dom, id, action)

def callback(userCallback,callbacks,instance):
	thread = threading.Thread(target=worker, args=(userCallback, XDHq.DOM(instance), callbacks))
	thread.daemon = True
	thread.start()
	return thread

def launch(callbacks, userCallback = lambda: None, headContent = "", dir = ""):
	XDHq.launch(callback,userCallback,callbacks,headContent,dir)

