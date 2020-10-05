# -*- coding: utf-8 -*-
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

import os, sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("../../atlastk")

import atlastk

view_mode_elements = ["Pattern", "CreateButton", "DescriptionToggling", "ViewNotes"]

def put(note, id, xml ):
  xml.push_tag("Note")
  xml.put_attribute("id", id)

  for key in note:
    xml.put_tag_and_value(key, note[key])

  xml.pop_tag()

class Notes:
  def __init__(self):
    self.pattern = ""
    self.hide_descriptions = False
    self.index = 0
    self.notes = [
      {
      'title': '',
      'description': '',
      },
      {
      'title': 'Improve design',
      'description': "Tastes and colors… (aka «CSS aren't my cup of tea…»)",
      },
      {
      'title': 'Fixing bugs',
      'description': "There are bugs ? Really ?",
      },
      {
      'title': 'Implement new functionalities',
      'description': "Although it's almost perfect…, isn't it ?",
      },
    ]

  def handle_descriptions(self,dom):
    if self.hide_descriptions:
      dom.disable_element("ViewDescriptions")
    else:
      dom.enable_element("ViewDescriptions")

  def display_list(self,dom):
    xml = atlastk.create_XML("XDHTML")
    values = {}

    xml.push_tag("Notes")

    for index in range(len(self.notes)):
      if index == 0: # 0 skipped, as it serves as buffer for the new ones.
        continue
      if self.notes[index]['title'][:len(self.pattern)].lower() == self.pattern:
        put(self.notes[index], index, xml)
        values["Description." + str(index)] = self.notes[index]['description']

    dom.inner("Notes", xml, "Notes.xsl")
    dom.set_values(values)
    dom.enable_elements(view_mode_elements)

  def view(self, dom):
    dom.enable_elements(view_mode_elements)
    dom.set_value("Edit." + str(self.index), "")
    self.index = -1

def ac_connect(notes, dom):
  dom.inner("", open( "Main.html").read() )
  notes.display_list(dom)

def ac_toggle_descriptions(notes, dom, id):
  notes.hide_descriptions = dom.get_value(id)=="true"
  notes.handle_descriptions(dom)

def ac_search(notes, dom):
  notes.pattern = dom.get_value("Pattern").lower()
  notes.display_list(dom)

def ac_edit(notes, dom, id):
  index = dom.get_mark(id)
  notes.index = int(index)
  note = notes.notes[notes.index]

  dom.inner("Edit." + index, open( "Note.html").read() )
  dom.set_values({ "Title": note['title'], "Description": note['description'] })
  dom.disable_elements(view_mode_elements)
  dom.focus("Title")

def ac_delete(notes, dom, id):
  if dom.confirm("Are you sure you want to delete this entry?"):
    notes.notes.pop(int(dom.get_mark(id)))
    notes.display_list(dom)

def ac_submit(notes, dom):
  result = dom.get_values(["Title", "Description"])
  title = result["Title"].strip()
  description = result["Description"]

  if title:
    notes.notes[notes.index] = { "title": title, "description": description }

    if notes.index == 0:
      notes.notes.insert(0, { 'title': '', 'description': ''})
      notes.display_list( dom )
    else:
      dom.set_values( { "Title." + str(notes.index): title, "Description." + str(notes.index): description })
      notes.view( dom )
  else:
    dom.alert("Title can not be empty!")
    dom.focus("Title")

def ac_cancel(notes, dom):
  note = notes.notes[notes.index]

  result = dom.get_values(["Title", "Description"])
  title = result["Title"].strip()
  description = result["Description"]

  if (title != note['title']) or (description != note['description']):
    if dom.confirm("Are you sure you want to cancel your modifications?"):
      notes.view( dom )
  else:
    notes.view( dom )

callbacks = {	
  "": ac_connect,
  "ToggleDescriptions": ac_toggle_descriptions,
  "Search": ac_search,
  "Edit": ac_edit,
  "Delete": ac_delete,
  "Submit": ac_submit,
  "Cancel": ac_cancel,
}

atlastk.launch(callbacks, Notes, open("Head.html").read())
