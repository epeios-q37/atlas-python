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

# To control a Poppy Ergo Jr

import os, time, sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("../../atlastk")

import atlastk

# Import des librairies et creation du robot
from poppy_ergo_jr import PoppyErgoJr

poppy = PoppyErgoJr()
# Comment above and uncomment below to control a simulated robot.
# poppy = PoppyErgoJr(simulator='vrep',use_snap=True) # vrep ou poppy-simu

for m in poppy.motors:
    print(m.name)

"""
for _ in range(3):
    poppy.m3.goal_position = 30
    time.sleep(0.5)
    poppy.m3.goal_position = -30
    time.sleep(0.5)

for _ in range(3):
    poppy.m1.goal_position = -20
    poppy.m3.goal_position = 30
    time.sleep(0.5)
    poppy.m1.goal_position = 20
    poppy.m3.goal_position = -30
    time.sleep(0.5)
"""

class Poppy:
  pass

def acConnect(Poppy,dom):
	dom.inner("", open( "Main.html").read() )

def acMove(Poppy,dom,id):
  global poppy
  poppy.goto_position({id: int(dom.get_value(id))},0,wait=True)

def set( dom, motor, position ):
  global poppy
  poppy.goto_position({motor: position},0,wait=False)
  dom.set_value( motor, position )
	
def reset( dom, motor ):
  set(dom, motor, 0)
	
def acReset(Poppy,dom):
  global poppy
  reset( dom, "m1")
  reset( dom, "m2")
  reset( dom, "m3")
  reset( dom, "m4")
  reset( dom, "m5")
  reset( dom, "m6")
	
callbacks = {
		"": acConnect,
		"Move": acMove,
		"Reset": acReset,
	}
	
atlastk.launch(callbacks, Poppy, open("Head.html").read())
