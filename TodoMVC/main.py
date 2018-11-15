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
def _readAsset(path):
	return Atlas.readAsset(path, "TodoMVC")

class TodoMVC(Atlas.DOM):
	def __init__(this):
		Atlas.DOM.__init__(this)
		this._exclude = None
		this._index = -1
		this._todos = []

		if False:	# At 'True' for testing purpose.
			this._todos.append({"label": "Todo 1", "completed": False })
			this._todos.append({"label": "Todo 2", "completed": True })

	def _itemsLeft(this):
		count = 0

		for index in range(len(this._todos)):
			if not this._todos[index]['completed']:
				count += 1

		return count

	def _push(this, todo, id, xml):
		xml.pushTag("Todo")
		xml.setAttribute("id", id)
		xml.setAttribute("completed", "true" if todo['completed'] else "false")
		xml.setValue(todo['label'])
		xml.popTag()

	def _displayCount(this, dom, count):
		text = ""

		if count == 1:
			text = "1 item left"
		elif count != 0:
			text = str(count) + " items left"

		dom.setContent("Count", text)

	def _handleCount(this, dom):
		count = this._itemsLeft()

		if count != len(this._todos):
			dom.disableElement("HideClearCompleted")
		else:
			dom.enableElement("HideClearCompleted")

		this._displayCount(dom, count)

	def _displayTodos(this, dom):
		xml = Atlas.createXML("XDHTML")

		xml.pushTag("Todos")

		for index in range(len(this._todos)):
			todo = this._todos[index]

			if (this._exclude == None) or (todo['completed'] != this._exclude):
				this._push(todo, index, xml)

		xml.popTag()

		dom.setLayoutXSL("Todos", xml, "Todos.xsl")
		this._handleCount(dom)

	def _acConnect(this, dom, id):
		dom.setLayout("", _readAsset("Main.html"))
		dom.focus("Input")
		this._displayTodos(dom)
		dom.disableElements([ "HideActive", "HideCompleted"])

	def _submitNew(this, dom):
		content = dom.getContent("Input").strip()
		dom.setContent("Input", "")

		if content:
			this._todos.insert(0, {'label': content, 'completed': False})
			this._displayTodos(dom)

	def _submitModification(this, dom):
		index = this._index
		this._index = -1

		content = dom.getContent("Input." + str(index).strip())
		dom.setContent("Input." + str(index), "")

		if content:
			this._todos[index]['label'] = content

			dom.setContent("Label." + str(index), content)

			dom.removeClasses({"View." + str(index): "hide", "Todo." + str(index): "editing"})
		else:
			this._todos.pop(index)
			this._displayTodos(dom)

	def _acDestroy(this, dom, id):
		this._todos.pop(int(dom.getContent(id)))
		this._displayTodos(dom)

	def _acToggle(this, dom, id):
		index = int(id)
		this._todos[index]['completed'] = not this._todos[index]['completed']

		dom.toggleClass("Todo." + id, "completed")
		dom.toggleClass("Todo." + id, "active")

		this._handleCount(dom)

	def _acAll(this, dom, id):
		this._exclude = None

		dom.addClass("All", "selected")
		dom.removeClasses({"Active": "selected", "Completed": "selected"})
		dom.disableElements(["HideActive", "HideCompleted"])

	def _acActive(this, dom, id):
		this._exclude = True

		dom.addClass("Active", "selected")
		dom.removeClasses({"All": "selected", "Completed": "selected"})
		dom.disableElement("HideActive")
		dom.enableElement("HideCompleted")

	def _acCompleted(this, dom, id):
		this._exclude = False

		dom.addClass("Completed", "selected")
		dom.removeClasses({"All": "selected", "Active": "selected"})
		dom.disableElement("HideCompleted")
		dom.enableElement("HideActive")

	def _acClear(this, dom, id):
		index = len(this._todos)

		while index:
			index -= 1

			if this._todos[index]['completed']:
				this._todos.pop(index)

		this._displayTodos(dom)

	def _acEdit(this, dom, id):
		content = dom.getContent(id)
		this._index = int(content)

		dom.addClasses({"View." + content: "hide", id: "editing"})
		dom.setContent("Input." + content, this._todos[this._index]['label'])
		dom.focus("Input." + content)

	def _acCancel(this, dom, id):
		index = str(this._index)
		this._index = -1

		dom.setContent("Input." + index, "")
		dom.removeClasses({"View." + index: "hide", "Todo." + index: "editing"})

	_callbacks = {
		"Connect": _acConnect,
		"Submit": lambda this, dom, id: this._submitNew(dom) if this._index == -1 else this._submitModification(dom),
		"Destroy": _acDestroy,
		"Toggle": _acToggle,
		"All": _acAll,
		"Active": _acActive,
		"Completed": _acCompleted,
		"Clear": _acClear,
		"Edit": _acEdit,
		"Cancel": _acCancel,
	}

	def handle(this,dom,action,id):
		this._callbacks[action](this,dom,id)

Atlas.launch("Connect", _readAsset("HeadDEMO.html"), TodoMVC, "TodoMVC")
