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

  def build_xml(self,session):
    xml = atlastk.create_XML("XDHTML")
    xml.push_tag("Messages")
    xml.put_attribute("pseudo",session.pseudo)

    with self.lock:
      index = len(self.messages) - 1

      while index >= session.last_message:
        message = self.messages[index]

        xml.push_tag( "Message" )
        xml.put_attribute( "id", index )
        xml.put_attribute( "pseudo", message['pseudo'] )
        xml.put_value( message['content'] )
        xml.pop_tag()

        index -= 1

      session.last_message = len(self.messages)

    xml.pop_tag()

    return xml

  def display_messages(self,session,dom):
   
    if len(self.messages) > session.last_message:
      dom.begin("Board", self.build_xml(session), "Messages.xsl")
      
      
  def handle_pseudo(self,pseudo):
    with self.lock:
      if pseudo in self.pseudos:
        result = False
      else:
        self.pseudos.append(pseudo)
        result= True

    return result

  def add_message(self,pseudo,message):
    message = message.strip()

    if message:
      with self.lock:
        self.messages.append({'pseudo': pseudo, 'content': message})

class Session:
  def __init__(self):
    self.room = None
    self.last_message = None
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

def get_rooms():
  xml = atlastk.create_XML("Rooms")

  for id in rooms:
    xml.push_tag("Room")
    xml.put_attribute("id", id)
    xml.put_attribute("URL", atlastk.get_app_url(id))
    xml.put_value(rooms[id]["name"])
    xml.pop_tag()

  return xml

def display_rooms(dom):
  dom.inner("Rooms",get_rooms(), "Rooms.xsl")

def ac_connect(session,dom,id):
  if id:
    dom.inner("",open("Room.html").read())
    dom.set_content("Name",rooms[id]["name"])
    session.room = rooms[id]["core"]
    session.last_message = 0
    dom.focus("Pseudo")
    session.room.display_messages(session,dom)    
  else:
    dom.inner("",open("Admin.html").read())
    dom.focus("Name")
    display_rooms(dom)

def ac_create(session,dom):
  global rooms

  name = dom.get_content("Name").strip()

  if not name:
    dom.alert(f"A room name can not be empty!")
  elif any( room["name"] == name for room in rooms.values()):
    dom.alert(f"There is already a room named '{name}'")
  else:
    id = str(uuid.uuid4())
    url = atlastk.get_app_url(id)
    rooms[id]={"name": name, "core": Room()}
    display_rooms(dom)
    dom.set_content("Name", "")

  dom.focus("Name")

def ac_qrcode(session,dom,id):
  mark = dom.get_mark(id)

  if mark:
    url = atlastk.get_app_url(mark)
    dom.inner(dom.last_child(id), f'<a href="{url}" title="{url}" target="_blank"><img src="https://api.qrserver.com/v1/create-qr-code/?size=125x125&data={url}"/></a>')
    dom.set_mark(id,"")

def ac_submit_pseudo(session,dom):
  pseudo = dom.get_value("Pseudo").strip()

  room = session.room

  if not pseudo:
    dom.alert("Pseudo. can not be empty !")
    dom.set_value("Pseudo", "")
    dom.focus("Pseudo")
  elif room.handle_pseudo(pseudo.upper()):
    session.pseudo = pseudo
    dom.add_class("PseudoButton", "hidden")
    dom.disable_element("Pseudo")
    dom.enable_elements(["Message", "MessageButton"])
    dom.focus("Message")
  else:
    dom.alert("Pseudo. not available!")
    dom.set_value("Pseudo", pseudo)
    dom.focus("Pseudo")

def ac_submit_message(session,dom):
  room = session.room

  message = dom.get_value("Message")
  dom.set_value("Message", "")
  dom.focus("Message")
  room.add_message(session.pseudo,message)
  room.display_messages(session,dom)
  atlastk.broadcast_action("Update")     

CALLBACKS = {
  "": ac_connect,
  "Create": ac_create,
  "QRCode": ac_qrcode,
  "SubmitPseudo": ac_submit_pseudo,
  "SubmitMessage": ac_submit_message,
  "Update": lambda session,dom: session.room.display_messages(session,dom) if session.room else None,
}
    
atlastk.launch(CALLBACKS, Session, open("Head.html").read())
