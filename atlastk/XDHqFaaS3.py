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

import inspect

def l():
	frameInfo = inspect.getouterframes(inspect.currentframe())[1]
	print(frameInfo.filename + ":" + str(frameInfo.lineno))

def recv_(socket,size):
	buffer = bytes()
	l = 0

	while size != l:
		buffer += socket.recv(size-l)
		l = len(buffer)

	return buffer

def writeUInt(socket, value):
	result = bytes([value & 0x7f])
	value >>= 7

	while value != 0:
		result = bytes([(value & 0x7f) | 0x80]) + result
		value >>= 7

	socket.send(result)

def writeString(socket, string):
	bString = bytes(string, "utf-8")
	writeUInt(socket, len(bString))
	socket.send(bString)

def _readByte(socket):
	return ord(recv_(socket,1))

def readUInt(socket):
	byte = _readByte(socket)
	value = byte & 0x7f

	while byte & 0x80:
		byte = _readByte(socket)
		value = (value << 7) + (byte & 0x7f)

	return value

def getString(socket):
	size = readUInt(socket)

	if size:
		return recv_(socket, size).decode("utf-8")
	else:
		return ""


