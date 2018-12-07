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

import XDHqSHRD

import os, socket, sys

if sys.version_info[0] == 2:
	import XDHqDEMO2
	_writeSize = XDHqDEMO2.writeSize
	_writeString = XDHqDEMO2.writeString
	_writeStringNUL = XDHqDEMO2.writeStringNUL
	_getSize = XDHqDEMO2.getSize
	_getString = XDHqDEMO2.getString
elif sys.version_info[0] == 3:
	import XDHqDEMO3
	_writeSize = XDHqDEMO3.writeSize
	_writeString = XDHqDEMO3.writeString
	_writeStringNUL = XDHqDEMO3.writeStringNUL
	_getSize = XDHqDEMO3.getSize
	_getString = XDHqDEMO3.getString
else:
	print("Unhandled python version!")
	os._exit(1)

_protocolLabel = "3f0aef6b-b893-4ccd-9316-d468588fc572"
_protocolVersion = "0"

_newSessionAction = ""
_headContent = ""
_token = ""

def _getEnv( name, value= "" ):
	if name in os.environ:
		return os.environ[name].strip()
	else:
		return value.strip()

def launch(newSessionAction,headContent):
	global _newSessionAction,_headContent

	_newSessionAction = newSessionAction
	_headContent = headContent


class DOM_DEMO:
	_firstLaunch = True

	def _isTokenEmpty(this):
		global _token
		return not _token or _token[0] == "&"

	def _writeSize(this, size):
		_writeSize( this._socket, size )

	def _writeString(this, string):
		_writeString(this._socket, string)

	def _writeStrings(this, strings):
		this._writeSize(len(strings))

		for string in strings:
			this._writeString(string)

	def _getSize(this):
		return _getSize( this._socket)

	def _getString(this):
		return _getString(this._socket)

	def _getStrings(this):
		amount = this._getSize()
		strings = []

		while amount:
			strings.append(this._getString())
			amount -= 1

		return strings

	def __init__(this):
		global _protocolLabel, _protocolVersion, _newSessionAction,_headContent, _token
		pAddr = "atlastk.org"
		pPort = 53800
		wAddr = ""
		wPort = ""
		cgi = "xdh"

		atk = _getEnv("ATK")

		if atk == "DEV":
			pAddr = "localhost"
			wPort = "8080"
			print("\tDEV mode !")
		elif atk == "TEST":
			cgi = "xdh_"
			print("\tTEST mode!")
		elif atk:
			sys.exit("Bad 'ATK' environment variable value : should be 'DEV' or 'TEST' !")

		pAddr = _getEnv("ATK_PADDR", pAddr)
		pPort = int(_getEnv("ATK_PPORT", str(pPort)))
		wAddr = _getEnv("ATK_WADDR", wAddr)
		wPort = _getEnv("ATK_WPORT",wPort)

		if wAddr == "":
			wAddr = pAddr

		if wPort != "":
			wPort = ":" + wPort

		if this._isTokenEmpty():
			token = _getEnv("ATK_TOKEN")

			if token:
				_token = "&" + token
		
		this._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		this._socket.connect((pAddr,pPort))

		this._writeString(_token)

		if this._isTokenEmpty():
			this._writeString(_headContent)

			_token = this._getString()

			if this._isTokenEmpty():
				sys.exit("Invalid connection information !!!")

			if ( wPort != ":0" ):
				url = "http://" + wAddr + wPort + "/" + cgi + ".php?_token=" + _token

				print(url)
				print("Open above URL in a web browser. Enjoy!\n")
				XDHqSHRD.open(url)

		elif this._getString() != _token:
				sys.exit("Unmatched token !!!")

		this._writeString(_protocolLabel)
		this._writeString(_protocolVersion)

		errorMessage = this._getString()

		if ( errorMessage != "" ):
			sys.exit(errorMessage)

		this._getString()	# Language.
		this._writeString("PYH")

	def getAction(this):
		if this._firstLaunch:
			this._firstLaunch = False
		else:
			_writeStringNUL( this._socket, "StandBy_1")

		id = this._getString();
		action = this._getString()

		if not action:
			action = _newSessionAction

		return [action,id]

	def call(this, command, type, *args):
		i=0
		_writeStringNUL( this._socket, command )

		amount = args[i]
		i += 1

		while amount:
			this._writeString(args[i])
			i += 1
			amount -= 1

		amount = args[i]
		i += 1

		while amount:
			this._writeStrings(args[i])
			i += 1
			amount -= 1

		if type == XDHqSHRD.RT_STRING:
			return this._getString();
		elif type == XDHqSHRD.RT_STRINGS:
			return this._getStrings()
		elif type != XDHqSHRD.RT_VOID:
			sys.exit("Unknown return type !!!")

		
