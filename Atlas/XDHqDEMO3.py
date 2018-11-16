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

def _getByte(socket):
	return ord(socket.recv(1))

def getSize(socket):
	byte = _getByte(socket)
	size = byte & 0x7f

	while byte & 0x80:
		byte = _getByte(socket)
		size = (size << 7) + byte & 0x7f

	return size

def getString(socket):
	size = getSize(socket)

	if size:
		return socket.recv(size).decode("utf-8")
	else:
		return ""


