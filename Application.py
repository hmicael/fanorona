# !/usr/bin/python3.8
# -*- coding: utf-8 -*-

import pickle
import time
import traceback
from tkinter import messagebox

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
        # self.table.random_placing()
        self.labels["red"].pack(side=TOP)
        self.labels["yellow"].pack(side=BOTTOM)

        self.set_view()
        self.set_view_button_action()
        self.pack()

    def set_view(self):
        self.view = TableView(self)

    def set_view_button_action(self):
        self.view.draw_pawns()
        self.master.title('>>>>> PLAY THIS FUCKING GAME <<<<<')
        self.view.bind("<Button-1>", self.mouse_down)
        self.view.bind("<Button1-Motion>", self.mouse_move)
        self.view.bind("<Button1-ButtonRelease>", self.mouse_up)
        self.bind('<Destroy>', self.pop_quit_choice)
        self.master.protocol("WM_DELETE_WINDOW", self.pop_quit_choice)
        self.set_menu_bar()
        self.view.pack(padx=10, pady=10)

    def set_menu_bar(self):
        menu_bar = Menu(self)
        menu_file = Menu(menu_bar, tearoff=0)
        menu_file.add_command(label='New', underline=0, accelerator="Ctrl+N", command=self.new)
        menu_file.add_command(label='Save', underline=0, accelerator="Ctrl+S", command=self.save)
        menu_file.add_command(label='Restore', underline=0, accelerator="Ctrl+R", command=self.restore)
        menu_file.add_separator()
        menu_file.add_command(label='Exit', underline=1, accelerator="Ctrl+Q", command=self.pop_quit_choice)
        menu_bar.add_cascade(label="File", menu=menu_file)
        self.master.config(menu=menu_bar)
        self.bind_all("<Control-n>", self.new)
        self.bind_all("<Control-s>", self.save)
        self.bind_all("<Control-r>", self.restore)
        self.bind_all("<Control-q>", self.pop_quit_choice)

    def pop_quit_choice(self, event=None):
        want_to_quit = messagebox.askyesno(
            message="Do you want to quit the game?", icon="question", title="Quit")
        if want_to_quit:
            self.close()

    def mouse_down(self, event=None, info=()):
        if type(info) not in (tuple, list):
            raise TypeError("Info must be a list")

        if event and not info:
            info = [event.x, event.y, ""]
        self.view.mouse_down(info)

    def mouse_move(self, event=None, info=()):
        if type(info) not in (tuple, list):
            raise TypeError("Info must be a list")

        if event and not info:
            info = [event.x, event.y, ""]
        self.view.mouse_move(info)

    def mouse_up(self, event=None, info=()):
        if type(info) not in (tuple, list):
            raise TypeError("Info must be a list")

        if event and not info:
            info = [event.x, event.y, ""]
        self.view.mouse_up(info)
        return self.check_finish()

    def check_finish(self):
        if self.table.winner in ("red", "yellow"):
            self.scores[self.table.winner] += 1
            text = "{} : {} points".format(self.table.winner.upper(), self.scores[self.table.winner])
            replay = messagebox.askyesno(
                message="Do you want to continue ?", icon="question", title="Replay")
            if replay:
                self.labels[self.table.winner].config(text=text)
                self.table.winner = ""
                self.hits = 0
                self.table = Table()
                self.table.random_placing()
                self.view.draw_pawns()
                return True
            else:
                self.close()
        return False

    def new(self, event=None):
        self.hits = 0
        self.turn = 0
        self.table = Table()
        time.sleep(0.5)
        self.table.random_placing()
        self.view.draw_pawns()
        self.scores = {
            "red": 0,
            "yellow": 0
        }
        for key in self.labels.keys():
            self.labels[key].config(text="{} : {} points".format(key.upper(), self.scores[key]))

    def close(self, event=None):
        sys.exit()

    def save(self, event=None):
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

    def restore(self, event=None):
        with open('data.txt', 'rb') as file:
            unpickler = pickle.Unpickler(file)
            try:
                data = unpickler.load()
            except pickle.UnpicklingError as e:
                print(traceback.format_exc(e))
                pass
            except (AttributeError, EOFError, ImportError, IndexError) as e:
                # secondary errors
                print(traceback.format_exc(e))
                pass
            except Exception as e:
                # everything else, possibly fatal
                print(traceback.format_exc(e))
                pass
            else:
                self.table = data["table"]
                self.hits = data["hits"]
                self.turn = data["turn"]
                self.scores = data["scores"]
                time.sleep(0.5)
                # self.setView()
                self.view.draw_pawns()
                for key in self.labels.keys():
                    self.labels[key].config(text="{} : {} points".format(key.upper(), self.scores[key]))
            file.close()


if __name__ == '__main__':
    Application().mainloop()
