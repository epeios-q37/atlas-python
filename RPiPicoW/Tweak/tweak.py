import os, sys, time, io, json, datetime

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.extend(("..","../../atlastk"))

import ucuq, atlastk

onDuty = False

# Duties
D_RATIO = "Ratio"
D_WIDTH = "Width"

# Inputs
I_DUTY = "Duty"
I_PIN="Pin"
I_FREQ = "Freq"
I_RATIO = "Ratio"
I_RATIO_STEP = "RatioStep"
I_WIDTH = "Width"

# Outputs
O_FREQ = "TrueFreq"
O_RATIO = "TrueRatio"
O_WIDTH = "TrueWidth"

#Outputs

# Micorcontroller scripts
MC_INIT = """
from machine import Pin, PWM

def getParams():
  return [pwm.freq(), pwm.duty_u16(), pwm.duty_ns()]

"""

MC_INIT_PWM = """
pin = Pin({})
pwm = PWM(pin, freq={}, {}=({}))

params = getParams()
"""

MC_RESET_PWM = """
pwm.deinit()
"""

MC_SET_FREQ = """
pwm.freq({})

params = getParams()
"""

MC_SET_RATIO = """
pwm.duty_u16({})

params = getParams()
"""

MC_SET_WIDTH = """
pwm.duty_ns({})

params = getParams()
"""

MC_PARAMS = """
params = getParams()
"""

with open('Body.html', 'r') as file:
  BODY = file.read()

with open('Head.html', 'r') as file:
  HEAD = file.read()


def getParams():
  return device.execute(MC_PARAMS, "params") if onDuty else None


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
  values = dom.getValues([I_DUTY, I_PIN, I_FREQ, I_RATIO, I_WIDTH])

  return {
    I_PIN: convert(values[I_PIN], int),
    I_FREQ: convert(values[I_FREQ], int),
    I_DUTY: {
      "Type": values[I_DUTY],
      "Value": convert(values[I_RATIO], int) if values[I_DUTY] == D_RATIO else convert(values[I_WIDTH], float)
    } 
  }


def test(dom, inputs):
  if inputs[I_PIN] == None:
    dom.alert("Bad or no pin value!")
  elif inputs[I_FREQ] ==  None:
    dom.alert("Bad or no freq. value!")
  elif inputs[I_DUTY]["Type"] == D_RATIO:
    if inputs[I_DUTY]["Value"] == None:
      dom.alert("Bad or no ratio value!")
    else:
      return True
  elif inputs[I_DUTY]["Type"] == D_WIDTH:
    if inputs[I_DUTY]["Value"] == None:
      dom.alert("Bad or no width value!")
    else:
      return True
  else:
    raise Exception("Unknown duty type!!!")
  
  return False


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
  return device.execute(MC_INIT_PWM.format(
    inputs[I_PIN],
    inputs[I_FREQ],
    "duty_u16" if inputs[I_DUTY]["Type"] == D_RATIO else "duty_ns",
    int(inputs[I_DUTY]["Value"] * (1 if inputs[I_DUTY]["Type"] == D_RATIO else 1000000))),
    "params")
  

def setFreq(freq):
  return device.execute(MC_SET_FREQ.format(freq), "params")
  

def setRatio(ratio):
  return device.execute(MC_SET_RATIO.format(ratio), "params")
  

def setWidth(width):
  return device.execute(MC_SET_WIDTH.format(width), "params")
  

def acConnect(dom):
  dom.inner("", BODY)
  updateDutyBox(dom)
  
  
def acSwitch(dom, id):
  global onDuty

  if dom.getValue(id) == "true":
    inputs = getInputs(dom)

    if not test(dom, inputs):
      dom.setValue(id, False)
    else:
      dom.disableElement(I_PIN)
      updateDuties(dom, initPWM(inputs))
      onDuty = True
  else:
    if onDuty:
      device.execute(MC_RESET_PWM)
      onDuty = False
    updateDuties(dom)
    dom.enableElement(I_PIN)


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
  "Switch": acSwitch,
  "Freq": acFreq,
  "Select": acSelect,
  "Ratio": acRatio,
  "RatioStep": lambda dom, id: dom.setAttribute(I_RATIO, "step", dom.getValue(id)),
  "Width": acWidth,
  "WidthStep": lambda dom, id: dom.setAttribute(I_WIDTH, "step", dom.getValue(id)),
}

device = ucuq.UCUq("Black")
device.execute(MC_INIT)

atlastk.launch(CALLBACKS, headContent=HEAD)