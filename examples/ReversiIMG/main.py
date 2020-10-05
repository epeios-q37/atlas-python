"""
MIT License

Copyright (c) 2017 Hajime Nakagami<nakagami@gmail.com>
Copyright (c) 2019 Claude SIMON (https://q37.info/s/rmnmqd49)

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

# This is the adaptation of the program found on:
# https://gist.github.com/nakagami/7a7d799bd4bd4ad8fcea96135c4af179

import os, sys, random, itertools, time

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("../../atlastk")

import atlastk

EMPTY = 0
BLACK = -1
WHITE = 1

# http://uguisu.skr.jp/othello/5-1.html

WEIGHT_MATRIX = [
  [120, -20, 20, 5, 5, 20, -20, 120],
  [-20, -40, -5, -5, -5, -5, -40, -20],
  [20, -5, 15, 3, 3, 15, -5, 20],
  [5, -5, 3, 3, 3, 3, -5, 5],
  [5, -5, 3, 3, 3, 3, -5, 5],
  [20, -5, 15, 3, 3, 15, -5, 20],
  [-20, -40, -5, -5, -5, -5, -40, -20],
  [120, -20, 20, 5, 5, 20, -20, 120],
]


class Reversi:
  def reset(self):
    self.board = []
    for _ in range(8):
      self.board.append([EMPTY] * 8)

    self.board[3][3] = self.board[4][4] = BLACK
    self.board[4][3] = self.board[3][4] = WHITE

  def __init__(self, orig=None):
    self.reset()

    # copy constructor
    if orig:
      assert isinstance(orig, Reversi)
      for i in range(8):
        for j in range(8):
          self.board[i][j] = orig.board[i][j]

  def count(self, bwe):
    "Count pieces or empty spaces in the board"
    assert bwe in (BLACK, WHITE, EMPTY)
    n = 0
    for i in range(8):
      for j in range(8):
        if self.board[i][j] == bwe:
          n += 1
    return n

  def _has_my_piece(self, bw, x, y, delta_x, delta_y):
    "There is my piece in the direction of (delta_x, delta_y) from (x, y)."
    assert bw in (BLACK, WHITE)
    assert delta_x in (-1, 0, 1)
    assert delta_y in (-1, 0, 1)
    x += delta_x
    y += delta_y

    if x < 0 or x > 7 or y < 0 or y > 7 or self.board[x][y] == EMPTY:
      return False
    if self.board[x][y] == bw:
      return True
    return self._has_my_piece(bw, x, y, delta_x, delta_y)

  def reversible_directions(self, bw, x, y):
    "Can put piece on (x, y) ? Return list of reversible direction tuple"
    assert bw in (BLACK, WHITE)

    directions = []
    if self.board[x][y] != EMPTY:
      return directions

    for d in itertools.product([-1, 1, 0], [-1, 1, 0]):
      if d == (0, 0):
        continue
      nx = x + d[0]
      ny = y + d[1]
      if nx < 0 or nx > 7 or ny < 0 or ny > 7 or self.board[nx][ny] != bw * -1:
        continue
      if self._has_my_piece(bw, nx, ny, d[0], d[1]):
        directions.append(d)
    return directions

  def _reverse_piece(self, bw, x, y, delta_x, delta_y):
    "Reverse pieces in the direction of (delta_x, delta_y) from (x, y) untill bw."
    assert bw in (BLACK, WHITE)

    x += delta_x
    y += delta_y
    assert self.board[x][y] in (BLACK, WHITE)

    if self.board[x][y] == bw:
      return

    self.board[x][y] = bw
    return self._reverse_piece(bw, x, y, delta_x, delta_y)

  def isAllowed(self, x, y, bw):
    return len(self.reversible_directions(bw, x, y)) != 0

  def put(self, x, y, bw):
    """
    True: Put bw's piece on (x, y) and change board status.
    False: Can't put bw's piece on (x, y)
    """

    assert bw in (BLACK, WHITE)
    directions = self.reversible_directions(bw, x, y)
    if len(directions) == 0:
      return False
    self.board[x][y] = bw
    for delta in directions:
      self._reverse_piece(bw, x, y, delta[0], delta[1])
    return True

  def _calc_score(self, bw, weight_matrix):
    assert bw in (BLACK, WHITE)
    my_score = 0
    against_score = 0
    for i in range(8):
      for j in range(8):
        if self.board[i][j] == bw:
          my_score += weight_matrix[i][j]
        elif self.board[i][j] == bw * -1:
          against_score += weight_matrix[i][j]
    return my_score - against_score

  def find_best_position(self, bw, weight_matrix):
    "Return the best next position."
    assert bw in (BLACK, WHITE)

    next_positions = {}
    for i in range(8):
      for j in range(8):
        reversi = Reversi(self)
        if reversi.put(i, j, bw):
          next_positions.setdefault(
            reversi._calc_score(bw, weight_matrix), []
          ).append((i, j))
    if next_positions:
      next_position = random.choice(next_positions[max(next_positions)])
    else:
      next_position = None
    return next_position


# -------------------------------------------------------------------------------

def drawBoard(reversi, dom, prefetch=False):
  board = atlastk.createHTML("tbody")
  for y, row in enumerate(reversi.board):
    board.push_tag("tr")
    for x, r in enumerate(row):
      board.push_tag("td")
      board.put_attribute("id", str(x) + str(y))
      if (r == EMPTY) and (reversi.isAllowed(y, x, reversi.player)):
        board.put_attribute("data-xdh-onevent", "Play")
        if (prefetch == True):
          r = reversi.player
          board.put_attribute(
            "style", "opacity: 0.1; background-color: white;")
      board.put_attribute(
        "class", {EMPTY: 'none', BLACK: 'black', WHITE: 'white'}[r])
      board.pop_tag()
    board.pop_tag()

  dom.inner("board", board)

  dom.set_values({
    "black": reversi.count(BLACK),
    "white": reversi.count(WHITE)
  })


def acConnect(reversi, dom):
  reversi.player = BLACK
  reversi.weight_matrix = WEIGHT_MATRIX
  dom.inner("", open("Main.html").read())
  drawBoard(reversi, dom)
  dom.alert("Welcome to this Reversi (aka Othello) game made with the Atlas toolkit.\n\nYou play against the computer with the black pieces.")


def acPlay(reversi, dom, id):
  xy = [int(id[1]), int(id[0])]

  player = reversi.player
  weight_matrix = reversi.weight_matrix

  if (reversi.put(xy[0], xy[1], player)):
    drawBoard(reversi, dom, False)

    xy = reversi.find_best_position(player * -1, weight_matrix)
    if xy:
      reversi.put(xy[0], xy[1], player * -1)
      time.sleep(1)

    drawBoard(reversi, dom)

  if (reversi.count(EMPTY) == 0 or
    reversi.count(BLACK) == 0 or
      reversi.count(WHITE) == 0):
    if reversi.count(player) > reversi.count(player * -1):
      dom.alert('You win!')
    elif reversi.count(player) < reversi.count(player * -1):
      dom.alert('You lose!')
    else:
      dom.alert('Egality!')


def acNew(reversi, dom):
  reversi.reset()
  drawBoard(reversi, dom)


callbacks = {
  "": acConnect,
  "Play": acPlay,
  "New": acNew
}

atlastk.launch(callbacks, Reversi, open("Head.html").read())
