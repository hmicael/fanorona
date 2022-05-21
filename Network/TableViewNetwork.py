# !/usr/bin/python3.8
# -*- coding: utf-8 -*-

from TableView import TableView


class TableViewNetwork(TableView):
    def __init__(self, app):
        TableView.__init__(self, app)

    def mouse_down(self, info):
        if type(info) not in (tuple, list):
            raise TypeError("Info must be a list")
        self.col_start, self.line_start = int(info[0]), int(info[1])
        self.start_place = self.find_place_by_real_position((self.col_start, self.line_start))

        if self.find_closest(self.col_start, self.line_start) in self.pawns and (
                info[2] == 'server' or  # selecting a pawn: only server or adequate turn/color can select a pawn
                (self.app.turn % 2 == 0 and self.start_place.pawn == 'red' == info[2]) or (
                        self.app.turn % 2 == 1 and self.start_place.pawn == 'yellow' == info[2])
        ):
            self.selected_item = self.find_closest(self.col_start, self.line_start)
            self.itemconfig(self.selected_item, width=3)
            # <lift> move the selected item to the first plan :
            self.lift(self.selected_item)
        else:
            self.selected_item = None

    def mouse_up(self, info):
        if type(info) not in (tuple, list):
            raise TypeError("Info must be a list")

        if self.selected_item in self.pawns:
            col_destination, line_destination = int(info[0]), int(info[1])
            destination_place = self.find_place_by_real_position((col_destination, line_destination))
            self.itemconfig(self.selected_item, width=1)
            # if the move if accepted, the pawn will be moved,
            # and the turn incremented to allow the other player to play
            if self.selected_item and self.app.table.move(self.start_place, destination_place):
                col_destination, line_destination = self.places[destination_place.get_coords()]
                if info[2] != "server":  # no need to change turn when it's the server who make the change
                    self.app.turn += 1
                self.app.hits += 1
            else:  # the pawn is replaced to its start place
                col_destination, line_destination = self.places[self.start_place.get_coords()]
            # drawing the pawn
            self.coords(self.selected_item, col_destination - 15, line_destination - 15, col_destination + 15,
                        line_destination + 15)
            self.selected_item = None
            self.start_place = None
