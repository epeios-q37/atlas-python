import os, sys, threading, math

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.extend(("..","../../atlastk"))

import atlastk, ucuq

class Setting:
  MODE = 0
  VALUE = 1
  SELECTED = 2

class Mode:
  OUT = 0
  IN = 1
  PWM = 2
  label = {
    IN: "IN",
    OUT: "OUT",
    PWM: "PWM",
  }

lock = threading.Lock()

availableUserId = 0
currentUserId = None
settings = {}

mapping = {
  23 : {},
  22 : {},
  1 : {},
  3 : {},
  21 : {},
  19 : {},
  18 : {},
  5 : {},
  17 : {},
  16: {},
}

HEAD = """
<title>GPIO controler</title>
<link rel="icon" type="image/png" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgBAMAAACBVGfHAAAAMFBMVEUEAvyEhsxERuS8urQsKuycnsRkYtzc2qwUFvRUVtysrrx0ctTs6qTMyrSUksQ0NuyciPBdAAABHklEQVR42mNgwAa8zlxjDd2A4POfOXPmzZkFCAH2M8fNzyALzDlzg2ENssCbMwkMOsgCa858YOjBKxBzRoHhD7LAHiBH5swCT9HQ6A9ggZ4zp7YCrV0DdM6pBpAAG5Blc2aBDZA68wCsZPuZU0BDH07xvHOmAGKKvgMP2NA/Zw7ADIYJXGDgLQeBBSCBFu0aoAPYQUadMQAJAE29zwAVWMCWpgB08ZnDQGsbGhpsgCqBQHNfzRkDEIPlzFmo0T5nzoMovjPHoAK8Zw5BnA5yDosDSAVYQOYMKIDZzkoDzagAsjhqzjRAfXTmzAQgi/vMQZA6pjtAvhEk0E+ATWRRm6YBZuScCUCNN5szH1D4TGdOoSrggtiNAH3vBBjwAQCglIrSZkf1MQAAAABJRU5ErkJggg==" />
<style type="text/css">
 table, th, td {border: 1px solid black;}
</style>"""

BODY = """
<fieldset>
  <legend>GPIO</legend>
  <div id="GPIO"></div>
</fieldset>
"""


def getNewUserId():
  global availableUserId

  with lock:
    userId = availableUserId
    availableUserId += 1

  return userId

def setCurrentUserId(id):
  global currentUserId

  with lock:
    wasMe = currentUserId == id or currentUserId == None
    currentUserId = id

  return wasMe

def set(wId,field,value):
  global settings

  with lock:
    settings[wId][field] = value

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
  command = ""

  for key in mapping:
    settings[key] = retrieveSetting(key)
    command += f"PWM(Pin({key})).deinit()\nPin({key}, Pin.OUT).value(0)\n"
    # GPIOq.pinMode(key,Mode.IN)	# Default to IN mode, to avoid short-circuit.

  print(command)

  device.execute(command)

  return settings

def syncSettings():
  global settings

  with lock:
    settings = retrieveSettings()

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
      dom.enableElements(buttons)
    else:
      dom.disableElements(buttons)

  def _getSetting(self,wId):
    global settings

    return settings[wId]

  def _getMode(self,wId):
    return self._getSetting(wId)[Setting.MODE]

  def _setMode(self,wId,mode):
    set(wId,Setting.MODE,mode)
    device.execute(f"PWM(Pin({wId})).deinit()")
#    set(wId,Setting.VALUE,GPIOq.digitalRead(wId))

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
      device.execute(f"Pin({wId}, Pin.OUT).value({1 if value > 0 else 0})")
    elif (mode == Mode.PWM):
      v = int(1023 * (value / 100))
      v = int(1023 * (1 - math.cos(math.pi / 200 * value)))
      print(v)
      device.execute(f"PWM(Pin({wId})).duty({v})")
    else:
      sys.exit("Unknown mode !")

  def _setSelected(self,wId,value):
    set(wId,Setting.SELECTED, not self._getSetting(wId)[Setting.SELECTED] if value == None else value )

  def _getModeLabel(self,wId):
    return Mode.label[self._getSetting(wId)[Setting.MODE]]

  def _getSelected(self,wId):
    return self._getSetting(wId)[Setting.SELECTED]

  def _buildModeCorpus(self,xml):
    xml.pushTag("Modes")

    for mode in Mode.label:
      xml.pushTag("Mode")
      xml.putAttribute("id", mode)
      xml.putAttribute("Label", Mode.label[mode])
      xml.popTag()

    xml.popTag()

  def _buildCorpus(self,xml):
    xml.pushTag( "Corpus")

    self._buildModeCorpus(xml)

    xml.popTag()

  def _buildXML(self):
    global mapping
    xml = atlastk.createXML("XDHTML")
    self._buildCorpus(xml)
    xml.pushTag("GPIOs")

    for wId in mapping:
      xml.pushTag("GPIO")
      xml.putAttribute( "id", wId)
      xml.putAttribute("Selected", self._getSelected(wId))
      xml.putAttribute("Mode",self._getMode(wId))
      xml.putAttribute("Value",self._getValue(wId))
      xml.popTag()

    xml.popTag()

    return xml

  def take(self):
    return setCurrentUserId(self._userId)

  def display(self,dom):
    dom.inner("GPIO", self._buildXML(), "GPIO.xsl")
    self._handleModeButtons(dom)

  def setMode(self,dom,wId,mode):
    id = "Value."+str(wId)

    self._setMode(wId, mode)

    dom.setValue("Value." + str(wId),self._getValue(wId))
    dom.setAttribute(id,"value",self._getValue(wId))

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
  dom.inner("", BODY )
  GPIO.take()
  GPIO.display(dom)

def acSwitchMode(GPIO,dom,id):
  GPIO.setMode(dom,getWId(id),int(dom.getValue(id)))
  
def acChangeValue(GPIO,dom,id):
  GPIO.setValue(dom,getWId(id),int(dom.getValue(id)))

CALLBACKS = {
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

device = ucuq.UCUq("Red")

syncSettings()

atlastk.launch(CALLBACKS, GPIO, headContent=HEAD)
