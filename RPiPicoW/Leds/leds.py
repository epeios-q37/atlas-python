import os, sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.extend(("..","../../atlastk"))

import atlastk, ucuq

with open('Body.html', 'r') as file:
  BODY = file.read()

with open('Head.html', 'r') as file:
  HEAD = file.read()


C_INIT = """
import neopixel, machine

n = neopixel.NeoPixel(machine.Pin({}), {})

def set(leds):
  global n

  for led in leds:
    n[led] = leds[led]
  n.write()
"""

def convert_(hex):
  return int(int(hex,16) * 100 / 256)

def getValues_(target, R, G, B):
  return {
    target + "R": R,
    target + "G": G,
    target + "B": B
  }

def getNValues_(R, G, B):
  return getValues_("N", R, G, B)

def getSValues_(R, G, B):
  return getValues_("S", R, G, B)

def getAllValues_(R, G, B):
  return getNValues_(R, G, B) | getSValues_(R, G, B)

def update_(dom, R, G, B):
  command = "set({"

  for led in range(4):
    command += f'{led}: ({R},{G},{B}), '

  black.execute(command + "})")

  command = "set({"

  for led in range(128):
    command += f'{led}: ({R},{G},{B}), '

  red.execute(command + "})")
  yellow.execute(command + "})")


def acConnect(dom):
  dom.inner("", BODY)
  dom.executeVoid("setColorWheel()")
  black.execute(C_INIT.format(16,4))
  red.execute(C_INIT.format(2,128))
  yellow.execute(C_INIT.format(2,128))
  dom.executeVoid(f"colorWheel.rgb = [0, 0, 0]")
  update_(dom, 0, 0, 0)
  
  
def acSelect(dom):
  R, G, B = dom.getValues(["rgb-r", "rgb-g", "rgb-b"]).values()
  dom.setValues(getAllValues_(R, G, B))
  update_(dom, R, G, B)

def acSlide(dom):
  (R,G,B) = dom.getValues(["SR", "SG", "SB"]).values()
  dom.setValues(getNValues_(R, G, B))
  dom.executeVoid(f"colorWheel.rgb = [{R},{G},{B}]")
  update_(dom, R, G, B)

def acAdjust(dom):
  (R,G,B) = dom.getValues(["NR", "NG", "NB"]).values()
  dom.setValues(getSValues_(R, G, B))
  dom.executeVoid(f"colorWheel.rgb = [{R},{G},{B}]")
  update_(dom, R, G, B)

def acReset(dom):
  dom.executeVoid(f"colorWheel.rgb = [0, 0, 0]")
  update_(dom, 0, 0, 0)

def acAll(dom):
  dom.setValues(
    {
      "0": "true",
      "1": "true",
      "2": "true",
      "3": "true",
    })   

def acNone(dom):
  dom.setValues(
    {
      "0": "false",
      "1": "false",
      "2": "false",
      "3": "false",
    })   

def connect_(id):
  device = ucuq.UCUq()

  if not device.connect(id):
    print(f"Device '{id}' not available.")

  return device


CALLBACKS = {
  "": acConnect,
  "Select": acSelect,
  "Slide": acSlide,
  "Adjust": acAdjust,
  "All": acAll,
  "None": acNone,
  "Reset": acReset
}

black = ucuq.UCUq("Black")

red = connect_("Red")
yellow = connect_("Yellow")

atlastk.launch(CALLBACKS, headContent=HEAD)
