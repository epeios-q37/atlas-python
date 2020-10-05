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

"""

  This file comes from https://www.pygame.org.

  It needs PyGame to be installed, and was modified to be controlled
  by a web interface thanks to the Atlas toolkit (http://atlastk.org).
   
"""


import random, math, pygame, os, sys
from pygame.locals import *
from threading import Thread
import threading

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("../../atlastk")

import atlastk

#constants
WINSIZE = [640, 480]
WINCENTER = [320, 240]
NUMSTARS = 150
STEP = 20

def init_star():
  "creates new star values"
  dir = random.randrange(100000)
  velmult = random.random()*.6+.4
  vel = [math.sin(dir) * velmult, math.cos(dir) * velmult]
  return vel, WINCENTER[:]


def initialize_stars():
  "creates a new starfield"
  stars = []
  for x in range(NUMSTARS):
    star = init_star()
    vel, pos = star
    steps = random.randint(0, WINCENTER[0])
    pos[0] = pos[0] + (vel[0] * steps)
    pos[1] = pos[1] + (vel[1] * steps)
    vel[0] = vel[0] * (steps * .09)
    vel[1] = vel[1] * (steps * .09)
    stars.append(star)
  move_stars(stars)
  return stars
  

def draw_stars(surface, stars, color):
  "used to draw (and clear) the stars"
  for vel, pos in stars:
    pos = (int(pos[0]), int(pos[1]))
    surface.set_at(pos, color)


def move_stars(stars):
  "animate the star values"
  for vel, pos in stars:
    pos[0] = pos[0] + vel[0]
    pos[1] = pos[1] + vel[1]
    if not 0 <= pos[0] <= WINSIZE[0] or not 0 <= pos[1] <= WINSIZE[1]:
      vel[:], pos[:] = init_star()
    else:
      vel[0] = vel[0] * 1.05
      vel[1] = vel[1] * 1.05

def acConnect(dom):
  dom.inner("", open("Main.html").read())

pos = WINCENTER

def acCenter(dom):
  global pos;
  pos = [WINSIZE[0]/2, WINSIZE[1]/2]

def acRight(dom):
  global pos;
  pos = [pos[0] + STEP, pos[1]]

def acEnd(dom):
  global pos;
  pos = [WINSIZE[0], pos[1]]

def acDown(dom):
  global pos;
  pos = [pos[0], pos[1] + STEP]

def acBottom(dom):
  global pos;
  pos = [pos[0], WINSIZE[1]]

def acLeft(dom):
  global pos;
  pos = [pos[0] - STEP, pos[1]]

def acBegin(dom):
  global pos;
  pos = [0,pos[1]]

def acUp(dom):
  global pos;
  pos = [pos[0], pos[1] - STEP]

def acTop(dom):
  global pos;
  pos = [pos[0], 0]

def acToggle(dom):
  dom.toggle_class("Simple", "hidden")
  dom.toggle_class("Expert", "hidden")

callbacks = {
  "": acConnect,
  "Center": acCenter,
  "Right": acRight,
  "Down": acDown,
  "Left": acLeft,
  "Up": acUp,
  "End": acEnd,
  "Bottom": acBottom,
  "Begin": acBegin,
  "Top": acTop,
  "Toggle": acToggle,
}

def atlas():
  atlastk.launch(callbacks, None, open("Head.html").read())

def main():
  global pos;
  thread = threading.Thread(target=atlas)
  thread.daemon = True
  thread.start()

  pygame.time.wait(2000);

  "This is the starfield code"
  #create our starfield
  random.seed()
  stars = initialize_stars()
  clock = pygame.time.Clock()
  #initialize and prepare screen
  pygame.init()
  screen = pygame.display.set_mode(WINSIZE)
  pygame.display.set_caption('pygame Stars Example')
  white = 255, 240, 200
  black = 20, 20, 40
  screen.fill(black)

  #main game loop
  done = 0
  while not done:
    draw_stars(screen, stars, black)
    move_stars(stars)
    draw_stars(screen, stars, white)
    pygame.display.update()
    for e in pygame.event.get():
      if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
        done = 1
        break
      elif e.type == MOUSEBUTTONDOWN and e.button == 1:
        pos = list(e.pos)


    WINCENTER[:] = pos
    clock.tick(50)

main()
