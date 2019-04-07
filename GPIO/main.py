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

import GPIOq, sys, threading

sys.path.append("./Atlas.python.zip")
sys.path.append("../Atlas.python.zip")
sys.path.append("./Atlas")

import atlastk as Atlas

lock = threading.Lock()

availableUserId = 0
currentUserId = None
settings = {}

mappings = {
	GPIOq.D_ODROID_C2:
	sorted({
#		1: {},
#		2: {},
		3: {},
#		4: {},
		5: {},
#		6: {},
		7: {},
#		8: {},
#		9: {},
#		10: {},
		11: {},
		12: {},
		13: {},
#		14: {},
		15: {},
		16: {},
#		17: {},
		18: {},
		19: {},
#		20: {},
		21: {},
		22: {},
		23: {},
		24: {},
#		25: {},
		26: {},
#		27: {},
#		28: {},
		29: {},
#		30: {},
		31: {},
		32: {},
		33: {},
#		34: {},
		35: {},
		36: {},
#		37: {},
#		38: {},
#		39: {},
#		40: {},
	}),
	GPIOq.D_RASPBERRY_PI:
	sorted({
#		1: {},
#		2: {},
		3: {},
#		4: {},
		5: {},
#		6: {},
		7: {},
		8: {},
#		9: {},
		10: {},
		11: {},
		12: {},
		13: {},
#		14: {},
		15: {},
		16: {},
#		17: {},
		18: {},
		19: {},
#		20: {},
		21: {},
		22: {},
		23: {},
		24: {},
#		25: {},
		26: {},
#		27: {},
#		28: {},
		29: {},
#		30: {},
		31: {},
		32: {},
		33: {},
#		34: {},
		35: {},
		36: {},
		37: {},
		38: {},
#		39: {},
		40: {},
	}),
}

mappings[GPIOq.D_TESTING] = mappings[GPIOq.D_ODROID_C2]

mapping = mappings[GPIOq.device]

class Setting:
	MODE = 0
	VALUE = 1
	SELECTED = 2

class Mode:
	IN = GPIOq.M_IN
	OUT = GPIOq.M_OUT
	PWM = GPIOq.M_PWM
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
	wasMe = currentUserId == id or currentUserId == None
	currentUserId = id
	lock.release()

	return wasMe

def set(wId,field,value):
	global settings, lock
	lock.acquire()
	settings[wId][field] = value
	lock.release()

def retrieveMode(wId):
	return Mode.IN

def retrieveValue(wId):
	return 0

def retrieveSelected(wId):
	return False

def retrieveSetting(wId):
	return {
		Setting.MODE: retrieveMode(wId),
		Setting.VALUE: retrieveValue(wId),
		Setting.SELECTED: retrieveSelected(wId),
	}

