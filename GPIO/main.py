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

import os, pprint, sys, threading
import wiringpi

sys.path.append("./Atlas.python.zip")
sys.path.append("../Atlas.python.zip")
sys.path.append("./Atlas")

import Atlas

lock = threading.Lock()

availableUserId = 0
currentUserId = None
settings = {}

mappings = {
	"Odroid C2":
	{
		0: {},
		1: {},
		2: {},
		3: {},
		4: {},
		5: {},
		6: {},
		7: {},
# 8: {},
# 9: {},
		10: {},
		11: {},
		12: {},
		13: {},
		14: {},
#	15: {},
#	16: {},
		21: {},
		22: {},
		23: {},
		24: {},
#	25: {},
		26: {},
		27: {},
#	28: {},
#	29: {},
#	30: {},
#	31: {},
	}
}

mapping = mappings["Odroid C2"]

class Setting:
	MODE = 0
	VALUE = 1

class Mode:
	IN = 0
	OUT = 1
	PWM = 2
	label = {
		IN: "IN",
		OUT: "OUT",
		PWM: "PWM",
	}

def getNewUserId():
	global availableUserId, lock

	lock.acquire()

	userId = availableUserId
	availableUserId += 1

	lock.release()

	return userId

def setCurrentUserId(id):
	global currentUserId, lock

	lock.acquire()

	wasMe = currentUserId == id

	currentUserId = id

	lock.release()

	return wasMe

def set(userId,wId,field,value):
	global settings, lock
	if (setCurrentUserId(userId)):
		lock.acquire()
		settings[wId][field] = value
		lock.release()
		return True
	else:
		return False

def retrieveMode(wId):
	return 0

def retrieveValue(wId):
	return wiringpi.digitalRead(wId)

def retrieveSetting(wId):
	return {
		Setting.MODE: retrieveMode(wId),
		Setting.VALUE: retrieveValue(wId),
	}

def retrieveSettings():
	settings = {}

	for key in mapping:
		settings[key] = retrieveSetting(key)
		wiringpi.pinMode(key,0)	# Default to IN mode, to avoid short-circuit.

	return settings

def syncSettings():
	global settings, lock

	lock.acquire()

	settings = retrieveSettings()

	lock.release()

def readAsset(path):
	return Atlas.readAsset(path, "GPIO")

def getWId(pattern):
	return int(pattern[pattern.find('.')+1:])

class GPIO:
	def __init__(this):
		this._userId = getNewUserId()
		this._settings = {}
# 	setCurrentUserId(this._userId)	To early ! Must be done at connection !

	def _set(this,dom,field,wId,mode):
		if (not(set(this._userId, field, wId, mode))):
			dom.alert( "State externally modified: updating!")
			this.display(dom)
			return False
		else:
			return True

	def _getSetting(this,wId):
		global settings

		return settings[wId]

	def _getMode(this,wId):
		return this._getSetting(wId)[Setting.MODE]

	def _setMode(this,dom,wId,mode):
		if (this._set(dom,wId,Setting.MODE, mode)):
			wiringpi.pinMode(wId,1 if mode > 1 else mode)
			if ( mode == Mode.PWM ):
				wiringpi.softPwmCreate(wId,0,100)
			if ( this._set(dom,wId,Setting.VALUE,wiringpi.digitalRead(wId))):
				dom.setContent("Value." + str(wId),this._getValue(wId))
			return True
		else:
			return False

	def _getValue(this,wId):
		value = this._getSetting(wId)[Setting.VALUE]

		if ( (value != 0) and (this._getMode(wId) != Mode.PWM) ):
			value = 100

		return value

	def _setValue(this,dom,wId,value):
		if ( this._set(dom,wId,Setting.VALUE,value) ):
			mode = this._getMode(wId)
			if ( mode == Mode.IN ):
				sys.exit("Can not set value for a pin in IN mode !")
			elif (mode == Mode.OUT):
				wiringpi.digitalWrite( wId, 1 if value > 0 else 0 )
			elif (mode == Mode.PWM):
				wiringpi.softPwmWrite(wId,value)
			else:
				sys.exit("Unknown mode !")
			return True
		else:
			return False

	def _getModeLabel(this,wId):
		return Mode.label[this._getSetting(wId)[Setting.MODE]]

	def _buildModeCorpus(this,xml):
		xml.pushTag("Modes")

		for wId in Mode.label:
			xml.pushTag("Mode")
			xml.setAttribute("id", wId)
			xml.setAttribute("Label", Mode.label[wId])
			xml.popTag()

		xml.popTag()

	def _buildCorpus(this,xml):
		xml.pushTag( "Corpus")

		this._buildModeCorpus(xml)

		xml.popTag()

	def _buildXML(this):
		global mapping
		xml = Atlas.createXML("XDHTML")
		this._buildCorpus(xml)
		xml.pushTag("GPIOs")

		for wId in mapping:
			xml.pushTag("GPIO")
			xml.setAttribute( "id", wId)
			xml.setAttribute("Mode",this._getMode(wId))
			xml.setAttribute("Value",this._getValue(wId))
			xml.popTag()

		xml.popTag()

#		pprint.pprint(xml.toString())

		return xml

	def take(this):
		setCurrentUserId(this._userId)

	def display(this,dom):
		dom.setLayoutXSL("GPIO", this._buildXML(), "GPIO.xsl")

	def setMode(this,dom,wId,mode):
		id = "Value."+str(wId);

		if (this._setMode(dom,wId,mode)):
			dom.setAttribute(id,"value",this._getValue(wId))

			if (mode==Mode.IN):
				dom.disableElement(id)
				dom.setAttribute(id,"step","100")
			elif (mode==Mode.OUT):
				dom.enableElement(id)
				dom.setAttribute(id,"step","100")
			elif (mode==Mode.PWM):
				dom.enableElement(id)
				dom.setAttribute(id,"step","1")
			else:
				sys.exit("???")

	def setValue(this,dom,wId,value):
		if (this._setValue(dom,wId,value)):
			pass

def acConnect(GPIO,dom,id):
	dom.setLayout("", readAsset( "Main.html") )
	GPIO.take()
	GPIO.display(dom)

def acSwitchMode(GPIO,dom,id):
	GPIO.setMode(dom,getWId(id),int(dom.getContent(id)))
	
def acChangeValue(GPIO,dom,id):
	GPIO.setValue(dom,getWId(id),int(dom.getContent(id)))

callbacks = {
		"Connect": acConnect,
		"SwitchMode": acSwitchMode,
		"ChangeValue": acChangeValue,
	}

wiringpi.wiringPiSetup()

syncSettings()
		
Atlas.launch("Connect", callbacks, GPIO, readAsset("Head.html"), "GPIO")
