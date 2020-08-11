#!/usr/bin/env python

# Constants
from constants import OCCUPIED

class Cell:
    def __init__(self, row=0, column=0):
        self.row = row
        self.col = column

    def verify_cell(self, cell, grid):
        """
        Verify if the cell is valid.

        Parameters
        ----------
        cell : Cell
            The Cell object to be tested.

        Returns
        -------
        bool
            True if the cell is valid, False otherwise.

        """
        if cell.row < 0:
            return False
        elif cell.col < 0:
            return False
        elif cell.row >= grid.shape[0]:
            return False
        elif cell.col >= grid.shape[1]:
            return False
        elif grid[cell.row][cell.col] == OCCUPIED:
            return False

        return True