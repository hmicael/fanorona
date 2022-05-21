# !/usr/bin/python3.8
# -*- coding: utf-8 -*-

from random import choice

from Place import *


class Table:
    def __init__(self, table_size=3, nb_pawn=3):
        self.places = {}
        self.table_size = table_size
        self.nb_pawn = nb_pawn
        self.winner = ""
        for line in range(0, self.table_size):
            for col in range(0, self.table_size):
                allowed_moves = []  # List where is listed allowed moves for a given place
                # List of all possible moves up, down, left, right
                list_allowed_moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
                # Setting list of all possible moves up, down, left, right, oblique
                if line % 2 == col % 2:  # oblique
                    list_allowed_moves = [(0, -1), (1, 0), (0, 1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
                for colMove, lineMove in list_allowed_moves:
                    col1, line1 = col + colMove, line + lineMove
                    # If col1, line1, the next position is not out of range
                    # Then (colMove, lineMove) is added to the list of allowed moves for this place
                    if col1 in range(0, self.table_size) and line1 in range(0, self.table_size):
                        allowed_moves.append((colMove, lineMove))
                # Set the Place inside the Table
                self.places[col, line] = Place(allowed_moves, col, line)

    def random_placing(self):
        """
        Function which place randomly the pawn on the Table
        """
        for pawn in ["red", "yellow"]:
            left_pawns = self.nb_pawn
            while left_pawns > 0:
                col, line = choice(range(0, self.table_size)), choice(range(0, self.table_size))
                if self.places[col, line].place_pawn(pawn):
                    left_pawns -= 1

    def print(self):
        """
        Print the table on standard output
        """
        for col in range(0, self.table_size):
            for line in range(0, self.table_size):
                if self.places[col, line].pawn is None:
                    print('O', end=" ")
                elif self.places[col, line].pawn == 'yellow':
                    print('Y', end=" ")
                elif self.places[col, line].pawn == 'red':
                    print("R", end=" ")
            print("")
        print("")

    def neighbors(self, place: Place, free=False):
        """
        Return List of the free or not neighbors of a place, according to the value of the arg free
        """
        neighbors = []
        for colMove, lineMove in place.allowed_moves:
            col, line = place.get_coords()[0] + colMove, place.get_coords()[1] + lineMove
            if self.places[col, line].empty == free:
                neighbors.append(self.places[col, line])
        return neighbors

    def move(self, start_place, destination_place):
        """
        Move the pawn in the start place to destination place, return True if the move
        is possible, False if not
        """
        if type(start_place) != Place and type(destination_place) != Place:
            raise TypeError("startPlace and destinationPlace must be a Place object")

        # If the destination place is among the list of empty neighbors
        if destination_place in self.neighbors(start_place, True):
            # The pawn is placed on the destination place and remove from the old one
            destination_place.place_pawn(start_place.pawn)
            start_place.remove_pawn()
            # Check if the game is finished to find out the winner
            if self.finish(destination_place):
                self.winner = destination_place.pawn
            return True
        return False

    def finish(self, place):
        """
        Check if the game is finished
        """
        if type(place) != Place:
            raise TypeError("place must be a Place object")

        col_place, line_place = place.get_coords()
        # #################### HORIZONTAL ####################
        count = self.nb_pawn - 1  # -1 because the current place
        col1, col2 = col_place - 1, col_place + 1
        # move to left
        while col1 >= 0:
            if self.places[col1, line_place].pawn == place.pawn:
                count -= 1
            else:
                break
            # If count == O, then the is enough of aligned pawn to win the game
            if count == 0:
                return True
            col1 -= 1
        # move to right
        while col2 < self.table_size:
            if self.places[col2, line_place].pawn == place.pawn:
                count -= 1
            else:
                break
            if count == 0:
                return True
            col2 += 1
        # ##################### VERTICAL #####################
        count = self.nb_pawn - 1  # -1 because the current place
        line1, line2 = line_place - 1, line_place + 1
        # move to up
        while line1 >= 0:
            if self.places[col_place, line1].pawn == place.pawn:
                count -= 1
            else:
                break
            if count == 0:
                return True
            line1 -= 1
        # move to down
        while line2 < self.table_size:
            if self.places[col_place, line2].pawn == place.pawn:
                count -= 1
            else:
                break
            if count == 0:
                return True
            line2 += 1
        # #################### OBLIQUE ####################
        if line_place % 2 == col_place % 2:  # oblique
            # oblique up left to down right
            count = self.nb_pawn - 1  # -1 because the current place
            # move to up left
            col1, line1 = col_place - 1, line_place - 1
            while (col1, line1) in self.places.keys():
                if self.places[col1, line1].pawn == place.pawn:
                    count -= 1
                else:
                    break
                if count == 0:
                    return True
                col1 -= 1
                line1 -= 1
            # move to down right
            col1, line1 = col_place + 1, line_place + 1
            while (col1, line1) in self.places.keys():
                if self.places[col1, line1].pawn == place.pawn:
                    count -= 1
                else:
                    break
                if count == 0:
                    return True
                col1 += 1
                line1 += 1

            # oblique up right to down left
            count = self.nb_pawn - 1  # -1 because the current place
            # move to up right
            col1, line1 = col_place + 1, line_place - 1
            while (col1, line1) in self.places.keys():
                if self.places[col1, line1].pawn == place.pawn:
                    count -= 1
                else:
                    break
                if count == 0:
                    return True
                col1 += 1
                line1 -= 1
            # move to down left
            col1, line1 = col_place - 1, line_place + 1
            while (col1, line1) in self.places.keys():
                if self.places[col1, line1].pawn == place.pawn:
                    count -= 1
                else:
                    break
                if count == 0:
                    return True
                col1 -= 1
                line1 += 1
        return False
