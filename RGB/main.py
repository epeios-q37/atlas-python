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

import GPIOq, sys

sys.path.append("./Atlas.python.zip")
sys.path.append("../Atlas.python.zip")
sys.path.append("./Atlas")

import Atlas

rPin = None
gPin = None
bPin = None

def readAsset(path):
	return Atlas.readAsset(path, "RGB")

class RGB:
	def __init__(this):
		pass

def set(dom, id, value):
	if value != None:
		dom.setContent(id, value)

def acConnect(RGB,dom,id):
	global rPin, gPin, bPin
	dom.setLayout("", readAsset( "Main.html") )
	set( dom, "Red", rPin)
	set( dom, "Green", gPin)
	set( dom, "Blue", bPin)
	dom.focus("Red")

def convert(hex):
	return int(int(hex,16) * 100 / 256)

def acSelect(RGB, dom, id):
	global rPin, gPin, bPin
	if ( ( rPin != None) and (gPin != None ) and ( bPin != None ) ):
		R = convert(id[0:2])
		G = convert(id[2:4])
		B = convert(id[4:6])
		print (R, G, B)
		GPIOq.softPWMWrite(rPin,100 - R)
		GPIOq.softPWMWrite(gPin,100 - G)
		GPIOq.softPWMWrite(bPin,100 - B)

def getPin(dom, id):
	pin = None
	value = dom.getContent(id).strip()

	try:
		pin = int(value)
		pin = None if ( pin > 99 ) or ( pin < 0 ) else pin
	except:
		pin = None

	if value  and ( pin == None ):
		dom.alert("Invalid pin number!")
		dom.setContent(id, "")
		dom.focus(id)
	elif pin != None:
		GPIOq.softPWMCreate(pin)

	return pin

def acRed(RGB, dom, id):
	global rPin
	rPin = getPin(dom, id)

def acGreen(RGB, dom, id):
	global gPin
	gPin = getPin(dom, id)

def acBlue(RGB, dom, id):
	global bPin
	bPin = getPin(dom, id)

callbacks = {
		"": acConnect,
		"Select": acSelect,
		"Red": acRed,
		"Green": acGreen,
		"Blue": acBlue,
	}

GPIOq.setup()

Atlas.launch(callbacks, RGB, readAsset("Head.html"), "RGB")
