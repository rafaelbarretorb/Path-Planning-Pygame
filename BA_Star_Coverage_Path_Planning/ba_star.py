#!/usr/bin/env python

from boustrophedon import Boustrophedon
from cell import Cell


class BAStar:
    """
    Class for the Coverage Path Planning BA*.

    """
    def __init__(self, start_cell, coverage_grid):
        self.start_cell = start_cell
        self.cov_grid = coverage_grid

    def planning(self):
        """."""
        self.bous = Boustrophedon([self.start_cell.row, self.start_cell.col], self.cov_grid)

        curr_cell, path = self.bous.motion()

        return path
