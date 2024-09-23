import os, sys, time, io, json, datetime

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("../atlastk")

import mcrcq, atlastk

BODY = """
<fieldset>
  <fieldset id="Matrix" style="display: grid; grid-template-columns: repeat(16, auto)">
  </fieldset>
  <fieldset style="display: flex; justify-content: space-evenly">
    <label style="display: flex; align-items: center;">
      <span>Brightness:&nbsp;</span>
      <input xdh:onevent="Brightness" type="range" min="0" max="15" value="0">
    </label>
    <label>
      <span>Blink:</span>
    <select xdh:onevent="Blink">
      <option value="0">None</option>
      <option value="0.5">0.5 Hz</option>
      <option value="1">1 Hz</option>
      <option value="2">2 Hz</option>
    </select>
      </label>
  </fieldset>
</fieldset>"""

with open('mc_init.py', 'r') as file:
  INIT = file.read()

def acConnect(dom):
  html = ""

  dom.inner("", BODY)

  for y in range(8):
    for x in range(16):
      html += f"<input type='checkbox' xdh:onevent='Toggle' xdh:mark='{x} {7-y}'>"

  dom.inner("Matrix", html)

def acToggle(dom,id):
  [x, y] = dom.getMark(id).split()
  mcrcq.execute(f"matrix.plot({x},{y},{1 if dom.getValue(id) == "true" else 0}).draw()")


CALLBACKS = {
  "": acConnect,
  "Toggle": acToggle,
  "Brightness": lambda dom, id: mcrcq.execute(f"matrix.set_brightness({dom.getValue(id)})"),
  "Blink": lambda dom, id: mcrcq.execute(f"matrix.set_blink_rate({dom.getValue(id)})"),
}

mcrcq.connect()

mcrcq.execute(INIT)

mcrcq.execute("test()")

atlastk.launch(CALLBACKS)
