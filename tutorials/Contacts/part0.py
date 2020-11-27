# You don't need following 3 lines in your own applications.
import sys, os
sys.path.append("../../atlastk")
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Sole purpose of this program is to display all the elements of the HTML page.

import atlastk

def ac_connect(dom):
  dom.inner("",open("Main.html").read())
  dom.disable_elements(("HideDisplay","HideDisplayAndSelect","HideEdition"))

CALLBACKS = {
  "": ac_connect,
 }

atlastk.launch(CALLBACKS,None,open("Head.html").read())