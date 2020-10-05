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

import GPIOq, os, sys, threading

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("../../atlastk")

import atlastk

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

def getWId(pattern):
  return int(pattern[pattern.find('.')+1:])

class GPIO:
  def __init__(self):
    self._userId = getNewUserId()
    self._settings = {}
# 	setCurrentUserId(self._userId)	To early ! Must be done at connection !

  def _handleModeButtons(self,dom):
    global mapping
    enable = False
    buttons=[]

    for label in Mode.label:
      buttons.append(Mode.label[label])

    for key in mapping:
      if settings[key][Setting.SELECTED]:
        enable = True
        break

    if enable:
      dom.enable_elements(buttons)
    else:
      dom.disable_elements(buttons)

  def _getSetting(self,wId):
    global settings

    return settings[wId]

  def _getMode(self,wId):
    return self._getSetting(wId)[Setting.MODE]

  def _setMode(self,wId,mode):
    set(wId,Setting.MODE,mode)
    GPIOq.pinMode(wId,1 if mode > 1 else mode)
    if ( mode == Mode.PWM ):
      GPIOq.softPWMCreate(wId)
    set(wId,Setting.VALUE,GPIOq.digitalRead(wId))

  def _getValue(self,wId):
    value = self._getSetting(wId)[Setting.VALUE]

    if ( (value != 0) and (self._getMode(wId) != Mode.PWM) ):
      value = 100

    return value

  def _setValue(self,wId,value):
    set(wId,Setting.VALUE,value)
    mode = self._getMode(wId)
    if ( mode == Mode.IN ):
      sys.exit("Can not set value for a pin in IN mode !")
    elif (mode == Mode.OUT):
      GPIOq.digitalWrite( wId, 1 if value > 0 else 0 )
    elif (mode == Mode.PWM):
      GPIOq.softPWMWrite(wId,value)
    else:
      sys.exit("Unknown mode !")

  def _setSelected(self,wId,value):
    set(wId,Setting.SELECTED, not self._getSetting(wId)[Setting.SELECTED] if value == None else value )

  def _getModeLabel(self,wId):
    return Mode.label[self._getSetting(wId)[Setting.MODE]]

  def _getSelected(self,wId):
    return self._getSetting(wId)[Setting.SELECTED]

  def _buildModeCorpus(self,xml):
    xml.push_tag("Modes")

    for mode in Mode.label:
      xml.push_tag("Mode")
      xml.put_attribute("id", mode)
      xml.put_attribute("Label", Mode.label[mode])
      xml.pop_tag()

    xml.pop_tag()

  def _buildCorpus(self,xml):
    xml.push_tag( "Corpus")

    self._buildModeCorpus(xml)

    xml.pop_tag()

  def _buildXML(self):
    global mapping
    xml = atlastk.createXML("XDHTML")
    self._buildCorpus(xml)
    xml.push_tag("GPIOs")

    for wId in mapping:
      xml.push_tag("GPIO")
      xml.put_attribute( "id", wId)
      xml.put_attribute("Selected", self._getSelected(wId))
      xml.put_attribute("Mode",self._getMode(wId))
      xml.put_attribute("Value",self._getValue(wId))
      xml.pop_tag()

    xml.pop_tag()

    return xml

  def take(self):
    return setCurrentUserId(self._userId)

  def display(self,dom):
    dom.inner("GPIO", self._buildXML(), "GPIO.xsl")
    self._handleModeButtons(dom)

  def setMode(self,dom,wId,mode):
    id = "Value."+str(wId);

    self._setMode(wId, mode)

    dom.set_value("Value." + str(wId),self._getValue(wId))
    dom.setAttribute(id,"value",self._getValue(wId))

    if (mode==Mode.IN):
      dom.disable_element(id)
      dom.setAttribute(id,"step","100")
    elif (mode==Mode.OUT):
      dom.enable_element(id)
      dom.setAttribute(id,"step","100")
    elif (mode==Mode.PWM):
      dom.enable_element(id)
      dom.setAttribute(id,"step","1")
    else:
      sys.exit("???")

  def setValue(self,dom,wId,value):
    self._setValue(wId,value)

  def setSelected(self,dom,wId,value):
    self._setSelected(wId,value)
    self._handleModeButtons(dom)

  def setAllSelected(self,dom,value):
    global mapping

    for key in mapping:
      self._setSelected(int(key),value)

    self.display(dom)	

  def setAllMode(self,dom,mode):
    global mapping,settings

    for key in settings:
      if settings[key][Setting.SELECTED]:
        self._setMode(int(key),mode)

    self.display(dom)
  
def preProcess(GPIO,dom):
  if GPIO.take():
    return True
  else:
    dom.alert("Out of sync! Resynchronizing !")
    GPIO.display(dom)

def acConnect(GPIO,dom):
  dom.inner("", open( "Main.html").read() )
  GPIO.take()
  GPIO.display(dom)

def acSwitchMode(GPIO,dom,id):
  GPIO.setMode(dom,getWId(id),int(dom.get_value(id)))
  
def acChangeValue(GPIO,dom,id):
  GPIO.setValue(dom,getWId(id),int(dom.get_value(id)))

callbacks = {
    "_PreProcess": preProcess,
    "": acConnect,
    "SwitchMode": acSwitchMode,
    "ChangeValue": acChangeValue,
    "Toggle": lambda GPIO, dom, id: GPIO.setSelected(dom,getWId(id),None),
    "All": lambda GPIO, dom: GPIO.setAllSelected(dom, True),
    "None": lambda GPIO, dom: GPIO.setAllSelected(dom, False),
    "Invert": lambda GPIO, dom: GPIO.setAllSelected(dom, None),
    "IN": lambda GPIO, dom: GPIO.setAllMode(dom,Mode.IN),
    "OUT": lambda GPIO, dom: GPIO.setAllMode(dom,Mode.OUT),
    "PWM": lambda GPIO, dom: GPIO.setAllMode(dom,Mode.PWM),
  }

GPIOq.setup()

syncSettings()
    
atlastk.launch(callbacks, GPIO, open("Head.html").read())
