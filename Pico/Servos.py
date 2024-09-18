import os, sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("../atlastk")

import mcrcq, atlastk

BODY = """
<fieldset>
  <label xdh:mark="LF" style="display: flex; align-items: center;">
    <span>LF:&nbsp;</span>
    <input xdh:onevent="Slide" id="LFS" type="range" min="-45" max="45" step="1" value="0">
    <span>&nbsp;</span>
    <input xdh:onevent="Adjust" id="LFN" type="number" min="-45" max="45" value="0" step="5" size="3">
    <span>&nbsp;</span>
    <button xdh:onevent="Test">Test</button>
  </label>
  <label xdh:mark="LL" style="display: flex; align-items: center;">
    <span>LL:&nbsp;</span>
    <input xdh:onevent="Slide" id="LLS" type="range" min="-45" max="45" step="1" value="0">
    <span>&nbsp;</span>
    <input xdh:onevent="Adjust" id="LLN" type="number" min="-45" max="45" value="0" step="5" size="3">
    <span>&nbsp;</span>
    <button xdh:onevent="Test">Test</button>
  </label>
  <label xdh:mark="RL" style="display: flex; align-items: center;">
    <span>RL:&nbsp;</span>
    <input xdh:onevent="Slide" id="RLS" type="range" min="-45" max="45" step="1" value="0">
    <span>&nbsp;</span>
    <input xdh:onevent="Adjust" id="RLN" type="number" min="-45" max="45" value="0" step="5" size="3">
    <span>&nbsp;</span>
    <button xdh:onevent="Test">Test</button>
  </label>
  <label xdh:mark="RF" style="display: flex; align-items: center;">
    <span>RF:&nbsp;</span>
    <input xdh:onevent="Slide" id="RFS" type="range" min="-45" max="45" step="1" value="0">
    <span>&nbsp;</span>
    <input xdh:onevent="Adjust" id="RFN" type="number" min="-45" max="45" value="0" step="5" size="3">
    <span>&nbsp;</span>
    <button xdh:onevent="Test">Test</button>
  </label>
  <label xdh:mark="X1" style="display: flex; align-items: center;">
    <span>X1:&nbsp;</span>
    <input xdh:onevent="Slide" id="X1S" type="range" min="-45" max="45" step="1" value="0">
    <span>&nbsp;</span>
    <input xdh:onevent="Adjust" id="X1N" type="number" min="-45" max="45" value="0" step="5" size="3">
    <span>&nbsp;</span>
    <button xdh:onevent="Test">Test</button>
  </label>
  <label xdh:mark="X2" style="display: flex; align-items: center;">
    <span>X2:&nbsp;</span>
    <input xdh:onevent="Slide" id="X2S" type="range" min="-45" max="45" step="1" value="0">
    <span>&nbsp;</span>
    <input xdh:onevent="Adjust" id="X2N" type="number" min="-45" max="45" value="0" step="5" size="3">
    <span>&nbsp;</span>
    <button xdh:onevent="Test">Test</button>
  </label>
  <div style="height: 10px;"></div>
  <div style="display: flex;width: 100%; justify-content: center">
    <button xdh:onevent="Reset">Reset</button>
  </div>
</fieldset>
"""

C_INIT = """
from machine import Pin,PWM
import time

class Servo:
  __servo_pwm_freq = 50
  __min_u16_duty = 1640 - 2 # offset for correction
  __max_u16_duty = 7864 - 0  # offset for correction
  min_angle = 0
  max_angle = 180
  current_angle = 0.001


  def __init__(self, pin):
    self.__initialise(pin)


  def update_settings(self, servo_pwm_freq, min_u16_duty, max_u16_duty, min_angle, max_angle, pin):
    self.__servo_pwm_freq = servo_pwm_freq
    self.__min_u16_duty = min_u16_duty
    self.__max_u16_duty = max_u16_duty
    self.min_angle = min_angle
    self.max_angle = max_angle
    self.__initialise(pin)


  def move(self, angle):
    # round to 2 decimal places, so we have a chance of reducing unwanted servo adjustments
    angle = round(angle, 2)
    # do we need to move?
    if angle == self.current_angle:
        return
    self.current_angle = angle
    # calculate the new duty cycle and move the motor
    duty_u16 = self.__angle_to_u16_duty(angle)
    self.__motor.duty_u16(duty_u16)

  def __angle_to_u16_duty(self, angle):
    return int((angle - self.min_angle) * self.__angle_conversion_factor) + self.__min_u16_duty


  def __initialise(self, pin):
    self.current_angle = -0.001
    self.__angle_conversion_factor = (self.__max_u16_duty - self.__min_u16_duty) / (self.max_angle - self.min_angle)
    self.__motor = PWM(Pin(pin))
    self.__motor.freq(self.__servo_pwm_freq)


LL_PIN = 10
LF_PIN = 11
RL_PIN = 12
RF_PIN = 13
X1_PIN = 14
X2_PIN = 15

lf = Servo(LF_PIN)
ll = Servo(LL_PIN)
rl = Servo(RL_PIN)
rf = Servo(RF_PIN)
x1 = Servo(X1_PIN)
x2 = Servo(X2_PIN)

def test(servo):
  servo.move(90)  # tourne le servo à 0°
  servo.move(45)  # tourne le servo à 0°
  time.sleep(0.5)
  servo.move(135)  # tourne le servo à 45°
  time.sleep(0.5)
  servo.move(90)  # tourne le servo à 0°

lf.move(90)
ll.move(90)
rl.move(90)
rf.move(90)
x1.move(90)
x2.move(90)
"""


def move_(servo, angle):
  mcrcq.execute(f"{servo.lower()}.move({int(angle)+90})")
   

def acConnect(dom):
  dom.inner("", BODY)
  mcrcq.execute(C_INIT)


def acTest(dom, id):
  mark = dom.getMark(id);
  dom.setValues({
    f"{mark}S": "0",
    f"{mark}N": "0",
  })
  mcrcq.execute(f"test({mark.lower()})")


def acSlide(dom, id):
  mark = dom.getMark(id)
  angle = dom.getValue(f"{mark}S")
  dom.setValue(f"{mark}N", angle )
  move_(mark, angle)


def acAdjust(dom, id):
  mark = dom.getMark(id)
  angle = dom.getValue(f"{mark}N")
  dom.setValue(f"{mark}S", angle )
  move_(mark, angle)


def acReset(dom):
  dom.setValues({
    "LFN": 0,
    "LFS": 0,
    "LLN": 0,
    "LLS": 0,
    "RLN": 0,
    "RLS": 0,
    "RFN": 0,
    "RFS": 0,
    "X1N": 0,
    "X1S": 0,
    "X2N": 0,
    "X2S": 0,
  })
  move_("lf",0)
  move_("ll",0)
  move_("rl",0)
  move_("rf",0)
  move_("x1",0)
  move_("x2",0)
  

CALLBACKS = {
   "": acConnect,
   "Test": acTest,
   "Slide": acSlide,
   "Adjust": acAdjust,
   "Reset": acReset
}

mcrcq.connect()

atlastk.launch(CALLBACKS)