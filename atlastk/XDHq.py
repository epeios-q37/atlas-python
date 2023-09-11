# coding: utf-8

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

import XDHqFaaS,XDHqSHRD,XDHqXML
from XDHqFaaS import launch, set_supplier, get_app_url, setBye, l

import os,sys
from collections import OrderedDict

if sys.version_info[0] == 2:
	import urllib
	def _encode(string):
		return urllib.quote(string)
elif sys.version_info[0] == 3:
	import urllib.parse
	def _encode(string):
		return urllib.parse.quote(string)
else:
	print("Unhandled python version!")
	os._exit(1)

_VOID = XDHqSHRD.RT_VOID
_STRING = XDHqSHRD.RT_STRING
_STRINGS = XDHqSHRD.RT_STRINGS
XML = XDHqXML.XML


def _split(keysAndValues):
	keys = []
	values = []

	for key in keysAndValues:
		keys.append(str(key))
		values.append(str(keysAndValues[key]))

	return [keys,values]

def _unsplit(keys,values):
	i = 0
	# With 'OrderedDict', the order of the items is keeped under Python 2.
	# This facilitates the retrieving of values by using 'values()' method.
	# Dicts are ordered by default under Python 3.
	keysAndValues = OrderedDict()
	length = len(keys)

	while i < length:
		keysAndValues[keys[i]] = values[i]
		i += 1

	return keysAndValues

def _getAssetPath():
	if not XDHqSHRD.isDev():
		throw("Should only be called in DEV context!!!")

	return os.path.join(os.path.realpath(os.path.join(os.environ["Q37_EPEIOS"].replace('h:','/cygdrive/h'),"tools/xdhq/examples/common/")),os.path.relpath(os.getcwd(),os.path.realpath(os.path.join(os.environ["Q37_EPEIOS"].replace('h:','/cygdrive/h'),"tools/xdhq/examples/PYH/"))))


def get_asset_filename(path):
	return os.path.join(_getAssetPath(),path )


broadcastAction = XDHqFaaS.broadcastAction


def _readXSLAsset(path):
	if (path.lstrip()[0]=='<'):
		return path.lstrip()
	else:
		return open(get_asset_filename(path) if XDHqSHRD.isDev() else path).read()

