# !/usr/bin/python3.8
# -*- coding: utf-8 -*-

class Place:
    """
    Place where pawns are put
    """

    def __init__(self, allowed_moves, col=-1, line=-1):
        self.col = col
        self.line = line
        self.empty = True
        self.pawn = None
        self.allowed_moves = allowed_moves  # (colMove, lineMove)

    def get_coords(self):
        """
        Function which return the coord of a places
        """
        return self.col, self.line

    def place_pawn(self, pawn):
        """
        Place a pawn on an empty place
        Return True if the action is possible, False if not
        """
        if self.empty:
            self.pawn = pawn
            self.empty = False
            return True
        return False

    def remove_pawn(self):
        """
        Remove pawn on the place
        Return True if the action is possible, False if not
        """
        if self.pawn is not None:
            self.pawn = None
            self.empty = True
            return True
        return False
