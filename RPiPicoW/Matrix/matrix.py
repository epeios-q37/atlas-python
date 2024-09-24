import os, sys, time, io, json, datetime

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.extend(("..","../../atlastk"))

import mcrcq, atlastk

with open('Body.html', 'r') as file:
  BODY = file.read()

with open('mc_init.py', 'r') as file:
  INIT = file.read()

def acConnect(dom):
  html = ""

  dom.inner("", BODY)

  for y in range(8):
    for x in range(16):
      html += f"<input type='checkbox' xdh:onevent='Toggle' xdh:mark='{x} {7-y}'>"

  dom.inner("Matrix", html)


def plot(x,y,ink=True):
  mcrcq.execute(f"matrix.plot({x},{y},{1 if ink else 0}).render()")


def clear():
  mcrcq.execute(f"matrix.clear()")

def acToggle(dom,id):
  [x, y] = dom.getMark(id).split()
  plot(x,y, dom.getValue(id) == "true")

def draw(motif):
  clear()

  mcrcq.execute(f"matrix.draw(\"{motif}\").render()")


def acMotif(dom):
  draw("0FF0300C4002866186614002300C0FF0")
  time.sleep(1)
  draw("000006000300FFFFFFFF030006000000")
  time.sleep(1)
  draw("00001824420000000018244200000000")



CALLBACKS = {
  "": acConnect,
  "Test": lambda: mcrcq.execute("test()"),
  "Motif": acMotif,
  "Toggle": acToggle,
  "Brightness": lambda dom, id: mcrcq.execute(f"matrix.set_brightness({dom.getValue(id)})"),
  "Blink": lambda dom, id: mcrcq.execute(f"matrix.set_blink_rate({dom.getValue(id)})"),
}

mcrcq.connect()

mcrcq.execute(INIT)

atlastk.launch(CALLBACKS)
