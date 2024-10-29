import os, sys, time, io, json, datetime

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.extend(("..","../../atlastk"))

import ucuq, atlastk

pwm = None

onDuty = False

# Duties
D_RATIO = "Ratio"
D_WIDTH = "Width"

# Inputs
I_MODE_BOX = "ModeBox"
I_MODE = "Mode"
I_PIN = "Pin"
I_SDA = "SDA"
I_SCL = "SCL"
I_DRIVER = "Driver"
I_FREQ = "Freq"
I_DUTY = "Duty"
I_RATIO = "Ratio"
I_RATIO_STEP = "RatioStep"
I_WIDTH = "Width"

# Modes
M_STRAIGHT = "Straight"
M_PCA9685 = "PCA9685"

# Outputs
O_FREQ = "TrueFreq"
O_RATIO = "TrueRatio"
O_WIDTH = "TrueWidth"


MC_INIT = """
def getParams(pwm):
  return [pwm.freq(), pwm.duty_u16(), pwm.duty_ns()]
"""

with open('Body.html', 'r') as file:
  BODY = file.read()

with open('Head.html', 'r') as file:
  HEAD = file.read()


def getParams():
  return device.execute("", f"getParams({pwm.getObject()})") if onDuty else None


def getDuty(dom):
  if not ( duty:= dom.getValue("Duty") ) in [D_RATIO, D_WIDTH]:
    raise Exception ("Bad duty value!!!")
  
  return duty


def convert(value, converter):
  try:
    value = converter(value)
  except:
    return None
  else:
    return value


def getInputs(dom):
  values = dom.getValues([I_MODE, I_PIN, I_SDA, I_SCL, I_DRIVER, I_FREQ, I_DUTY, I_RATIO, I_WIDTH])

  return {
    I_MODE: values[I_MODE],
    I_PIN: convert(values[I_PIN], int),
    I_SDA: convert(values[I_SDA], int),
    I_SCL: convert(values[I_SCL], int),
    I_DRIVER: convert(values[I_DRIVER], int),
    I_FREQ: convert(values[I_FREQ], int),
    I_DUTY: {
      "Type": values[I_DUTY],
      "Value": convert(values[I_RATIO], int) if values[I_DUTY] == D_RATIO else convert(values[I_WIDTH], float)
    } 
  }


def test(dom, inputs):
  error = True

  if inputs[I_MODE] == "":
    dom.alert("Please select a mode!")
  elif inputs[I_MODE] == M_STRAIGHT:
    if inputs[I_PIN] == None:
      dom.alert("Bad or no pin value!")
    else:
      error = False
  elif inputs[I_MODE] == M_PCA9685:
    if inputs[I_SCL] == None:
      dom.alert("No or bad SCL value!")
    elif inputs[I_SDA]== None:
      dom.alert("No or bad SDA value!")
    elif inputs[I_DRIVER] == None:
      dom.alert("No or bad Driver value!")
    else:
      error = False
  else:
    raise Exception("Unknown mode!!!")
  
  
  if error:
    return False
  
  error = True

  if inputs[I_FREQ] ==  None:
    dom.alert("Bad or no freq. value!")
  elif inputs[I_DUTY]["Type"] == D_RATIO:
    if inputs[I_DUTY]["Value"] == None:
      dom.alert("Bad or no ratio value!")
    else:
      error = False
  elif inputs[I_DUTY]["Type"] == D_WIDTH:
    if inputs[I_DUTY]["Value"] == None:
      dom.alert("Bad or no width value!")
    else:
      error = False
  else:
    raise Exception("Unknown duty type!!!")
  
  return not error


def updateDutyBox(dom, params = None):
# 'params = getParams()' does not work as 'getParams()' is only called
# at function definition and not at calling.
  if params == None:
    params = getParams()

  match getDuty(dom):
    case "Ratio":
      dom.enableElement(I_RATIO)
      dom.disableElement(I_WIDTH)
      if onDuty:
        dom.setValues({
        I_WIDTH: "",
        I_RATIO: params[1] if onDuty else ""})
    case "Width":
      dom.enableElement("Width")
      dom.disableElement("Ratio")
      dom.setValues({
        I_RATIO: "",
        I_WIDTH: params[2]/1000000 if onDuty else ""})
    case _:
      raise Exception("!!!")
    

