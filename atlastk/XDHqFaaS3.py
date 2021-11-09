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

import inspect, sys, _thread, time
from socket import timeout 

def l():
	frameInfo = inspect.getouterframes(inspect.currentframe())[1]
	print( "(" + time.strftime("%X") + ") " + frameInfo.filename + ":" + str(frameInfo.lineno))

def _recv(socket,size,bye):
	buffer = bytes()
	l = 0

	while l != size:
		try:
			buffer += socket.recv(size-l)
		except timeout:
			if bye():
				raise timeout

		l = len(buffer)

	return buffer

def _send(socket, value, bye):
	totalAmount = len(value)
	amountSent = 0

	while amountSent < totalAmount:
		try:
			amountSent += socket.send(value[amountSent:])	
		except timeout:
			if bye():
				raise timeout

def writeUInt(socket, value, bye):
	result = bytes([value & 0x7f])
	value >>= 7

	while value != 0:
		result = bytes([(value & 0x7f) | 0x80]) + result
		value >>= 7

	_send(socket, result, bye)

def writeString(socket, string, bye):
	bString = bytes(string, "utf-8")
	writeUInt(socket, len(bString), bye)
	_send(socket, bString, bye)

def _readByte(socket,bye):
	return ord(_recv(socket,1, bye))

def readUInt(socket,bye):
	byte = _readByte(socket,bye)
	value = byte & 0x7f

	while byte & 0x80:
		byte = _readByte(socket,bye)
		value = (value << 7) + (byte & 0x7f)

	return value

def getString(socket,bye):
	size = readUInt(socket,bye)

	if size:
		return _recv(socket, size, bye).decode("utf-8")
	else:
		return ""

exitThread = _thread.exit

