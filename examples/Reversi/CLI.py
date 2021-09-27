#!/usr/bin/env python3
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

# from term2web import *

# T2WS = True

import os, sys

DEFAULT = ''

if ('Q37_XPP' in os.environ):
  sys.path.append(os.path.join(os.environ["HOME"],"epeios/other/libs/term2web/PYH/term2web"))
  from term2web import *
  DEFAULT = 'a'
  T2WS = True 
 
T2W = 'term2web' in sys.modules

from core import *

BLACK_MARK = 'X'
WHITE_MARK = 'O'
LEVEL = 1

def is_t2ws():
  try:
    return T2W and T2WS
  except:
    return False
      
def t2w_sp(list_or_name, value=None):
  if not is_t2ws():
    return

  if value is None:
    set_properties(list_or_name)
  else:
    set_property(list_or_name, value)

def t2w_rp():
  if not is_t2ws():
    return

  reset_properties()
  set_property("font-size", "large")

def print_board(board):
  print('\n ', end="")
  t2w_sp("background-color", "aqua")
  print('  a b c d e f g h ')
  t2w_rp()
  print(' ', end='')
  t2w_sp("background-color", "aqua")
  print(' ', end='')
  t2w_rp()
  print('+-+-+-+-+-+-+-+-+')
  for i, row in enumerate(board.array()):
    print(' ', end='')
    t2w_sp("background-color", "aqua")
    print((i + 1), end='')
    t2w_rp()
    print('|', end='')
    for j, r in enumerate(row):
      t2w_sp('font-weight', 'bolder')
      if r == EMPTY:
        if board.isAllowed(i,j,BLACK):
          t2w_sp('background-color', 'lightgreen')
        elif board.isAllowed(i,j,WHITE):
          t2w_sp('background-color', 'lightblue')
      t2w_sp(
        'color', {
          EMPTY: 'white',
          BLACK: 'green',
          WHITE: 'blue'
        }[r]
      )
      print({
        EMPTY: ' ',
        BLACK: BLACK_MARK,
        WHITE: WHITE_MARK
      }[r], end='')
      t2w_rp()
      print('|', end='')
    print('\n ', end='')
    t2w_sp("background-color", "aqua")
    print(' ', end='')
    t2w_rp()
    print('+-+-+-+-+-+-+-+-+')
  print()


def input_position(player):
  while True:
    s = input('{}? [a-h][1-8]'.format(BLACK_MARK if player ==
                      BLACK else WHITE_MARK)).lower()
    if s == '' or (len(s) == 2 and s[0] in list('abcdefgh')
             and s[1] in list('12345678')):
      break
  if s == '':
    return None

  y, x = ord(s[0]) - 97, ord(s[1]) - 49
  #print('input_position=', x, y)
  return x, y


def print_position(player, xy):
  if xy is None:
    print('{}: skip'.format(BLACK_MARK if player == BLACK else WHITE_MARK))
  else:
    print('{}: {}{}'.format(BLACK_MARK if player == BLACK else WHITE_MARK,
                chr(xy[1] + 97), chr(xy[0] + 49)))


board = None
humans = []

def humanTurn(player):
  xy = input_position(player)
  while xy and not board.put(xy[0], xy[1], player):
      xy = input_position(player)

def computerTurn(player):
  xy = board.find_best_position(player,LEVEL)
  if xy:
    board.put(xy[0], xy[1], player)
  print_position(player, xy)

def turn(player):
  if player in humans:
    humanTurn(player)
  else:
    computerTurn(player)
  print_board(board)
  if not humans:
    input("Hit Enter key to continue.")

TYPES = {
  'a': [BLACK],
  'b': [WHITE],
  'c': [BLACK, WHITE],
  'd': []
}

def getHumans():
  global humans
  answer = DEFAULT

  while answer not in TYPES:
    print("a: 'X' human, 'O' computer")
    print("b: 'O' computer, 'X' human")
    print("c: 'X' human, 'O' human")
    print("d: 'X' computer, 'O' computer")
    answer = input("Please choose ('X' begins): ").lower()

  humans = TYPES[answer]

def start_game():
  global board
  board = Board()

  getHumans()

  print_board(board)

  while (board.count(EMPTY) != 0 and board.count(BLACK) != 0
         and board.count(WHITE) != 0):
    turn(BLACK)
    turn(WHITE)

  print_board(board)
  print(f"'X': {board.count(BLACK)}, 'O': {board.count(WHITE)}")
  if board.count(BLACK) > board.count(WHITE):
    print("'X' wins!")
  elif board.count(BLACK) < board.count(WHITE):
    print("'Y' wins!")
  else:
    print('Equality)')

if __name__ == "__main__":
  start_game()
