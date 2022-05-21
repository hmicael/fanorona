# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
import socket
import sys
from threading import Thread

from AppServer import AppServer


class ThreadRcvServer(Thread):
    """Thread that manage message received from clients"""

    def __init__(self, app_server: AppServer, connexion, color):
        Thread.__init__(self)
        self.connexion = connexion
        self.app_server = app_server
        self.color = color

    def run(self) -> None:
        while 1:
            try:
                msg_client = self.connexion.recv(1024).decode("Utf8")
            except socket.error as message:
                print('socket.error - ' + message)
                sys.exit()
            else:
                action = msg_client.split(';')[0]
                if action == "":
                    break
                elif action == "leave":  # a player quit the game
                    self.app_server.lock.acquire()
                    msg_server = self.app_server.delete_player(self.color)
                    self.app_server.write_log(msg_server)
                    self.send_msg(msg_server)
                    self.connexion.send("end".encode("Utf8"))
                    self.app_server.lock.release()
                    break
                elif action == "client ok":
                    self.app_server.lock.acquire()
                    coord_pawn = self.app_server.game_start()
                    if coord_pawn:
                        msg = "new"
                        msg += coord_pawn
                    else:
                        msg = "wait"
                    self.app_server.lock.release()
                    for key in self.app_server.client_connexions:
                        self.app_server.client_connexions[key].send(msg.encode("Utf8"))
                elif action in ["mouse_down", "mouse_move", "mouse_up"]:  # action;col;line;initiator
                    msg = msg_client.split(";")
                    if len(msg) == 4:  # To be sure if the msg is correct
                        info = [int(msg[1]), int(msg[2]), ""]
                        if msg[3] in ["red", "yellow", "server"]:
                            info[2] = msg[3]
                        msg[3] = "server"  # because it's the server who initiate the action
                        msg = ";".join(msg)
                        self.app_server.lock.acquire()
                        if action == "mouse_down":
                            self.app_server.mouse_down(info=info)
                        elif action == "mouse_move":
                            self.app_server.mouse_move(info=info)
                        elif action == "mouse_up":
                            finish = self.app_server.mouse_up(info=info)
                            if finish is not False:
                                msg = finish
                        self.send_msg(msg)
                        self.app_server.lock.release()
                elif action == "new":
                    self.app_server.lock.acquire()
                    msg = "new"
                    msg += self.app_server.new()
                    for key in self.app_server.client_connexions:
                        self.app_server.client_connexions[key].send(msg.encode("Utf8"))
                    self.app_server.lock.release()

    def send_msg(self, msg_server):
        """
        Send message to other client except the sender
        """
        for key in self.app_server.client_connexions:
            if key != self.color:
                self.app_server.client_connexions[key].send(msg_server.encode("Utf8"))
