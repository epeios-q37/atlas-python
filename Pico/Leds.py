import os, sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("../atlastk")

import mcrcq, atlastk

COORDS_AND_IDS = [
[63,  0,    72,   4,    72,   15, 63, 19, 54, 15, 54, 4, "003366"],
[81,  0,    90,   4,    90,   15, 81, 19, 72, 15, 72, 4, "336699"],
[99,  0,    108,  4,    108,  15, 99, 19, 90, 15, 90, 4, "3366CC"],
[117, 0,    126,  4,    126,  15, 117,  19, 108,  15, 108,  4, "003399"],
[135, 0,    144,  4,    144,  15, 135,  19, 126,  15, 126,  4, "000099"],
[153, 0,    162,  4,    162,  15, 153,  19, 144,  15, 144,  4, "0000CC"],
[171, 0,    180,  4,    180,  15, 171,  19, 162,  15, 162,  4, "000066"],
[54,  15,   63,   19,   63,   30, 54, 34, 45, 30, 45, 19, "006666"],
[72,  15,   81,   19,   81,   30, 72, 34, 63, 30, 63, 19, "006699"],
[90,  15,   99,   19,   99,   30, 90, 34, 81, 30, 81, 19, "0099CC"],
[108, 15,   117,  19,   117,  30, 108,  34, 99, 30, 99, 19, "0066CC"],
[126, 15,   135,  19,   135,  30, 126,  34, 117,  30, 117,  19, "0033CC"],
[144, 15,   153,  19,   153,  30, 144,  34, 135,  30, 135,  19, "0000FF"],
[162, 15,   171,  19,   171,  30, 162,  34, 153,  30, 153,  19, "3333FF"],
[180, 15,   189,  19,   189,  30, 180,  34, 171,  30, 171,  19, "333399"],
[45,  30,   54,   34,   54,   45, 45, 49, 36, 45, 36, 34, "669999"],
[63,  30,   72,   34,   72,   45, 63, 49, 54, 45, 54, 34, "009999"],
[81,  30,   90,   34,   90,   45, 81, 49, 72, 45, 72, 34, "33CCCC"],
[99,  30,   108,  34,   108,  45, 99, 49, 90, 45, 90, 34, "00CCFF"],
[117, 30,   126,  34,   126,  45, 117,  49, 108,  45, 108,  34, "0099FF"],
[135, 30,   144,  34,   144,  45, 135,  49, 126,  45, 126,  34, "0066FF"],
[153, 30,   162,  34,   162,  45, 153,  49, 144,  45, 144,  34, "3366FF"],
[171, 30,   180,  34,   180,  45, 171,  49, 162,  45, 162,  34, "3333CC"],
[189, 30,   198,  34,   198,  45, 189,  49, 180,  45, 180,  34, "666699"],
[36,  45,   45,   49,   45,   60, 36, 64, 27, 60, 27, 49, "339966"],
[54,  45,   63,   49,   63,   60, 54, 64, 45, 60, 45, 49, "00CC99"],
[72,  45,   81,   49,   81,   60, 72, 64, 63, 60, 63, 49, "00FFCC"],
[90,  45,   99,   49,   99,   60, 90, 64, 81, 60, 81, 49, "00FFFF"],
[108, 45,   117,  49,   117,  60, 108,  64, 99, 60, 99, 49, "33CCFF"],
[126, 45,   135,  49,   135,  60, 126,  64, 117,  60, 117,  49, "3399FF"],
[144, 45,   153,  49,   153,  60, 144,  64, 135,  60, 135,  49, "6699FF"],
[162, 45,   171,  49,   171,  60, 162,  64, 153,  60, 153,  49, "6666FF"],
[180, 45,   189,  49,   189,  60, 180,  64, 171,  60, 171,  49, "6600FF"],
[198, 45,   207,  49,   207,  60, 198,  64, 189,  60, 189,  49, "6600CC"],
[27,  60,   36,   64,   36,   75, 27, 79, 18, 75, 18, 64, "339933"],
[45,  60,   54,   64,   54,   75, 45, 79, 36, 75, 36, 64, "00CC66"],
[63,  60,   72,   64,   72,   75, 63, 79, 54, 75, 54, 64, "00FF99"],
[81,  60,   90,   64,   90,   75, 81, 79, 72, 75, 72, 64, "66FFCC"],
[99,  60,   108,  64,   108,  75, 99, 79, 90, 75, 90, 64, "66FFFF"],
[117, 60,   126,  64,   126,  75, 117,  79, 108,  75, 108,  64, "66CCFF"],
[135, 60,   144,  64,   144,  75, 135,  79, 126,  75, 126,  64, "99CCFF"],
[153, 60,   162,  64,   162,  75, 153,  79, 144,  75, 144,  64, "9999FF"],
[171, 60,   180,  64,   180,  75, 171,  79, 162,  75, 162,  64, "9966FF"],
[189, 60,   198,  64,   198,  75, 189,  79, 180,  75, 180,  64, "9933FF"],
[207, 60,   216,  64,   216,  75, 207,  79, 198,  75, 198,  64, "9900FF"],
[18,  75,   27,   79,   27,   90, 18, 94, 9,  90, 9,  79, "006600"],
[36,  75,   45,   79,   45,   90, 36, 94, 27, 90, 27, 79, "00CC00"],
[54,  75,   63,   79,   63,   90, 54, 94, 45, 90, 45, 79, "00FF00"],
[72,  75,   81,   79,   81,   90, 72, 94, 63, 90, 63, 79, "66FF99"],
[90,  75,   99,   79,   99,   90, 90, 94, 81, 90, 81, 79, "99FFCC"],
[108, 75,   117,  79,   117,  90, 108,  94, 99, 90, 99, 79, "CCFFFF"],
[126, 75,   135,  79,   135,  90, 126,  94, 117,  90, 117,  79, "CCCCFF"],
[144, 75,   153,  79,   153,  90, 144,  94, 135,  90, 135,  79, "CC99FF"],
[162, 75,   171,  79,   171,  90, 162,  94, 153,  90, 153,  79, "CC66FF"],
[180, 75,   189,  79,   189,  90, 180,  94, 171,  90, 171,  79, "CC33FF"],
[198, 75,   207,  79,   207,  90, 198,  94, 189,  90, 189,  79, "CC00FF"],
[216, 75,   225,  79,   225,  90, 216,  94, 207,  90, 207,  79, "9900CC"],
[9,   90,   18,   94,   18,   105,  9,  109,  0,  105,  0,  94, "003300"],
[27,  90,   36,   94,   36,   105,  27, 109,  18, 105,  18, 94, "009933"],
[45,  90,   54,   94,   54,   105,  45, 109,  36, 105,  36, 94, "33CC33"],
[63,  90,   72,   94,   72,   105,  63, 109,  54, 105,  54, 94, "66FF66"],
[81,  90,   90,   94,   90,   105,  81, 109,  72, 105,  72, 94, "99FF99"],
[99,  90,   108,  94,   108,  105,  99, 109,  90, 105,  90, 94, "CCFFCC"],
[117, 90,   126,  94,   126,  105,  117,  109,  108,  105,  108,  94, "FFFFFF"],
[135, 90,   144,  94,   144,  105,  135,  109,  126,  105,  126,  94, "FFCCFF"],
[153, 90,   162,  94,   162,  105,  153,  109,  144,  105,  144,  94, "FF99FF"],
[171, 90,   180,  94,   180,  105,  171,  109,  162,  105,  162,  94, "FF66FF"],
[189, 90,   198,  94,   198,  105,  189,  109,  180,  105,  180,  94, "FF00FF"],
[207, 90,   216,  94,   216,  105,  207,  109,  198,  105,  198,  94, "CC00CC"],
[225, 90,   234,  94,   234,  105,  225,  109,  216,  105,  216,  94, "660066"],
[18,  105,  27,   109,  27,   120,  18, 124,  9,  120,  9,  109, "336600"],
[36,  105,  45,   109,  45,   120,  36, 124,  27, 120,  27, 109, "009900"],
[54,  105,  63,   109,  63,   120,  54, 124,  45, 120,  45, 109, "66FF33"],
[72,  105,  81,   109,  81,   120,  72, 124,  63, 120,  63, 109, "99FF66"],
[90,  105,  99,   109,  99,   120,  90, 124,  81, 120,  81, 109, "CCFF99"],
[108, 105,  117,  109,  117,  120,  108,  124,  99, 120,  99, 109, "FFFFCC"],
[126, 105,  135,  109,  135,  120,  126,  124,  117,  120,  117,  109, "FFCCCC"],
[144, 105,  153,  109,  153,  120,  144,  124,  135,  120,  135,  109, "FF99CC"],
[162, 105,  171,  109,  171,  120,  162,  124,  153,  120,  153,  109, "FF66CC"],
[180, 105,  189,  109,  189,  120,  180,  124,  171,  120,  171,  109, "FF33CC"],
[198, 105,  207,  109,  207,  120,  198,  124,  189,  120,  189,  109, "CC0099"],
[216, 105,  225,  109,  225,  120,  216,  124,  207,  120,  207,  109, "993399"],
[27,  120,  36,   124,  36,   135,  27, 139,  18, 135,  18, 124, "333300"],
[45,  120,  54,   124,  54,   135,  45, 139,  36, 135,  36, 124, "669900"],
[63,  120,  72,   124,  72,   135,  63, 139,  54, 135,  54, 124, "99FF33"],
[81,  120,  90,   124,  90,   135,  81, 139,  72, 135,  72, 124, "CCFF66"],
[99,  120,  108,  124,  108,  135,  99, 139,  90, 135,  90, 124, "FFFF99"],
[117, 120,  126,  124,  126,  135,  117,  139,  108,  135,  108,  124, "FFCC99"],
[135, 120,  144,  124,  144,  135,  135,  139,  126,  135,  126,  124, "FF9999"],
[153, 120,  162,  124,  162,  135,  153,  139,  144,  135,  144,  124, "FF6699"],
[171, 120,  180,  124,  180,  135,  171,  139,  162,  135,  162,  124, "FF3399"],
[189, 120,  198,  124,  198,  135,  189,  139,  180,  135,  180,  124, "CC3399"],
[207, 120,  216,  124,  216,  135,  207,  139,  198,  135,  198,  124, "990099"],
[36,  135,  45,   139,  45,   150,  36, 154,  27, 150,  27, 139, "666633"],
[54,  135,  63,   139,  63,   150,  54, 154,  45, 150,  45, 139, "99CC00"],
[72,  135,  81,   139,  81,   150,  72, 154,  63, 150,  63, 139, "CCFF33"],
[90,  135,  99,   139,  99,   150,  90, 154,  81, 150,  81, 139, "FFFF66"],
[108, 135,  117,  139,  117,  150,  108,  154,  99, 150,  99, 139, "FFCC66"],
[126, 135,  135,  139,  135,  150,  126,  154,  117,  150,  117,  139, "FF9966"],
[144, 135,  153,  139,  153,  150,  144,  154,  135,  150,  135,  139, "FF6666"],
[162, 135,  171,  139,  171,  150,  162,  154,  153,  150,  153,  139, "FF0066"],
[180, 135,  189,  139,  189,  150,  180,  154,  171,  150,  171,  139, "CC6699"],
[198, 135,  207,  139,  207,  150,  198,  154,  189,  150,  189,  139, "993366"],
[45,  150,  54,   154,  54,   165,  45, 169,  36, 165,  36, 154, "999966"],
[63,  150,  72,   154,  72,   165,  63, 169,  54, 165,  54, 154, "CCCC00"],
[81,  150,  90,   154,  90,   165,  81, 169,  72, 165,  72, 154, "FFFF00"],
[99,  150,  108,  154,  108,  165,  99, 169,  90, 165,  90, 154, "FFCC00"],
[117, 150,  126,  154,  126,  165,  117,  169,  108,  165,  108,  154, "FF9933"],
[135, 150,  144,  154,  144,  165,  135,  169,  126,  165,  126,  154, "FF6600"],
[153, 150,  162,  154,  162,  165,  153,  169,  144,  165,  144,  154, "FF5050"],
[171, 150,  180,  154,  180,  165,  171,  169,  162,  165,  162,  154, "CC0066"],
[189, 150,  198,  154,  198,  165,  189,  169,  180,  165,  180,  154, "660033"],
[54,  165,  63,   169,  63,   180,  54, 184,  45, 180,  45, 169, "996633"],
[72,  165,  81,   169,  81,   180,  72, 184,  63, 180,  63, 169, "CC9900"],
[90,  165,  99,   169,  99,   180,  90, 184,  81, 180,  81, 169, "FF9900"],
[108, 165,  117,  169,  117,  180,  108,  184,  99, 180,  99, 169, "CC6600"],
[126, 165,  135,  169,  135,  180,  126,  184,  117,  180,  117,  169, "FF3300"],
[144, 165,  153,  169,  153,  180,  144,  184,  135,  180,  135,  169, "FF0000"],
[162, 165,  171,  169,  171,  180,  162,  184,  153,  180,  153,  169, "CC0000"],
[180, 165,  189,  169,  189,  180,  180,  184,  171,  180,  171,  169, "990033"],
[63,  180,  72,   184,  72,   195,  63, 199,  54, 195,  54, 184, "663300"],
[81,  180,  90,   184,  90,   195,  81, 199,  72, 195,  72, 184, "996600"],
[99,  180,  108,  184,  108,  195,  99, 199,  90, 195,  90, 184, "CC3300"],
[117, 180,  126,  184,  126,  195,  117,  199,  108,  195,  108,  184, "993300"],
[135, 180,  144,  184,  144,  195,  135,  199,  126,  195,  126,  184, "990000"],
[153, 180,  162,  184,  162,  195,  153,  199,  144,  195,  144,  184, "800000"],
[171, 180,  180,  184,  180,  195,  171,  199,  162,  195,  162,  184, "993333"],
]

