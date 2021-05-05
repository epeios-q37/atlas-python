#!/usr/bin/env python3
################################################################################
# MIT License
# 
# Copyright (c) 2020 Hajime Nakagami <nakagami@gmail.com>
# Copyright (c) 2021 Claude SIMON (https://q37.info/s/rmnmqd49)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
################################################################################

from tkinter import *
from tkinter import font
import tkinter.messagebox
from functools import partial
import tkinter as tk

import core as reversi


def player_put_action(app, press_x, press_y):
  def wrapper(obj=app, x=press_x, y=press_y):
    return obj.player_put(x, y)
  return wrapper


class App(Frame):
  def __init__(self):
    super().__init__()
    self.master.title('TkReversi')
    frame = Frame(self)
    self.player_color = reversi.BLACK
    self.level = None

    l = Label(frame, text="Level:")
    l.grid(row=1, column=1, columnspan=2)
    self.spin = Spinbox(frame, from_=1, to=2, command=self.restart)
    self.spin.grid(row=1, column=4, columnspan=6)

    self.buttons = [[None] * 8 for _ in range(8)]
    for i in range(8):
      for j in range(8):
        self.buttons[i][j] = Button(frame, font=("Courier", 20),command=player_put_action(self, i, j))
        self.buttons[i][j].grid(row=i+2, column=j+1)

    b = Button(frame, text="pass", command=self.player_pass)
    b.grid(row=10, column=1, columnspan=2)
    self._indicator = StringVar()
    l = Label(frame, textvariable=self._indicator)
    l.grid(row=10, column=3, columnspan=6)
    frame.pack()

    self.pack()
    self.show_message("You: ●")

    self.restart()

  def computer_put(self):
    xy = self.reversi.find_best_position(self.player_color * -1, self.level)
    if xy:
      self.reversi.put(xy[0], xy[1], self.player_color * -1)

  def update_board(self):
    if len(self.buttons) == 0:
      return
    for i in range(8):
      for j in range(8):
        self.buttons[i][j]["text"] = {
          reversi.BLACK: "●",
          reversi.WHITE: "○",
          reversi.EMPTY: " ",
        }[self.reversi.array()[i][j]]

    # check finish
    if not (
      self.reversi.count(reversi.EMPTY) == 0 or
      self.reversi.count(reversi.BLACK) == 0 or
      self.reversi.count(reversi.WHITE) == 0
    ):
      return
    if self.reversi.count(self.player_color) > self.reversi.count(self.player_color * -1):
      tkinter.messagebox.showinfo("TkReverse", "You win!")
      self.show_message('You win!')
    elif self.reversi.count(self.player_color) < self.reversi.count(self.player_color * -1):
      tkinter.messagebox.showinfo("TkReverse", "You lose!")
      self.show_message('You lose!')

  def restart(self):
    level = int(self.spin.get())
    if self.level != level:
      self.level = level
      self.reversi = reversi.Board()
      self.update_board()

  def player_put(self, x, y):
    if not self.buttons:
      return
    if self.reversi.put(x, y, self.player_color):
      self.computer_put()
    self.update_board()

  def player_pass(self):
    self.computer_put()
    self.update_board()

  def show_message(self, s):
    self._indicator.set(s)


if __name__ == "__main__":
  app = App()
  app.mainloop()