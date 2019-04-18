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

def writeByte(socket, byte):
	socket.send(bytes([byte]))

def writeSize(socket, size):
	result = bytes([size & 0x7f])
	size >>= 7

	while size != 0:
		result = bytes([(size & 0x7f) | 0x80]) + result
		size >>= 7

	socket.send(result)

def writeString(socket, string):
	bString = bytes(string, "utf-8")
	writeSize(socket, len(bString))
	socket.send(bString)

def writeStringNUL(socket, string):
	socket.send(bytes(string + "\0", "utf-8"))

def getByte(socket):
	return ord(socket.recv(1))

def getSize(socket):
	byte = getByte(socket)
	size = byte & 0x7f

	while byte & 0x80:
		byte = getByte(socket)
		size = (size << 7) + (byte & 0x7f)

	return size

def getString(socket):
	size = getSize(socket)

	if size:
		return socket.recv(size).decode("utf-8")
	else:
		return ""


