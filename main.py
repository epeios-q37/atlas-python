#!/usr/bin/python3
# coding: utf-8

# All files under MIT license
# Copyright (c) 2019 Claude SIMON (https://q37.info/s/rmnmqd49)
# See  'LICENSE' file.

# For 'Repl.it'.

import os,sys

if ('HOME' in os.environ) and (os.environ['HOME'] == '/home/runner'):
  os.environ["ATK"] = "REPLit"

try:
    input = raw_input
except NameError:
    pass

success = False

demos = (
    "Blank",
    "Hello",
    "Chatroom",
    "ReversiTXT",
    "Notes",
    "TodoMVC",
    "Hangman",
    "15-puzzle",
    "ReversiIMG",
    "ReversiXSL",
)

demosAmount = len(demos)


while not success:
    for id in range(0,demosAmount):
        print(chr(id + ord('a')) + ": " + demos[id]) 
        
    lastChar = chr(demosAmount + ord('a') - 1)
        
    demoId = input("Select one of above demos ('a' … '" + lastChar + "') : ").lower()
   
    try:
        demo = demos[ord(demoId) - ord('a')] + "." + "main"
        
        # Below line is needed by 'Repl.it'.
        sys.argv[0]=demos[ord(demoId) - ord('a')] + "/"

        if True:  # Simplifies debugging when set to False
            try:
                __import__(demo)
            except ImportError:
                print("'" + demo + ".py' not found!")
            else:
                success = True
        else:
            __import__(demo)
    except Exception:
        pass
