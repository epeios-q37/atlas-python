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

import atlastk
from random import *

# Although empty, must exist, as it will be filled later.
class Puzzle:
  pass


def fill(puzzle, dom):
  numbers = []
  values = {}

  for i in range(16):
    numbers.append(i)

  for i in range(len(numbers)):
    number = numbers.pop(randint(0, len(numbers)-1))
    if number != 0:
      values["t"+str(i)] = number
    else:
      puzzle.blank = i

  dom.setValues(values)
  dom.toggleClass(puzzle.blank, "hidden")


def swap(puzzle, dom, source):
  dom.setValues({
    "t"+str(puzzle.blank): dom.getValue("t"+str(source)),
    "t"+str(source): ""
  })

  dom.toggleClasses({
    puzzle.blank: "hidden",
    source: "hidden"
  })

  puzzle.blank = source


def convertX(pos):
  return pos % 4


def convertY(pos):
  return pos >> 2  # pos / 4


def convert(pos):
  return convertX(pos), convertY(pos)


def drawSquare(board, x, y):
  board.pushTag("use")
  board.putAttribute("id", y * 4 + x)
  board.putAttribute("xdh:onevent", "Swap")
  board.putAttribute("x", x * 100 + 24)
  board.putAttribute("y", y * 100 + 24)
  board.putAttribute("href", "#stone")
  board.popTag()


def drawGrid(dom):
  board = atlastk.create_HTML("g")
  for x in range(0, 4):
    for y in range(0, 4):
      drawSquare(board, x, y)
  dom.inner("Stones", board)


def setText(texts, x, y):
  texts.pushTag("tspan")
  texts.putAttribute("id", "t" + str(y * 4 + x))
  texts.putAttribute("x", x * 100 + 72)
  texts.putAttribute("y", y * 100 + 90)
  texts.popTag()


def setTexts(dom):
  texts = atlastk.create_HTML("text")
  for x in range(0, 4):
    for y in range(0, 4):
      setText(texts, x, y)
  dom.inner("Texts", texts)


def scramble(puzzle, dom):
  drawGrid(dom)
  setTexts(dom)
  fill(puzzle, dom)


def atk(self, dom):
  dom.inner("", open("Main.html").read())
  scramble(self, dom)


def build(sourceIds,targetIds,sourceIdsAndValues, blank):
  targetIdsAndValues = {}

  for i in range(len(sourceIds)):
    targetIdsAndValues[targetIds[i]] = sourceIdsAndValues[sourceIds[i]]
    
  targetIdsAndValues["t" + blank] = ""
    
  return targetIdsAndValues


def atkSwap(self, dom, id):
  target = int(id)
  source = self.blank
  sourceIds = []
  targetIds = []

  ix, iy = convert(target)
  bx, by = convert(source)

  if (ix == bx):
    delta = 4 if by < iy else -4
    while(by != iy):
      targetIds.append("t"+str(source))
      source += delta
      sourceIds.append("t"+str(source))
      by = convertY(source)
  elif (iy == by):
    delta = 1 if bx < ix else -1
    while(bx != ix):
      targetIds.append("t"+str(source))
      source += delta
      sourceIds.append("t"+str(source))
      bx = convertX(source)

  dom.setValues(build(sourceIds, targetIds, dom.getValues(sourceIds), id))

  dom.toggleClasses({
    self.blank: "hidden",
    target: "hidden"
  })

  self.blank = target

atkScramble = lambda self, dom, id: scramble(self, dom)

ATK_HEAD = open("Head.html").read()

ATK_USER = Puzzle

atlastk.launch(globals=globals())
