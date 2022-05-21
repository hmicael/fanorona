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
        self.draw_lines_and_places()

    def draw_lines_and_places(self):
        """
        Draw different line of the Table
        :return:
        """
        self.create_rectangle(self.margin, self.margin, self.width, self.height, width=7)
        k = 0
        index_limit = self.app.table.tableSize - 1
        for i in range(0, self.app.table.tableSize):
            # Begin : oblique line
            # If k < index_limit * 2 because only one half of table is required to draw oblique lines
            if k < index_limit * 2:
                # At first, we start the iteration on (0,0), (k,0), ..., (k?,0) where k? is the valid value <
                # index_limit In order to avoid getting out of range. When k? > index_limit we apply % index_limit on
                # k, then Starting a new iteration on (index_limit, k % index_limit) cd (else part) From left to right
                if k < self.app.table.tableSize:
                    # Oblique from down left to up right
                    if (0, k) != (k, 0):
                        self.create_line(self.places[0, k], self.places[k, 0])
                    # Oblique from up left to down right
                    if (k, 0) != (index_limit, index_limit - k):
                        self.create_line(self.places[k, 0], self.places[index_limit, index_limit - k])
                # Right to left
                else:
                    #  Oblique from up right to down left
                    if (index_limit, k % index_limit) != (k % index_limit, index_limit):
                        self.create_line(self.places[index_limit, k % index_limit],
                                         self.places[k % index_limit, index_limit])
                    # When index_limit % 2 == 1, the tracing is incoherent, so I add 1 to k, idk why but it works :)
                    kk = k
                    if index_limit % 2 == 1:
                        kk = k + 1
                    #  Oblique from down right to up left
                    if (index_limit - (kk % index_limit), index_limit) != (0, kk % index_limit):
                        self.create_line(self.places[index_limit - (kk % index_limit), index_limit],
                                         self.places[0, kk % index_limit])
                k = k + 2
            # End : oblique line
            # Horizontal and vertical lines
            self.create_line(self.places[i, 0], self.places[i, self.app.table.tableSize - 1], width=3)
            self.create_line(self.places[0, i], self.places[self.app.table.tableSize - 1, i], width=3)
            # Drawing places
            for coord in self.app.table.places.keys():
                x, y = self.places[coord]
                self.create_oval(x - 15, y - 15, x + 15, y + 15, fill='black')

    def draw_pawns(self):
        """
        Drawing pawns on the Table
        """
        self.pawns = []  # Reset of pawns
        for coord in self.app.table.places.keys():
            x, y = self.places[coord]
            if self.app.table.places[coord].pawn is not None:
                self.pawns.append(
                    (self.create_oval(x - 15, y - 15, x + 15, y + 15, fill=self.app.table.places[coord].pawn),))

    def mouse_down(self, position):
        if type(position) not in (tuple, list):
            raise TypeError("Position must be a list")
        self.colStart, self.lineStart = int(position[0]), int(position[1])
        self.startPlace = self.find_place_by_real_position((self.colStart, self.lineStart))

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

    def mouse_move(self, position):
        if type(position) not in (tuple, list):
            raise TypeError("Position must be a list")

        col_destination, line_destination = int(position[0]), int(position[1])
        x_move, y_move = col_destination - self.colStart, line_destination - self.lineStart
        if self.selectedItem and self.selectedItem in self.pawns:
            self.move(self.selectedItem, x_move, y_move)
            self.colStart, self.lineStart = col_destination, line_destination
            return x_move, y_move

    def mouse_up(self, position):
        if type(position) not in (tuple, list):
            raise TypeError("Position must be a list")

        if self.selectedItem in self.pawns:  # Only pawn can be moved
            col_destination, line_destination = int(position[0]), int(position[1])
            destination_place = self.find_place_by_real_position((col_destination, line_destination))
            self.itemconfig(self.selectedItem, width=1)
            # If the move if accepted, the pawn will be moved,
            # and the turn is incremented to allow the other player to play
            if self.selectedItem and self.app.table.move(self.startPlace, destination_place):
                col_destination, line_destination = self.places[destination_place.get_coords()]
                self.app.turn += 1
                self.app.hits += 1
            else:  # the pawn is replaced to its start place
                col_destination, line_destination = self.places[self.startPlace.get_coords()]
            # Drawing the pawn
            self.coords(self.selectedItem, col_destination - 15, line_destination - 15, col_destination + 15,
                        line_destination + 15)
            self.selectedItem = None
            self.startPlace = None
            return col_destination, line_destination

    def find_place_by_real_position(self, position):
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

    def place_pawn(self, place: Place):
        """
        Place a pawn on the pressed place
        """
        if self.app.turn % 2 == 0:
            color = 'red'
        else:
            color = 'yellow'
        place.place_pawn(color)
        x, y = self.places[place.get_coords()]
        self.app.turn += 1
        self.pawns.append(
            (self.create_oval(x - 15, y - 15, x + 15, y + 15, fill=place.pawn),))
