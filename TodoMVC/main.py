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

sys.path.append("./Atlas.python.zip")
sys.path.append("../Atlas.python.zip")

import Atlas
def readAsset(path):
	return Atlas.readAsset(path, "TodoMVC")

class TodoMVC:
	def __init__(this):
		this.exclude = None
		this.index = -1
		this.todos = []

		if False:	# Set to 'True' for testing purpose.
			this.todos.append({"label": "Todo 1", "completed": False })
			this.todos.append({"label": "Todo 2", "completed": True })

	def itemsLeft(this):
		count = 0

		for index in range(len(this.todos)):
			if not this.todos[index]['completed']:
				count += 1

		return count

	def push(this, todo, id, xml):
		xml.pushTag("Todo")
		xml.setAttribute("id", id)
		xml.setAttribute("completed", "true" if todo['completed'] else "false")
		xml.setValue(todo['label'])
		xml.popTag()

	def displayCount(this, dom, count):
		text = ""

		if count == 1:
			text = "1 item left"
		elif count != 0:
			text = str(count) + " items left"

		dom.setContent("Count", text)

	def handleCount(this, dom):
		count = this.itemsLeft()

		if count != len(this.todos):
			dom.disableElement("HideClearCompleted")
		else:
			dom.enableElement("HideClearCompleted")

		this.displayCount(dom, count)

	def displayTodos(this, dom):
		xml = Atlas.createXML("XDHTML")

		xml.pushTag("Todos")

		for index in range(len(this.todos)):
			todo = this.todos[index]

			if (this.exclude == None) or (todo['completed'] != this.exclude):
				this.push(todo, index, xml)

		xml.popTag()

		dom.setLayoutXSL("Todos", xml, "Todos.xsl")
		this.handleCount(dom)

	def submitNew(this, dom):
		content = dom.getContent("Input").strip()
		dom.setContent("Input", "")

		if content:
			this.todos.insert(0, {'label': content, 'completed': False})
			this.displayTodos(dom)

	def submitModification(this, dom):
		index = this.index
		this.index = -1

		content = dom.getContent("Input." + str(index)).strip()
		dom.setContent("Input." + str(index), "")

		if content:
			this.todos[index]['label'] = content

			dom.setContent("Label." + str(index), content)

			dom.removeClasses({"View." + str(index): "hide", "Todo." + str(index): "editing"})
		else:
			this.todos.pop(index)
			this.displayTodos(dom)

def acConnect(this, dom, id):
	dom.setLayout("", readAsset("Main.html"))
	dom.focus("Input")
	this.displayTodos(dom)
	dom.disableElements(["HideActive", "HideCompleted"])

def acDestroy(this, dom, id):
	this.todos.pop(int(dom.getContent(id)))
	this.displayTodos(dom)

def acToggle(this, dom, id):
	index = int(id)
	this.todos[index]['completed'] = not this.todos[index]['completed']

	dom.toggleClass("Todo." + id, "completed")
	dom.toggleClass("Todo." + id, "active")

	this.handleCount(dom)

def acAll(this, dom, id):
	this.exclude = None

	dom.addClass("All", "selected")
	dom.removeClasses({"Active": "selected", "Completed": "selected"})
	dom.disableElements(["HideActive", "HideCompleted"])

def acActive(this, dom, id):
	this.exclude = True

	dom.addClass("Active", "selected")
	dom.removeClasses({"All": "selected", "Completed": "selected"})
	dom.disableElement("HideActive")
	dom.enableElement("HideCompleted")

def acCompleted(this, dom, id):
	this.exclude = False

	dom.addClass("Completed", "selected")
	dom.removeClasses({"All": "selected", "Active": "selected"})
	dom.disableElement("HideCompleted")
	dom.enableElement("HideActive")

def acClear(this, dom, id):
	index = len(this.todos)

	while index:
		index -= 1

		if this.todos[index]['completed']:
			this.todos.pop(index)

	this.displayTodos(dom)

def acEdit(this, dom, id):
	content = dom.getContent(id)
	this.index = int(content)

	dom.addClasses({"View." + content: "hide", id: "editing"})
	dom.setContent("Input." + content, this.todos[this.index]['label'])
	dom.focus("Input." + content)

def acCancel(this, dom, id):
	index = str(this.index)
	this.index = -1

	dom.setContent("Input." + index, "")
	dom.removeClasses({"View." + index: "hide", "Todo." + index: "editing"})

callbacks = {
	"Connect": acConnect,
	"Submit": lambda this, dom, id: this.submitNew(dom) if this.index == -1 else this.submitModification(dom),
	"Destroy": acDestroy,
	"Toggle": acToggle,
	"All": acAll,
	"Active": acActive,
	"Completed": acCompleted,
	"Clear": acClear,
	"Edit": acEdit,
	"Cancel": acCancel,
}

Atlas.launch("Connect", callbacks, TodoMVC, readAsset("HeadDEMO.html"), "TodoMVC")