def retrieveSettings():
	settings = {}

	for key in mapping:
		settings[key] = retrieveSetting(key)
		GPIOq.pinMode(key,Mode.IN)	# Default to IN mode, to avoid short-circuit.

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

	def _handleModeButtons(this,dom):
		global mapping
		enable = False;
		buttons=[]

		for label in Mode.label:
			buttons.append(Mode.label[label])

		for key in mapping:
			if settings[key][Setting.SELECTED]:
				enable = True
				break

		if enable:
			dom.enableElements(buttons)
		else:
			dom.disableElements(buttons)

	def _getSetting(this,wId):
		global settings

		return settings[wId]

	def _getMode(this,wId):
		return this._getSetting(wId)[Setting.MODE]

	def _setMode(this,wId,mode):
		set(wId,Setting.MODE,mode)
		GPIOq.pinMode(wId,1 if mode > 1 else mode)
		if ( mode == Mode.PWM ):
			GPIOq.softPWMCreate(wId)
		set(wId,Setting.VALUE,GPIOq.digitalRead(wId))

	def _getValue(this,wId):
		value = this._getSetting(wId)[Setting.VALUE]

		if ( (value != 0) and (this._getMode(wId) != Mode.PWM) ):
			value = 100

		return value

	def _setValue(this,wId,value):
		set(wId,Setting.VALUE,value)
		mode = this._getMode(wId)
		if ( mode == Mode.IN ):
			sys.exit("Can not set value for a pin in IN mode !")
		elif (mode == Mode.OUT):
			GPIOq.digitalWrite( wId, 1 if value > 0 else 0 )
		elif (mode == Mode.PWM):
			GPIOq.softPWMWrite(wId,value)
		else:
			sys.exit("Unknown mode !")

	def _setSelected(this,wId,value):
		set(wId,Setting.SELECTED, not this._getSetting(wId)[Setting.SELECTED] if value == None else value )

	def _getModeLabel(this,wId):
		return Mode.label[this._getSetting(wId)[Setting.MODE]]

	def _getSelected(this,wId):
		return this._getSetting(wId)[Setting.SELECTED]

	def _buildModeCorpus(this,xml):
		xml.pushTag("Modes")

		for mode in Mode.label:
			xml.pushTag("Mode")
			xml.setAttribute("id", mode)
			xml.setAttribute("Label", Mode.label[mode])
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
			xml.setAttribute("Selected", this._getSelected(wId))
			xml.setAttribute("Mode",this._getMode(wId))
			xml.setAttribute("Value",this._getValue(wId))
			xml.popTag()

		xml.popTag()

		return xml

	def take(this):
		return setCurrentUserId(this._userId)

	def display(this,dom):
		dom.setLayoutXSL("GPIO", this._buildXML(), "GPIO.xsl")
		this._handleModeButtons(dom)

	def setMode(this,dom,wId,mode):
		id = "Value."+str(wId);

		this._setMode(wId, mode)

		dom.setContent("Value." + str(wId),this._getValue(wId))
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
		this._setValue(wId,value)

	def setSelected(this,dom,wId,value):
		this._setSelected(wId,value)
		this._handleModeButtons(dom)

	def setAllSelected(this,dom,value):
		global mapping

		for key in mapping:
			this._setSelected(int(key),value)

		this.display(dom)	

	def setAllMode(this,dom,mode):
		global mapping,settings

		for key in settings:
			if settings[key][Setting.SELECTED]:
				this._setMode(int(key),mode)

		this.display(dom)
	
def preProcessing(GPIO,dom,action,id):
	if GPIO.take():
		return True
	else:
		dom.alert("Out of sync! Resynchronizing !")
		GPIO.display(dom)

def acConnect(GPIO,dom,id):
	dom.setLayout("", readAsset( "Main.html") )
	GPIO.take()
	GPIO.display(dom)

def acSwitchMode(GPIO,dom,id):
	GPIO.setMode(dom,getWId(id),int(dom.getContent(id)))
	
def acChangeValue(GPIO,dom,id):
	GPIO.setValue(dom,getWId(id),int(dom.getContent(id)))

callbacks = {
		"_PreProcessing": preProcessing,
		"": acConnect,
		"SwitchMode": acSwitchMode,
		"ChangeValue": acChangeValue,
		"Toggle": lambda GPIO, dom, id: GPIO.setSelected(dom,getWId(id),None),
		"All": lambda GPIO, dom, id: GPIO.setAllSelected(dom, True),
		"None": lambda GPIO, dom, id: GPIO.setAllSelected(dom, False),
		"Invert": lambda GPIO, dom, id: GPIO.setAllSelected(dom, None),
		"IN": lambda GPIO, dom, id: GPIO.setAllMode(dom,Mode.IN),
		"OUT": lambda GPIO, dom, id: GPIO.setAllMode(dom,Mode.OUT),
		"PWM": lambda GPIO, dom, id: GPIO.setAllMode(dom,Mode.PWM),
	}

GPIOq.setup()

syncSettings()
		
Atlas.launch(callbacks, GPIO, readAsset("Head.html"), "GPIO")
