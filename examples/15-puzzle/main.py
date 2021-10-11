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

  dom.set_values(values)
  dom.toggle_class(puzzle.blank, "hidden")


def swap(puzzle, dom, source):
  dom.set_values({
    "t"+str(puzzle.blank): dom.get_value("t"+str(source)),
    "t"+str(source): ""
  })

  dom.toggle_classes({
    puzzle.blank: "hidden",
    source: "hidden"
  })

  puzzle.blank = source


def convert_x(pos):
  return pos % 4


def convert_y(pos):
  return pos >> 2  # pos / 4


def convert(pos):
  return convert_x(pos), convert_y(pos)


def draw_square(board, x, y):
  board.push_tag("use")
  board.put_attribute("id", y * 4 + x)
  board.put_attribute("xdh:onevent", "Swap")
  board.put_attribute("x", x * 100 + 24)
  board.put_attribute("y", y * 100 + 24)
  board.put_attribute("href", "#stone")
  board.pop_tag()


def draw_grid(dom):
  board = atlastk.create_HTML("g")
  for x in range(0, 4):
    for y in range(0, 4):
      draw_square(board, x, y)
  dom.inner("Stones", board)


def set_text(texts, x, y):
  texts.push_tag("tspan")
  texts.put_attribute("id", "t" + str(y * 4 + x))
  texts.put_attribute("x", x * 100 + 72)
  texts.put_attribute("y", y * 100 + 90)
  texts.pop_tag()


def set_texts(dom):
  texts = atlastk.create_HTML("text")
  for x in range(0, 4):
    for y in range(0, 4):
      set_text(texts, x, y)
  dom.inner("Texts", texts)


def scramble(puzzle, dom):
  draw_grid(dom)
  set_texts(dom)
  fill(puzzle, dom)


def ac_connect(self, dom):
  dom.inner("", open("Main.html").read())
  scramble(self, dom)


def build(sourceIds,targetIds,sourceIdsAndValues, blank):

  targetIdsAndValues = {}

  for i in range(len(sourceIds)):
    targetIdsAndValues[targetIds[i]] = sourceIdsAndValues[sourceIds[i]]
    
  targetIdsAndValues["t" + blank] = ""
    
  return targetIdsAndValues


def ac_swap(self, dom, id):
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
      by = convert_y(source)
  elif (iy == by):
    delta = 1 if bx < ix else -1
    while(bx != ix):
      targetIds.append("t"+str(source))
      source += delta
      sourceIds.append("t"+str(source))
      bx = convert_x(source)

  dom.set_values(build(sourceIds, targetIds, dom.get_values(sourceIds), id))

  dom.toggle_classes({
    self.blank: "hidden",
    target: "hidden"
  })

  self.blank = target


callbacks = {
  "": ac_connect,
  "Swap": ac_swap,
  "Scramble": lambda self, dom, id: scramble(self, dom)
}


atlastk.launch(callbacks, Puzzle, open("Head.html").read())
