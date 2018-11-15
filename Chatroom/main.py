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

if not "EPEIOS_SRV" in os.environ:
	sys.path.append("Atlas.python.zip")

import Atlas

_messages = []
_pseudos = []
_lock = threading.Lock()

def _readAsset(path):
	return Atlas.readAsset(path, "chatroom")

class Chatroom(Atlas.DOM):
	def __init__(this):
		Atlas.DOM.__init__(this)
		this._lastMessage = 0
		this._pseudo = ""

	def _buildXML(this):
		xml = Atlas.createXML("XDHTML")
		xml.pushTag( "Messages" )
		xml.setAttribute( "pseudo", this._pseudo )

		global _messages, _pseudos, _lock

		_lock.acquire()

		index = len( _messages ) - 1

		while index >= this._lastMessage:
			message = _messages[index]

			xml.pushTag( "Message" )
			xml.setAttribute( "id", index )
			xml.setAttribute( "pseudo", message['pseudo'] )
			xml.setValue( message['content'] )
			xml.popTag()

			index -= 1

		this._lastMessage = len(_messages)

		_lock.release()

		xml.popTag()

		return xml

	def _displayMessages(this, dom):
		global _messages
		
		if len(_messages) >= this._lastMessage:
			id = dom.createElement("span")
			dom.setLayoutXSL(id, this._buildXML(), "Messages.xsl")
			dom.insertChild(id, "Board")

	def _acConnect(this, dom, id):
		dom.setLayout("", _readAsset("Main.html"))
		dom.focus("Pseudo")
		dom.setTimeout(1000, "Update")
		this._displayMessages(dom)
	
	def _handlePseudo(this, pseudo):
		global _pseudos, _lock

		_lock.acquire()

		if pseudo in _pseudos:
			result = False
		else:
			_pseudos.append(pseudo)
			result= True

		_lock.release()

		return result

	def _acSubmitPseudo(this, dom, id):
		pseudo = dom.getContent("Pseudo").strip()

		if not pseudo:
			dom.alert("Pseudo. can not be empty !")
			dom.setContent("Pseudo", "")
			dom.focus("Pseudo")
		elif this._handlePseudo(pseudo.upper()):
			this._pseudo = pseudo
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

	def _addMessage(this, pseudo, message):
		global _messages, _lock
		message = message.strip()

		if message:
			print("'" + pseudo + "': " + message)
			_lock.acquire()
			_messages.append({'pseudo': pseudo, 'content': message})
			_lock.release()

	def _acSubmitMessage(this, dom, id):
		message = dom.getContent("Message")
		dom.setContent("Message", "")
		dom.focus("Message")
		this._addMessage(this._pseudo, message)
		this._displayMessages(dom)

	def _acUpdate(this, dom, id):
		this._displayMessages(dom)
		dom.setTimeout(1000, "Update")

	_callbacks = {
			"Connect": _acConnect,
			"SubmitPseudo": _acSubmitPseudo,
			"SubmitMessage": _acSubmitMessage,
			"Update": _acUpdate,
		}
		
	def handle(this,dom,action,id):
		this._callbacks[action](this,dom,id)

Atlas.launch("Connect", _readAsset("Head.html"), Chatroom, "chatroom")
