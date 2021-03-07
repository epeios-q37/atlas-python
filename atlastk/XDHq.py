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
	# Dict are ordered by default under Python 3.
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

	def _execute(self,script,type):
		return self._dom.call("Execute_1" ,type,script)

	def execute_void(self,script):
		return self._dom.call("Execute_1" ,_VOID,script)

	def execute_string(self,script):
		return self._dom.call("Execute_1" ,_STRING,script)

	def execute_strings(self,script):
		return self._dom.call("Execute_1" ,_STRINGS,script)

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
		# 	If 'xml' is HTML and uses the compressed form, if it has a root tag,only the children will be used.
		self._dom.call("HandleLayout_1",_VOID,variant,id,xml if isinstance(xml,str) else xml.toString(),xsl)

	def prepend_layout(self,id,html):	# Deprecated!
		self._handleLayout("Prepend",id,html,"")

	prependLayout = prepend_layout	# Deprecated!

	def set_layout(self,id,html):	# Deprecated!
		self._handleLayout("Set",id,html,"")

	setLayout = set_layout	# Deprecated!

	def append_layout(self,id,html):	# Deprecated!
		self._handleLayout("Append",id,html,"")

	appendLayout = append_layout	# Deprecated!

	def _handleLayoutXSL(self,variant,id,xml,xsl):	# Deprecated!
		xslURL = xsl

		if True:	# Testing if 'SlfH' or 'FaaS' mode when available.
			xslURL = "data:text/xml;charset=utf-8," + _encode(_readXSLAsset(xsl))

		self._handleLayout(variant,id,xml,xslURL )

	def prepend_layout_XSL(self,id,xml,xsl):	# Deprecated!
		self._handleLayoutXSL("Prepend",id,xml,xsl)

	prependLayoutXSL = prepend_layout_XSL	# Deprecated!

	def set_layout_XSL(self,id,xml,xsl):	# Deprecated!
		self._handleLayoutXSL("Set",id,xml,xsl)

	setLayoutXSL = set_layout_XSL	# Deprecated!

	def append_layout_XSL(self,id,xml,xsl):	# Deprecated!
		self._handleLayoutXSL("Append",id,xml,xsl)

	appendLayoutXSL = append_layout_XSL	# Deprecated!

	def _layout(self,variant,id,xml,xsl):
		if xsl:
			xsl = "data:text/xml;charset=utf-8," + _encode(_readXSLAsset(xsl))

		self._dom.call("HandleLayout_1",_VOID,variant,id,xml if isinstance(xml,str) else xml.toString(),xsl)

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

	def get_contents(self,ids):	# Deprecated!
		return _unsplit(ids,self._dom.call("GetContents_1",_STRINGS,ids))

	getContents = get_contents	# Deprecated!

	def get_content( self,id):	# Deprecated!
		return self.getContents([id])[id]

	getContent = get_content	# Deprecated!

	def get_values(self,ids):
		return _unsplit(ids,self._dom.call("GetValues_1",_STRINGS,ids))

	def get_value( self,id):
		return self.get_values([id])[id]

	def get_marks(self,ids):
		return _unsplit(ids,self._dom.call("GetMarks_1",_STRINGS,ids))

	def get_mark( self,id):
		return self.get_marks([id])[id]

	def set_contents(self,ids_and_contents):	# Deprecated!
		[ids,contents] = _split(ids_and_contents)

		self._dom.call("SetContents_1",_VOID,ids,contents)

	setContents = set_contents	# Deprecated!

	def set_content(self,id,content):	# Deprecated!
		self.set_contents({id: content})

	setContent = set_content	# Deprecated!

	def set_values(self,ids_and_values):
		[ids,values] = _split(ids_and_values)

		self._dom.call("SetValues_1",_VOID,ids,values)

	def set_value(self,id,value):
		self.set_values({id: value})

	def set_marks(self,ids_and_marks):
		[ids,marks] = _split(ids_and_marks)

		self._dom.call("SetMarks_1",_VOID,ids,marks)

	def set_mark(self,id,mark):
		self.set_marks({id: mark})

	"""
	# Following 4 methods will either be removed or redesigned.

	# Will become a variation of 'createElementNS(…)',
	# with a optional list of attributes.
	def createElement(self,name,id = "" ):
		return self._dom.call( "CreateElement_1",_STRING,2,name,id,0 )

	# Will become 'prependChild(…)',with variations.
	def insertChild(self,child,id):
		self._dom.call( "InsertChild_1",_VOID,2,child,id,0 )

	# NOTA: The 'CSSRule' related methods will be probably removed.
	# Enabling/disabling styles are easier to use.
	def insertCSSRule(self,rule,index,id=""):
		self._dom.call("InsertCSSRule_1",_VOID,3,id,rule,str(index),0)

	def appendCSSRule(self,rule,id=""):
		return int(self._dom.call("AppendCSSRule_1",_STRING,2,id,rule,0))

	def removeCSSRule(self,index,id=""):
		self._dom.call("RemoveCSSRule_1",_VOID,2,id,str(index),0)
	"""

	def _handleClasses(self,variant,idsAndClasses):
		[ids,classes] = _split(idsAndClasses)

		self._dom.call("HandleClasses_1",_VOID,variant,ids,classes)

	def add_classes(self,ids_and_classes):
		self._handleClasses("Add",ids_and_classes)

	addClasses = add_classes

	def remove_classes(self,ids_and_classes):
		self._handleClasses("Remove",ids_and_classes)

	removeClasses = remove_classes		

	def toggle_classes(self,ids_and_classes):
		self._handleClasses("Toggle",ids_and_classes)

	toggleClasses = toggle_classes

	def add_class(self,id,clas ):
		self.addClasses({id: clas})

	addClass = add_class

	def remove_class(self,id,class_ ):
		self.removeClasses({id: class_})

	removeClass	= remove_class

	def toggle_class(self,id,clas ):
		self.toggleClasses({id: clas})

	toggleClass = toggle_class

	def enable_elements(self,ids):
		self._dom.call("EnableElements_1",_VOID,ids )

	enableElements = enable_elements		

	def enable_element(self,id):
		self.enableElements([id] )

	enableElement = enable_element		

	def disable_elements(self,ids):
		self._dom.call("DisableElements_1",_VOID,ids )

	disableElements = disable_elements		

	def disable_element(self,id):
		self.disableElements([id])

	disableElement = disable_element

	def set_attribute(self,id,name,value ):
		self._dom.call("SetAttribute_1",_VOID,id,name,str(value) )

	setAttribute = set_attribute		

	def get_attribute(self,id,name):
		return self._dom.call("GetAttribute_1",_STRING,id,name )

	getAttribute = get_attribute		

	def remove_attribute(self,id,name ):
		self._dom.call("RemoveAttribute_1",_VOID,id,name )

	removeAttribute = remove_attribute

	def set_property(self,id,name,value ):
		self._dom.call("SetProperty_1",_VOID,id,name,value )

	setProperty = set_property		

	def get_property(self,id,name ):
		return self._dom.call("GetProperty_1",_STRING,id,name )

	getProperty = get_property		

	def focus(self,id):
		self._dom.call("Focus_1",_VOID,id)

	def parent(self,id):
		return self._dom.call("Parent_1",_STRING,id)

	def first_child(self,id):
		return self._dom.call("FirstChild_1",_STRING,id)

	def last_child(self,id):
		return self._dom.call("LastChild_1",_STRING,id)

	def previous_sibling(self,id):
		return self._dom.call("PreviousSibling_1",_STRING,id)

	def next_sibling(self,id):
		return self._dom.call("NextSibling_1",_STRING,id)

	def scroll_to(self,id):
		self._dom.call("ScrollTo_1",_VOID,id)
