#!/usr/bin/env python3
"""
MIT License

Copyright (c) 2021 Claude SIMON (https://q37.info/s/rmnmqd49)

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
sys.path.extend(["../../atlastk", "."])

import atlastk, random, threading, time, urllib, uuid

#DEBUG = True  # Uncomment for debug mode.

# To put checkpoints.
# from XDHq import l

LIMIT = 100

GAME_CONTROLS = ["New"]
PLAY_CONTROLS = ["Roll", "Hold"]

METER = '<span class="{}" style="width: {}%;"></span>'

lock = threading.Lock()
games = {}

dices = {}


def upload_dice(affix):
  return open(f"{affix}.svg").read()


def upload_dices():
  global dices

  dices[0] = upload_dice("Pig")

  for i in range(1, 7):
    dices[i] = upload_dice(f"dice-{i}")


class Game:
  def __init__(self):
    self.current = 1 # 1 or 2

    self.available = 1 # 0 (no more player available), 1 or 2

    self.scores = {
      1: 0,
      2: 0
    }

    self.turn = 0  
    self.dice = 0


class User:
  def __init__(self):
    self._player = 0
    self._game = None
    self.token = None   # == None ('_game' != None): 2 human players
                        # != None ('_game' == None): human vs computer.
  def __del__(self):
    if self.token:
      remove_game(self.token, self._player)

  def init(self, token = None):
    deleted = False

    if self.token:
      deleted = remove_game(self.token, self._player)

    self.token = token
    self._game = None if token else Game()  
    self._player = 0

    return deleted

  def get_game(self):
    if self.token:
      game = get_game(self.token)
      if game is None:
        self.token = None
    else:
      game = self._game

    return game

  def get_raw_player(self):
    return self._player

  def get_player(self): # Assign a place, if not yet done, and if possible.
    if self._player == 0:
      self._player = get_game_available_player(self.token) if self.token else get_available_player(self._game)

    return self._player


def debug():
  try:
    return DEBUG
  except:
    return False    


def create_game(token):
  global games

  game = Game()  

  with lock:
    games[token] = game
    if debug():
      print("Create: ", token)

  return game


def remove_game(token, player):
  with lock:
    if token in games:
      game = games[token]

      print(game.available, player)
      if game.available == 1 or player != 0:
        del games[token]
        if debug():
          print("Remove: ", token)
        return True

  return False


def get_game(token):
  with lock:
    return games[token] if token in games else None


def get_available_player(game):
  player = 0

  if game.available:
    player = game.available

    game.available = 2 if game.available == 1 else 0

  return player


def get_game_available_player(token):
  with lock:
    return get_available_player(games[token]) if token in games else 0


def fade(dom, element):
  dom.remove_class(element, "fade-in")
  dom.flush()
  dom.add_class(element, "fade-in")


def update_meter(dom, ab, score, turn, dice): # turn includes dice
  if turn != 0:
    dom.end(f"ScoreMeter{ab}", METER.format("fade-in dice-meter", dice))
  else:
    dom.inner(f"ScoreMeter{ab}", METER.format("score-meter", score))

  dom.set_content(f"ScoreText{ab}", score)


def disable_game_controls(dom):
  dom.disable_elements(GAME_CONTROLS)


def enable_game_controls(dom):
  dom.enable_elements(GAME_CONTROLS)


def disable_play_controls(dom):
  dom.disable_elements(PLAY_CONTROLS)


def enable_play_controls(dom):
  dom.enable_elements(PLAY_CONTROLS)


def get_opponent(player_ab):
  if player_ab == 'A':
    return 'B'
  elif player_ab == 'B':
    return 'A'
  elif player_ab == 1:
    return 2
  else:
    return 1


def mark_player(dom, ab):
  if ab == 'B':
    dom.disable_element("DisplayMarkerA")
  else:
    dom.enable_element("DisplayMarkerA")


def display_dice(dom, value):
  fade(dom, "dice")

  if value <= 6:
    dom.inner("dice", dices[value])


def update_meters(dom, game, my_turn):
  if my_turn is None:
    a, b = 1, 2
    turn_A = game.turn if game.current == 1 else 0
    turn_B = game.turn if game.current == 2 else 0
    dice_A = game.dice if game.current == 1 else 0
    dice_B = game.dice if game.current == 2 else 0
  else:  
    a = game.current if my_turn else get_opponent(game.current)
    b = get_opponent(a)
    turn_A = game.turn if my_turn else 0
    turn_B = 0 if my_turn else game.turn
    dice_A = game.dice if my_turn else 0
    dice_B = 0 if my_turn else game.dice

  update_meter(dom, 'A', game.scores[a], turn_A, dice_A)
  update_meter(dom, 'B', game.scores[b], turn_B, dice_B)


def update_markers(dom, game, my_turn):
  if my_turn is None:
    mark_player(dom, 'A' if game.current == 1 else 'B')
  elif my_turn:
    mark_player(dom, 'A')
  else:
    mark_player(dom, 'B')


def update_play_controls(dom, my_turn, winner):
  if my_turn is None or not my_turn or winner != 0:
    disable_play_controls(dom)
  else:
    enable_play_controls(dom)


def display_turn(dom, element, value):
    fade(dom, element)
    dom.set_content(element, value)


def update_dice(dom, game, winner):
  if winner != 0 or game.turn != 0 or game.dice == 1:
    display_dice(dom, game.dice)


def update_turn(dom, game):
  display_turn(dom, "Cumul", game.turn)
  display_turn(dom, "Total", game.scores[game.current] + game.turn)


def report_winner(dom, player, winner):
  if winner == player or player == 0 and winner == 1:
    ab = 'A'
  else:
    ab = 'B'

  dom.set_content(f"ScoreMeter{ab}", "<span style='background-color: lightgreen; width: 100%;'><span class='winner'>Winner!</span></span>")
  dom.set_content(f"ScoreText{ab}", 100)


def update_layout(dom, game, player):
  if game.scores[1] + (game.turn if game.current == 1 else 0) >= LIMIT:
    winner = 1
  elif game. scores[2] + (game.turn if game.current == 2 else 0) >= LIMIT:
    winner = 2
  else:
    winner = 0

  if player != 0:
    my_turn = player == game.current
  elif game.available != 0:
    my_turn = game.available == game.current
  else:
    my_turn = None

  update_dice(dom, game, winner)
  update_turn(dom, game)
  update_meters(dom, game, my_turn)
  update_markers(dom, game, my_turn)
  update_play_controls(dom, my_turn, winner)

  if winner != 0:
    report_winner(dom, player, winner)


def display(dom, game, player):
  if game is None:
    disable_play_controls(dom)
    dom.alert("Game aborted!")
    return

  if game.available == 0 and player == 0:
    dom.disable_element("PlayerView")

  update_layout(dom, game, player)


def set_layout(dom):
  dom.inner("", open("Main.html").read())

  if debug():
    dom.remove_class("debug", "removed")


def ac_connect(user, dom, id):
  set_layout(dom)
  display_dice(dom, 0)

  user.init(id)
  display(dom, user.get_game(), user.get_raw_player())


def get_player(user, dom):
  return user.get_player()


def bot_decision(bot_score, turn_score, human_score, times_thrown):
  return turn_score < 20
  # Replace by your own algorithm.


def computer_turn(game, dom):
  game.current = 2
  times_thrown = 0

  disable_game_controls(dom)

  time.sleep(1)

  while True:
    game.dice = random.randint(1, 6)
    times_thrown += 1

    if game.dice == 1:
      game.turn = 0
      game.current = 1
      display(dom, game, 1)
      break;

    game.turn += game.dice

    if game.scores[2] + game.turn >= LIMIT:
      display(dom, game, 1)
      break

    display(dom, game, 1)
    time.sleep(2.5)    

    if not bot_decision(game.scores[2], game.turn, game.scores[1], times_thrown):
      game.scores[2] += game.turn
      game.turn = 0
      game.current = 1
      display(dom, game, 1)
      break;

  enable_game_controls(dom)


def broadcast(token):
  atlastk.broadcast_action("Display", token)


def ac_roll(user, dom):
  disable_play_controls(dom)
  player = get_player(user, dom)

  if player == 0:
    return

  game = user.get_game()

  if game is None:
    broadcast(user.token)
    return

  game.dice = random.randint(1, 6)

  if debug():
    debug_dice = dom.get_content("debug")
    if debug_dice:
      game.dice = int(debug_dice)

  if game.dice == 1:
    game.current = get_opponent(game.current)
    game.turn = 0
  else:
    game.turn += game.dice

  if user.token:
    broadcast(user.token)
  else:
    display(dom, game, 1)
    if game.dice == 1:
      computer_turn(game, dom)


def ac_hold(user, dom):
  disable_play_controls(dom)

  player = get_player(user, dom)

  if player == 0:
    return

  game = user.get_game()

  if game is None:
    disable_play_controls(dom)
    dom.alert("Game aborted!")
    return

  game.scores[player] += game.turn
  game.current = get_opponent(game.current)
  game.turn = 0
  game.dice = 0

  if user.token:
    broadcast(user.token)
  else:
    display(dom, game, 1)
    computer_turn(game, dom)


def new_between_humans(user, dom):
  global games

  token = "debug" if debug() else str(uuid.uuid4())

  create_game(token)

  url = atlastk.get_app_url(token)
  dom.inner("qrcode", f'<a href="{url}" title="{url}" target="_blank"><img style="margin: auto; width:100%;" src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={urllib.parse.quote(url)}&bgcolor=FFB6C1"/></a>')
  dom.disable_element("HideHHLinkSection")

  return user.init(token)


def new_against_computer(user, dom):
  dom.enable_element("HideHHLinkSection")
  deleted = user.init()

  user.get_player() ## To assign player.
  get_available_player(user.get_game()) # To eat remaining available player.

  return deleted


def ac_new(user, dom):
  mode = dom.get_content("Mode")
  token = user.token

  set_layout(dom)
  dom.enable_element("PlayerView")
  display_dice(dom, 0)

  deleted = new_against_computer(user, dom) if mode == "HC" else new_between_humans(user, dom)

  display(dom, user.get_game(), 1)

  if deleted:
    broadcast(token)


def ac_display(user, dom, id):
  if id != user.token:
    return

  game = user.get_game()

  if game is None:
    disable_play_controls(dom)
    dom.alert("Game aborted!")
    return

  display(dom, user.get_game(), user.get_raw_player())


CALLBACKS = {
  "": ac_connect,
  "Roll": ac_roll,
  "Hold": ac_hold,
  "New": ac_new,
  "Display": ac_display
}

upload_dices()

atlastk.launch(CALLBACKS, User, open("Head.html").read())
