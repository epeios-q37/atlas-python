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

_VERSION = "0.13.3"

import XDHqSHRD
from XDHqSHRD import getEnv

import inspect, os, socket, sys, threading, time

if sys.version_info[0] == 2:
	import XDHqFaaS2
	l = XDHqFaaS2.l
	_writeUInt = XDHqFaaS2.writeUInt
	_writeString = XDHqFaaS2.writeString
	_readUInt = XDHqFaaS2.readUInt
	_getString = XDHqFaaS2.getString
	_exitThread = XDHqFaaS2.exitThread
else:
	import XDHqFaaS3
	l = XDHqFaaS3.l
	_writeUInt = XDHqFaaS3.writeUInt
	_writeString = XDHqFaaS3.writeString
	_readUInt = XDHqFaaS3.readUInt
	_getString = XDHqFaaS3.getString
	_exitThread = XDHqFaaS3.exitThread

_bye = False	# For use in Jupiter notebooks, to quit an application.

_DEFAULT_SUPPLIER_LABEL = "auto"

class _Supplier:
	current = None

	_actions = {
		"none": lambda url : None,
		_DEFAULT_SUPPLIER_LABEL: XDHqSHRD.open,
		"qrcode": lambda url: XDHqSHRD.open( '"' + url + '&_supplier=qrcode"'),
		"jupyter": lambda url : None
	}

def _supply(url):
	supplier = getEnv("ATK").strip().lower() or _Supplier.current or _DEFAULT_SUPPLIER_LABEL

	while True:
		supplier = _Supplier._actions[supplier](url) if isinstance(supplier, str) else supplier(url)

		if not supplier:
			break;
			
def set_supplier(supplier = None):
	_Supplier.current = supplier

_FAAS_PROTOCOL_LABEL = "4c837d30-2eb5-41af-9b3d-6c8bf01d8dbf"
_FAAS_PROTOCOL_VERSION = "1"
_MAIN_PROTOCOL_LABEL = "22bb5d73-924f-473f-a68a-14f41d8bfa83"
_MAIN_PROTOCOL_VERSION = "0"
_SCRIPTS_VERSION = "0"

_FORBIDDEN_ID = -1
_CREATION_ID = -2
_CLOSING_ID = -3
_HEAD_RETRIEVING_ID = -4

_BROADCAST_ACTION_ID = -3
_HEAD_SENDING_ID = -4

_writeLock = threading.Lock()

_readLock = threading.Lock()	# Global read lock.
_readLock.acquire()


def _waitForInstance():
	_readLock.acquire()


def _instanceDataRead():
	_readLock.release()


_url = ""

class _Instance:
	def __init__(self,thread_retriever,id):
		# https://github.com/epeios-q37/atlas-python/pull/7 (Condition -> Lock)
		self._readLock = threading.Lock()	#Per instance read lock.
		self._readLock.acquire()
		self.quit = False
		self.id = id
		self.thread = thread_retriever(self)
		self.language = None
	def getId(self):
		return self.id
	def waitForData(self):
		self._readLock.acquire()
		if self.quit:
			_instanceDataRead()
			_exitThread()
	def dataAvailable(self):
		self._readLock.release()

def isTokenEmpty():
	return not _token or _token[0] == "&"

def writeUInt(value):
	global _socket
	_writeUInt( _socket, value, lambda: _bye )

def writeSInt(value):
	writeUInt( ( ( -value - 1 ) << 1 ) | 1 if value < 0 else value << 1 )

def writeString(string):
	global _socket
	_writeString(_socket, string, lambda: _bye)

def writeStrings(strings):
	writeUInt(len(strings))

	for string in strings:
		writeString(string)

def readUInt():
	global _socket
	return _readUInt( _socket, lambda: _bye)

def readSInt():
	value = readUInt()
	return -( ( value >> 1 ) + 1 ) if ( value & 1 ) else value >> 1

def getString():
	global _socket
	return _getString(_socket, lambda: _bye)

def getStrings():
	amount = readUInt()
	strings = []

	while amount:
		strings.append(getString())
		amount -= 1

	return strings

def _dismiss(id):
	with _writeLock:
		writeSInt(id)
		writeString("#Dismiss_1")

def _report(message):
	with _writeLock:
		writeSInt(-1)
		writeString("#Inform_1")
		writeString(message)

def _init():
	global _token, _socket, _wAddr, _wPort, _cgi
	pAddr = "faas.q37.info"
	pPort = 53700
	_token = ""
	_wAddr = ""
	_wPort = ""
	_cgi = "xdh"

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

	try:
		_socket.connect((pAddr,pPort))
	except:
		sys.exit("Unable to connect to '" + str(pAddr) + ":" + str(pPort) + "'!")
	else:
		print("Connected to '" + str(pAddr) + ":" + str(pPort) + "'.")

	_socket.settimeout(1)	# In order to quit an application, in Jupyter notebooks.		

