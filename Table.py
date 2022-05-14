#!/usr/bin/python3.6
from random import choice

from Fanorona.Place import Place


class Table:
    def __init__(self, tableSize=3, nbPawn=3):
        self.places = {}
        self.tableSize = tableSize
        self.nbPawn = nbPawn
        self.winner = ""
        for line in range(0, self.tableSize):
            for col in range(0, self.tableSize):
                allowedMoves = []  # List where is listed allowed moves for a given place
                # List of all possible moves up, down, left, right
                listAllowedMoves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
                # Setting list of all possible moves up, down, left, right, oblique
                if line % 2 == col % 2:  # oblique
                    listAllowedMoves = [(0, -1), (1, 0), (0, 1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
                for colMove, lineMove in listAllowedMoves:
                    col1, line1 = col + colMove, line + lineMove
                    # If col1, line1, the next position is not out of range
                    # Then (colMove, lineMove) is added to the liste of allowed moves for this place
                    if col1 in range(0, self.tableSize) and line1 in range(0, self.tableSize):
                        allowedMoves.append((colMove, lineMove))
                # Set the Place inside the Table
                self.places[col, line] = Place(allowedMoves, col, line)
        # self.randomPlacing()

    def randomPlacing(self):
        """
        Function which place randomly the pawn on the Table
        """
        for pawn in ["red", "yellow"]:
            left_pawns = self.nbPawn
            while left_pawns > 0:
                col, line = choice(range(0, self.tableSize)), choice(range(0, self.tableSize))
                if self.places[col, line].placePawn(pawn):
                    left_pawns -= 1

    def print(self):
        """
        Print the table on standard output
        """
        for col in range(0, self.tableSize):
            for line in range(0, self.tableSize):
                if self.places[col, line].pawn is None:
                    print('O', end=" ")
                elif self.places[col, line].pawn == 'yellow':
                    print('Y', end=" ")
                elif self.places[col, line].pawn == 'red':
                    print("R", end=" ")
            print("")
        print("")

    def neighbors(self, place, free=False):
        """
        Return List of the free or not neighbors of a place, according to the value of the arg free
        """
        if type(place) != 'Place':
            raise TypeError("place must be a Place object")

        neighbors = []
        for colMove, lineMove in place.allowedMoves:
            col, line = place.getCoords()[0] + colMove, place.getCoords()[1] + lineMove
            if self.places[col, line].empty == free:
                neighbors.append(self.places[col, line])
        return neighbors

    def move(self, startPlace, destinationPlace):
        """
        Move the pawn in the start place to destination place, return True if the move
        is possible, False if not
        """
        if type(startPlace) != 'Place' and type(destinationPlace) != 'Place':
            raise TypeError("startPlace and destinationPlace must be a Place object")

        # If the destination place is among the list of empty neighbors
        if destinationPlace in self.neighbors(startPlace, True):
            # The pawn is placed on the destination place and remove from the old one
            destinationPlace.placePawn(startPlace.pawn)
            startPlace.removePawn()
            # Check if the game is finished to find out the winner
            if self.finish(destinationPlace):
                self.winner = destinationPlace.pawn
            return True
        return False

    def finish(self, place):
        """
        Check if the game is finished
        """
        if type(place) != 'Place':
            raise TypeError("place must be a Place object")

        colPlace, linePlace = place.getCoords()
        # #################### HORIZONTAL ####################
        count = self.nbPawn - 1  # -1 because the current place
        col1, col2 = colPlace - 1, colPlace + 1
        # move to left
        while col1 >= 0:
            if self.places[col1, linePlace].pawn == place.pawn:
                count -= 1
            else:
                break
            # If count == O, then the is enough of aligned pawn to win the game
            if count == 0:
                return True
            col1 -= 1
        # move to right
        while col2 < self.tableSize:
            if self.places[col2, linePlace].pawn == place.pawn:
                count -= 1
            else:
                break
            if count == 0:
                return True
            col2 += 1
        # ##################### VERTICAL #####################
        count = self.nbPawn - 1  # -1 because the current place
        line1, line2 = linePlace - 1, linePlace + 1
        # move to up
        while line1 >= 0:
            if self.places[colPlace, line1].pawn == place.pawn:
                count -= 1
            else:
                break
            if count == 0:
                return True
            line1 -= 1
        # move to down
        while line2 < self.tableSize:
            if self.places[colPlace, line2].pawn == place.pawn:
                count -= 1
            else:
                break
            if count == 0:
                return True
            line2 += 1
        # #################### OBLIQUE ####################
        if linePlace % 2 == colPlace % 2:  # oblique
            # oblique up left to down right
            count = self.nbPawn - 1  # -1 because the current place
            # move to up left
            col1, line1 = colPlace - 1, linePlace - 1
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
            col1, line1 = colPlace + 1, linePlace + 1
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
            count = self.nbPawn - 1  # -1 because the current place
            # move to up right
            col1, line1 = colPlace + 1, linePlace - 1
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
            col1, line1 = colPlace - 1, linePlace + 1
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
