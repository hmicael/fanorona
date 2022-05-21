# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
from Fanorona.TableView import TableView


class TableViewNetwork(TableView):
    def __init__(self, app):
        TableView.__init__(self, app)

    def mouseDown(self, info):
        if type(info) not in (tuple, list):
            raise TypeError("Info must be a list")

        self.colStart, self.lineStart = int(info[0]), int(info[1])
        self.startPlace = self.findPlaceByRealPosition((self.colStart, self.lineStart))
        # placing a pawn on an empty place
        # if self.startPlace.pawn is None:
        #     self.placePawn(self.startPlace)
        #     self.startPlace = None
        if self.find_closest(self.colStart, self.lineStart) in self.pawns and (
                info[2] == 'server' or  # selecting a pawn: only server or adequate turn/color can select a pawn
                (self.app.turn % 2 == 0 and self.startPlace.pawn == 'red' == info[2]) or (
                        self.app.turn % 2 == 1 and self.startPlace.pawn == 'yellow' == info[2])
        ):
            self.selectedItem = self.find_closest(self.colStart, self.lineStart)
            self.itemconfig(self.selectedItem, width=3)
            # <lift> move the selected item to the first plan :
            self.lift(self.selectedItem)
        else:
            self.selectedItem = None

    def mouseUp(self, info):
        if type(info) not in (tuple, list):
            raise TypeError("Info must be a list")

        if self.selectedItem in self.pawns:
            colDestination, lineDestination = int(info[0]), int(info[1])
            destinationPlace = self.findPlaceByRealPosition((colDestination, lineDestination))
            self.itemconfig(self.selectedItem, width=1)
            # if the move if accepted, the pawn will be moved,
            # and the turn incremented to allow the other player to play
            if self.selectedItem and self.app.table.move(self.startPlace, destinationPlace):
                colDestination, lineDestination = self.places[destinationPlace.getCoords()]
                if info[2] != "server":  # no need to change turn when it's the server who make the change
                    self.app.turn += 1
                self.app.hits += 1
            else:  # the pawn is replaced to its start place
                colDestination, lineDestination = self.places[self.startPlace.getCoords()]
            # drawing the pawn
            self.coords(self.selectedItem, colDestination - 15, lineDestination - 15, colDestination + 15,
                        lineDestination + 15)
            self.selectedItem = None
            self.startPlace = None
