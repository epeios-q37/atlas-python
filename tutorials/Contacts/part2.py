# You don't need following 3 lines in your own applications.
import sys, os
sys.path.append("../../atlastk")
os.chdir(os.path.dirname(os.path.realpath(__file__)))

import atlastk

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

contacts = EXAMPLE


def display_contacts(dom):
  html = ""

  for contactId in range(len(contacts)):
    contact = contacts[contactId]
    html += f'<tr id="{contactId}" data-xdh-onevent="Select" style="cursor: pointer;">'
    for key in contact:
      html += f'<td>{contact[key]}</td>'
    html += '</td>'

  dom.inner("Content", html)


def ac_connect(dom):
  dom.inner("",open("Main.html").read())
  display_contacts(dom)


CALLBACKS = {
  "": ac_connect,
 }

atlastk.launch(CALLBACKS,None,open("Head.html").read())