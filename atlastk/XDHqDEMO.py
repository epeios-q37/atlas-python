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
	from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer	# For 'repl.it'.
	import XDHqDEMO2
	l = XDHqDEMO2.l
	_writeByte = XDHqDEMO2.writeByte
	_writeSize = XDHqDEMO2.writeSize
	_writeString = XDHqDEMO2.writeString
	_writeStringNUL = XDHqDEMO2.writeStringNUL
	_getByte = XDHqDEMO2.getByte
	_getSize = XDHqDEMO2.getSize
	_getString = XDHqDEMO2.getString
	def _REPLit_convert(str):
		return str
elif sys.version_info[0] == 3:
	from http.server import BaseHTTPRequestHandler, HTTPServer	# For 'repl.it'.
	import XDHqDEMO3
	l = XDHqDEMO3.l
	_writeByte = XDHqDEMO3.writeByte
	_writeSize = XDHqDEMO3.writeSize
	_writeString = XDHqDEMO3.writeString
	_writeStringNUL = XDHqDEMO3.writeStringNUL
	_getByte = XDHqDEMO3.getByte
	_getSize = XDHqDEMO3.getSize
	_getString = XDHqDEMO3.getString
	def _REPLit_convert(str):
		return bytes(str,"utf-8")
else:
	print("Unhandled python version!")
	os._exit(1)

def _REPLHTML1(url):
	return "<html><body><iframe style=\"border-style: none; width: 100%;height: 100%\" src=\"" + url + "\"</iframe></body></html>"

def _REPLHTML2(url):
	return(
"""
<html>
	<head>
		<script src="https://atlastk.org/xdh/qrcode.min.js"></script>
		<script>
function genQRCode(url) {
"""
+ "\tnew QRCode('qrcode', {width:125, height:125, correctLevel: QRCode.CorrectLevel.L}).makeCode('" + url +"');" +
"""
}
		</script>
	</head>
"""
+ "\t<body onload=\"genQRCode('" + url + "')\">\n"
+
"""
		<div style="display:table; margin: 10px auto 5px auto;">
			<span style="display: table; margin: 15px auto 10px auto;font-style: oblique;">Click or scan this QR code:</span>
			<div style="display: flex; justify-content: space-around;">
"""
+ "\t\t\t\t<a target=\"_blank\" href=\"" + url + "\" alt=\"" + url + "\">" +
"""
 					<div id="qrcode"></div>
				</a>
			</div>
		</div>
	</body>
</html>
"""
)

def _REPLHTML3(url):
	return "<html><body><iframe style=\"border-style: none; width: 100%;height: 100%\" src=\"https://atlastk.org/repl_it.php?url=" + url + "\"</iframe></body></html>"

class _REPLit_class(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(_REPLit_convert(_REPLHTML3(globals()['_REPLit_url'])))

def _REPLit(url):
    global _REPLit_url
    _REPLit_url = url
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, _REPLit_class)
    httpd.handle_request()

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
	def __init__(self):
		self.condVar = threading.Condition()
		self.handshakeDone = False
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
	elif atk == "REPLit":
		pass
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
		if ( getEnv("ATK") == "REPLit"):
#			print("IF THE PROGRAM DOES NOT WORK PROPERLY, PLEASE SEE http://q37.info/s/zbgfjtp9")
			print("IF THE PROGRAM DOES NOT WORK PROPERLY, YOU PROBABLY FORGOT TO FORK!")
			print("IF IT STILL DOES NOT WORK AFTER FORKING, RELOAD THE COMPLETE PAGE!")
			print( "See http://q37.info/s/zbgfjtp9 for more details.\n")
			_REPLit(url)
		else:
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
			instance.set(callback(userCallback, callbacks, instance),id)
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

	def __init__(self, instance):
		self.instance = instance
	def wait(self):
		self.instance.wait()
	def signal(self):
		with _globalCondition:
			_globalCondition.notify()
	def getAction(self):
		if self._firstLaunch:
			self._firstLaunch = False
		else:
			_writeLock.acquire()
			writeByte(self.instance.getId())
			writeStringNUL("StandBy_1")
			_writeLock.release()

		self.wait()

		id = getString()
		action = getString()

		self.signal()

		return [action,id]

	def call(self, command, type, *args):
		i=0

		_writeLock.acquire()
		writeByte(self.instance.getId())
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