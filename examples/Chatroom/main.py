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

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("../../atlastk")

import atlastk

messages = []
pseudos = []
lock = threading.Lock()

class Chatroom:
  def __init__(self):
    self.lastMessage = 0
    self.pseudo = ""

  def buildXML(self):
    xml = atlastk.createXML("XDHTML")
    xml.pushTag( "Messages" )
    xml.putAttribute( "pseudo", self.pseudo )

    global messages, pseudos

    with lock:
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

    xml.popTag()

    return xml

  def displayMessages(self, dom):
    global messages
    
    if len(messages) > self.lastMessage:
      dom.begin("Board", self.buildXML(), "Messages.xsl")

  def handlePseudo(self, pseudo):
    global pseudos

    with lock:
      if pseudo in pseudos:
        result = False
      else:
        pseudos.append(pseudo)
        result= True

    return result

  def addMessage(self, pseudo, message):
    global messages
    message = message.strip()

    if message:
      print("'" + pseudo + "': " + message)
      with lock:
        messages.append({'pseudo': pseudo, 'content': message})

def acConnect(chatroom, dom):
  dom.inner("", open("Main.html").read())
  dom.focus("Pseudo")
  chatroom.displayMessages(dom)
  
def acSubmitPseudo(chatroom, dom):
  pseudo = dom.getValue("Pseudo").strip()

  if not pseudo:
    dom.alert("Pseudo. can not be empty !")
    dom.setValue("Pseudo", "")
    dom.focus("Pseudo")
  elif chatroom.handlePseudo(pseudo.upper()):
    chatroom.pseudo = pseudo
    dom.addClass("PseudoButton", "hidden")
#		dom.disableElements(["Pseudo", "PseudoButton"])
    dom.disableElement("Pseudo")
    dom.enableElements(["Message", "MessageButton"])
#		dom.setValue("Pseudo", pseudo)
    dom.focus("Message")
    print("\t>>>> New user: " + pseudo)
  else:
    dom.alert("Pseudo. not available!")
    dom.setValue("Pseudo", pseudo)
    dom.focus("Pseudo")

def acSubmitMessage(chatroom, dom):
  message = dom.getValue("Message")
  dom.setValue("Message", "")
  dom.focus("Message")
  chatroom.addMessage(chatroom.pseudo, message)
  chatroom.displayMessages(dom)
  atlastk.broadcastAction("Update")

CALLBACKS = {
  "": acConnect,
  "SubmitPseudo": acSubmitPseudo,
  "SubmitMessage": acSubmitMessage,
  "Update": lambda chatroom, dom: chatroom.displayMessages(dom),
}

ATK_HEAD = open("Head.html").read()

ATK_USER = Chatroom
    
atlastk.launch(CALLBACKS, globals=globals())
