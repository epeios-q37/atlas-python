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

import XDHqSHRD

import inspect, os, socket, sys, threading

if sys.version_info[0] == 2:
	import XDHqDEMO2
	l = XDHqDEMO2.l
	_writeByte = XDHqDEMO2.writeByte
	_writeSize = XDHqDEMO2.writeSize
	_writeString = XDHqDEMO2.writeString
	_writeStringNUL = XDHqDEMO2.writeStringNUL
	_getByte = XDHqDEMO2.getByte
	_getSize = XDHqDEMO2.getSize
	_getString = XDHqDEMO2.getString
elif sys.version_info[0] == 3:
	import XDHqDEMO3
	l = XDHqDEMO3.l
	_writeByte = XDHqDEMO3.writeByte
	_writeSize = XDHqDEMO3.writeSize
	_writeString = XDHqDEMO3.writeString
	_writeStringNUL = XDHqDEMO3.writeStringNUL
	_getByte = XDHqDEMO3.getByte
	_getSize = XDHqDEMO3.getSize
	_getString = XDHqDEMO3.getString
else:
	print("Unhandled python version!")
	os._exit(1)

_demoProtocolLabel = "877c913f-62df-40a1-bf5d-4bb5e66a6dd9"
_demoProtocolVersion = "0"
_mainProtocolLabel = "6e010737-31d8-4be3-9195-c5b5b2a9d5d9"
_mainProtocolVersion = "0"

_writeLock = threading.Lock()
_globalCondition = threading.Condition()

_headContent = ""
_token = ""
_instances = {}

class Instance:
	def __init__(this):
		this.condVar = threading.Condition()
		this.handshakeDone = False
	def set(this,thread,id):
		this.thread = thread
		this.id = id
	def IsHandshakeDone(this):
		if this.handshakeDone:
			return True
		else:
			this.handshakeDone = True
			return False
	def getId(this):
		return this.id
	def wait(this):
		with this.condVar:
			this.condVar.wait()
	def signal(this):
		with this.condVar:
			this.condVar.notify()

def isTokenEmpty():
	return not _token or _token[0] == "&"

def getEnv( name, value= "" ):
	if name in os.environ:
		return os.environ[name].strip()
	else:
		return value.strip()

def writeByte(byte):
	global _socket
	_writeByte( _socket, byte )

def writeSize(size):
	global _socket
	_writeSize( _socket, size )

def writeString(string):
	global _socket
	_writeString(_socket, string)

def writeStrings(strings):
	writeSize(len(strings))

	for string in strings:
		writeString(string)

def writeStringNUL(string):
	global _socket
	_writeStringNUL(_socket, string)

def getByte():
	global _socket
	return _getByte( _socket)

def getSize():
	global _socket
	return _getSize( _socket)

def getString():
	global _socket
	return _getString(_socket)

def getStrings():
	amount = getSize()
	strings = []

	while amount:
		strings.append(getString())
		amount -= 1

	return strings

def _init():
	global _token, _socket, _wAddr, _wPort, _cgi
	pAddr = "atlastk.org"
	pPort = 53800
	_wAddr = ""
	_wPort = ""
	_cgi = "xdh"

	atk = getEnv("ATK")

	if atk == "DEV":
		pAddr = "localhost"
		_wPort = "8080"
		print("\tDEV mode !")
	elif atk == "TEST":
		_cgi = "xdh_"
		print("\tTEST mode!")
	elif atk:
		sys.exit("Bad 'ATK' environment variable value : should be 'DEV' or 'TEST' !")

	pAddr = getEnv("ATK_PADDR", pAddr)
	pPort = int(getEnv("ATK_PPORT", str(pPort)))
	_wAddr = getEnv("ATK_WADDR", _wAddr)
	_wPort = getEnv("ATK_WPORT", _wPort)

	if _wAddr == "":
		_wAddr = pAddr

	if _wPort != "":
		_wPort = ":" + _wPort

	if isTokenEmpty():
		_token = getEnv("ATK_TOKEN")

	if _token:
		_token = "&" + _token

	_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Connection to '" + str(pAddr) + ":" + str(pPort) + "'...")
	_socket.connect((pAddr,pPort))

def _demoHandshake():
	global _writeLock

	_writeLock.acquire()

	writeString(_demoProtocolLabel)
	writeString(_demoProtocolVersion)

	_writeLock.release()

	error = getString()

	if error:
		sys.exit(error)

	notification = getString()

	if notification:
		print(notification)

def _ignition():
	global _token
	_writeLock.acquire()

	writeString( _token)
	writeString(_headContent)

	_writeLock.release()

	_token = getString()

	if isTokenEmpty():
		sys.exit(getString())

	if ( _wPort != ":0" ):
		url = "http://" + _wAddr + _wPort + "/" + _cgi + ".php?_token=" + _token

		print(url)
		print("".rjust(len(url),'^'))
		print("Open above URL in a web browser. Enjoy!\n")
		XDHqSHRD.open(url)

def _serve(callback, userCallback, callbacks ):
	global _writeLock, _globalCondition
	while True:

#		l()

		id = getByte()
		
		if id == 255:    # Value reporting a new front-end.
			id = getByte()  # The id of the new front-end.

			if id in _instances:
				sys.exit("Instance of id '" + id + "' exists but should not !")

			instance = Instance()
			instance.set(callback(userCallback(), callbacks, instance),id)
			_instances[id] = instance

			_writeLock.acquire()
			writeByte(id)
			writeString(_mainProtocolLabel)
			writeString(_mainProtocolVersion)
			_writeLock.release()

		elif not id in _instances:
			sys.exit("Unknown instance of id '" + str(id) + "'!")
		elif not _instances[id].IsHandshakeDone():
			error = getString()

			if error:
				sys.exit(error)

			getString()	# Language. Not handled yet.

			_writeLock.acquire()
			writeByte(id)
			writeString("PYH")
			_writeLock.release()
		else:
			_instances[id].signal()

			with _globalCondition:
				_globalCondition.wait()

def launch(callback, userCallback,callbacks,headContent):
	global _headContent

	_headContent = headContent

	_init()

	_demoHandshake()

	_ignition()

	_serve(callback, userCallback, callbacks)

class DOM_DEMO:
	_firstLaunch = True

	def __init__(this, instance):
		this.instance = instance
	def wait(this):
		this.instance.wait()
	def signal(this):
		with _globalCondition:
			_globalCondition.notify()
	def getAction(this):
		if this._firstLaunch:
			this._firstLaunch = False
		else:
			_writeLock.acquire()
			writeByte(this.instance.getId())
			writeStringNUL("StandBy_1")
			_writeLock.release()

		this.wait()

		id = getString();
		action = getString()

		this.signal()

		return [action,id]

	def call(this, command, type, *args):
		i=0

		_writeLock.acquire()
		writeByte(this.instance.getId())
		writeStringNUL(command )

		amount = args[i]
		i += 1

		while amount:
			writeString(args[i])
			i += 1
			amount -= 1

		amount = args[i]
		i += 1

		while amount:
			writeStrings(args[i])
			i += 1
			amount -= 1
		_writeLock.release()

		if type == XDHqSHRD.RT_STRING:
			this.wait()
			string = getString();
			this.signal()
			return string
		elif type == XDHqSHRD.RT_STRINGS:
			this.wait()
			strings = getStrings()
			this.signal()
			return strings
		elif type != XDHqSHRD.RT_VOID:
			sys.exit("Unknown return type !!!")