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

import os, sys


D_TESTING = 0
D_ODROID_C2 = 1
D_RASPBERRY_PI = 2

labels = {
  D_TESTING: "Testing",
  D_ODROID_C2: "ODROID-C2",
  D_RASPBERRY_PI: "Raspberry Pi"
}

M_OUT = 0
M_IN = 1
M_PWM = 2

def getModelLabel():
  global labels
  file = "/proc/device-tree/model"
  if os.path.isfile(file):
    return open(file).read()
  else:
    return labels[D_TESTING]

def detectDevice(label):
  global labels
  for key in labels.keys():
    if label.startswith(labels[key]):
      return key

  return D_TESTING

device = detectDevice(getModelLabel())

if ( device == D_TESTING ):
  print( "Unknown device; switching to '" + labels[device] + "' device.")

  def setup():
    pass

  def pinMode(pin,mode):
    pass

  def digitalRead(pin):
    return 0

  def digitalWrite(pin,value):
    pass

  def softPWMCreate(pin):
    pass

  def softPWMWrite(pin,value):
    pass

  def softPWMDestroy(pin):
    pass

elif ( device == D_ODROID_C2 ):
  import wiringpi

  print("'" + labels[device] + "' detected.")

  def setup():
    wiringpi.wiringPiSetupPhys()

  def pinMode(pin,mode):
    mode = (mode + 1) % 2 
    wiringpi.pinMode(pin,mode)

  def digitalRead(pin):
    return wiringpi.digitalRead(pin)

  def digitalWrite(pin,value):
    wiringpi.digitalWrite(pin,value)

  def softPWMCreate(pin):
    wiringpi.softPwmCreate(pin,0,100)

  def softPWMWrite(pin,value):
    wiringpi.softPwmWrite(pin,value)

  def softPWMDestroy(pin):
    pass

elif (device == D_RASPBERRY_PI ):
  import RPi.GPIO as GPIO

  print("'" + labels[device] + "' detected.")

  pwms = {}

  def destroyPWMIfNeeded(pin):
    global pwms
    if (pin in pwms):
      pwms[pin].stop()
      pwms.pop(pin)

  def setup():
    GPIO.setmode(GPIO.BOARD)

  def pinMode(pin,mode):
    destroyPWMIfNeeded(pin)
    GPIO.setup(pin,mode)

  def digitalRead(pin):
    return GPIO.input(pin)

  def digitalWrite(pin,value):
    GPIO.output(pin,value)

  def softPWMCreate(pin):
    global pwms
    destroyPWMIfNeeded(pin)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    pwms[pin] = GPIO.PWM(pin, 100)
    pwms[pin].start(0)

  def softPWMWrite(pin,value):
    global pwms
    pwms[pin].ChangeDutyCycle(value)

  def softPWMDestroy(pin):
    destroyPWMIfNeeded(pin)
else:
  sys.exit("???")

    




