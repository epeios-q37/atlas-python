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

import atlastk, html, re

"""
From here and up to and including the 'acConnect' function,
to simplify the writing of the program, there are a lot of quirks
which should not be used in regular applications.
"""

def clean(s):
  return re.sub(' id="_CGN.*?"', '', s).strip(" \n").replace ("    <", "<").replace("xdh:widget_", "xdh:widget")


def displayCode(dom, element):
# source = dom.nextSibling(dom.firstChild(element));
  source = dom.executeString(f"getOrGenerateId(getElement('{element}').firstElementChild.nextElementSibling);")
  code = clean(dom.getValue(source))
  # target = dom.nextSibling(dom.firstChild(dom.nextSibling(dom.firstChild(dom.nextSibling(dom.nextSibling(source))))))
  target = dom.executeString(f"getOrGenerateId(getElement('{source}').nextElementSibling.nextElementSibling.firstElementChild.nextElementSibling.firstElementChild.nextElementSibling);")
  dom.setValue(target, html.escape(code))


def acConnect(dom):
  dom.inner("", open("Main.html").read())
  last = dom.nextSibling(dom.nextSibling(dom.firstChild("")))
  current = dom.lastChild(dom.parent(last))

  while True:
    widget = dom.getAttribute(current, "id")
    dom.setValue("RetrievedWidget", widget)
    displayCode(dom,current)
    dom.removeClass(widget, "hidden")
    if current == last:
      break
    current = dom.previousSibling(current)

  dom.executeVoid("document.querySelectorAll('pre').forEach((block) => {hljs.highlightBlock(block);});")

  dom.addClass("Retrieving", "hidden")

  dom.setAttribute("ckInput", "xdh:widget", dom.getAttribute("ckInput", "xdh:widget_"))
  dom.after("ckInput", "")


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


def acRgSubmit(dom, id):
  value = dom.getValue(id)

  dom.setValues({
    "rgRange": value,
    "rgNumber": value,
    "rgMeter": value
  })


def slEmbed(other):
  html = atlastk.createHTML()

  html.pushTag("option")
  html.putAttribute("selected", "selected")
  html.putValue(other)

  return html


def acSlAdd(dom):
  dom.begin("slOthers", slEmbed(dom.getValue("slInput")))
  dom.setValue("slInput", "")
  dom.focus("slInput")  


CALLBACKS = {
  "": acConnect,

  "btSubmit": lambda dom: dom.alert("Click on button detected!"),

  "pwSubmit": lambda dom, id: dom.setValue("pwOutput", dom.getValue(id)),

  "cbSelect": lambda dom, id: dom.setValue("cbOutput", "{} ({})".format(id, dom.getValue(id))),
  "cbSubmit": lambda dom: dom.alert(str(dom.getValues(["cbBicycle", "cbCar", "cbPirogue"]))),

  "rdCheck": lambda dom, id: dom.setValue("rdSelect", dom.getValue(id)),
  "rdSelect": lambda dom, id: dom.setValue("rdRadios", dom.getValue(id)),
  "rdReset": lambda dom: dom.setValues({"rdSelect": "None", "rdRadios": ""}),

  "dlSubmit": acDlSubmit,

  "dtSelect": lambda dom, id: dom.setValue("dtOutput", dom.getValue(id)),

  "clSelect": lambda dom, id: dom.setValue("clOutput", dom.getValue(id)),

  "rgSubmit": acRgSubmit,

  "slSelect": lambda dom, id: dom.setValue("slOutput", dom.getValue(id)),
  "slAdd": acSlAdd,
  "slToggle": lambda dom, id: dom.disableElement("slOthers") if dom.getValue(id) == 'true' else dom.enableElement("slOthers"),
  "slRadio": lambda dom: dom.scrollTo("radio"),

  "ckSubmit": lambda dom, id: dom.setValue("ckOutput", dom.getValue("ckInput")),
}

ATK_HEAD = open("Head.html").read()


atlastk.launch(CALLBACKS, globals=globals())
