# !/usr/bin/python3.8
# -*- coding: utf-8 -*-

import socket
import sys
from threading import Thread

import AppClient


class ThreadRcvClient(Thread):
    """Thread that manage message received from clients"""

    def __init__(self, appClient: AppClient, host, port):
        Thread.__init__(self)
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connexion.connect((host, port))
        except socket.error:
            print("Connexion error")
            sys.exit()
        else:
            print("Connexion established")
        self.appClient = appClient

    def run(self) -> None:
        while 1:
            try:
                msgServer = self.connexion.recv(1024).decode("Utf8")
            except Exception:
                break
            else:
                action = msgServer.split(';')[0]
                print(msgServer)
                if action == "you":  # you;turn;color
                    msgServer = msgServer.split(";")
                    self.appClient.turn = msgServer[1]
                    # self.appClient.player = msgServer[2]
                    self.connexion.send("client ok".encode("Utf8"))
                elif action == "end" or action == "":
                    self.appClient.end()
                    break
                elif action == "new":  # new;(color,col,line)*
                    msgServer = msgServer.split(";")
                    del msgServer[0]  # delete the string new
                    self.appClient.lock.acquire()
                    for info in msgServer:
                        self.appClient.setPawnByStr(info)
                    self.appClient.view.draw()
                    self.connexion.send("ok".encode("Utf8"))
                    self.appClient.lock.release()
                elif action in ["mouse_down", "mouse_move", "mouse_up"]:  # action;col;line;initiator
                    msg = msgServer.split(";")
                    if len(msg) == 4:
                        info = [int(msg[1]), int(msg[2]), ""]
                        if msg[3] in [self.appClient.player, "server"]:
                            info[2] = msg[3]
                        msg[3] = self.appClient.player  # because it's the player who initiate the action
                        msg = ";".join(msg)
                        self.appClient.lock.acquire()
                        if action == "mouse_down":
                            self.appClient.mouse_down(info=info)
                        elif action == "mouse_move":
                            self.appClient.mouse_move(info=info)
                        elif action == "mouse_up":
                            self.appClient.mouse_up(info=info)
                        self.connexion.send(msg.encode("Utf8"))
                        self.appClient.lock.release()
                elif action == "finish":  # finish;redScore;yellowScore
                    info = msgServer.split(";")
                    self.appClient.lock.acquire()
                    self.appClient.scores["red"] = int(info[1])
                    self.appClient.scores["yellow"] = int(info[2])
                    self.appClient.check_finish()
                    self.appClient.lock.release()
