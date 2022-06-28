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


def uploadDice(affix):
  return open(f"{affix}.svg").read()


def uploadDices():
  global dices

  dices[0] = uploadDice("Pig")

  for i in range(1, 7):
    dices[i] = uploadDice(f"dice-{i}")


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
      removeGame(self.token, self._player)

  def init(self, token = None):
    deleted = False

    if self.token:
      deleted = removeGame(self.token, self._player)

    self.token = token
    self._game = None if token else Game()  
    self._player = 0

    return deleted

  def getGame(self):
    if self.token:
      game = getGame(self.token)
      if game is None:
        self.token = None
    else:
      game = self._game

    return game

  def getRawPlayer(self):
    return self._player

  def getPlayer(self): # Assign a place, if not yet done, and if possible.
    if self._player == 0:
      self._player = getGameAvailablePlayer(self.token) if self.token else getAvailablePlayer(self._game)

    return self._player


def debug():
  try:
    return DEBUG
  except:
    return False    


def createGame(token):
  global games

  game = Game()  

  with lock:
    games[token] = game
    if debug():
      print("Create: ", token)

  return game


def removeGame(token, player):
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


def getGame(token):
  with lock:
    return games[token] if token in games else None


def getAvailablePlayer(game):
  player = 0

  if game.available:
    player = game.available

    game.available = 2 if game.available == 1 else 0

  return player


def getGameAvailablePlayer(token):
  with lock:
    return getAvailablePlayer(games[token]) if token in games else 0


def fade(dom, element):
  dom.removeClass(element, "fade-in")
  dom.flush()
  dom.addClass(element, "fade-in")


def updateMeter(dom, ab, score, turn, dice): # turn includes dice
  if turn != 0:
    dom.end(f"ScoreMeter{ab}", METER.format("fade-in dice-meter", dice))
  else:
    dom.inner(f"ScoreMeter{ab}", METER.format("score-meter", score))

  dom.setValue(f"ScoreText{ab}", score)


def disableGameControls(dom):
  dom.disableElements(GAME_CONTROLS)


def enableGameControls(dom):
  dom.enableElements(GAME_CONTROLS)


def disablePlayControls(dom):
  dom.disableElements(PLAY_CONTROLS)


def enablePlayControls(dom):
  dom.enableElements(PLAY_CONTROLS)


def getOpponent(playerAB):
  if playerAB == 'A':
    return 'B'
  elif playerAB == 'B':
    return 'A'
  elif playerAB == 1:
    return 2
  else:
    return 1


def markPlayer(dom, ab):
  if ab == 'B':
    dom.disableElement("DisplayMarkerA")
  else:
    dom.enableElement("DisplayMarkerA")


def displayDice(dom, value):
  fade(dom, "dice")

  if value <= 6:
    dom.inner("dice", dices[value])


def updateMeters(dom, game, myTurn):
  if myTurn is None:
    a, b = 1, 2
    turnA = game.turn if game.current == 1 else 0
    turnB = game.turn if game.current == 2 else 0
    diceA = game.dice if game.current == 1 else 0
    diceB = game.dice if game.current == 2 else 0
  else:  
    a = game.current if myTurn else getOpponent(game.current)
    b = getOpponent(a)
    turnA = game.turn if myTurn else 0
    turnB = 0 if myTurn else game.turn
    diceA = game.dice if myTurn else 0
    diceB = 0 if myTurn else game.dice

  updateMeter(dom, 'A', game.scores[a], turnA, diceA)
  updateMeter(dom, 'B', game.scores[b], turnB, diceB)


def updateMarkers(dom, game, myTurn):
  if myTurn is None:
    markPlayer(dom, 'A' if game.current == 1 else 'B')
  elif myTurn:
    markPlayer(dom, 'A')
  else:
    markPlayer(dom, 'B')


def updatePlayControls(dom, myTurn, winner):
  if myTurn is None or not myTurn or winner != 0:
    disablePlayControls(dom)
  else:
    enablePlayControls(dom)


def displayTurn(dom, element, value):
    fade(dom, element)
    dom.setValue(element, value)


def updateDice(dom, game, winner):
  if winner != 0 or game.turn != 0 or game.dice == 1:
    displayDice(dom, game.dice)


def updateTurn(dom, game):
  displayTurn(dom, "Cumul", game.turn)
  displayTurn(dom, "Total", game.scores[game.current] + game.turn)


def reportWinner(dom, player, winner):
  ab = 'A' if winner == player or player == 0 and winner == 1 else 'B'
  dom.setValue(f"ScoreMeter{ab}", "<span style='background-color: lightgreen; width: 100%;'><span class='winner'>Winner!</span></span>")
  dom.setValue(f"ScoreText{ab}", 100)


