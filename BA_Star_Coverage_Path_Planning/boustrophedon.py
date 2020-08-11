#!/usr/bin/env python

import math
import numpy as np
from cell import Cell

# Constants
from constants import NORTH, SOUTH, EAST, WEST
from constants import NOT_VISITED, FREE_AND_VISITED, OCCUPIED


class Boustrophedon:
    """
    Class Boustrophedon for the Coverage Path Planning.

    """
    def __init__(self, start_cell, coverage_grid):

        self.curr_cell = Cell(start_cell[0], start_cell[1])

        self.cov_grid = coverage_grid

        self.path = list()

    def collision(self, direction):
        """
        For the given direction, return true if there is a collision. Return
        false otherwise.

        Parameters
        ----------

        direction : string
            One of the 4 directions: { "north", "south", "east", "west"}.

        Returns
        -------

        bool
            True if there is a collision, False otherwise.

        """
        if direction == "north":
            # valide north cell
            if self.check_coverage_collision(self.curr_cell.row - 1,
                                             self.curr_cell.col):
                return True

        elif direction == "south":
            # valide north cell
            if self.check_coverage_collision(self.curr_cell.row + 1,
                                             self.curr_cell.col):
                return True

        elif direction == "east":
            # valide north cell
            if self.check_coverage_collision(self.curr_cell.row,
                                             self.curr_cell.col + 1):
                return True

        elif direction == "west":
            # valide north cell
            if self.check_coverage_collision(self.curr_cell.row,
                                             self.curr_cell.col - 1):
                return True

        return False

    def motion(self):
        """
        Performs the boustrophedon motion.

        Returns
        -------
        Cell
            Last cell position of the boustrophedon path.


        """
        priority = {"north": [-1, 0], "south": [1, 0],
                    "east": [0, 1], "west": [0, -1]}

        priority_list = ["north", "south", "east", "west"]

        critical_point = False
        while critical_point is False:
            row = self.curr_cell.row
            column = self.curr_cell.col

            if self.allow_to_move(priority_list[0],
                                  row + priority[priority_list[0]][0],
                                  column + priority[priority_list[0]][1]):

                self.move(priority_list[0])

            elif self.allow_to_move(priority_list[1],
                                    row + priority[priority_list[1]][0],
                                    column + priority[priority_list[1]][1]):

                self.move(priority_list[1])

            elif self.allow_to_move(priority_list[2],
                                    row + priority[priority_list[2]][0],
                                    column + priority[priority_list[2]][1]):

                self.move(priority_list[2])

            elif self.allow_to_move(priority_list[3],
                                    row + priority[priority_list[3]][0],
                                    column + priority[priority_list[3]][1]):

                self.move(priority_list[3])

            else:
                # Robot isolated
                critical_point = True

        return self.curr_cell, self.path

    def allow_to_move(self, direction, row, column):
        """
        Return True if a valid cell is no occupied AND is not visited yet.

        Parameters
        ----------
        direction : string
            One of the 4 directions: { "north", "south", "east", "west"}.

        row : int
            Row of the cell.

        column : int
            Column of the cell.

        Returns
        -------

        bool
            True if there is no collision in the direction chosen and the cell
            was not visited before.

        """
        if self.valid_coverage_cell(row, column):
            if self.collision(direction) is False and \
               self.cov_grid[row][column] == NOT_VISITED:
                return True
        else:
            return False

    def go_and_update(self, row_add, column_add):
        """ ."""
        # Update current cell
        self.curr_cell.row = self.curr_cell.row + row_add
        self.curr_cell.col = self.curr_cell.col + column_add

        self.path.append((self.curr_cell.row, self.curr_cell.col))

        # Set the current cell as ALREADY VISITED
        self.cov_grid[self.curr_cell.row,
                      self.curr_cell.col] = FREE_AND_VISITED

    def valid_coverage_cell(self, row, column):
        """ Verify if the cell is valid."""

        if (row < self.cov_grid.shape[0] and
           row >= 0) and \
           (column < self.cov_grid.shape[1] and
           column >= 0):
            return True
        else:
            return False

    def check_coverage_collision(self, row, column):
        """ Verify if the coverage cell is occupied. """

        if self.cov_grid[row][column] == OCCUPIED:
            return True
        else:
            return False

    def move(self, direction):
        """ Move to the given direction. """

        if direction == "north":
            self.go_and_update(-1, 0)

        elif direction == "south":
            self.go_and_update(1, 0)

        elif direction == "east":
            self.go_and_update(0, 1)

        elif direction == "west":
            self.go_and_update(0, -1)