def _handshakeFaaS():
	with _writeLock:
		writeString(_FAAS_PROTOCOL_LABEL)
		writeString(_FAAS_PROTOCOL_VERSION)
		writeString("PYH " + _VERSION)

	error = getString()

	if error:
		sys.exit(error)

	notification = getString()

	if notification:
		print(notification)

def _handshakeMain():
	with _writeLock:
		writeString(_MAIN_PROTOCOL_LABEL)
		writeString(_MAIN_PROTOCOL_VERSION)
		writeString(_SCRIPTS_VERSION)

	error = getString()

	if error:
		sys.exit(error)

	notification = getString();

	if notification:
		print(notification)

def _handshakes():
	_handshakeFaaS()
	_handshakeMain()

def _ignition():
	global _token, _url
	with _writeLock:
		writeString( _token)
#		writeString(_headContent)	# Dedicated call from proxy since protocol v1
		writeString(_wAddr)
		writeString("")	# Currently not used; for future use.

	_token = getString()

	if isTokenEmpty():
		sys.exit(getString())

	if ( _wPort != ":0" ):
		_url = getString()

		print(_url)
		print("".rjust(len(_url),'^'))
		print("Open above URL in a web browser (click, right click or copy/paste). Enjoy!\n")

		_supply(_url)

def _serve(callback,userCallback,callbacks ):
	while True:
		id = readSInt()
		
		if id == _FORBIDDEN_ID:	# Should never happen. 
			sys.exit("Received unexpected undefined command id!")
		if id == _CREATION_ID:    # Value reporting a new session.
			id = readSInt()  # The id of the new session.

			if id in _instances:
				_report("Instance of id '" + str(id) + "' exists but should not !")

			_instances[id] = _Instance(lambda instance : callback(userCallback, callbacks, instance), id)
		elif id == _CLOSING_ID:	# Value instructing that a session is closed.
			id = readSInt();

			if not id in _instances:
				_report("Instance of id '" + str(id) + "' not available for destruction!")
			else:
				instance = _instances.pop(id)
				instance.quit = True
				instance.dataAvailable()
				_waitForInstance()
				instance = None # Without this, instance will only be destroyed
												# when 'instance" is set to a new instance.
		elif id == _HEAD_RETRIEVING_ID:
			writeSInt(_HEAD_SENDING_ID)
			writeString(_headContent)
		elif not id in _instances:
			_report("Unknown instance of id '" + str(id) + "'!")
			_dismiss(id)
		else:
			instance = _instances[id]

			if instance.language is None:
				instance.language = getString()
			else:
				instance.dataAvailable()
				_waitForInstance()


def launch(callback, userCallback, callbacks, headContent):
	global _headContent, _instances

	if headContent is None:
		if not "_headContent" in globals():
			_headContent = "" 
	else:
		_headContent = headContent
	
	_instances = {}

	_init()

	_handshakes()

	_ignition()

	_serve(callback,userCallback,callbacks)

def get_app_url(id=""):
	return _url + ("&_id=" + str(id) if id else "") 

def broadcastAction(action, id = ""):
	with _writeLock:
		writeSInt(_BROADCAST_ACTION_ID)
		writeString(action)
		writeString(id)

class DOM_FaaS:
	_firstLaunch = True

	def __init__(self, instance):
		self.instance = instance

	def _waitForData(self):
		self.instance.waitForData()
		
	def _standBy(self):
		with _writeLock:
			writeSInt(self.instance.getId())
			writeString("#StandBy_1")

	def getAction(self):
		if self._firstLaunch:
			self._firstLaunch = False
		else:
			self._standBy()

		self._waitForData()

		[id,action] = [getString(),getString()]

		_instanceDataRead()

		return [action,id]

	def call(self, command, type, *args):
		if self.instance.quit:
			"""
			Below function unlocks the main thread,
			and exits the thread corresponding
			to the current instance.
			"""
			self._waitForData()

		with _writeLock:
			writeSInt(self.instance.getId())
			writeString(command)

			writeUInt(type)

			for arg in args:
				if isinstance(arg,str):
					writeUInt(XDHqSHRD.RT_STRING)
					writeString(arg)
				else:
					writeUInt(XDHqSHRD.RT_STRINGS)
					writeStrings(arg)

			writeUInt(XDHqSHRD.RT_VOID)	# To report end of argument list.

		if type == XDHqSHRD.RT_STRING:
			self._waitForData()
			string = getString()
			_instanceDataRead()
			return string
		elif type == XDHqSHRD.RT_STRINGS:
			self._waitForData()
			strings = getStrings()
			_instanceDataRead()
			return strings
		elif type != XDHqSHRD.RT_VOID:
			sys.exit("Unknown return type !!!")

def setBye(value):
	global _bye

	_bye = value
