#!/usr/bin/env python3
"""
MIT License

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

import os, sys, time, uuid, enum, threading, urllib

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.extend(["../../atlastk", "."])

import atlastk
import core

DELAY = 1 # Delay in seconds before computer move.
DEFAULT_LAYOUT_FLAG = True # At 'True', displays the text layout.

_lock = threading.Lock()
_games = {}

class Items(enum.Enum):
  BOARD = enum.auto()
  TURN = enum.auto()
  LOCKED = enum.auto()


def create(token):
  global _games
  assert token, token not in _games

  with _lock:
    board = core.Board()
    _games[token] = {
      Items.BOARD: board,
      Items.TURN: core.EMPTY,
      Items.LOCKED: False
    }
    return board


def remove(token):
  global _games
  assert token

  with _lock:
    if token in _games:
      del _games[token]


def take_black(token):
  global _games
  assert token

  with _lock:
    if token not in _games or _games[token][Items.TURN] != core.EMPTY:
      return False
    _games[token][Items.TURN] = core.WHITE
    return True


def set_turn(token, bw):
  global _games
  assert token, bw in [core.BLACK, core.WHITE]

  with _lock:
    if token not in _games:
      return False
    assert _games[token][Items.TURN] in [core.BLACK, core.WHITE], _games[token][Items.TURN] != bw
    _games[token][Items.TURN] = bw
    return True


def get_board(token):
  global _games
  assert token

  with _lock:
    if token not in _games:
      return None
    else:
      return _games[token][Items.BOARD]


def get_turn(token):
  global _games
  assert token

  with _lock:
    if token not in _games:
      return core.EMPTY
    else:
      return _games[token][Items.TURN]


def lock(token):
  global _games
  assert token

  with _lock:
    if token not in _games:
      return False

    assert Items.LOCKED in _games[token]

    if _games[token][Items.LOCKED]:
      return False

    _games[token][Items.LOCKED] = True
    return True


class Reversi:
  def _reset(self):
    if self.token:
      remove(self.token)
      atlastk.broadcast_action("Refresh", self.token)

  def __init__(self):
    self.board = None
    self.level = 0
    self.bw = core.EMPTY
    self.layoutFlag = DEFAULT_LAYOUT_FLAG
    self.token = None

  def init(self, level=0, bw=core.EMPTY, token=None, board=None):
    self._reset()
    assert bool(token) == bool(board)
    assert (level == 0 ) == bool(board)
    self.level = level
    self.bw = bw
    self.token = token
    self.board = board or core.Board()

  def __del__(self):
    self._reset()


def draw_board(reversi, dom, playability = True):
  board = atlastk.createHTML("tbody")
  for y, row in enumerate(reversi.board.array()):
    board.push_tag("tr")
    for x, r in enumerate(row):
      board.push_tag("td")
      board.put_attribute("id", str(x) + str(y))
      playable = playability and (r == core.EMPTY) and (reversi.board.isAllowed(y, x, reversi.bw if reversi.bw != core.EMPTY else core.BLACK))
      if playable:
        board.put_attribute("xdh:onevent", "Play")
      board.put_attribute(
        "class", {core.EMPTY: 'none', core.BLACK: 'black', core.WHITE: 'white'}[r] + (" playable" if playable else ""))
      board.putValue({core.EMPTY: ' ', core.BLACK: 'X', core.WHITE: 'O'}[r])
      board.pop_tag()
    board.pop_tag()

  dom.inner("board", board)

  dom.set_values({
    "black": reversi.board.count(core.BLACK),
    "white": reversi.board.count(core.WHITE)
  })


def set_status(dom, status, color):
  dom.inner("HHStatus",f'<span style="color: {color}">{status}</span>')


def ac_connect(reversi, dom, id):
  if reversi.layoutFlag:
    dom.disable_element("EnhancedLayout")

  dom.inner("", open("Main.html").read())

  if id and not lock(id):
    dom.alert("Game has already two players!\nReverting to single player game.")
    id = ""

  if id:
    bw = core.EMPTY if get_turn(id) == core.EMPTY else core.WHITE
    reversi.init(token = id, board = get_board(id), bw = bw)
    set_status(dom, "Play or wait for the opponent's move." if bw == core.EMPTY else "It's your turn!", "green")
    dom.disable_element("HideHHStatusSection")
  else:
    reversi.init(level=int(dom.get_value("level")), bw=core.BLACK)

  draw_board(reversi, dom)


def computer_move(reversi, dom):
  bw = reversi.bw
  board = reversi.board
  xy = board.find_best_position(bw * -1, reversi.level)
  if xy:
    board.put(xy[0], xy[1], bw * -1)
    time.sleep(DELAY)

  draw_board(reversi, dom)


def test_eog(board, dom, bw):
  if ( board.count(core.EMPTY) == 0
       or board.count(core.BLACK) == 0
       or board.count(core.WHITE) == 0 ):
    if board.count(bw) > board.count(bw * -1):
      dom.alert('You win!')
    elif board.count(bw) < board.count(bw * -1):
      dom.alert('You lose!')
    else:
      dom.alert('Tie game!') 
    return True
  return False


def ac_play(reversi, dom, id):
  xy = [int(id[1]), int(id[0])]

  bw = reversi.bw
  token = reversi.token

  if token: # HH mode
    if bw == core.EMPTY:
      if not take_black(token):
        set_status(dom, "Wait for the opponent's move.", "red")
        reversi.bw = core.WHITE
        draw_board(reversi, dom, False)
        return
      reversi.bw = core.BLACK
      bw = core.BLACK
    board = get_board(token)
    if board:
      if board.put(xy[0], xy[1], bw):
        set_turn(token, bw * -1)
        atlastk.broadcast_action("Refresh", token)
    else:
      set_status(dom, "Game interrupted!", "blue")
  else:
    board = reversi.board

    if (board.put(xy[0], xy[1], bw)):
      draw_board(reversi, dom)

    computer_move(reversi, dom)

    test_eog(board, dom, bw)


def ac_toggle_layout(reversi, dom):
  if reversi.layoutFlag:
    dom.enable_element("EnhancedLayout")
  else:
    dom.disable_element("EnhancedLayout")

  reversi.layoutFlag = not reversi.layoutFlag


def new_between_humans(reversi, dom):
  token = str(uuid.uuid4())
  url = atlastk.get_app_url(token)
  dom.inner("qrcode", f'<a href="{url}" title="{url}" target="_blank"><img style="margin: auto; width:100%;" src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={urllib.parse.quote(url)}"/></a>')
  set_status(dom, "Play or wait for the opponent's move.", "green")
  dom.disable_elements(("HideHHStatusSection", "HideHHLinkSection"))
  reversi.init(token=token, board=create(token))
  draw_board(reversi, dom)


def new_versus_computer(reversi, dom, bw):
  reversi.init(level=int(dom.get_value("level")), bw=bw)
  dom.enable_elements(("HideHHStatusSection", "HideHHLinkSection"))

  if bw == core.WHITE:
    draw_board(reversi, dom, False)
    time.sleep(DELAY)
    computer_move(reversi,dom)
  else:
    draw_board(reversi, dom)


def ac_new(reversi, dom):
  players = dom.get_value("players")
  assert players in ["HH", "HC", "CH"]

  if players == "HH":
    new_between_humans(reversi, dom)
  else:
    new_versus_computer(reversi, dom, core.BLACK if players == "HC" else core.WHITE)


def ac_refresh(reversi, dom, id):
  assert id

  token = reversi.token
  board = reversi.board

  if token == id:
    bw = get_turn(token)

    if bw == core.EMPTY:
      set_status(dom, "Game interrupted!", "blue")
    else:
      if reversi.bw == core.EMPTY:
        reversi.bw = core.WHITE
      draw_board(reversi, dom, reversi.bw == bw)
      if test_eog(board, dom, reversi.bw):
        set_status(dom, "Game over!", "blue")
      elif reversi.bw == bw:
        set_status(dom, "It's your turn!", "green")
      else:
        set_status(dom, "Wait for the opponent's move.", "red")
 

CALLBACKS = {
  "": ac_connect,
  "Play": ac_play,
  "ToggleLayout": ac_toggle_layout,
  "New": ac_new,
  "Refresh": ac_refresh,
  "SelectMode": lambda reversi, dom, id: dom.set_attribute("level", "style",
  f"visibility: {'hidden' if dom.get_value(id) == 'HH' else 'visible'};"),
}

atlastk.launch(CALLBACKS, Reversi, open("Head.html").read())