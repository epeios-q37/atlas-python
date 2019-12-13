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

sys.path.append("./atlastk")
sys.path.append("../atlastk")

import atlastk as Atlas

viewModeElements = ["Pattern", "CreateButton", "DescriptionToggling", "ViewNotes"]

def readAsset(path):
	return Atlas.readAsset(path, "Notes")

def put(note, id, xml ):
	xml.pushTag("Note")
	xml.putAttribute("id", id)

	for key in note:
		xml.putTagAndValue(key, note[key])

	xml.popTag()

class Notes:
	def __init__(self):
		self.pattern = ""
		self.hideDescriptions = False
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

	def handleDescriptions(self,dom):
		if self.hideDescriptions:
			dom.disableElement("ViewDescriptions")
		else:
			dom.enableElement("ViewDescriptions")

	def displayList(self,dom):
		xml = Atlas.createXML("XDHTML")
		contents = {}

		xml.pushTag("Notes")

		for index in range(len(self.notes)):
			if index == 0: # 0 skipped, as it serves as buffer for the new ones.
				continue
			if self.notes[index]['title'][:len(self.pattern)].lower() == self.pattern:
				put(self.notes[index], index, xml)
				contents["Description." + str(index)] = self.notes[index]['description']

		dom.setLayoutXSL("Notes", xml, "Notes.xsl")
		dom.setContents(contents)
		dom.enableElements(viewModeElements)

	def view(self, dom):
		dom.enableElements(viewModeElements)
		dom.setContent("Edit." + str(self.index), "")
		self.index = -1

def acConnect(notes, dom):
		dom.setLayout("", readAsset( "Main.html") )
		notes.displayList(dom)

def acToggleDescriptions(notes, dom, id):
		notes.hideDescriptions = dom.getContent(id)=="true"
		notes.handleDescriptions(dom)

def acSearch(notes, dom):
		notes.pattern = dom.getContent("Pattern").lower()
		notes.displayList(dom)

def acEdit(notes, dom, id):
	index = dom.getContent(id)
	notes.index = int(index)
	note = notes.notes[notes.index]

	dom.setLayout("Edit." + index, readAsset( "Note.html") )
	dom.setContents({ "Title": note['title'], "Description": note['description'] })
	dom.disableElements(viewModeElements)
	dom.dressWidgets("Notes")
	dom.focus("Title")

def acDelete(notes, dom, id):
	if dom.confirm("Are you sure you want to delete this entry?"):
		notes.notes.pop(int(dom.getContent(id)))
		notes.displayList(dom)

def acSubmit(notes, dom):
	result = dom.getContents(["Title", "Description"])
	title = result["Title"].strip()
	description = result["Description"]

	if title:
		notes.notes[notes.index] = { "title": title, "description": description }

		if notes.index == 0:
			notes.notes.insert(0, { 'title': '', 'description': ''})
			notes.displayList( dom )
		else:
			dom.setContents( { "Title." + str(notes.index): title, "Description." + str(notes.index): description })
			notes.view( dom )
	else:
		dom.alert("Title can not be empty!")
		dom.focus("Title")

def acCancel( notes, dom):
	note = notes.notes[notes.index]

	result = dom.getContents(["Title", "Description"])
	title = result["Title"].strip()
	description = result["Description"]

	if (title != note['title']) or (description != note['description']):
		if dom.confirm("Are you sure you want to cancel your modifications?"):
			notes.view( dom )
	else:
		notes.view( dom )

callbacks = {	
	"": acConnect,
	"ToggleDescriptions": acToggleDescriptions,
	"Search": acSearch,
	"Edit": acEdit,
	"Delete": acDelete,
	"Submit": acSubmit,
	"Cancel": acCancel,
}

Atlas.launch(callbacks, Notes, readAsset("Head.html"), "Notes")
