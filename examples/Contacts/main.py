"""
MIT License

Copyright (c) 2019 Claude SIMON (https://q37.info/s/rmnmqd49)

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

"""
This example focuses on the GUI, as well as some features ot the Atlas toolkit.

Therefore, the 'contacts' object is common to all instances, but its access
is not protected as it should be, to avoid the example being too complex.
"""

import os, sys, enum

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("../../atlastk")

import atlastk

class State(enum.Enum):
  DISPLAY = enum.auto()
  EDIT = enum.auto()
  
class Board:
  def __init__(self):
    self.state = State.DISPLAY
    self.contactId = None

EMPTY_CONTACT = {
    "Name": "",
    "Address": "",
    "Phone": "",
    "Note": ""
}

EXAMPLE = [
  {
    "Name": "Holmes, Sherlock",
    "Address": "221B Baker Street, Londres",
    "Phone": "(use telegraph)",
    "Note": "Great detective!"
  },
  {
    "Name": "Holmes, Mycroft",
    "Address": "Diogenes Club, Pall Mall, Londres",
    "Phone": "(use telegraph)",
    "Note": "Works for the British government.\nBrother of Holmes, Sherlock."
  },
  {
    "Name": "Tintin",
    "Address": "Château de Moulinsart",
    "Phone": "421",
    "Note": "Has a dog named Snowy."
  },
  {
    "Name": "Tournesol, Tryphon (prof.)",
    "Address": "Château de Moulinsart",
    "Phone": "421",
    "Note": "Creator of the Bianca rose."
  }
]

# Will be filed later.
fields = []

# contacts = []
contacts = EXAMPLE


def displayContact(contactId,dom):
  dom.setValues(EMPTY_CONTACT if contactId == None else contacts[contactId])


def displayContacts(contacts,dom):
  html = ""

  for contactId in range(len(contacts)):
    contact = contacts[contactId]
    html += f"""
<tr id="{contactId}" xdh:onevent="Select" style="cursor: pointer;">
  <td>{contact["Name"]}</td>
  <td>{contact["Address"]}</td>
  <td>{contact["Phone"]}</td>
  <td>{contact["Note"]}</td>
</td>
"""

  dom.inner("Content", html)


def updateOutfit(board, dom):
  if board.state == State.DISPLAY:
    dom.disableElement("HideDisplay")
    dom.enableElement("HideEdition")
    dom.disableElements(fields)
    if board.contactId != None:
      dom.disableElement("HideDisplayAndSelect")
    else:
      dom.enableElement("HideDisplayAndSelect")
  elif board.state == State.EDIT:
    dom.enableElements(("HideDisplay","HideDisplayAndSelect"))
    dom.disableElement("HideEdition")
    dom.enableElements(fields)
  else:
    raise Exception("Unknown state!")


def acConnect(board, dom):
  dom.inner("",open("Main.html").read())
  displayContacts(contacts,dom)
  board.state = State.DISPLAY
  updateOutfit(board,dom)


def acRefresh(board,dom):
  displayContacts(contacts,dom)


def acSelect(board,dom,id):
  contactId = int(id)

  displayContact(contactId,dom)
  board.state = State.DISPLAY
  board.contactId = contactId

  updateOutfit(board, dom)


def acDelete(board,dom):
  if board.contactId == None:
    raise Exception("No contact selected!")

  contacts.pop(board.contactId)
  board.contactId = None;

  displayContact(None,dom)

  updateOutfit(board,dom)

  atlastk.broadcastAction("Refresh")


def edit(board,dom):
  contactId = board.contactId

  board.state = State.EDIT

  displayContact(contactId,dom)

  updateOutfit(board,dom)

  dom.focus("Name")


def acNew(board,dom):
  board.contactId = None

  edit(board,dom)


def acEdit(board,dom):
  if board.contactId == None:
    raise Exception("No contact selected!")  

  edit(board,dom)


def acSubmit(board,dom):
  idsAndValues = dom.getValues(fields)

  if not idsAndValues['Name'].strip():
    dom.alert("The name field can not be empty!")
    return

  if board.contactId == None or board.contactId >= len(contacts):
    contacts.append(idsAndValues)
    displayContact(None,dom)
  else:
    contacts[board.contactId] = idsAndValues

  atlastk.broadcastAction("Refresh")

  board.state = State.DISPLAY

  updateOutfit(board,dom)


def acCancel(board,dom):
  if not dom.confirm("Are you sure?"):
    return

  displayContact(board.contactId,dom)

  board.state = State.DISPLAY

  updateOutfit(board,dom)


CALLBACKS = {
  "": acConnect,
  "Refresh": acRefresh,
  "Select": acSelect,
  "Delete": acDelete,
  "New": acNew,
  "Edit": acEdit,
  "Submit": acSubmit,
  "Cancel": acCancel
}

for key in EMPTY_CONTACT.keys():
  fields.append(key)

atlastk.launch(CALLBACKS,Board,open("Head.html").read())
