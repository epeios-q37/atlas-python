""" 
    Copyright (C) 2019 Claude SIMON (http://q37.info/contact/).

    This file is part of XDHq.

    XDHq is free software: you can redistribute it and/or
    modify it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    XDHq is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with XDHq If not, see <http://www.gnu.org/licenses/>.
"""

"""

    This file comes from https://www.pygame.org.

    It needs PyGame to be installed, and was modified to be controlled
    by a web interface thanks to the Atlas toolkit (http://atlastk.org).
   
"""


import random, math, pygame, sys
from pygame.locals import *
from threading import Thread
import threading

sys.path.append("./Atlas.python.zip")
sys.path.append("../Atlas.python.zip")
sys.path.append("../../Atlas.python.zip")

import atlastk as Atlas

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

def readAsset(path):
#     return open(path, 'r').read()
	return Atlas.readAsset(path, "Stars")

def acConnect(this,dom,id):
	dom.setLayout("", readAsset("Main.html"))

pos = WINCENTER

def acCenter(this,dom,id):
    global pos;
    pos = [WINSIZE[0]/2, WINSIZE[1]/2]

def acRight(this,dom,id):
    global pos;
    pos = [pos[0] + STEP, pos[1]]

def acEnd(this,dom,id):
    global pos;
    pos = [WINSIZE[0], pos[1]]

def acDown(this,dom,id):
    global pos;
    pos = [pos[0], pos[1] + STEP]

def acBottom(this,dom,id):
    global pos;
    pos = [pos[0], WINSIZE[1]]

def acLeft(this,dom,id):
    global pos;
    pos = [pos[0] - STEP, pos[1]]

def acBegin(this,dom,id):
    global pos;
    pos = [0,pos[1]]

def acUp(this,dom,id):
    global pos;
    pos = [pos[0], pos[1] - STEP]

def acTop(this,dom,id):
    global pos;
    pos = [pos[0], 0]

def acToggle(this,dom,id):
    dom.toggleClass("Simple", "hidden")
    dom.toggleClass("Expert", "hidden")

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
    Atlas.launch(callbacks, lambda: None, readAsset("Head.html"), "Stars")

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
