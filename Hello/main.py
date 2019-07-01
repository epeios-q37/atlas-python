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

import os, sys

sys.path.append("./Atlas.python.zip")
sys.path.append("../Atlas.python.zip")

import atlastk as Atlas

def readAsset(path):
	return Atlas.readAsset(path, "Hello")

def acConnect(self, dom):
	dom.setLayout("", readAsset( "Main.html") )
	dom.focus( "input")

def acSubmit(self, dom):
	dom.alert("Hello, " + dom.getContent("input") + "!")
	dom.focus( "input")

def acClear(self, dom):
	if ( dom.confirm("Are you sure?" ) ):
		dom.setContent("input", "" )
	dom.focus( "input")

callbacks = {
	"": acConnect,
	"Submit": acSubmit,
	"Clear": acClear,
}
		
Atlas.launch(callbacks, lambda: None, readAsset("Head.html"))
