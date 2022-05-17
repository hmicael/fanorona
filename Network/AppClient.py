#!/usr/bin/python3.6
from threading import Lock

from Fanorona.Application import Application
from Fanorona.Network.TableViewNetwork import TableViewNetwork
from Fanorona.Network.ThreadRcvClient import *


class AppClient(Application):
    """
    Client side application
    """

    def __init__(self, host, port):
        Application.__init__(self)
        self.lock = Lock()
        self.player = "server"
        self.threadConnexion = ThreadRcvClient(self, host, port)
        self.threadConnexion.start()

    def spec(self):
        self.view = TableViewNetwork(self)
        self.view.draw()
        self.master.title('>>>>> PLAY THIS FUCKING GAME <<<<<')
        self.view.bind("<Button-1>", self.mouseDown)
        self.view.bind("<Button1-Motion>", self.mouseMove)
        self.view.bind("<Button1-ButtonRelease>", self.mouseUp)
        self.bind('<Destroy>', self.close)
        self.view.pack(padx=10, pady=10)

    def setPawnByStr(self, info):
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
        else:
            pass

    def new(self):
        self.threadConnexion.connexion.send("new".encode("Utf8"))

    def end(self):
        self.threadConnexion.connexion.close()
        self.quit()
        sys.exit()

    def close(self, event=None):
        self.threadConnexion.connexion.send("leave".encode("Utf8"))

    def mouseDown(self, event=None, info=[]):
        if type(info) != 'list':
            raise TypeError("Info must be a list")

        if not info:
            info = [event.x, event.y, self.player]
        Application.mouseDown(self, event, info)
        msg = "mouseDown;{};{};{}".format(info[0], info[1], self.player)
        try:
            self.threadConnexion.connexion.send(msg.encode("Utf8"))
        except BrokenPipeError:
            sys.exit()

    def mouseMove(self, event=None, info=[]):
        if type(info) != 'list':
            raise TypeError("Info must be a list")

        if not info:
            info = [event.x, event.y, self.player]
        Application.mouseMove(self, event, info)
        msg = "mouseMove;{};{};{}".format(info[0], info[1], self.player)
        try:
            self.threadConnexion.connexion.send(msg.encode("Utf8"))
        except BrokenPipeError:
            sys.exit()

    def mouseUp(self, event=None, info=[]):
        if type(info) != 'list':
            raise TypeError("Info must be a list")

        if not info:
            info = [event.x, event.y, self.player]
        Application.mouseUp(self, event, info)
        msg = "mouseUp;{};{};{}".format(info[0], info[1], self.player)
        try:
            self.threadConnexion.connexion.send(msg.encode("Utf8"))
        except BrokenPipeError:
            sys.exit()


if __name__ == '__main__':
    AppClient("192.168.200.208", 40000).mainloop()