def updateLayout(dom, game, player):
  if game.scores[1] + (game.turn if game.current == 1 else 0) >= LIMIT:
    winner = 1
  elif game. scores[2] + (game.turn if game.current == 2 else 0) >= LIMIT:
    winner = 2
  else:
    winner = 0

  if player != 0:
    myTurn = player == game.current
  elif game.available != 0:
    myTurn = game.available == game.current
  else:
    myTurn = None

  updateDice(dom, game, winner)
  updateTurn(dom, game)
  updateMeters(dom, game, myTurn)
  updateMarkers(dom, game, myTurn)
  updatePlayControls(dom, myTurn, winner)

  if winner != 0:
    reportWinner(dom, player, winner)


def display(dom, game, player):
  if game is None:
    disablePlayControls(dom)
    dom.alert("Game aborted!")
    return

  if game.available == 0 and player == 0:
    dom.disableElement("PlayerView")

  updateLayout(dom, game, player)


def setLayout(dom):
  dom.inner("", open("Main.html").read())

  if debug():
    dom.removeClass("debug", "removed")


def acConnect(user, dom, id):
  setLayout(dom)
  displayDice(dom, 0)

  user.init(id)
  display(dom, user.getGame(), user.getRawPlayer())


def getPlayer(user, dom):
  return user.getPlayer()


def botDecision(botScore, turnScore, humanScore, timesThrown):
  return turnScore < 20
  # Replace by your own algorithm.
  # Algorithm can be more elaborate by using the other parameters.


def computerTurn(game, dom):
  game.current = 2
  timesThrown = 0

  disableGameControls(dom)

  time.sleep(1)

  while True:
    game.dice = random.randint(1, 6)
    timesThrown += 1

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

    if not botDecision(game.scores[2], game.turn, game.scores[1], timesThrown):
      game.scores[2] += game.turn
      game.turn = 0
      game.current = 1
      display(dom, game, 1)
      break;

  enableGameControls(dom)


def broadcast(token):
  atlastk.broadcastAction("Display", token)


def acRoll(user, dom):
  disablePlayControls(dom)
  player = getPlayer(user, dom)

  if player == 0:
    return

  game = user.getGame()

  if game is None:
    broadcast(user.token)
    return

  game.dice = random.randint(1, 6)

  if debug():
    debugDice = dom.getValue("debug")
    if debugDice:
      game.dice = int(debugDice)

  if game.dice == 1:
    game.current = getOpponent(game.current)
    game.turn = 0
  else:
    game.turn += game.dice

  if user.token:
    broadcast(user.token)
  else:
    display(dom, game, 1)
    if game.dice == 1:
      computerTurn(game, dom)


def acHold(user, dom):
  disablePlayControls(dom)

  player = getPlayer(user, dom)

  if player == 0:
    return

  game = user.getGame()

  if game is None:
    disablePlayControls(dom)
    dom.alert("Game aborted!")
    return

  game.scores[player] += game.turn
  game.current = getOpponent(game.current)
  game.turn = 0
  game.dice = 0

  if user.token:
    broadcast(user.token)
  else:
    display(dom, game, 1)
    computerTurn(game, dom)


def newBetweenHumans(user, dom):
  global games

  token = "debug" if debug() else str(uuid.uuid4())

  createGame(token)

  url = atlastk.getAppURL(token)
  dom.inner("qrcode", f'<a href="{url}" title="{url}" target="_blank"><img style="margin: auto; width:100%;" src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={urllib.parse.quote(url)}&bgcolor=FFB6C1"/></a>')
  dom.disableElement("HideHHLinkSection")

  return user.init(token)


def newAgainstComputer(user, dom):
  dom.enableElement("HideHHLinkSection")
  deleted = user.init()

  user.getPlayer() ## To assign player.
  getAvailablePlayer(user.getGame()) # To eat remaining available player.

  return deleted


def acNew(user, dom):
  mode = dom.getValue("Mode")
  token = user.token

  setLayout(dom)
  dom.enableElement("PlayerView")
  displayDice(dom, 0)

  deleted = newAgainstComputer(user, dom) if mode == "HC" else newBetweenHumans(user, dom)

  display(dom, user.getGame(), 1)

  if deleted:
    broadcast(token)


def acDisplay(user, dom, id):
  if id != user.token:
    return

  game = user.getGame()

  if game is None:
    disablePlayControls(dom)
    dom.alert("Game aborted!")
    return

  display(dom, user.getGame(), user.getRawPlayer())


CALLBACKS = {
  "": acConnect,
  "Roll": acRoll,
  "Hold": acHold,
  "New": acNew,
  "Display": acDisplay
}

uploadDices()

atlastk.launch(CALLBACKS, User, open("Head.html").read())
