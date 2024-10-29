import os, json

import atlastk

config = {}

BODY = """
<fieldset>
  <fieldset style="display: flex; flex-direction: column">
    <legend>Device</legend>
    <label style="display: flex; justify-content: space-between; margin: 5px;">
      <span>Token:</span>
      <input id="Token">
    </label>
    <label style="display: flex; justify-content: space-between; margin: 5px;">
      <span>Id:</span>
      <input id="Id">
    </label>
  </fieldset>
  <div style="display: flex; justify-content: space-around; margin: 5px;">
    <button xdh:onevent="Save">Save</button>
  </div>
  <fieldset>
    <output id="Output">Enter token and/or id.</output>
  </fiedlset>
</fieldset>
"""


def acConnect(dom):
  dom.inner("", BODY)

  if "Token" in device:
    dom.setAttribute("Token", "placeholder", "<hidden>")
    dom.focus("Id")
  else:
    dom.focus("Token")

  if "Id" in device:
    dom.setValue("Id", device["Id"])


def acSave(dom):
  token, id = dom.getValues(["Token", "Id"]).values()

  token = token.strip()
  id = id.strip()

  if token == "" and not "Token" in device:
    dom.alert("Please entre a token value!")
    dom.focus("Token")
    return

  if token != "":
    device["Token"] = token

  if id != "":
    device["Id"] = id

  config["Device"] = device

  with open(CONFIG_FILE, "w") as file:
    json.dump(config,file, indent=2)

  dom.setValue("Output", "Config file updated!")

CONFIG_FILE = ( "/home/csimon/q37/epeios/tools/ucuq/remote/wrappers/PYH/" if "Q37_EPEIOS" in os.environ else "../" ) + "ucuq.json"

if os.path.isfile(CONFIG_FILE):
  with open(CONFIG_FILE, "r") as file:
    config = json.load(file)
else:
  config["Device"] = {}

device = config["Device"]

CALLBACKS = {
  "": acConnect,
  "Save": acSave
}

atlastk.launch(CALLBACKS)