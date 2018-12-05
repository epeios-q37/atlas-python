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

import os, sys, threading

sys.path.append("./Atlas.python.zip")
sys.path.append("../Atlas.python.zip")

import Atlas

messages = []
pseudos = []
lock = threading.Lock()

def readAsset(path):
	return Atlas.readAsset(path, "chatroom")

class Chatroom:
	def __init__(this):
		this.lastMessage = 0
		this.pseudo = ""

	def buildXML(this):
		xml = Atlas.createXML("XDHTML")
		xml.pushTag( "Messages" )
		xml.setAttribute( "pseudo", this.pseudo )

		global messages, pseudos, lock

		lock.acquire()

		index = len( messages ) - 1

		while index >= this.lastMessage:
			message = messages[index]

			xml.pushTag( "Message" )
			xml.setAttribute( "id", index )
			xml.setAttribute( "pseudo", message['pseudo'] )
			xml.setValue( message['content'] )
			xml.popTag()

			index -= 1

		this.lastMessage = len(messages)

		lock.release()

		xml.popTag()

		return xml

	def displayMessages(this, dom):
		global messages
		
		if len(messages) >= this.lastMessage:
			id = dom.createElement("span")
			dom.setLayoutXSL(id, this.buildXML(), "Messages.xsl")
			dom.insertChild(id, "Board")

	def handlePseudo(this, pseudo):
		global pseudos, lock

		lock.acquire()

		if pseudo in pseudos:
			result = False
		else:
			pseudos.append(pseudo)
			result= True

		lock.release()

		return result

	def addMessage(this, pseudo, message):
		global messages, lock
		message = message.strip()

		if message:
			print("'" + pseudo + "': " + message)
			lock.acquire()
			messages.append({'pseudo': pseudo, 'content': message})
			lock.release()

def acConnect(this, dom, id):
	dom.setLayout("", readAsset("Main.html"))
	dom.focus("Pseudo")
	dom.setTimeout(1000, "Update")
	this.displayMessages(dom)
	
def acSubmitPseudo(this, dom, id):
	pseudo = dom.getContent("Pseudo").strip()

	if not pseudo:
		dom.alert("Pseudo. can not be empty !")
		dom.setContent("Pseudo", "")
		dom.focus("Pseudo")
	elif this.handlePseudo(pseudo.upper()):
		this.pseudo = pseudo
		dom.addClass("PseudoButton", "hidden")
		dom.disableElements(["Pseudo", "PseudoButton"])
		dom.enableElements(["Message", "MessageButton"])
		dom.setContent("Pseudo", pseudo)
		dom.focus("Message")
		print("\t>>>> New user: " + pseudo)
	else:
		dom.alert("Pseudo. not available !")
		dom.setContent("Pseudo", pseudo)
		dom.focus("Pseudo")

def acSubmitMessage(this, dom, id):
	message = dom.getContent("Message")
	dom.setContent("Message", "")
	dom.focus("Message")
	this.addMessage(this.pseudo, message)
	this.displayMessages(dom)

def acUpdate(this, dom, id):
	this.displayMessages(dom)
	dom.setTimeout(1000, "Update")

callbacks = {
		"Connect": acConnect,
		"SubmitPseudo": acSubmitPseudo,
		"SubmitMessage": acSubmitMessage,
		"Update": acUpdate,
	}
		
Atlas.launch("Connect", callbacks, Chatroom, readAsset("Head.html"), "chatroom")
