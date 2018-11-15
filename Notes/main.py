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
_viewModeElements = ["Pattern", "CreateButton", "DescriptionToggling", "ViewNotes"]

def _readAsset(path):
	return Atlas.readAsset(path, "notes")

def _put(note, id, xml ):
	xml.pushTag("Note")
	xml.setAttribute("id", id)

	for key in note:
		xml.pushTag(key)
		xml.setValue(note[key])
		xml.popTag()

	xml.popTag()

class Notes(Atlas.DOM):
	def __init__(this):
		Atlas.DOM.__init__(this)
		this._pattern = ""
		this._hideDescriptions = False
		this._index = 0
		this._notes = [
			{
			'title': '',
			'description': '',
			},
			{
			'title': 'Improve design',
			'description': "Tastes and colors... (aka «CSS aren't my cup of tea...»)",
			},
			{
			'title': 'Fixing bugs',
			'description': "There are bugs ? Really ?",
			},
			{
			'title': 'Implement new functionalities',
			'description': "Although it's almost perfect..., isn't it ?",
			},
		]

	def _handleDescriptions(this,dom):
		if this._hideDescriptions:
			dom.disableElement("ViewDescriptions")
		else:
			dom.enableElement("ViewDescriptions")

	def _displayList(this,dom):
		xml = Atlas.createXML("XDHTML")
		contents = {}

		xml.pushTag("Notes")

		for index in range(len(this._notes)):
			if index == 0: # 0 skipped, as it serves as buffer for the new ones.
				continue
			if this._notes[index]['title'][:len(this._pattern)].lower() == this._pattern:
				_put(this._notes[index], index, xml)
				contents["Description." + str(index)] = this._notes[index]['description']

		dom.setLayoutXSL("Notes", xml, "Notes.xsl")
		dom.setContents(contents)
		dom.enableElements(_viewModeElements)

	def _view(this, dom):
		dom.enableElements(_viewModeElements)
		dom.setContent("Edit." + str(this._index), "")
		this._index = -1

	def _acConnect(this, dom, id):
			dom.setLayout("", _readAsset( "Main.html") )
			this._displayList(dom)

	def _acToggleDescriptions(this, dom, id):
			this._hideDescriptions = dom.getContent(id)=="true"
			this._handleDescriptions(dom)

	def _acSearch(this, dom, id):
			this._pattern = dom.getContent("Pattern").lower()
			this._displayList(dom)

	def _acEdit(this, dom, id):
		index = dom.getContent(id)
		this._index = int(index)
		note = this._notes[this._index]

		dom.setLayout("Edit." + index, _readAsset( "Note.html") )
		dom.setContents({ "Title": note['title'], "Description": note['description'] })
		dom.disableElements(_viewModeElements)
		dom.dressWidgets("Notes")
		dom.focus("Title")

	def _acDelete(this, dom, id):
		if dom.confirm("Are you sure you want to delete this entry ?"):
			this._notes.pop(int(dom.getContent(id)))
			this._displayList(dom)

	def _acSubmit(this, dom, id):
		result = dom.getContents(["Title", "Description"])
		title = result["Title"].strip()
		description = result["Description"]

		if title:
			this._notes[this._index] = { "title": title, "description": description }

			if this._index == 0:
				this._notes.insert(0, { 'title': '', 'description': ''})
				this._displayList( dom )
			else:
				dom.setContents( { "Title." + str(this._index): title, "Description." + str(this._index): description })
				this._view( dom )
		else:
			dom.alert("Title can not be empty !")
			dom.focus("Title")

	def _acCancel( this, dom, id):
		note = this._notes[this._index]

		result = dom.getContents(["Title", "Description"])
		title = result["Title"].strip()
		description = result["Description"]

		if (title != note['title']) or (description != note['description']):
			if dom.confirm("Are you sure you want to cancel your modifications ?"):
				this._view( dom )
		else:
			this._view( dom )

	_callbacks = {	
		"Connect": _acConnect,
		"ToggleDescriptions": _acToggleDescriptions,
		"Search": _acSearch,
		"Edit": _acEdit,
		"Delete": _acDelete,
		"Submit": _acSubmit,
		"Cancel": _acCancel,
	}

	def handle(this,dom,action,id):
		this._callbacks[action](this,dom,id)			

Atlas.launch("Connect", _readAsset("Head.html"), Notes, "notes")
