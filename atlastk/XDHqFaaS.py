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
_readLock = threading.Event()


def waitForInstance():
	_readLock.wait()
	_readLock.clear()


def instanceDataRead():
	_readLock.set()


_url = ""

class Instance:
	def __init__(self):
		# https://github.com/epeios-q37/atlas-python/pull/7 (Condition -> Event)
		self._readLock = threading.Event()
		self.handshakeDone = False
		self.quit = False
	def __del__(self):
		_report("Inst.  #" + str(self.id) + " closed!")
	def set(self,thread,id):
		self.thread = thread
		self.id = id
	def IsHandshakeDone(self):
		if self.handshakeDone:
			return True

		self.handshakeDone = True
		return False
	def getId(self):
		return self.id
	def waitForData(self):
		self._readLock.wait()
		self._readLock.clear()
		if self.quit:
			instanceDataRead()
			_exitThread()
	def dataAvailable(self):
		self._readLock.set()

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
	with _writeLock:
		writeString(_FAAS_PROTOCOL_LABEL)
		writeString(_FAAS_PROTOCOL_VERSION)

	error = getString()

	if error:
		sys.exit(error)

	notification = getString()

	if notification:
		print(notification)

def _ignition():
	global _token, _url
	with _writeLock:
		writeString( _token)
		writeString(_headContent)
		writeString(_wAddr);
		writeString("PYH")

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
		
		if id == -1:	# Should never happen. 
			sys.exit("Received unexpected undefined command id!")
		if id == -2:    # Value reporting a new session.
			id = readSInt()  # The id of the new session.

			if id in _instances:
				_report("Instance of id '" + str(id) + "' exists but should not !")
			instance = Instance()
			instance.set(callback(userCallback, callbacks, instance),id)
			_instances[id] = instance

			with _writeLock:
				writeSInt(id)
				writeString(_MAIN_PROTOCOL_LABEL)
				writeString(_MAIN_PROTOCOL_VERSION)
		elif id == -3:	# Value instructing that a session is closed.
			id = readSInt();

			if not id in _instances:
				_report("Instance of id '" + str(id) + "' not available for destruction!")
			else:
				instance = _instances.pop(id)
				instance.quit = True
				instance.dataAvailable()
				waitForInstance()
				instance = None # Without this, instance will only be destroyed
												# when 'instance" is set to a new instance.
		elif not id in _instances:
			message = "Unknown instance of id '" + str(id) + "'!"
			print(message)
			_report(message)
			_dismiss(id)
		elif not _instances[id].IsHandshakeDone():
			error = getString()

			if error:
				sys.exit(error)

			getString()	# Language. Not handled yet.
		else:
			_instances[id].dataAvailable()
			waitForInstance()


def launch(callback, userCallback, callbacks, headContent):
	global _headContent, _instances

	if headContent is None:
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
	return _url + ("&_id=" + str(id) if id else "") 

def broadcastAction(action, id = ""):
	with _writeLock:
		writeSInt(-3)
		writeString(action)
		writeString(id)

class DOM_FaaS:
	_firstLaunch = True

	def __init__(self, instance):
		self.instance = instance

	def waitForData(self):
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

		self.waitForData()

		[id,action] = [getString(),getString()]

		instanceDataRead()

		return [action,id]

	def call(self, command, type, *args):
		if self.instance.quit:
			"""
			Below function unlocks the main thread,
			and exits the thread corresponding
			to the current instance.
			"""
			self.waitForData()

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
			self.waitForData()
			string = getString()
			instanceDataRead()
			return string
		elif type == XDHqSHRD.RT_STRINGS:
			self.waitForData()
			strings = getStrings()
			instanceDataRead()
			return strings
		elif type != XDHqSHRD.RT_VOID:
			sys.exit("Unknown return type !!!")

def setBye(value):
	global _bye

	_bye = value
