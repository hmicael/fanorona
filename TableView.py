# !/usr/bin/python3.8
# -*- coding: utf-8 -*-

from math import sqrt
from tkinter import *
from Place import *


class TableView(Canvas):
    """
    Class which represent the graphical Table game
    """

    def __init__(self, app, width=960, height=600):
        Canvas.__init__(self, bg='dark grey', bd=3, relief=SUNKEN)
        self.app = app
        self.configure(width=width, height=height)
        # Real width and height without margin
        self.realWidth = width
        self.realHeight = height
        self.margin = 25
        # Rest of width and height after removing margin
        self.width = self.realWidth - self.margin
        self.height = self.realHeight - self.margin
        # Width and height of a division of the Table according to the tableSize
        self.wSub = (self.width - self.margin) / (self.app.table.tableSize - 1)
        self.hSub = (self.height - self.margin) / (self.app.table.tableSize - 1)
        self.places = {}
        for line in range(0, self.app.table.tableSize):
            for col in range(0, self.app.table.tableSize):
                # Setting the real position of a place in the GUI
                self.places[col, line] = ((self.margin + self.wSub * col), (self.margin + self.hSub * line))
        self.pawns = []  # List of pawns
        self.selectedItem = None  # Selected pawn
        # The starting position of a pawn when it's being moved
        self.colStart, self.lineStart = 0, 0
        # The place where the pawn start to be moved to
        self.startPlace = None
        self.drawLinesAndPlaceOfPawn()

    def drawLinesAndPlaceOfPawn(self):
        """
        Drawing different lines and the place of pawn and pawn
        """
        self.create_rectangle(self.margin, self.margin, self.width, self.height, width=7)
        k = 0
        indexLimit = self.app.table.tableSize - 1
        for i in range(0, self.app.table.tableSize):
            # Begin : oblique line
            # If k < indexLimit * 2 because only one half of table is required to draw oblique lines
            if k < indexLimit * 2:
                # At first, we start the iteration on (0,0), (k,0), ..., (k?,0) where k? is the valid value < indexLimit
                # In order to avoid getting out of range. When k? > indexLimit we apply % indexLimit on k, then
                # Starting a new iteration on (indexLimit, k % indexLimit) cd (else part)
                # From left to right
                if k < self.app.table.tableSize:
                    # Oblique from down left to up right
                    if (0, k) != (k, 0):
                        self.create_line(self.places[0, k], self.places[k, 0])
                    # Oblique from up left to down right
                    if (k, 0) != (indexLimit, indexLimit - k):
                        self.create_line(self.places[k, 0], self.places[indexLimit, indexLimit - k])
                # Right to left
                else:
                    #  Oblique from up right to down left
                    if (indexLimit, k % indexLimit) != (k % indexLimit, indexLimit):
                        self.create_line(self.places[indexLimit, k % indexLimit],
                                         self.places[k % indexLimit, indexLimit])
                    # When indexLimit % 2 == 1, the tracing is incoherent, so I add 1 to k, idk why but it works :)
                    kk = k
                    if indexLimit % 2 == 1:
                        kk = k + 1
                    #  Oblique from down right to up left
                    if (indexLimit - (kk % indexLimit), indexLimit) != (0, kk % indexLimit):
                        self.create_line(self.places[indexLimit - (kk % indexLimit), indexLimit],
                                         self.places[0, kk % indexLimit])
                k = k + 2
            # End : oblique line
            # Horizontal and vertical lines
            self.create_line(self.places[i, 0], self.places[i, self.app.table.tableSize - 1], width=3)
            self.create_line(self.places[0, i], self.places[self.app.table.tableSize - 1, i], width=3)
        # Drawing places or pawns
        for coord in self.app.table.places.keys():
            x, y = self.places[coord]
            self.create_oval(x - 15, y - 15, x + 15, y + 15, fill='black')
            if self.app.table.places[coord].pawn is not None:
                self.pawns.append(
                    (self.create_oval(x - 15, y - 15, x + 15, y + 15, fill=self.app.table.places[coord].pawn),))

    def mouseDown(self, position):
        if type(position) not in (tuple, list):
            raise TypeError("Position must be a list")
        self.colStart, self.lineStart = int(position[0]), int(position[1])
        self.startPlace = self.findPlaceByRealPosition((self.colStart, self.lineStart))
        # Placing a pawn on an empty place
        # if self.startPlace.pawn is None:
        #     self.placePawn(self.startPlace)
        #     self.startPlace = None

        # Selecting a pawn
        # Canvas.find_closest is a function which return the closest element of the canvas
        # Here if the closest item is an pawn and if the turn match the correct color
        # then the pawn can be selected for any move
        if self.find_closest(self.colStart, self.lineStart) in self.pawns and \
                ((self.app.turn % 2 == 0 and self.startPlace.pawn == 'red') or (
                        self.app.turn % 2 == 1 and self.startPlace.pawn == 'yellow')):
            self.selectedItem = self.find_closest(self.colStart, self.lineStart)
            self.itemconfig(self.selectedItem, width=3)
            # <lift> move the selected item to the first plan :
            self.lift(self.selectedItem)
        else:
            self.selectedItem = None

    def mouseMove(self, position):
        if type(position) not in (tuple, list):
            raise TypeError("Position must be a list")

        colDestination, lineDestination = int(position[0]), int(position[1])
        xMove, yMove = colDestination - self.colStart, lineDestination - self.lineStart
        if self.selectedItem and self.selectedItem in self.pawns:
            self.move(self.selectedItem, xMove, yMove)
            self.colStart, self.lineStart = colDestination, lineDestination
            return xMove, yMove

    def mouseUp(self, position):
        if type(position) not in (tuple, list):
            raise TypeError("Position must be a list")

        if self.selectedItem in self.pawns:  # Only pawn can be moved
            colDestination, lineDestination = int(position[0]), int(position[1])
            destinationPlace = self.findPlaceByRealPosition((colDestination, lineDestination))
            self.itemconfig(self.selectedItem, width=1)
            # If the move if accepted, the pawn will be moved,
            # and the turn is incremented to allow the other player to play
            if self.selectedItem and self.app.table.move(self.startPlace, destinationPlace):
                colDestination, lineDestination = self.places[destinationPlace.getCoords()]
                self.app.turn += 1
                self.app.hits += 1
            else:  # the pawn is replaced to its start place
                colDestination, lineDestination = self.places[self.startPlace.getCoords()]
            # Drawing the pawn
            self.coords(self.selectedItem, colDestination - 15, lineDestination - 15, colDestination + 15,
                        lineDestination + 15)
            self.selectedItem = None
            self.startPlace = None
            return colDestination, lineDestination

    def findPlaceByRealPosition(self, position):
        """
        Return the <Place> according to the real position
        """
        if type(position) != tuple:
            raise TypeError("Position must be a list")

        distance = 1000  # 1000 just to get high distance
        coord = (-1, -1)
        for key in self.places:
            # Calculate the distance between the given position and each place
            distance1 = sqrt((self.places[key][0] - position[0]) ** 2 + (self.places[key][1] - position[1]) ** 2)
            # The smallest distance means, the most probable corresponding place
            if distance > int(distance1):
                distance = distance1
                coord = key
        return self.app.table.places[coord]

    def placePawn(self, place: Place):
        """
        Place a pawn on the pressed place
        """
        if self.app.turn % 2 == 0:
            color = 'red'
        else:
            color = 'yellow'
        place.placePawn(color)
        x, y = self.places[place.getCoords()]
        self.app.turn += 1
        self.pawns.append(
            (self.create_oval(x - 15, y - 15, x + 15, y + 15, fill=place.pawn),))
