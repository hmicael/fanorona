# !/usr/bin/python3.8
# -*- coding: utf-8 -*-

from threading import Thread

import AppServer


class ThreadRcvServer(Thread):
    """Thread that manage message received from clients"""

    def __init__(self, appServer: AppServer, connexion, color):
        Thread.__init__(self)
        self.connexion = connexion
        self.appServer = appServer
        self.color = color

    def run(self) -> None:
        while 1:
            try:
                msgClient = self.connexion.recv(1024).decode("Utf8")
            except Exception:
                break
            else:
                action = msgClient.split(';')[0]
                if action == "":
                    break
                elif action == "leave":  # a player quit the game
                    self.appServer.lock.acquire()
                    msgServer = self.appServer.deletePlayer(self.color)
                    self.appServer.writeLog(msgServer)
                    self.sendMsg(msgServer)
                    self.connexion.send("end".encode("Utf8"))
                    self.appServer.lock.release()
                    break
                elif action == "client ok":
                    self.appServer.lock.acquire()
                    coordPawn = self.appServer.gameStart()
                    if coordPawn:
                        msg = "new"
                        msg += coordPawn
                    else:
                        msg = "wait"
                    self.appServer.lock.release()
                    for key in self.appServer.clientConnexions:
                        self.appServer.clientConnexions[key].send(msg.encode("Utf8"))
                elif action in ["mouse_down", "mouse_move", "mouse_up"]:  # action;col;line;initiator
                    msg = msgClient.split(";")
                    if len(msg) == 4:  # To be sure if the msg is correct
                        info = [int(msg[1]), int(msg[2]), ""]
                        if msg[3] in ["red", "yellow", "server"]:
                            info[2] = msg[3]
                        msg[3] = "server"  # because it's the server who initiate the action
                        msg = ";".join(msg)
                        self.appServer.lock.acquire()
                        if action == "mouse_down":
                            self.appServer.mouse_down(info=info)
                        elif action == "mouse_move":
                            self.appServer.mouse_move(info=info)
                        elif action == "mouse_up":
                            finish = self.appServer.mouse_up(info=info)
                            if finish is not False:
                                msg = finish
                        self.sendMsg(msg)
                        self.appServer.lock.release()
                elif action == "new":
                    self.appServer.lock.acquire()
                    msg = "new"
                    msg += self.appServer.new()
                    for key in self.appServer.clientConnexions:
                        self.appServer.clientConnexions[key].send(msg.encode("Utf8"))
                    self.appServer.lock.release()

    def sendMsg(self, msgServer):
        """
        Send message to other client except the sender
        """
        for key in self.appServer.clientConnexions:
            if key != self.color:
                self.appServer.clientConnexions[key].send(msgServer.encode("Utf8"))
