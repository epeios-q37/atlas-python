import os, sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.extend(("..","../../atlastk"))

import atlastk, ucuq

with open('Body.html', 'r') as file:
  BODY = file.read()

with open('Head.html', 'r') as file:
  HEAD = file.read()

leds = None

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
  leds.fill((int(R), int(G), int(B)))
  leds.write()

def acConnect(dom):
  dom.inner("", BODY)
  dom.executeVoid("setColorWheel()")
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
  dom.setValues(getAllValues_(0, 0, 0))
  update_(dom, 0, 0, 0)

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
  "Reset": acReset
}

device = ucuq.UCUq("")
leds = ucuq.WS2812(device, 16, 4)


atlastk.launch(CALLBACKS, headContent=HEAD)
