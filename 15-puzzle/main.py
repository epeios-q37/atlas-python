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

import sys
from random import *

sys.path.append("./Atlas.python.zip")
sys.path.append("../Atlas.python.zip")

import atlastk as Atlas

class Puzzle:
    pass


def readAsset(path):
    return Atlas.readAsset(path, "15-puzzle")


def fill(puzzle, dom):
    numbers = []
    contents = {}

    for i in range(16):
        numbers.append(i)

    for i in range(len(numbers)):
        number = numbers.pop(randint(0, len(numbers)-1))
        if number != 0:
            contents["t"+str(i)] = number
        else:
            puzzle.blank = i

    dom.setContents(contents)
    dom.toggleClass(puzzle.blank, "hidden")


def swap(puzzle, dom, source):
    dom.setContents({
        "t"+str(puzzle.blank): dom.getContent("t"+str(source)),
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


def drawSquare(xml, x, y):
    xml.pushTag("use")
    xml.setAttribute("id", y * 4 + x)
    xml.setAttribute("data-xdh-onevent", "Swap")
    xml.setAttribute("x", x * 100 + 24)
    xml.setAttribute("y", y * 100 + 24)
    xml.setAttribute("xlink:href", "#stone")
    xml.popTag()


def drawGrid(dom):
    xml = Atlas.createXML("g")
    for x in range(0, 4):
        for y in range(0, 4):
            drawSquare(xml, x, y)
    dom.setLayout("Stones", xml)


def setText(xml, x, y):
    xml.pushTag("tspan")
    xml.setAttribute("id", "t" + str(y * 4 + x))
    xml.setAttribute("x", x * 100 + 72)
    xml.setAttribute("y", y * 100 + 90)
    xml.popTag()


def setTexts(dom):
    xml = Atlas.createXML("text")
    for x in range(0, 4):
        for y in range(0, 4):
            setText(xml, x, y)
    dom.setLayout("Texts", xml)


def scramble(puzzle, dom):
    drawGrid(dom)
    setTexts(dom)
    fill(puzzle, dom)


def acConnect(this, dom, id):
    dom.setLayout("", readAsset("Main.html"))
    scramble(this, dom)


def acSwap(this, dom, id):
    ix, iy = convert(int(id))
    bx, by = convert(this.blank)

    if (ix == bx):
        delta = 4 if by < iy else -4
        while(by != iy):
            swap(this, dom, this.blank+delta)
            by = convertY(this.blank)
    elif (iy == by):
        delta = 1 if bx < ix else -1
        while(bx != ix):
            swap(this, dom, this.blank+delta)
            bx = convertX(this.blank)


callbacks = {
    "": acConnect,
    "Swap": acSwap,
    "Scramble": lambda this, dom, id: scramble(this, dom)
}

Atlas.launch(callbacks, Puzzle, readAsset("Head.html"), "15-puzzle")
