import os, sys, time, io, json, datetime, binascii

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.extend(("..","../../atlastk"))

import ucuq, atlastk

pattern = "0" * 32

with open('Head.html', 'r') as file:
  HEAD = file.read()

with open('Body.html', 'r') as file:
  BODY = file.read()

MATRICES = (
  "0FF0300C4002866186614002300C0FF",
  "000006000300FFFFFFFF030006",
  "00004002200410080810042003c",
  "0000283810282838000000400040078",
  "081004200ff01bd83ffc2ff428140c3",
  "042003c004200c300ff007e00db",
  "0420024027e42db43ffc18180a50042",
  "0420024007e00ff02bd41ff824241bd8",
  "0300030009c007a0018002600fc0048",
  "08800f800a8007100210079007d00be",
  "02000e000e1003e003e003e00220066",
  "06001a000e000f000ff00fe00f8002",
  "024001800fe01850187018500ff00fe",
  "038004400960041004180408021001e",
  "000003c0042005a005a0042003c",
  "03c0042009900a500a5009e0040803f",
  "239f6441204223862401241177ce",
  "43dc421242124392421242127bdc",
  "00003c3c727272727e7e7e7e3c3c",
  "00003ffc40025ffa2ff417e8081007e",
)

def test():
  for y in range(8):
    for x in range(16):
      matrix.plot(x,y)
    matrix.render()
    # time.sleep(.06)
    matrix.clear()

  for x in range(16):
    for y in range(8):
      matrix.plot(x,y)
    matrix.render()
    # time.sleep(.06)
    matrix.clear()

  for x in range(16):
    for y in range(8):
      matrix.plot(x,y)

  matrix.render()

  for b in range(0, 16):
    matrix.setBrightness(b)
    device.render()
    # time.sleep(0.05)

  for b in range(15, -1, -1):
    matrix.setBrightness(b)
    device.render()
    # time.sleep(0.05)

  matrix.clear()


def drawOnGUI(dom, motif = pattern):
  html = ""

  for i, c in enumerate(motif.ljust(32,"0")):
    for o in range(4):
      on = int(c, 16) & (1 << (3 - o)) != 0
      html += f"<div class='led{ '' if on else ' off'}' xdh:onevent='Toggle' data-state='{'on' if on else 'off'}' xdh:mark='{(i % 4) * 4 + o} {i >> 2}'></div>"

  dom.inner("Matrix", html)


def drawLittleMatrix(motif):
  html = ""

  for i, c in enumerate(motif.ljust(32,"0")):
    for o in range(4):
      on = int(c, 16) & (1 << (3 - o)) != 0
      html += f"<div class='little-led{ '' if on else ' little-off'}'></div>"

  return html


def drawLittleMatrices(dom, matrices):
  html = ""

  for i, matrix in enumerate(matrices):
    html += f"<fieldset xdh:mark=\"{i}\" style=\"cursor: pointer;\" class=\"little-matrix\" xdh:onevent=\"Draw\">"\
      + drawLittleMatrix(matrix)\
      +"</fieldset>"

  dom.inner("LittleMatrices", html)


def setHexa(dom, motif = pattern):
  dom.setValue("Hexa", motif)


def drawOnMatrix(motif = pattern):
  matrix.draw(motif)

def draw(dom, motif = pattern):
  global pattern

  pattern = motif
  
  drawOnMatrix(motif)

  drawOnGUI(dom, motif)

  setHexa(dom, motif)


def acConnect(dom):
  dom.inner("", BODY)

  draw(dom, "")

  dom.executeVoid("patchHexaInput();")

  drawLittleMatrices(dom,MATRICES)


def plot(x,y,ink=True):
  matrix.plot(x,y)
  matrix.render()

def clear():
  matrix.clear()


def acToggle(dom, id):
  global pattern

  [x, y] = list(map(lambda v: int(v), dom.getMark(id).split()))

  pos = y * 16 + ( 4 * int(x / 4) + (3 - x % 4)) 

  bin = binascii.unhexlify(pattern.ljust(32,"0")[::-1].encode())[::-1]

  offset = int(pos/8)

  bin = bin[:offset] + bytearray([bin[offset] ^ (1 << (pos % 8))]) + bin[offset+1:]

  pattern = (binascii.hexlify(bin[::-1]).decode()[::-1])

  plot(x, y,  bin[offset] & (1 << (pos % 8)))

  draw(dom, pattern)


def acHexa(dom):
  global pattern

  drawOnMatrix(motif := dom.getValue("Hexa"))

  drawOnGUI(dom, motif)

  pattern = motif


def acAll(dom):
  for matrix in MATRICES:
    draw(dom, matrix)
    time.sleep(0.5)


def acBrightness(dom, id):
  matrix.setBrightness(int(dom.getValue(id)))
  device.render()

def acBlinkRate(dom, id):
  matrix.setBlinkRate(float(dom.getValue(id)))
  device.render()

def acDraw(dom, id):
  draw(dom,MATRICES[int(dom.getMark(id))])

def connect_(id):
  device = ucuq.UCUq()

  if not device.connect(id):
    print(f"Device '{id}' not available.")

  return device


CALLBACKS = {
  "": acConnect,
  "Test": lambda: test(),
  "All": acAll,
  "Toggle": acToggle,
  "Brightness": acBrightness,
  "Blink": acBlinkRate,
  "Hexa": acHexa,
  "Draw": acDraw
}

device = ucuq.UCUq("")
matrix = ucuq.HT16K33(device, 4, 5)
matrix.clear()
matrix.setBrightness(0)
matrix.setBlinkRate(0)
device.render()


atlastk.launch(CALLBACKS, headContent=HEAD)
