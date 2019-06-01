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

sys.path.append("./Atlas.python.zip")
sys.path.append("../Atlas.python.zip")

import atlastk as Atlas

def readAsset(path):
	return Atlas.readAsset(path, "TodoMVC")

class TodoMVC:
	def __init__(self):
		self.exclude = None
		self.index = -1
		self.todos = []

		if False:	# Set to 'True' for testing purpose.
			self.todos.append({"label": "Todo 1", "completed": False })
			self.todos.append({"label": "Todo 2", "completed": True })

	def itemsLeft(self):
		count = 0

		for index in range(len(self.todos)):
			if not self.todos[index]['completed']:
				count += 1

		return count

	def push(self, todo, id, xml):
		xml.pushTag("Todo")
		xml.setAttribute("id", id)
		xml.setAttribute("completed", "true" if todo['completed'] else "false")
		xml.setValue(todo['label'])
		xml.popTag()

	def displayCount(self, dom, count):
		text = ""

		if count == 1:
			text = "1 item left"
		elif count != 0:
			text = str(count) + " items left"

		dom.setContent("Count", text)

	def handleCount(self, dom):
		count = self.itemsLeft()

		if count != len(self.todos):
			dom.disableElement("HideClearCompleted")
		else:
			dom.enableElement("HideClearCompleted")

		self.displayCount(dom, count)

	def displayTodos(self, dom):
		xml = Atlas.createXML("XDHTML")

		xml.pushTag("Todos")

		for index in range(len(self.todos)):
			todo = self.todos[index]

			if (self.exclude == None) or (todo['completed'] != self.exclude):
				self.push(todo, index, xml)

		xml.popTag()

		dom.setLayoutXSL("Todos", xml, "Todos.xsl")
		self.handleCount(dom)

	def submitNew(self, dom):
		content = dom.getContent("Input").strip()
		dom.setContent("Input", "")

		if content:
			self.todos.insert(0, {'label': content, 'completed': False})
			self.displayTodos(dom)

	def submitModification(self, dom):
		index = self.index
		self.index = -1

		content = dom.getContent("Input." + str(index)).strip()
		dom.setContent("Input." + str(index), "")

		if content:
			self.todos[index]['label'] = content

			dom.setContent("Label." + str(index), content)

			dom.removeClasses({"View." + str(index): "hide", "Todo." + str(index): "editing"})
		else:
			self.todos.pop(index)
			self.displayTodos(dom)

def acConnect(self, dom, id):
	dom.setLayout("", readAsset("Main.html"))
	dom.focus("Input")
	self.displayTodos(dom)
	dom.disableElements(["HideActive", "HideCompleted"])

def acDestroy(self, dom, id):
	self.todos.pop(int(dom.getContent(id)))
	self.displayTodos(dom)

def acToggle(self, dom, id):
	index = int(id)
	self.todos[index]['completed'] = not self.todos[index]['completed']

	dom.toggleClass("Todo." + id, "completed")
	dom.toggleClass("Todo." + id, "active")

	self.handleCount(dom)

def acAll(self, dom, id):
	self.exclude = None

	dom.addClass("All", "selected")
	dom.removeClasses({"Active": "selected", "Completed": "selected"})
	dom.disableElements(["HideActive", "HideCompleted"])

def acActive(self, dom, id):
	self.exclude = True

	dom.addClass("Active", "selected")
	dom.removeClasses({"All": "selected", "Completed": "selected"})
	dom.disableElement("HideActive")
	dom.enableElement("HideCompleted")

def acCompleted(self, dom, id):
	self.exclude = False

	dom.addClass("Completed", "selected")
	dom.removeClasses({"All": "selected", "Active": "selected"})
	dom.disableElement("HideCompleted")
	dom.enableElement("HideActive")

def acClear(self, dom, id):
	index = len(self.todos)

	while index:
		index -= 1

		if self.todos[index]['completed']:
			self.todos.pop(index)

	self.displayTodos(dom)

def acEdit(self, dom, id):
	content = dom.getContent(id)
	self.index = int(content)

	dom.addClasses({"View." + content: "hide", id: "editing"})
	dom.setContent("Input." + content, self.todos[self.index]['label'])
	dom.focus("Input." + content)

def acCancel(self, dom, id):
	index = str(self.index)
	self.index = -1

	dom.setContent("Input." + index, "")
	dom.removeClasses({"View." + index: "hide", "Todo." + index: "editing"})

callbacks = {
	"": acConnect,
	"Submit": lambda self, dom, id: self.submitNew(dom) if self.index == -1 else self.submitModification(dom),
	"Destroy": acDestroy,
	"Toggle": acToggle,
	"All": acAll,
	"Active": acActive,
	"Completed": acCompleted,
	"Clear": acClear,
	"Edit": acEdit,
	"Cancel": acCancel,
}

Atlas.launch(callbacks, TodoMVC, readAsset("HeadDEMO.html"), "TodoMVC")
