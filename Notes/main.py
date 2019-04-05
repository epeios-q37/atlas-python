# -*- coding: utf-8 -*-
""" 
	Copyright (C) 2018 Claude SIMON (http://q37.info/contact/).

	This file is part of XDHq.

	XDHq is free software: you can redistribute it and/or
	modify it under the terms of the GNU Affero General Public License as
	published by the Free Software Foundation, either version 3 of the
	License, or (at your option) any later version.

	XDHq is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
	Affero General Public License for more details.

	You should have received a copy of the GNU Affero General Public License
	along with XDHq If not, see <http://www.gnu.org/licenses/>.
 """

import os, sys

if not "EPEIOS_SRV" in os.environ:
	sys.path.append("Atlas.python.zip")

import Atlas

viewModeElements = ["Pattern", "CreateButton", "DescriptionToggling", "ViewNotes"]

def readAsset(path):
	return Atlas.readAsset(path, "notes")

def put(note, id, xml ):
	xml.pushTag("Note")
	xml.setAttribute("id", id)

	for key in note:
		xml.pushTag(key)
		xml.setValue(note[key])
		xml.popTag()

	xml.popTag()

class Notes:
	def __init__(this):
		this.pattern = ""
		this.hideDescriptions = False
		this.index = 0
		this.notes = [
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

	def handleDescriptions(this,dom):
		if this.hideDescriptions:
			dom.disableElement("ViewDescriptions")
		else:
			dom.enableElement("ViewDescriptions")

	def displayList(this,dom):
		xml = Atlas.createXML("XDHTML")
		contents = {}

		xml.pushTag("Notes")

		for index in range(len(this.notes)):
			if index == 0: # 0 skipped, as it serves as buffer for the new ones.
				continue
			if this.notes[index]['title'][:len(this.pattern)].lower() == this.pattern:
				put(this.notes[index], index, xml)
				contents["Description." + str(index)] = this.notes[index]['description']

		dom.setLayoutXSL("Notes", xml, "Notes.xsl")
		dom.setContents(contents)
		dom.enableElements(viewModeElements)

	def view(this, dom):
		dom.enableElements(viewModeElements)
		dom.setContent("Edit." + str(this.index), "")
		this.index = -1

def acConnect(this, dom, id):
		dom.setLayout("", readAsset( "Main.html") )
		this.displayList(dom)

def acToggleDescriptions(this, dom, id):
		this.hideDescriptions = dom.getContent(id)=="true"
		this.handleDescriptions(dom)

def acSearch(this, dom, id):
		this.pattern = dom.getContent("Pattern").lower()
		this.displayList(dom)

def acEdit(this, dom, id):
	index = dom.getContent(id)
	this.index = int(index)
	note = this.notes[this.index]

	dom.setLayout("Edit." + index, readAsset( "Note.html") )
	dom.setContents({ "Title": note['title'], "Description": note['description'] })
	dom.disableElements(viewModeElements)
	dom.dressWidgets("Notes")
	dom.focus("Title")

def acDelete(this, dom, id):
	if dom.confirm("Are you sure you want to delete this entry ?"):
		this.notes.pop(int(dom.getContent(id)))
		this.displayList(dom)

def acSubmit(this, dom, id):
	result = dom.getContents(["Title", "Description"])
	title = result["Title"].strip()
	description = result["Description"]

	if title:
		this.notes[this.index] = { "title": title, "description": description }

		if this.index == 0:
			this.notes.insert(0, { 'title': '', 'description': ''})
			this.displayList( dom )
		else:
			dom.setContents( { "Title." + str(this.index): title, "Description." + str(this.index): description })
			this.view( dom )
	else:
		dom.alert("Title can not be empty !")
		dom.focus("Title")

def acCancel( this, dom, id):
	note = this.notes[this.index]

	result = dom.getContents(["Title", "Description"])
	title = result["Title"].strip()
	description = result["Description"]

	if (title != note['title']) or (description != note['description']):
		if dom.confirm("Are you sure you want to cancel your modifications ?"):
			this.view( dom )
	else:
		this.view( dom )

callbacks = {	
	"": acConnect,
	"ToggleDescriptions": acToggleDescriptions,
	"Search": acSearch,
	"Edit": acEdit,
	"Delete": acDelete,
	"Submit": acSubmit,
	"Cancel": acCancel,
}

Atlas.launch(callbacks, Notes, readAsset("Head.html"), "notes")
