import os, sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("../atlastk")

import atlastk, mcrcq

import math

HEAD = """
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/beautiful-piano@0.0.6/styles.min.css"></link>
  <script src="https://cdn.jsdelivr.net/npm/beautiful-piano@0.0.6/dist/piano.min.js"></script>
"""

BUZZER_PIN = 2
LOUDSPEAKER_PIN = 6

with open('Body.html', 'r') as file:
  BODY = file.read()

INIT = """
from machine import Pin, PWM
from time import sleep

def buzzer(buzzerPinObject,frequency,ratio):
    buzzerPinObject.duty_u16(int(65536*ratio))
    buzzerPinObject.freq(frequency)
    sleep(0.5)
    buzzerPinObject.duty_u16(int(65536*0))
"""

pinNotSet = True

baseFreq = 440.0*math.pow(math.pow(2,1.0/12), -16)
ratio = 0.5

def acConnect(dom):
  dom.inner("", BODY)
  mcrcq.execute(INIT.format(0))

def acPlay(dom,id):
  if pinNotSet:
    dom.alert("Please select a pin number!")
  else:
    freq = int(baseFreq*math.pow(math.pow(2,1.0/12), int(id)))
    mcrcq.execute(f"buzzer(BuzzerObj,{freq},{ratio})")

def acSetRatio(dom, id):
  global ratio
  
  ratio = float(dom.getValue(id))

  dom.setValue("RatioSlide" if id == "RatioValue" else "RatioValue", ratio)

def acSetPin(dom, id):
  global pinNotSet

  rawPin = dom.getValue(id)
  pin = None

  if rawPin in ("Buzzer", "Loudspeaker"):
    pin = BUZZER_PIN if rawPin == "Buzzer" else LOUDSPEAKER_PIN

    dom.disableElement("UserPin")
    dom.setValue("UserPin", pin)
  elif rawPin != "User":
    pin = int(rawPin)
  else:
    dom.enableElement("UserPin")
    
  if pin:
    pinNotSet = False
    mcrcq.execute(f"BuzzerObj=PWM(Pin({pin}))")

CALLBACKS = {
  "": acConnect,
  "Play": acPlay,
  "SetRatio": acSetRatio,
  "SetPin": acSetPin
}

mcrcq.connect()

atlastk.launch(CALLBACKS, headContent=HEAD)