class DOM:
	def __init__(self,instance):
		self._dom = XDHqFaaS.DOM_FaaS(instance)

	def get_action(self):
		return self._dom.getAction()

	getAction = get_action

	def isQuitting(self):
		return self._dom.isQuitting();

	def _execute(self,type,script):
		return self._dom.call("Execute_1",type,script)

	# Last statement of 'script' MUST be 'undefined', or the thread will be killed.
	def executeVoid(self,script):
		return self._execute(_VOID,script)

	execute_void = executeVoid

	def executeString(self,script):
		return self._execute(_STRING,script)

	execute_string = executeString

	def executeStrings(self,script):
		return self._execute(_STRINGS,script)

	execute_strings = executeStrings

	def _raw_send(self,type,data):
		return self._dom.call("RawSend_1",type,data)

	# Last statement of 'data' MUST be 'undefined', or the thread will be killed.
	def rawSendVoid(self,data):
		return self._raw_send(_VOID,data)

	raw_send_void = rawSendVoid

	def rawSendString(self,data):
		return self._raw_send(_STRING,data)

	raw_send_string = rawSendString

	def rawSendStrings(self,data):
		return self._raw_send(_STRINGS,data)

	raw_send_strings = rawSendStrings	

	def flush(self):	# Returns when all the pending commands were executed.
		self._dom.call("Flush_1",_STRING)

	def alert(self,message):
		self._dom.call( "Alert_1",_STRING,str(message) )
		# For the return value being 'STRING' instead of 'VOID',
		# see the 'alert' primitive in 'XDHqXDH'.

	def confirm(self,message):
		return self._dom.call( "Confirm_1",_STRING,message ) == "true"

	def _handleLayout(self,variant,id,xml,xsl):
		#	If 'xslFilename' is empty, 'xml' contents HTML.
		# If 'xml' is HTML and uses the compressed form, if it has a root tag, only the children will be used.
		# The corresponding primitive returns a value, which is only used internally, hence the lack of 'return'.
		# It also serves to do some synchronisation.
		self._dom.call("HandleLayout_1",_STRING,variant,id,xml if isinstance(xml,str) else xml.toString(),xsl)

	def prependLayout(self,id,html):	# Deprecated!
		self._handleLayout("Prepend",id,html,"")

	prepend_layout = prependLayout	# Deprecated!

	def setLayout(self,id,html):	# Deprecated!
		self._handleLayout("Set",id,html,"")

	set_layout = setLayout	# Deprecated!

	def appendLayout(self,id,html):	# Deprecated!
		self._handleLayout("Append",id,html,"")

	append_layout = appendLayout	# Deprecated!

	def _handleLayoutXSL(self,variant,id,xml,xsl):	# Deprecated!
		xslURL = xsl

		if True:	# Testing if 'SlfH' or 'FaaS' mode when available.
			xslURL = "data:text/xml;charset=utf-8," + _encode(_readXSLAsset(xsl))

		self._handleLayout(variant,id,xml,xslURL )

	def prependLayoutXSL(self,id,xml,xsl):	# Deprecated!
		self._handleLayoutXSL("Prepend",id,xml,xsl)

	prepend_layout_XSL = prependLayoutXSL	# Deprecated!

	def setLayoutXSL(self,id,xml,xsl):	# Deprecated!
		self._handleLayoutXSL("Set",id,xml,xsl)

	set_layout_XSL = setLayoutXSL	# Deprecated!

	def appendLayoutXSL(self,id,xml,xsl):	# Deprecated!
		self._handleLayoutXSL("Append",id,xml,xsl)

	append_layout_XSL = appendLayoutXSL	# Deprecated!

	def _layout(self,variant,id,xml,xsl):
		if xsl:
			xsl = "data:text/xml;charset=utf-8," + _encode(_readXSLAsset(xsl))

		self._dom.call("HandleLayout_1",_STRING,variant,id,xml if isinstance(xml,str) else xml.toString(),xsl)

	def before(self,id,xml,xsl=""):
		self._layout("beforebegin",id,xml,xsl)

	def begin(self,id,xml,xsl=""):
		self._layout("afterbegin",id,xml,xsl)

	def inner(self,id,xml,xsl=""):
		self._layout("inner",id,xml,xsl)

	def end(self,id,xml,xsl=""):
		self._layout("beforeend",id,xml,xsl)

	def after(self,id,xml,xsl=""):
		self._layout("afterend",id,xml,xsl)

	# Deprecated
	def getContents(self,ids):
		return _unsplit(ids,self._dom.call("GetContents_1",_STRINGS,ids))

	# Deprecated
	get_contents = getContents

	# Deprecated
	def getContent( self,id):
		return self.getContents([id])[id]

	# Deprecated
	get_content = getContent

	def getValues(self,ids):
		return _unsplit(ids,self._dom.call("GetValues_1",_STRINGS,ids))

	get_values = getValues

	def getValue( self,id):
		return self.get_values([id])[id]

	get_value =  getValue

	def getMarks(self,ids):
		return _unsplit(ids,self._dom.call("GetMarks_1",_STRINGS,ids))

	get_marks = getMarks

	def getMark( self,id):
		return self.get_marks([id])[id]

	get_mark = getMark

	# Deprecated
	def setContents(self,ids_and_contents):
		[ids,contents] = _split(ids_and_contents)

		self._dom.call("SetContents_1",_VOID,ids,contents)

	# Deprecated
	set_contents = setContents

	# Deprecated
	def setContent(self,id,content):
		self.set_contents({id: content})

	# Deprecated
	set_content = setContent

	def setValues(self,ids_and_values):
		[ids,values] = _split(ids_and_values)

		self._dom.call("SetValues_1",_VOID,ids,values)

	set_values = setValues

	def setValue(self,id,value):
		self.set_values({id: value})

	set_value = setValue

	def setMarks(self,ids_and_marks):
		[ids,marks] = _split(ids_and_marks)

		self._dom.call("SetMarks_1",_VOID,ids,marks)

	set_marks = setMarks

	def setMark(self,id,mark):
		self.set_marks({id: mark})

	set_mark = setMark

	def _handleClasses(self,variant,idsAndClasses):
		[ids,classes] = _split(idsAndClasses)

		self._dom.call("HandleClasses_1",_VOID,variant,ids,classes)

	def addClasses(self,ids_and_classes):
		self._handleClasses("Add",ids_and_classes)

	add_classes = addClasses

	def removeClasses(self,ids_and_classes):
		self._handleClasses("Remove",ids_and_classes)

	remove_classes = removeClasses		

	def toggleClasses(self,ids_and_classes):
		self._handleClasses("Toggle",ids_and_classes)

	toggle_classes = toggleClasses

	def addClass(self,id,clas ):
		self.addClasses({id: clas})

	add_class = addClass

	def removeClass(self,id,class_ ):
		self.removeClasses({id: class_})

	remove_class	= removeClass

	def toggleClass(self,id,clas ):
		self.toggleClasses({id: clas})

	toggle_class = toggleClass

	def enableElements(self,ids):
		self._dom.call("EnableElements_1",_VOID,ids )

	enable_elements = enableElements		

	def enableElement(self,id):
		self.enableElements([id] )

	enable_element = enableElement		

	def disableElements(self,ids):
		self._dom.call("DisableElements_1",_VOID,ids )

	disable_elements = disableElements		

	def disableElement(self,id):
		self.disableElements([id])

	disable_element = disableElement

	def setAttribute(self,id,name,value ):
		self._dom.call("SetAttribute_1",_VOID,id,name,str(value) )

	set_attribute = setAttribute		

	def getAttribute(self,id,name):
		return self._dom.call("GetAttribute_1",_STRING,id,name )

	get_attribute = getAttribute		

	def removeAttribute(self,id,name ):
		self._dom.call("RemoveAttribute_1",_VOID,id,name )

	remove_attribute = removeAttribute

	def setProperty(self,id,name,value ):
		self._dom.call("SetProperty_1",_VOID,id,name,value )

	set_property = setProperty		

	def getProperty(self,id,name ):
		return self._dom.call("GetProperty_1",_STRING,id,name )

	get_property = getProperty		

	def focus(self,id):
		self._dom.call("Focus_1",_VOID,id)

	def parent(self,id):
		return self._dom.call("Parent_1",_STRING,id)

	def firstChild(self,id):
		return self._dom.call("FirstChild_1",_STRING,id)

	first_child = firstChild

	def lastChild(self,id):
		return self._dom.call("LastChild_1",_STRING,id)

	last_child = lastChild

	def previousSibling(self,id):
		return self._dom.call("PreviousSibling_1",_STRING,id)

	previous_sibling = previousSibling		

	def nextSibling(self,id):
		return self._dom.call("NextSibling_1",_STRING,id)

	next_sibling = nextSibling

	def scrollTo(self,id):
		self._dom.call("ScrollTo_1",_VOID,id)

	scroll_to = scrollTo

	def debugLog(self,switch=True):
		self._dom.call("DebugLog_1",_VOID,"true" if switch else "false")

	def log(self,message):
		self._dom.call("Log_1",_VOID,message)
