# !/usr/bin/python3.8
# -*- coding: utf-8 -*-

from socket import socket
from threading import Thread

from ThreadRcvServer import ThreadRcvServer


class ThreadConnexion(Thread):
    """
    Thread that manage new connexion
    """

    def __init__(self, app_server, socket: socket):
        Thread.__init__(self)
        self.app_server = app_server
        self.socket = socket
        self.can_stop = False

    def run(self) -> None:
        self.app_server.write_log("Server waiting for new connexions")
        self.socket.listen(2)
        while not self.can_stop:
            if self.socket and len(self.app_server.client_connexions) < 2:  # only 2 clients can connect to server
                try:
                    new_connexion, info_connexion = self.socket.accept()
                except OSError:
                    print("Socket closed")
                else:
                    self.app_server.lock.acquire()
                    color = ["red", "yellow"]
                    self.app_server.turn += 1
                    color = color[self.app_server.turn % 2]
                    msg_server = "player;{};{}".format(self.app_server.turn, color)
                    thread_rcv_server = ThreadRcvServer(self.app_server, new_connexion, color)
                    # add the new connexion to the list of connected clients
                    self.app_server.client_connexions[color] = thread_rcv_server.connexion
                    thread_rcv_server.start()
                    self.app_server.write_log("Client: {}, IP : {}:{} connected".format(
                        thread_rcv_server.getName(),
                        info_connexion[0],
                        info_connexion[1])
                    )
                    self.app_server.write_log(msg_server)
                    new_connexion.send("you;{};{}".format(self.app_server.turn, color).encode("Utf8"))
                    # Send information about the new created client to other client
                    for key in self.app_server.client_connexions:
                        if key != thread_rcv_server.color:
                            self.app_server.client_connexions[key].send(msg_server.encode("Utf8"))
                    self.app_server.lock.release()