def updateDuties(dom, params = None):
  if params == None:
    params = getParams()

  if params != None:
    dom.setValues({
      O_FREQ: params[0],
      O_RATIO: params[1],
      O_WIDTH: params[2]/1000000
    })
  else:
    dom.setValues({
      O_FREQ: "N/A",
      O_RATIO: "N/A",
      O_WIDTH: "N/A",
    })



def initPWM(inputs):
  global pwm
  
  if inputs["Mode"] == M_STRAIGHT:
    pwm = ucuq.PWM(device, inputs[I_PIN], inputs[I_FREQ])
  elif inputs["Mode"] == M_PCA9685:
    pwm = ucuq.PCA9685Channel(device, ucuq.PCA9685(device, inputs[I_SDA], inputs[I_SCL], inputs[I_FREQ]), inputs[I_DRIVER],)
  else:
    raise Exception("Unknown mode!!!")

  if inputs[I_DUTY]["Type"] == D_RATIO:
    pwm.duty_u16(int(inputs[I_DUTY]["Value"]))
  else:
    pwm.duty_ns(int(1000000 * float(inputs[I_DUTY]["Value"])))
  
  return device.render(f"getParams({pwm.getObject()})")
  

def setFreq(freq):
  pwm.freq(freq)
  return device.render(f"getParams({pwm.getObject()})")
  

def setRatio(ratio):
  pwm.duty_u16(ratio)
  return device.render(f"getParams({pwm.getObject()})")
  

def setWidth(width):
  pwm.duty_ns(width)
  return device.render(f"getParams({pwm.getObject()})")
  

def acConnect(dom):
  dom.inner("", BODY)
  updateDutyBox(dom)


def acMode(dom, id):
  match dom.getValue(id):
    case "Straight":
      dom.disableElement("HideStraight")
      dom.enableElement("HidePCA9685")
    case "PCA9685":
      dom.enableElement("HideStraight")
      dom.disableElement("HidePCA9685")
    case _:
      raise Exception("Unknown mode!")
  
  
def acSwitch(dom, id):
  global onDuty

  if dom.getValue(id) == "true":
    inputs = getInputs(dom)

    if not test(dom, inputs):
      dom.setValue(id, False)
    else:
      dom.disableElement(I_MODE_BOX)
      updateDuties(dom, initPWM(inputs))
      onDuty = True
  else:
    if onDuty:
      pwm.deinit()
      device.render()
      onDuty = False
    updateDuties(dom)
    dom.enableElement(I_MODE_BOX)


def acSelect(dom):
  updateDutyBox(dom)


def acFreq(dom, id):
  if onDuty:
    value = dom.getValue(id)

    try:
      freq = int(value)
    except:
      pass
    else:
      updateDuties(dom, setFreq(freq))


def acRatio(dom, id):
  if onDuty:
    value = dom.getValue(id)

    try:
      ratio = int(value)
    except:
      pass
    else:
      updateDuties(dom, setRatio(ratio))


def acWidth(dom, id):
  if onDuty:
    value = dom.getValue(id)

    try:
      width = float(value)
    except:
      pass
    else:
      updateDuties(dom, setWidth(int(1000000 * width)))


CALLBACKS = {
  "": acConnect,
  "Mode": acMode,
  "Switch": acSwitch,
  "Freq": acFreq,
  "Select": acSelect,
  "Ratio": acRatio,
  "RatioStep": lambda dom, id: dom.setAttribute(I_RATIO, "step", dom.getValue(id)),
  "Width": acWidth,
  "WidthStep": lambda dom, id: dom.setAttribute(I_WIDTH, "step", dom.getValue(id)),
}

device = ucuq.UCUq("")
device.execute(MC_INIT)

atlastk.launch(CALLBACKS, headContent=HEAD)