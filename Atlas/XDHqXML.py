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

class XML:
	def _write(this,value):
		this._xml += str(value) + "\0"

	def __init__(this,rootTag):
		this._xml = ""
		this._write("dummy")
		this._write(rootTag)

	def pushTag(this,tag):
		this._xml += ">"
		this._write(tag)

	def popTag(this):
		this._xml += "<"

	def setAttribute(this,name,value):
		this._xml += "A"
		this._write(name)
		this._write(str(value))

	def setValue(this,value):
		this._xml += "V"
		this._write(str(value))

	def toString(this):
		return this._xml
