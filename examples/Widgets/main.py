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

target=""

"""
From here and up to and including the 'ac_connect' function,
to simplify the writing of the program, there are a lot a quirks
which should not be used by regular developers.
"""

def clean(s,i):
  pattern = f' id="_CGN{i}"'

  while pattern in s:
    s = s.replace(pattern, "")
    i += 1
    pattern = f' id="_CGN{i}"'

  return s.strip(" \n").replace ("    <","<").replace("data-xdh-widget_","data-xdh-widget"),i

def display_code(dom,element,i):
  source = dom.first_child(element);
  code,i = clean(dom.get_value(source),i)
  dom.set_value(dom.next_sibling(source),html.escape(code))

  return i

def ac_connect(dom):
  global target

  dom.inner("", open("Main.html").read())
  current = dom.next_sibling(dom.next_sibling(dom.first_child("")))
  i = 0

  target = ""
  list = "<option disabled selected value> -- Select a widget -- </option>"

  while current != "":
    id = dom.get_attribute(current,"id")
    list += f'<option value="{id}">{id}</option>'
    i = display_code(dom,current,i)
    current = dom.next_sibling(current)

  dom.execute_void("document.querySelectorAll('pre').forEach((block) => {hljs.highlightBlock(block);});")

  dom.set_attribute("ckInput","data-xdh-widget",dom.get_attribute("ckInput","data-xdh-widget_"))
  dom.after("ckInput","")
  dom.inner("List", list)

def ac_select(dom,id):
  global target

  if target:
    dom.add_class(target,"hidden")
  target = dom.get_value(id)
  dom.remove_class(target, "hidden")

def dl_shape(flavors):
  html = atlastk.create_HTML()

  for flavor in flavors:
    html.push_tag("option")
    html.put_attribute("value", flavor)
    html.pop_tag()

  return html

dl_flavors = ["Vanilla", "Chocolate", "Caramel"]  

def ac_dl_submit(dom, id):
  global dl_flavors

  flavor = dom.get_value(id)
  dom.set_value(id, "")
  if not flavor in dl_flavors:
    dl_flavors.append(flavor)
    dl_flavors.sort()
    dom.inner("dlFlavors", dl_shape(dl_flavors))
  dom.set_value("dlOutput", flavor)

def sl_embed(other):
  html = atlastk.create_HTML()

  html.push_tag("option")
  html.put_attribute("selected", "selected")
  html.put_value(other)
#  html.pop_tag()

  return html

def ac_sl_add(dom):
  dom.begin("slOthers", sl_embed(dom.get_value("slInput")))
  dom.set_value("slInput", "")
  dom.focus("slInput")  

callbacks = {
  "": ac_connect,
  "Select": ac_select,

  "btSubmit": lambda dom: dom.alert("Click on button detected!"),

  "pwSubmit": lambda dom, id: dom.set_value("pwOutput", dom.get_value(id)),

  "cbSelect": lambda dom, id: dom.set_value("cbOutput", "{} ({})".format(id, dom.get_value(id))),
  "cbSubmit": lambda dom: dom.alert(str(dom.get_values(["cbBicycle", "cbCar","cbPirogue"]))),

  "rdSelect": lambda dom, id: dom.set_value("rdOutput", id),
  "rdSubmit": lambda dom: dom.alert(str(dom.get_values(["rdEmail", "rdPhone","rdMail"]))),

  "dlSubmit": ac_dl_submit,

  "dtSelect": lambda dom, id: dom.set_value("dtOutput", dom.get_value(id)),

  "clSelect": lambda dom, id: dom.set_value("clOutput", dom.get_value(id)),

  "cpSelect": lambda dom, id: dom.set_value("cpOutput", dom.get_value(id)),

  "rgSlide": lambda dom: dom.set_attribute("rgOutput", "value", (dom.get_value("rgVolume"))),

  "slSelect": lambda dom, id: dom.set_value("slOutput", dom.get_value(id)),
  "slAdd": ac_sl_add,
  "slToggle": lambda dom, id: dom.disable_element("slOthers") if dom.get_value(id) == 'true' else dom.enable_element("slOthers"),

  "ckSubmit": lambda dom, id: dom.set_value("ckOutput", dom.get_value("ckInput")),
}

atlastk.launch(callbacks, None, open("Head.html").read())
