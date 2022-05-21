# !/usr/bin/python3.8
# -*- coding: utf-8 -*-

from threading import Thread

from Fanorona.Network.ThreadRcvServer import ThreadRcvServer


class ThreadConnexion(Thread):
    """
    Thread that manage new connexion
    """

    def __init__(self, appServer, connexion):
        Thread.__init__(self)
        self.appServer = appServer
        self.connexion = connexion
        self.stop = False

    def run(self) -> None:
        self.appServer.writeLog("Server waiting for new connexions")
        self.connexion.listen(2)
        while self.stop is False:  # only 2 clients can connect to server
            if self.connexion and len(self.appServer.clientConnexions) < 2:
                newConnexion, infoConnexion = self.connexion.accept()
                self.appServer.lock.acquire()
                color = ["red", "yellow"]
                self.appServer.turn += 1
                color = color[self.appServer.turn % 2]
                msgServer = "player;{};{}".format(self.appServer.turn, color)
                threadRcvServer = ThreadRcvServer(self.appServer, newConnexion, color)
                # add the new connexion to the list of connected clients
                self.appServer.clientConnexions[color] = threadRcvServer.connexion
                threadRcvServer.start()
                threadName = threadRcvServer.getName()
                self.appServer.writeLog("Client: {}, IP : {}:{} connected".format(
                    threadName,
                    infoConnexion[0],
                    infoConnexion[1])
                )
                self.appServer.writeLog(msgServer)
                newConnexion.send("you;{};{}".format(self.appServer.turn, color).encode("Utf8"))
                # Send information about the new created client to other client
                for key in self.appServer.clientConnexions:
                    if key != threadRcvServer.color:
                        self.appServer.clientConnexions[key].send(msgServer.encode("Utf8"))
                self.appServer.lock.release()
