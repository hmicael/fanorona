# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
import pickle
import time
from tkinter import *

from Table import *
from TableView import *


class Application(Frame):
    """Fenêtre principale de l'application"""

    def __init__(self):
        Frame.__init__(self)
        self.turn = 0
        self.hits = 0
        self.xMove, self.yMove = 0, 0  # Determine the movement of the mouse
        self.scores = {
            "red": 0,
            "yellow": 0
        }
        self.labels = {
            "red": Label(text="RED: {} points".format(self.scores["red"])),
            "yellow": Label(text="YELLOW: {} points".format(self.scores["yellow"])),
        }
        self.view = None
        self.table = Table()
        self.labels["red"].pack(side=TOP)
        self.labels["yellow"].pack(side=BOTTOM)
        self.pack()
        self.spec()

    def spec(self):
        self.view = TableView(self)
        #self.view.draw()
        self.master.title('>>>>> PLAY THIS FUCKING GAME <<<<<')
        self.view.bind("<Button-1>", self.mouseDown)
        self.view.bind("<Button1-Motion>", self.mouseMove)
        self.view.bind("<Button1-ButtonRelease>", self.mouseUp)
        self.bind('<Destroy>', self.close)
        self.view.pack(padx=10, pady=10)
        self.packing()

    def packing(self):
        fileMenu = Menubutton(self, text='File')
        menu1 = Menu(fileMenu)
        menu1.add_command(label='New', underline=0, command=self.new)
        menu1.add_command(label='Save', underline=0, command=self.save)
        menu1.add_command(label='Restore', underline=0, command=self.restore)
        menu1.add_command(label='Exit', underline=0, command=self.close)
        fileMenu.configure(menu=menu1)
        fileMenu.pack(anchor=NW)

    def mouseDown(self, event=None, info=()):
        if type(info) not in (tuple, list):
            raise TypeError("Info must be a list")

        if event and not info:
            info = [event.x, event.y, ""]
        self.view.mouseDown(info)

    def mouseMove(self, event=None, info=()):
        if type(info) not in (tuple, list):
            raise TypeError("Info must be a list")

        if event and not info:
            info = [event.x, event.y, ""]
        self.view.mouseMove(info)

    def mouseUp(self, event=None, info=()):
        if type(info) not in (tuple, list):
            raise TypeError("Info must be a list")

        if event and not info:
            info = [event.x, event.y, ""]
        self.view.mouseUp(info)
        return self.checkFinish()

    def checkFinish(self):
        if self.table.winner in ('red', 'yellow'):
            self.scores[self.table.winner] += 1
            text = "{} : {} points".format(self.table.winner.upper(), self.scores[self.table.winner])
            self.labels[self.table.winner].config(text=text)
            self.table.winner = ""
            self.hits = 0
            self.table = Table()
            self.table.randomPlacing()
            time.sleep(1)
            self.view.draw()
            return True
        return False

    def new(self):
        self.hits = 0
        self.turn = 0
        self.table = Table()
        time.sleep(0.5)
        self.table.randomPlacing()
        self.view.draw()
        self.scores = {
            "red": 0,
            "yellow": 0
        }
        for key in self.labels.keys():
            self.labels[key].config(text="{} : {} points".format(key.upper(), self.scores[key]))

    def close(self, event=None):
        sys.exit()

    def save(self):
        with open('data.txt', 'wb') as file:
            pickler = pickle.Pickler(file)
            data = {
                "table": self.table,
                "hits": self.hits,
                "turn": self.turn,
                "scores": self.scores
            }
            pickler.dump(data)
            file.close()

    def restore(self):
        with open('data.txt', 'rb') as file:
            unpickler = pickle.Unpickler(file)
            try:
                data = unpickler.load()
            except:
                print("Save is corrupted")
            else:
                self.table = data["table"]
                self.hits = data["hits"]
                self.turn = data["turn"]
                self.scores = data["scores"]
                time.sleep(0.5)
                # self.setView()
                self.view.draw()
                for key in self.labels.keys():
                    self.labels[key].config(text="{} : {} points".format(key.upper(), self.scores[key]))
            file.close()

if __name__ == '__main__':
    Application().mainloop()
