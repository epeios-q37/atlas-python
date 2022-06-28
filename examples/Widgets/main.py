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

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("../../atlastk")

import atlastk, html

target = ""

"""
From here and up to and including the 'acConnect' function,
to simplify the writing of the program, there are a lot a quirks
which should not be used by regular developers.
"""

def clean(s,i):
  pattern = f' id="_CGN{i}"'

  while pattern in s:
    s = s.replace(pattern, "")
    i += 1
    pattern = f' id="_CGN{i}"'

  return s.strip(" \n").replace ("    <","<").replace("xdh:widget_","xdh:widget"),i

def displayCode(dom,element,i):
  source = dom.firstChild(element);
  code,i = clean(dom.getValue(source),i)
  dom.setValue(dom.nextSibling(source),html.escape(code))

  return i

def acConnect(dom):
  global target

  dom.inner("", open("Main.html").read())
  current = dom.nextSibling(dom.nextSibling(dom.firstChild("")))
  i = 0

  target = ""
  list = "<option disabled selected value> -- Select a widget -- </option>"

  while current != "":
    id = dom.getAttribute(current,"id")
    dom.setValue("RetrievedWidget", id)
    list += f'<option value="{id}">{id}</option>'
    i = displayCode(dom,current,i)
    current = dom.nextSibling(current)

  dom.executeVoid("document.querySelectorAll('pre').forEach((block) => {hljs.highlightBlock(block);});")

  dom.setAttribute("ckInput","xdh:widget",dom.getAttribute("ckInput","xdh:widget_"))
  dom.after("ckInput","")
  dom.inner("List", list)

  dom.addClass("Retrieving","hidden")
  dom.removeClass("Regular","hidden")

def acSelect(dom,id,widget=""):
  global target

  if ( widget != "" ):
    dom.setValue("List", widget)  

  if target:
    dom.addClass(target,"hidden")
  target = dom.getValue(id)
  dom.removeClass(target, "hidden")


def dlShape(flavors):
  html = atlastk.create_HTML()

  for flavor in flavors:
    html.pushTag("option")
    html.putAttribute("value", flavor)
    html.popTag()

  return html

dlFlavors = ["Vanilla", "Chocolate", "Caramel", "Mint"]  

def acDlSubmit(dom, id):
  global dlFlavors

  flavor = dom.getValue(id)
  dom.setValue(id, "")
  if flavor not in dlFlavors:
    dlFlavors.append(flavor)
    dlFlavors.sort()
    dom.inner("dlFlavors", dlShape(dlFlavors))
  dom.setValue("dlOutput", flavor)

def slEmbed(other):
  html = atlastk.create_HTML()

  html.pushTag("option")
  html.putAttribute("selected", "selected")
  html.putValue(other)

  return html

def acSlAdd(dom):
  dom.begin("slOthers", slEmbed(dom.getValue("slInput")))
  dom.setValue("slInput", "")
  dom.focus("slInput")  

callbacks = {
  "": acConnect,
  "Select": acSelect,

  "btSubmit": lambda dom: dom.alert("Click on button detected!"),

  "pwSubmit": lambda dom, id: dom.setValue("pwOutput", dom.getValue(id)),

  "cbSelect": lambda dom, id: dom.setValue("cbOutput", "{} ({})".format(id, dom.getValue(id))),
  "cbSubmit": lambda dom: dom.alert(str(dom.getValues(["cbBicycle", "cbCar","cbPirogue"]))),

  "rdCheck": lambda dom, id: dom.setValue("rdSelect", dom.getValue(id)),
  "rdSelect": lambda dom, id: dom.setValue("rdRadios", dom.getValue(id)),
  "rdReset": lambda dom: dom.setValues({"rdSelect": "None", "rdRadios": ""}),

  "dlSubmit": acDlSubmit,

  "dtSelect": lambda dom, id: dom.setValue("dtOutput", dom.getValue(id)),

  "clSelect": lambda dom, id: dom.setValue("clOutput", dom.getValue(id)),

  "rgSlide": lambda dom: dom.setAttribute("rgOutput", "value", (dom.getValue("rgVolume"))),

  "slSelect": lambda dom, id: dom.setValue("slOutput", dom.getValue(id)),
  "slAdd": acSlAdd,
  "slToggle": lambda dom, id: dom.disableElement("slOthers") if dom.getValue(id) == 'true' else dom.enableElement("slOthers"),
  "slRadio": lambda dom: acSelect(dom, "List", "radio"),

  "ckSubmit": lambda dom, id: dom.setValue("ckOutput", dom.getValue("ckInput")),
}

atlastk.launch(callbacks, None, open("Head.html").read())
