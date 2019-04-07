""" 
 Copyright (C) 2018 Claude SIMON (http://q37.info/contact/).

	This file is part of XDHq.

	XDHq is free software: you can redistribute it and/or
	modify it under the terms of the GNU Affero General Public License as
	published by the Free Software Foundation, either version 3 of the
	License, or (at your option) any later version.

	XDHq is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
	Affero General Public License for more details.

	You should have received a copy of the GNU Affero General Public License
	along with XDHq If not, see <http://www.gnu.org/licenses/>.
 """

import XDHqDEMO, XDHqSHRD, XDHqXML

import os, sys

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

_dir = ""

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
	keysAndValues = {}
	length = len(keys)

	while i < length:
		keysAndValues[keys[i]] = values[i]
		i += 1

	return keysAndValues

def _getAssetPath(dir):
	if XDHqSHRD.isDev():
		return os.path.join("/cygdrive/h/hg/epeios/tools/xdhq/examples/common/", dir )
	else:
		return os.path.realpath(sys.path[0])

def _getAssetFilename(path, dir):
	return os.path.join(_getAssetPath(dir), path )

def readAsset(path, dir=""):
	return open(_getAssetFilename(path, dir)).read()

class DOM:
	def __init__(this,instance):
		this._dom = XDHqDEMO.DOM_DEMO(instance)

	def getAction(this):
		return this._dom.getAction()

	def execute(this,script):
		return this._dom.call("Execute_1" ,_STRING, 1, script, 0)

	def alert(this,message):
		this._dom.call( "Alert_1", _STRING, 1, message, 0 )
		# For the return value being 'STRING' instead of 'VOID',
		# see the 'alert' primitive in 'XDHqXDH'.

	def confirm(this,message):
		return this._dom.call( "Confirm_1", _STRING, 1, message, 0 ) == "true"

	def _setLayout(this, id, xml, xslFilename):
		this._dom.call("SetLayout_1", _VOID, 3, id, xml, xslFilename, 0)

	def setLayout(this,id,html):
		this._setLayout(id,html,"")

	def setLayoutXSL(this, id, xml, xsl ):
		global _dir
		xslURL = xsl

		if True:	# Testing if 'PROD' or 'DEMO' mode when available.
			xslURL = "data:text/xml;charset=utf-8," + _encode( readAsset( xsl, _dir ) )

		this._setLayout( id, xml if type(xml) == "str" else xml.toString(), xslURL )

	def getContents(this, ids):
		return _unsplit(ids,this._dom.call("GetContents_1",_STRINGS, 0, 1, ids))

	def getContent( this, id):
		return this.getContents([id])[id]

	def setContents(this,idsAndContents):
		[ids,contents] = _split(idsAndContents)

		this._dom.call("SetContents_1", _VOID, 0, 2, ids, contents)

	def setContent(this, id, content):
		this.setContents({id: content})

	def setTimeout(this,delay,action ):
		this._dom.call( "SetTimeout_1", _VOID, 2, str( delay ), action, 0 )

	def createElement(this, name, id = "" ):
		return this._dom.call( "CreateElement_1", _STRING, 2, name, id, 0 )

	def insertChild(this,child, id):
		this._dom.call( "InsertChild_1", _VOID, 2, child, id, 0 );

	def dressWidgets(this,id):
		return this._dom.call( "DressWidgets_1", _VOID, 1, id, 0 );

	def _handleClasses(this, command, idsAndClasses):
		[ids, classes] = _split(idsAndClasses)

		this._dom.call(command, _VOID, 0, 2, ids, classes)

	def addClasses(this, idsAndClasses):
		this._handleClasses("AddClasses_1", idsAndClasses)

	def removeClasses(this, idsAndClasses):
		this._handleClasses("RemoveClasses_1", idsAndClasses)

	def toggleClasses(this, idsAndClasses):
		this._handleClasses("ToggleClasses_1", idsAndClasses)

	def addClass(this, id, clas ):
		this.addClasses({id: clas})

	def removeClass(this, id, clas ):
		this.removeClasses({id: clas})

	def toggleClass(this, id, clas ):
		this.toggleClasses({id: clas})

	def enableElements(this,ids):
		this._dom.call("EnableElements_1", _VOID, 0, 1, ids )

	def enableElement(this, id):
		this.enableElements([id] )

	def disableElements(this, ids):
		this._dom.call("DisableElements_1", _VOID, 0, 1, ids )

	def disableElement(this, id):
		this.disableElements([id])

	def setAttribute(this, id, name, value ):
		this._dom.call("SetAttribute_1", _VOID, 3, id, name, str(value), 0 )

	def getAttribute(this, id, name):
		return this._dom.call("GetAttribute_1", _STRING, 2, id, name, 0 )

	def removeAttribute(this, id, name ):
		this._dom.call("RemoveAttribute_1", _VOID, 2, id, name, 0 )

	def setProperty(this, id, name, value ):
		this._dom.call("SetProperty_1", _VOID, 3, id, name, value, 0 )

	def getProperty(this, id, name ):
		return this._dom.call("GetProperty_1", _STRING, 2, id, name, 0 );

	def focus(this, id):
		this._dom.call("Focus_1", _VOID,1, id, 0)

def launch(callback, userCallback, callbacks, headContent, dir):
	global _dir
	_dir = dir
	XDHqDEMO.launch(callback, userCallback,callbacks,headContent)
