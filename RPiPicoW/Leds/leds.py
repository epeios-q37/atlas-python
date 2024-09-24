import os, sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.extend(("..","../../atlastk"))

import atlastk, mcrcq

with open('Body.html', 'r') as file:
  BODY = file.read()

with open('Head.html', 'r') as file:
  HEAD = file.read()


C_INIT = """
import neopixel, machine

pI = machine.Pin(16)
pE = machine.Pin(7)

nI = neopixel.NeoPixel(pI, 4)
nE = neopixel.NeoPixel(pE, 192)

def set(leds, n):
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
  return getNValues_(R, G, B) | getSValues_(R, G, B);
  mcrcq.execute(C_SET.format("0", R, G, B))

def update_(dom, R, G, B):
  command = "set({"

  for led in range(4):
    command += f'{led}: ({R},{G},{B}), '

  mcrcq.execute(command + "},nI)")

  command = "set({"

  for led in range(192):
    command += f'{led}: ({R},{G},{B}), '

  mcrcq.execute(command + "},nE)")


def acConnect(dom):
  dom.inner("", BODY)
  dom.executeVoid("setColorWheel()")
  mcrcq.execute(C_INIT)
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



CALLBACKS = {
  "": acConnect,
  "Select": acSelect,
  "Slide": acSlide,
  "Adjust": acAdjust,
  "All": acAll,
  "None": acNone,
  "Reset": acReset
}

mcrcq.connect()

atlastk.launch(CALLBACKS, headContent=HEAD)
