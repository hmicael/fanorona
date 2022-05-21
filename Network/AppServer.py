# !/usr/bin/python3.8
# -*- coding: utf-8 -*-

import socket
import sys
from threading import Lock

import Application
import TableViewNetwork
import ThreadConnexion


class AppServer(Application):
    """
    Server side application
    """

    def __init__(self, host, port):
        Application.__init__(self)
        self.lock = Lock()
        self.active = 1
        self.turn = -1  # -1 because there's 0 player at first
        self.clientConnexions = {}
        self.canStart = False
        self.player = "server"
        self.threadConnexion = None
        self.host = host
        self.port = port
        self.openConnexion()

    def spec(self):
        self.view = TableViewNetwork(self)
        self.view.draw()
        self.master.title('>>>>> SERVER <<<<<')
        self.view.bind("<Button-1>", self.mouse_down)
        self.view.bind("<Button1-Motion>", self.mouse_move)
        self.view.bind("<Button1-ButtonRelease>", self.mouse_up)
        self.bind('<Destroy>', self.close)
        # self.view.pack(padx=10, pady=10)

    def openConnexion(self):
        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            connexion.bind((self.host, self.port))
        except socket.error:
            self.writeLog("Link to socket failed")
            sys.exit()
        else:
            self.threadConnexion = ThreadConnexion(self, connexion)
            self.threadConnexion.start()

    @staticmethod
    def writeLog(text):
        with open('LogFile.txt', 'a') as file:
            file.write(text + "\n")
            file.close()

    def new(self):
        Application.new(self)
        return self.getPawnsCoord()

    def check_finish(self):
        finish = Application.check_finish(self)
        if finish:
            return "finish;{};{}".format(self.scores['red'], self.scores['yellow'])
        return False

    def close(self, event=None):
        for key in self.clientConnexions:
            self.clientConnexions[key].send("end".encode("Utf8"))
            self.clientConnexions[key].close()
        if self.threadConnexion is not None:
            self.threadConnexion.connexion.close()
            self.threadConnexion.connexion = None
            self.threadConnexion.stop = True
        del self.threadConnexion
        self.writeLog("Close Server")
        self.active = 0
        sys.exit()

    def gameStart(self):
        """
        Method to check if the game can start
        """
        if len(self.clientConnexions) == 2 and self.canStart is False:
            self.canStart = True
            return self.new()
        return False

    def deletePlayer(self, colorThread):
        del self.clientConnexions[colorThread]
        self.canStart = False
        return "leave;{}".format(colorThread)

    def getPawnsCoord(self):
        """
        Return Pawn's coord in str: color;x;y
        """
        coord = ""
        for key in self.table.places.keys():
            if self.table.places[key].pawn:
                coord += ";" + self.table.places[key].pawn + "," + str(key[0]) + "," + str(key[1])
        return coord


if __name__ == '__main__':
    AppServer("192.168.200.208", 40000).mainloop()
