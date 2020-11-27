# You don't need following 3 lines in your own applications.
import sys, os
sys.path.append("../../atlastk")
os.chdir(os.path.dirname(os.path.realpath(__file__)))

import atlastk

def ac_connect(dom):
  dom.inner("",open("Main.html").read())

CALLBACKS = {
  "": ac_connect,
 }

atlastk.launch(CALLBACKS,None,open("Head.html").read())