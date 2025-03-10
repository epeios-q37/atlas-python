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

import os, sys, threading, uuid

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("../../atlastk")

import atlastk

class Room:
  def __init__(self):
    self.messages = []
    self.pseudos = []
    self.lock = threading.Lock()

  def buildXML(self,session):
    xml = atlastk.create_XML("XDHTML")
    xml.pushTag("Messages")
    xml.putAttribute("pseudo",session.pseudo)

    with self.lock:
      index = len(self.messages) - 1

      while index >= session.lastMessage:
        message = self.messages[index]

        xml.pushTag( "Message" )
        xml.putAttribute( "id", index )
        xml.putAttribute( "pseudo", message['pseudo'] )
        xml.putValue( message['content'] )
        xml.popTag()

        index -= 1

      session.lastMessage = len(self.messages)

    xml.popTag()

    return xml

  def displayMessages(self,session,dom):
   
    if len(self.messages) > session.lastMessage:
      dom.begin("Board", self.buildXML(session), "Messages.xsl")
      
      
  def handlePseudo(self,pseudo):
    with self.lock:
      if pseudo in self.pseudos:
        result = False
      else:
        self.pseudos.append(pseudo)
        result= True

    return result

  def addMessage(self,pseudo,message):
    message = message.strip()

    if message:
      with self.lock:
        self.messages.append({'pseudo': pseudo, 'content': message})

class Session:
  def __init__(self):
    self.room = None
    self.lastMessage = None
    self.pseudo = ""

rooms = {
  str(uuid.uuid4()): {
    "name": "Test 1",
    "core": Room()
  },
  str(uuid.uuid4()): {
    "name": "Test 2",
    "core": Room()
  }
}

rooms = {}

def getRooms():
  xml = atlastk.create_XML("Rooms")

  for id in rooms:
    xml.pushTag("Room")
    xml.putAttribute("id", id)
    xml.putAttribute("URL", atlastk.getAppURL(id))
    xml.putValue(rooms[id]["name"])
    xml.popTag()

  return xml

def displayRooms(dom):
  dom.inner("Rooms",getRooms(), "Rooms.xsl")

def acConnect(session,dom,id):
  if id:
    dom.inner("",open("Room.html").read())
    dom.setValue("Name",rooms[id]["name"])
    session.room = rooms[id]["core"]
    session.lastMessage = 0
    dom.focus("Pseudo")
    session.room.displayMessages(session,dom)    
  else:
    dom.inner("",open("Admin.html").read())
    dom.focus("Name")
    displayRooms(dom)

def acCreate(session,dom):
  global rooms

  name = dom.getValue("Name").strip()

  if not name:
    dom.alert(f"A room name can not be empty!")
  elif any( room["name"] == name for room in rooms.values()):
    dom.alert(f"There is already a room named '{name}'")
  else:
    id = str(uuid.uuid4())
    url = atlastk.getAppURL(id)
    rooms[id]={"name": name, "core": Room()}
    displayRooms(dom)
    dom.setValue("Name", "")

  dom.focus("Name")

def acQRCode(session,dom,id):
  mark = dom.getMark(id)

  if mark:
    url = atlastk.getAppURL(mark)
    dom.inner(dom.lastChild(id), f'<a href="{url}" title="{url}" target="_blank"><img src="https://api.qrserver.com/v1/create-qr-code/?size=125x125&data={url}"/></a>')
    dom.setMark(id,"")

def acSubmitPseudo(session,dom):
  pseudo = dom.getValue("Pseudo").strip()

  room = session.room

  if not pseudo:
    dom.alert("Pseudo. can not be empty !")
    dom.setValue("Pseudo", "")
    dom.focus("Pseudo")
  elif room.handlePseudo(pseudo.upper()):
    session.pseudo = pseudo
    dom.addClass("PseudoButton", "hidden")
    dom.disableElement("Pseudo")
    dom.enableElements(["Message", "MessageButton"])
    dom.focus("Message")
  else:
    dom.alert("Pseudo. not available!")
    dom.setValue("Pseudo", pseudo)
    dom.focus("Pseudo")

def acSubmitMessage(session,dom):
  room = session.room

  message = dom.getValue("Message")
  dom.setValue("Message", "")
  dom.focus("Message")
  room.addMessage(session.pseudo,message)
  room.displayMessages(session,dom)
  atlastk.broadcastAction("Update")     

CALLBACKS = {
  "": acConnect,
  "Create": acCreate,
  "QRCode": acQRCode,
  "SubmitPseudo": acSubmitPseudo,
  "SubmitMessage": acSubmitMessage,
  "Update": lambda session,dom: session.room.displayMessages(session,dom) if session.room else None,
}

ATK_HEAD = open("Head.html").read()

ATK_USER = Session
    
atlastk.launch(CALLBACKS, globals=globals())
