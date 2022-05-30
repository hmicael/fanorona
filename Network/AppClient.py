#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
from threading import Lock
from tkinter import Label

from Application import Application
from TableViewNetwork import TableViewNetwork
from ThreadRcvClient import *


class AppClient(Application):
    """
    Client side application
    """

    def __init__(self, host, port):
        Application.__init__(self)
        self.lock = Lock()
        self.player = "server"
        self.label_info = Label(self, text="Information")
        self.label_info.pack()
        self.thread_connexion = ThreadRcvClient(self, host, port)
        self.thread_connexion.start()

    def set_view(self):
        self.view = TableViewNetwork(self)

    def set_pawn_by_str(self, info):
        """
        Set pawn place by str info: color,col,line
        """
        info = info.split(',')
        if info[0] in ["red", "yellow"]:
            try:
                col, line = int(info[1]), int(info[2])
            except ValueError:
                pass
            else:
                self.table.places[col, line].pawn = info[0]

    def new(self, event=None):
        self.thread_connexion.connexion.send("new".encode("Utf8"))

    def end(self):
        self.thread_connexion.connexion.close()
        self.quit()
        sys.exit()

    def close(self, event=None):
        self.thread_connexion.connexion.send("leave".encode("Utf8"))

    def mouse_down(self, event=None, info=()):
        if type(info) not in (tuple, list):
            raise TypeError("Info must be a list")

        if not info:
            info = [event.x, event.y, self.player]
        Application.mouse_down(self, event, info)
        msg = "mouse_down;{};{};{}".format(info[0], info[1], self.player)
        try:
            self.thread_connexion.connexion.send(msg.encode("Utf8"))
        except BrokenPipeError:
            sys.exit()

    def mouse_move(self, event=None, info=()):
        if type(info) not in (tuple, list):
            raise TypeError("Info must be a list")

        if not info:
            info = [event.x, event.y, self.player]
        Application.mouse_move(self, event, info)
        msg = "mouse_move;{};{};{}".format(info[0], info[1], self.player)
        try:
            self.thread_connexion.connexion.send(msg.encode("Utf8"))
        except BrokenPipeError:
            sys.exit()

    def mouse_up(self, event=None, info=()):
        if type(info) not in (tuple, list):
            raise TypeError("Info must be a list")

        if not info:
            info = [event.x, event.y, self.player]
        Application.mouse_up(self, event, info)
        self.label_info.config(text="Status: Opponent Turn")
        msg = "mouse_up;{};{};{}".format(info[0], info[1], self.player)
        try:
            self.thread_connexion.connexion.send(msg.encode("Utf8"))
        except BrokenPipeError:
            sys.exit()


if __name__ == '__main__':
    AppClient("192.168.182.8", 40000).mainloop()