BODY = """
<fieldset style="display: flex;">
  <span>
    <span style="display: flex;">
      <fieldset style="display:flex; flex-direction: column; padding: 20px 90px; align-content: space-between">
        <div style="display: flex;justify-content: space-between">
          <label>
            <span>4</span>
            <input id="3" checked="checked" type="checkbox">
          </label>
          <label>
            <input id="2" checked="checked" type="checkbox">
            <span>3</span>
          </label>
        </div>
          <div style="height: 20px;"></div>
        <div style="display: flex;justify-content: space-between">
          <label>
            <span>1</span>
            <input id="0" checked="checked" type="checkbox">
          </label>
          <label>
            <input id="1" checked="checked" type="checkbox">
            <span>2</span>
          </label>
        </div>
      </fieldset>
      <fieldset style="display: flex; flex-direction: column; adjust-content: space-between">
        <button xdh:onevent="All">All</button>
        <button xdh:onevent="None">None</button>
        <div style="height: 10px"></div>
        <button xdh:onevent="Reset">Reset</button>
      </fieldset>
    </span>
    <div style="height: 10px"></div>
    <fieldset style="display: flex; flex-direction: column; align-content: space-between">
      <div>
        <label style="display: flex; align-items: center;">
          <span>R:&nbsp;</span>
          <input id="SR" style="width: 100%" type="range" min="0" max="255" step="1" xdh:onevent="Slide" value="0">
        </label>
        <label style="display: flex; align-items: center;">
          <span>V:&nbsp;</span>
          <input id="SG" style="width: 100%" type="range" min="0" max="255" step="1" xdh:onevent="Slide" value="0">
        </label>
        <label style="display: flex; align-items: center;">
          <span>B:&nbsp;</span>
          <input id="SB"  style="width: 100%"type="range" min="0" max="255" step="1" xdh:onevent="Slide" value="0">
        </label>
      </div>
      <hr>
      <div>
        <label>
          <span>R:</span>
          <input id="NR" xdh:onevent="Adjust" type="number" min="0" max="255" step="5" value="0"  size="3">
        </label>
        <label>
          <span>V:</span>
          <input id="NG" xdh:onevent="Adjust" type="number" min="0" max="255" step="5" value="0"  size="3">
        </label>
        <label>
          <span>B:</span>
          <input id="NB" xdh:onevent="Adjust" type="number" min="0" max="255" step="5" value="0"  size="3">
        </label>
      </div>
    </fieldset>
  </span>
  <fieldset style="align-content: center;">
    <img
      src="data:image/png;base64,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"
      usemap="#colormap" alt="colormap">
    <map id="colormap" name="colormap">
    </map>
  </fieldset>
</fieldset>
"""

