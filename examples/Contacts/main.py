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


def display_contact(contactId,dom):
  dom.set_values(EMPTY_CONTACT if contactId == None else contacts[contactId])


def display_contacts(contacts,dom):
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


def update_outfit(board, dom):
  if board.state == State.DISPLAY:
    dom.disable_element("HideDisplay")
    dom.enable_element("HideEdition")
    dom.disable_elements(fields)
    if board.contactId != None:
      dom.disable_element("HideDisplayAndSelect")
    else:
      dom.enable_element("HideDisplayAndSelect")
  elif board.state == State.EDIT:
    dom.enable_elements(("HideDisplay","HideDisplayAndSelect"))
    dom.disable_element("HideEdition")
    dom.enable_elements(fields)
  else:
    raise Exception("Unknown state!")


def ac_connect(board, dom):
  dom.inner("",open("Main.html").read())
  display_contacts(contacts,dom)
  board.state = State.DISPLAY
  update_outfit(board,dom)


def ac_refresh(board,dom):
  display_contacts(contacts,dom)


def ac_select(board,dom,id):
  contactId = int(id)

  display_contact(contactId,dom)
  board.state = State.DISPLAY
  board.contactId = contactId

  update_outfit(board, dom)


def ac_delete(board,dom):
  if board.contactId == None:
    raise Exception("No contact selected!")

  contacts.pop(board.contactId)
  board.contactId = None;

  display_contact(None,dom)

  update_outfit(board,dom)

  atlastk.broadcast_action("Refresh")


def edit(board,dom):
  contactId = board.contactId

  board.state = State.EDIT

  display_contact(contactId,dom)

  update_outfit(board,dom)

  dom.focus("Name")


def ac_new(board,dom):
  board.contactId = None

  edit(board,dom)


def ac_edit(board,dom):
  if board.contactId == None:
    raise Exception("No contact selected!")  

  edit(board,dom)


def ac_submit(board,dom):
  idsAndValues = dom.get_values(fields)

  if not idsAndValues['Name'].strip():
    dom.alert("The name field can not be empty!")
    return

  if board.contactId == None or board.contactId >= len(contacts):
    contacts.append(idsAndValues)
    display_contact(None,dom)
  else:
    contacts[board.contactId] = idsAndValues

  atlastk.broadcast_action("Refresh")

  board.state = State.DISPLAY

  update_outfit(board,dom)


def ac_cancel(board,dom):
  if not dom.confirm("Are you sure?"):
    return

  display_contact(board.contactId,dom)

  board.state = State.DISPLAY

  update_outfit(board,dom)


CALLBACKS = {
  "": ac_connect,
  "Refresh": ac_refresh,
  "Select": ac_select,
  "Delete": ac_delete,
  "New": ac_new,
  "Edit": ac_edit,
  "Submit": ac_submit,
  "Cancel": ac_cancel
}

for key in EMPTY_CONTACT.keys():
  fields.append(key)

atlastk.launch(CALLBACKS,Board,open("Head.html").read())
