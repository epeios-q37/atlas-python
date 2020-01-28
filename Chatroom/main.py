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

import os, sys, threading

sys.path.append("./atlastk")
sys.path.append("../atlastk")

import atlastk as Atlas

messages = []
pseudos = []
lock = threading.Lock()

def readAsset(path):
	return Atlas.readAsset(path, "Chatroom")

class Chatroom:
	def __init__(self):
		self.lastMessage = 0
		self.pseudo = ""

	def buildXML(self):
		xml = Atlas.createXML("XDHTML")
		xml.pushTag( "Messages" )
		xml.putAttribute( "pseudo", self.pseudo )

		global messages, pseudos, lock

		lock.acquire()

		index = len( messages ) - 1

		while index >= self.lastMessage:
			message = messages[index]

			xml.pushTag( "Message" )
			xml.putAttribute( "id", index )
			xml.putAttribute( "pseudo", message['pseudo'] )
			xml.putValue( message['content'] )
			xml.popTag()

			index -= 1

		self.lastMessage = len(messages)

		lock.release()

		xml.popTag()

		return xml

	def displayMessages(self, dom):
		global messages
		
		if len(messages) > self.lastMessage:
			dom.prependLayoutXSL("Board", self.buildXML(), "Messages.xsl")

	def handlePseudo(self, pseudo):
		global pseudos, lock

		lock.acquire()

		if pseudo in pseudos:
			result = False
		else:
			pseudos.append(pseudo)
			result= True

		lock.release()

		return result

	def addMessage(self, pseudo, message):
		global messages, lock
		message = message.strip()

		if message:
			print("'" + pseudo + "': " + message)
			lock.acquire()
			messages.append({'pseudo': pseudo, 'content': message})
			lock.release()

def acConnect(chatroom, dom):
	dom.setLayout("", readAsset("Main.html"))
	dom.focus("Pseudo")
	dom.setTimeout(1000, "Update")
	chatroom.displayMessages(dom)
	
def acSubmitPseudo(chatroom, dom):
	pseudo = dom.getContent("Pseudo").strip()

	if not pseudo:
		dom.alert("Pseudo. can not be empty !")
		dom.setContent("Pseudo", "")
		dom.focus("Pseudo")
	elif chatroom.handlePseudo(pseudo.upper()):
		chatroom.pseudo = pseudo
		dom.addClass("PseudoButton", "hidden")
#		dom.disableElements(["Pseudo", "PseudoButton"])
		dom.disableElement("Pseudo")
		dom.enableElements(["Message", "MessageButton"])
#		dom.setContent("Pseudo", pseudo)
		dom.focus("Message")
		print("\t>>>> New user: " + pseudo)
	else:
		dom.alert("Pseudo. not available!")
		dom.setContent("Pseudo", pseudo)
		dom.focus("Pseudo")

def acSubmitMessage(chatroom, dom):
	message = dom.getContent("Message")
	dom.setContent("Message", "")
	dom.focus("Message")
	chatroom.addMessage(chatroom.pseudo, message)
	chatroom.displayMessages(dom)

def acUpdate(chatroom, dom):
	chatroom.displayMessages(dom)
	dom.setTimeout(1000, "Update")

callbacks = {
		"": acConnect,
		"SubmitPseudo": acSubmitPseudo,
		"SubmitMessage": acSubmitMessage,
		"Update": acUpdate,
	}
		
Atlas.launch(callbacks, Chatroom, readAsset("Head.html"), "Chatroom")