C_INIT = """
import neopixel, machine

p = machine.Pin(16)

n = neopixel.NeoPixel(p, 4)

def set(leds):
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
  leds = dom.getValues(["0", "1", "2", "3"])
  command = "set({"

  for led in leds:
    if ( leds[led] == "true" ):
      command += f'{led}: ({R},{G},{B}), '

  mcrcq.execute(command + "})")


def acConnect(dom):
  dom.inner("", BODY)
  map = "<span>"
  for coords_and_id in COORDS_AND_IDS:
    map += "<area style=\"cursor:pointer\" shape=\"poly\" coords=\"{},{},{},{},{},{},{},{},{},{},{},{}\" xdh:onevent=\"Select\" id=\"{}\">".format(*coords_and_id)
  dom.inner("colormap", map + "</span>")
  mcrcq.execute(C_INIT)
  update_(dom, 0, 0, 0)

def acSelect(dom,id):
  R = int(convert_(id[0:2]) * 255 / 99)
  G = int(convert_(id[2:4]) * 255 / 99)
  B = int(convert_(id[4:6]) * 255 / 99)
  dom.setValues(getAllValues_(R, G, B))
  update_(dom, R, G, B)

def acSlide(dom):
  (R,G,B) = dom.getValues(["SR", "SG", "SB"]).values()
  dom.setValues(getNValues_(R, G, B))
  update_(dom, R, G, B)

def acAdjust(dom):
  (R,G,B) = dom.getValues(["NR", "NG", "NB"]).values()
  dom.setValues(getSValues_(R, G, B))
  update_(dom, R, G, B)

def acReset(dom):
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

atlastk.launch(CALLBACKS)
