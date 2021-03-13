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
from XDHqSHRD import getEnv

import inspect, os, socket, sys, threading

if sys.version_info[0] == 2:
	import XDHqFaaS2
	l = XDHqFaaS2.l
	_writeUInt = XDHqFaaS2.writeUInt
	_writeString = XDHqFaaS2.writeString
	_readUInt = XDHqFaaS2.readUInt
	_getString = XDHqFaaS2.getString
else:
	import XDHqFaaS3
	l = XDHqFaaS3.l
	_writeUInt = XDHqFaaS3.writeUInt
	_writeString = XDHqFaaS3.writeString
	_readUInt = XDHqFaaS3.readUInt
	_getString = XDHqFaaS3.getString

_bye = False	# For use in Jupiter notbooks, to quit an application.

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

_FAAS_PROTOCOL_LABEL = "9efcf0d1-92a4-4e88-86bf-38ce18ca2894"
_FAAS_PROTOCOL_VERSION = "0"
_MAIN_PROTOCOL_LABEL = "bf077e9f-baca-48a1-bd3f-bf5181a78666"
_MAIN_PROTOCOL_VERSION = "0"

_writeLock = threading.Lock()
_globalCondition = threading.Condition()

_url = ""

class Instance:
	def __init__(self):
		self.condVar = threading.Condition()
		self.handshakeDone = False
		self.quit = False;
	def set(self,thread,id):
		self.thread = thread
		self.id = id
	def IsHandshakeDone(self):
		if self.handshakeDone:
			return True
		else:
			self.handshakeDone = True
			return False
	def getId(self):
		return self.id
	def wait(self):
		with self.condVar:
			self.condVar.wait()
	def signal(self):
		with self.condVar:
			self.condVar.notify()

def isTokenEmpty():
	return not _token or _token[0] == "&"

def writeUInt(value):
	global _socket
	_writeUInt( _socket, value )

def writeSInt(value):
	writeUInt( ( ( -value - 1 ) << 1 ) | 1 if value < 0 else value << 1 )

def writeString(string):
	global _socket
	_writeString(_socket, string)

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

def _init():
	global _token, _socket, _wAddr, _wPort, _cgi
	pAddr = "faas1.q37.info"
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

def _handshake():
	global _writeLock

	_writeLock.acquire()

	writeString(_FAAS_PROTOCOL_LABEL)
	writeString(_FAAS_PROTOCOL_VERSION)

	_writeLock.release()

	error = getString()

	if error:
		sys.exit(error)

	notification = getString()

	if notification:
		print(notification)

def _ignition():
	global _token, _url
	_writeLock.acquire()

	writeString( _token)
	writeString(_headContent)
	writeString(_wAddr);
	writeString("PYH")

	_writeLock.release()

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
	global _writeLock, _globalCondition
	while True:
		id = readSInt()
		
		if id == -1:	# Should never happen. 
			sys.exit("Received unexpected undefined command id!")
		if id == -2:    # Value reporting a new session.
			id = readSInt()  # The id of the new session.

			if id in _instances:
				sys.exit("Instance of id '" + str(id) + "' exists but should not !")

			instance = Instance()
			instance.set(callback(userCallback, callbacks, instance),id)
			_instances[id] = instance

			_writeLock.acquire()
			writeSInt(id)
			writeString(_MAIN_PROTOCOL_LABEL)
			writeString(_MAIN_PROTOCOL_VERSION)
			_writeLock.release()
		elif id == -3:	# Value instructing that a session is closed.
			id = readSInt();
			if not id in _instances:
				sys.exit("Instance of id '" + str(id) + "' not available for destruction!")
			_instances[id].quit = True
			_instances[id].signal();
			with _globalCondition:
				_globalCondition.wait()
			del _instances[id]	# Seemingly destroy the object and remove the entry too.
		elif not id in _instances:
			sys.exit("Unknown instance of id '" + str(id) + "'!")
		elif not _instances[id].IsHandshakeDone():
			error = getString()

			if error:
				sys.exit(error)

			getString()	# Language. Not handled yet.
		else:
			_instances[id].signal()

			with _globalCondition:
				_globalCondition.wait()

def launch(callback, userCallback,callbacks,headContent):
	global _headContent, _instances

	if headContent == None:
		if not "_headContent" in globals():
			_headContent = "" 
	else:
		_headContent = headContent
	
	_instances = {}

	_init()

	_handshake()

	_ignition()

	_serve(callback,userCallback,callbacks)

def get_app_url(id=""):
	return _url + ("&_id=" + id if id else "") 

def broadcastAction(action,id=""):
	_writeLock.acquire()
	writeSInt(-3)
	writeString(action)
	writeString(id)
	_writeLock.release()	

class DOM_FaaS:
	_firstLaunch = True

	def __init__(self, instance):
		self.instance = instance

	def wait(self):
		self.instance.wait()
		
	def signal(self):
		with _globalCondition:
			_globalCondition.notify()

	def _sendSpecialAction(self, action):
		_writeLock.acquire()
		writeSInt(self.instance.getId())
		writeString(action)
		_writeLock.release()

	def getAction(self):
		if self._firstLaunch:
			self._firstLaunch = False
		else:
			self._sendSpecialAction("#StandBy_1")

		self.wait()

		[id,action]=["",""] if self.instance.quit else [getString(),getString()]

		# The below 'is_quitting()' method MUST be called, or the library will hang. 

		return [action,id]

	def isQuitting(self):
		answer = self.instance.quit

		# Below line were in 'getAction()', but, in case of quitting,
		# 'self.instance' could already be destroyed here.
		self.signal()

		return answer;


	def call(self, command, type, *args):
		_writeLock.acquire()
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

		_writeLock.release()

		if type == XDHqSHRD.RT_STRING:
			self.wait()
			string = getString()
			self.signal()
			return string
		elif type == XDHqSHRD.RT_STRINGS:
			self.wait()
			strings = getStrings()
			self.signal()
			return strings
		elif type != XDHqSHRD.RT_VOID:
			sys.exit("Unknown return type !!!")

def setBye(value):
	global _bye

	_bye = value
