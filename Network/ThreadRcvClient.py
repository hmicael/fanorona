# !/usr/bin/python3.8
# -*- coding: utf-8 -*-

import socket
import sys
from threading import Thread

from AppClient import AppClient


class ThreadRcvClient(Thread):
    """Thread that manage message received from clients"""

    def __init__(self, app_client: AppClient, host, port):
        Thread.__init__(self)
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connexion.connect((host, port))
        except socket.error as message:
            print('socket.error - ' + message)
            sys.exit()
        else:
            print("Connexion established")
        self.app_client = app_client

    def run(self) -> None:
        while 1:
            try:
                msg_server = self.connexion.recv(1024).decode("Utf8")
            except socket.error:
                break
            else:
                print(msg_server)
                action = msg_server.split(';')[0]
                if action == "you":  # you;turn;color
                    msg_server = msg_server.split(";")
                    self.app_client.turn = int(msg_server[1])
                    self.app_client.player = msg_server[2]
                    self.app_client.label_info.config(text="Status: Connected")
                    self.connexion.send("client ready".encode("Utf8"))
                elif action == "end" or action == "":
                    self.app_client.end()
                    break
                elif action == "wait":
                    self.app_client.label_info.config(text="Status: Waiting for opponent")
                elif action == "new":  # action = new;(color,col,line);(color,col,line);...;(color,col,line)
                    msg_server = msg_server.split(";")
                    del msg_server[0]  # delete the string new
                    self.app_client.lock.acquire()
                    self.app_client.label_info.config(text="Status: Game start")
                    for info in msg_server:
                        self.app_client.set_pawn_by_str(info)
                    self.app_client.view.draw_pawns()
                    self.connexion.send("ok".encode("Utf8"))
                    self.app_client.lock.release()
                elif action in ["mouse_down", "mouse_move", "mouse_up"]:  # action;col;line;initiator
                    msg = msg_server.split(";")
                    self.app_client.lock.acquire()
                    if len(msg) == 4:
                        info = [int(msg[1]), int(msg[2]), ""]
                        if msg[3] in [self.app_client.player, "server"]:
                            info[2] = msg[3]
                        msg[3] = self.app_client.player  # because it's the player who initiate the action
                        # msg = ";".join(msg)
                        if action == "mouse_down":
                            self.app_client.mouse_down(info=info)
                        elif action == "mouse_move":
                            self.app_client.mouse_move(info=info)
                        elif action == "mouse_up":
                            self.app_client.mouse_up(info=info)
                            self.app_client.label_info.config(text="Status: Your turn")
                        # self.connexion.send(msg.encode("Utf8"))
                        self.app_client.lock.release()
                elif action == "finish":  # finish;redScore;yellowScore
                    info = msg_server.split(";")
                    self.app_client.lock.acquire()
                    self.app_client.scores["red"] = int(info[1])
                    self.app_client.scores["yellow"] = int(info[2])
                    self.app_client.check_finish()
                    self.app_client.label_info.config(text="Status: Game Finished")
                    self.app_client.lock.release()
