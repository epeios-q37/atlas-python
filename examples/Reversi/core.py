"""
MIT License

Copyright (c) 2017,2020 Hajime Nakagami <nakagami@gmail.com>
Copyright (c) 2019,2021 Claude SIMON (https://q37.info/s/rmnmqd49)

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

import random, itertools, copy, threading

EMPTY = 0
BLACK = -1
WHITE = 1

# http://uguisu.skr.jp/othello/5-1.html
_WEIGHT1_MATRIX = [
  [120, -20, 20, 5, 5, 20, -20, 120],
  [-20, -40, -5, -5, -5, -5, -40, -20],
  [20, -5, 15, 3, 3, 15, -5, 20],
  [5, -5, 3, 3, 3, 3, -5, 5],
  [5, -5, 3, 3, 3, 3, -5, 5],
  [20, -5, 15, 3, 3, 15, -5, 20],
  [-20, -40, -5, -5, -5, -5, -40, -20],
  [120, -20, 20, 5, 5, 20, -20, 120],
]


_WEIGHT2_MATRIX = [
  [30, -12, 0, -1, -1, 0, -12, 30],
  [-12, -15, -3, -3, -3, -3, -15, -12],
  [0, -3, 0, -1, -1, 0, -3, 0],
  [-1, -3, -1, -1, -1, -1, -3, -1],
  [-1, -3, -1, -1, -1, -1, -3, -1],
  [0, -3, 0, -1, -1, 0, -3, 0],
  [-12, -15, -3, -3, -3, -3, -15, -12],
  [30, -12, 0, -1, -1, 0, -12, 30],
]

_WEIGHT_MATRICES = {
  1: _WEIGHT1_MATRIX,
  2: _WEIGHT2_MATRIX
}

class Board:
  def _reset(self):
    self._board = []
    self._lock = None
    for _ in range(8):
      self._board.append([EMPTY] * 8)

    self._board[3][3] = self._board[4][4] = BLACK
    self._board[4][3] = self._board[3][4] = WHITE

  def __init__(self, p = None):
    self._reset()
    self._lock = threading.Lock()
    if isinstance(p, Board):    # copy constructor
      with p._lock:
        self._board = copy.deepcopy(p._board)
    elif p != None:
      raise ValueError("invaid parameter")

  def count(self, bwe):
    "Count pieces or empty spaces in the board"
    assert bwe in (BLACK, WHITE, EMPTY)
    n = 0
    with self._lock:
      for i in range(8):
        for j in range(8):
          if self._board[i][j] == bwe:
            n += 1
    return n

  def _has_my_piece(self, bw, x, y, delta_x, delta_y):
    "There is my piece in the direction of (delta_x, delta_y) from (x, y)."
    assert bw in (BLACK, WHITE)
    assert delta_x in (-1, 0, 1)
    assert delta_y in (-1, 0, 1)
    x += delta_x
    y += delta_y

    if x < 0 or x > 7 or y < 0 or y > 7 or self._board[x][y] == EMPTY:
      return False
    if self._board[x][y] == bw:
      return True
    return self._has_my_piece(bw, x, y, delta_x, delta_y)

  def reversible_directions(self, bw, x, y):
    "Can put piece on (x, y) ? Return list of reversible direction tuple"
    assert bw in (BLACK, WHITE)

    with self._lock:
      directions = []
      if self._board[x][y] != EMPTY:
        return directions

      for d in itertools.product([-1, 1, 0], [-1, 1, 0]):
        if d == (0, 0):
          continue
        nx = x + d[0]
        ny = y + d[1]
        if nx < 0 or nx > 7 or ny < 0 or ny > 7 or self._board[nx][ny] != bw * -1:
          continue
        if self._has_my_piece(bw, nx, ny, d[0], d[1]):
          directions.append(d)
    return directions

  def _reverse_piece(self, bw, x, y, delta_x, delta_y):
    "Reverse pieces in the direction of (delta_x, delta_y) from (x, y) until bw."
    assert bw in (BLACK, WHITE)

    x += delta_x
    y += delta_y
    assert self._board[x][y] in (BLACK, WHITE)

    if self._board[x][y] == bw:
      return

    self._board[x][y] = bw
    return self._reverse_piece(bw, x, y, delta_x, delta_y)

  def put(self, x, y, bw):
    """
    True: Put bw's piece on (x, y) and change board status.
    False: Can't put bw's piece on (x, y)
    """
    assert bw in (BLACK, WHITE)

    directions = self.reversible_directions(bw, x, y)
    if len(directions) == 0:
      return False
    self._board[x][y] = bw
    with self._lock:
      for delta in directions:
        self._reverse_piece(bw, x, y, delta[0], delta[1])
    return True

  def isAllowed(self, x, y, bw):
    return len(self.reversible_directions(bw, x, y)) != 0

  # Calling function does not lock, as this function is called on a local copy.
  def _calc_score(self, bw, level):
    assert level in [1,2], bw in (BLACK, WHITE)
    my_score = 0
    against_score = 0
    for i in range(8):
      for j in range(8):
        if self._board[i][j] == bw:
          my_score += _WEIGHT_MATRICES[level][i][j]
        elif self._board[i][j] == bw * -1:
          against_score += _WEIGHT_MATRICES[level][i][j]
    return my_score - against_score

  def find_best_position(self, bw, level):
    "Return the best next position."
    assert bw in (BLACK, WHITE)

    board_copy = Board(self)

    next_positions = {}
    for i in range(8):
      for j in range(8):
        board = Board(board_copy)
        if board.put(i, j, bw):
          next_positions.setdefault(
            board._calc_score(bw,level), []
          ).append((i, j))

    return random.choice(next_positions[max(next_positions)]) if next_positions else None

  def array(self):
    return Board(self)._board

