#!/usr/bin/python3.6
class Place:
    """
    Place where pawns are put
    """

    def __init__(self, allowedMoves, col=-1, line=-1):
        self.col = col
        self.line = line
        self.empty = True
        self.pawn = None
        self.allowedMoves = allowedMoves  # (colMove, lineMove)

    def getCoords(self):
        """
        Function which return the coord of a places
        """
        return self.col, self.line

    def placePawn(self, pawn):
        """
        Place a pawn on an empty place
        Return True if the action is possible, False if not
        """
        if self.empty:
            self.pawn = pawn
            self.empty = False
            return True
        return False

    def removePawn(self):
        """
        Remove pawn on the place
        Return True if the action is possible, False if not
        """
        if self.pawn is not None:
            self.pawn = None
            self.empty = True
            return True
        return False
