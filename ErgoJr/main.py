""" 
 Copyright (C) 2019 Claude SIMON (http://q37.info/contact/).

	This file is part of XDHq.

	XDHq is free software: you can redistribute it and/or
	modify it under the terms of the GNU Affero General Public License as
	published by the Free Software Foundation, either version 3 of the
	License, or (at your option) any later version.

	XDHq is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
	Affero General Public License for more details.

	You should have received a copy of the GNU Affero General Public License
	along with XDHq If not, see <http://www.gnu.org/licenses/>.
 """

# To control a Poppy Ergo Jr

import time, sys

sys.path.append("./Atlas.python.zip")
sys.path.append("../Atlas.python.zip")
sys.path.append("./Atlas")

import Atlas

# Import des librairies et creation du robot
from poppy_ergo_jr import PoppyErgoJr

poppy = PoppyErgoJr()
# Comment above and uncomment below to control a simulated robot.
# poppy = PoppyErgoJr(simulator='vrep',use_snap=True) # vrep ou poppy-simu

import Atlas

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

def readAsset(path):
	return Atlas.readAsset(path, "ErgoJr")

class Poppy:
  pass

def acConnect(Poppy,dom,id):
	dom.setLayout("", readAsset( "Main.html") )

def acMove(Poppy,dom,id):
  global poppy
  poppy.goto_position({id: int(dom.getContent(id))},0,wait=True)

def set( dom, motor, position ):
  global poppy
  poppy.goto_position({motor: position},0,wait=False)
  dom.setContent( motor, position )
	
def reset( dom, motor ):
  set(dom, motor, 0)
	
def acReset(Poppy,dom,id):
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
	
Atlas.launch(callbacks, Poppy, readAsset("Head.html"), "ErgoJr")