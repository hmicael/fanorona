# !/usr/bin/python3.8
# -*- coding: utf-8 -*-

import socket
import sys
from threading import Lock

import ThreadConnexion
from Application import Application
from TableViewNetwork import TableViewNetwork


class AppServer(Application):
    """
    Server side application
    """

    def __init__(self, host, port):
        Application.__init__(self)
        self.lock = Lock()
        self.active = 1
        self.turn = -1  # -1 because there's 0 player at first
        self.client_connexions = {}
        self.can_start = False
        self.player = "server"
        self.thread_connexion = None
        self.host = host
        self.port = port
        self.open_connexion()

    def set_view(self):
        self.view = TableViewNetwork(self)

    def bind_mouse_action(self):
        self.master.title('>>>>> SERVER <<<<<')
        self.bind('<Destroy>', self.pop_quit_choice)
        self.master.protocol("WM_DELETE_WINDOW", self.pop_quit_choice)

    def open_connexion(self):
        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            connexion.bind((self.host, self.port))
            connexion.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error:
            self.write_log("Link to socket failed")
            sys.exit()
        else:
            self.thread_connexion = ThreadConnexion.ThreadConnexion(self, connexion)
            self.thread_connexion.start()

    @staticmethod
    def write_log(text):
        with open('LogFile.txt', 'a') as file:
            file.write(text + "\n")
            file.close()

    def new(self, event=None):
        Application.new(self)
        return self.get_pawns_coord()

    def check_finish(self):
        finish = Application.check_finish(self)
        if finish:
            return "finish;{};{}".format(self.scores["red"], self.scores["yellow"])
        return False

    def close(self, event=None):
        for key in self.client_connexions:
            self.client_connexions[key].send("end".encode("Utf8"))
            self.client_connexions[key].close()
        if self.thread_connexion:
            self.thread_connexion.can_stop = True
            self.thread_connexion.socket.shutdown(socket.SHUT_RDWR)
            self.thread_connexion.socket.close()
        self.write_log("Close Server")
        self.active = 0
        sys.exit()

    def can_game_start(self):
        """
        Method to check if the game can start
        """
        if len(self.client_connexions) == 2 and self.can_start is False:
            self.can_start = True
            return self.new()
        return False

    def delete_player(self, thread_color):
        del self.client_connexions[thread_color]
        self.can_start = False
        return "leave;{}".format(thread_color)

    def get_pawns_coord(self):
        """
        Return Pawn's coord in str: color,x,y
        """
        coord = ""
        for key in self.table.places.keys():
            if self.table.places[key].pawn:
                coord += ";" + self.table.places[key].pawn + "," + str(key[0]) + "," + str(key[1])
        return coord


if __name__ == '__main__':
    AppServer("192.168.200.167", 40000).mainloop()
