#!/usr/bin/python

import numpy as np

from ba_star import BAStar
from cell import Cell
from game import Game
import sys, pygame 
from pygame.locals import *

from constants import GREEN

def main():
    
    # GRID SPECS
    rows_size = 20
    columns_size = 20

    # Make Path
    grid = np.zeros([rows_size, columns_size])
    start_cell = Cell(rows_size, 0) # bottom left
    planner = BAStar(start_cell=start_cell, coverage_grid=grid)
    path = planner.planning()

    # game = Game(SCREEN_SIDE)


    ROWS = 20
    COLUMNS = 20
    SQUARE_SIDE = 30
    EXT_GRID = SQUARE_SIDE*ROWS
    GRID_THICK = 1
    SCREEN_SIDE = SQUARE_SIDE*ROWS

    SCREEN_OFFSET = 20
    SCREEN_SIZE = (ROWS*(SQUARE_SIDE)+2*SCREEN_OFFSET, COLUMNS*(SQUARE_SIDE)+2*SCREEN_OFFSET)

    # Draw Path
    game = Game(SCREEN_SIZE, SCREEN_OFFSET, SCREEN_SIDE, EXT_GRID, GRID_THICK, SQUARE_SIDE, ROWS, COLUMNS)
    game.initialize_grid()
    clock = pygame.time.Clock()

    i = 0
    while True:
        clock.tick(60)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()

        if i < len(path):
            game.draw_cell(GREEN, path[i][0], path[i][1])
            i = i + 1


if __name__ == '__main__':
	main()