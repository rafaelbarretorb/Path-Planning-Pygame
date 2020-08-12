
import pygame 
from pygame.locals import * 

class Game:

    def __init__(self, screen_size, screen_offset, screen_side, ext_grid,
                 grid_thick, square_side, rows_size, columns_size):
        self.screen = pygame.display.set_mode(screen_size)
        self.screen_offset = screen_offset
        self.screen_side = screen_side
        self.ext_grid = ext_grid
        self.grid_thick = grid_thick
        self.square_side = square_side
        self.rows_size = rows_size
        self.columns_size = columns_size
    
    def initialize_grid(self):
        #       1
        #     ______
        #    |      |
        # 4  |      |  2
        #    |______|
        #
        #       3

        # External Lines 1234
        # 1
        pygame.draw.line(self.screen, (0, 200, 200), (self.screen_offset , self.screen_offset),
                         (self.screen_offset + self.ext_grid, self.screen_offset ), (self.grid_thick )) # 1
        
        # 2
        pygame.draw.line(self.screen, (0, 200, 200), (self.screen_offset , self.ext_grid + self.screen_offset),
                         (self.screen_offset + self.ext_grid, self.screen_offset + self.ext_grid), (self.grid_thick))

        # 3
        pygame.draw.line(self.screen, (0, 200, 200), (self.screen_offset + self.ext_grid, self.screen_offset),
                         (self.screen_offset + self.ext_grid, self.screen_offset + self.ext_grid), (self.grid_thick)) # 3

        # 4
        pygame.draw.line(self.screen, (0, 200, 200), (self.screen_offset , self.screen_offset ),
                         (self.screen_offset , self.ext_grid + self.screen_offset), (self.grid_thick)) # 4       

        # Internal Lines of the grid
        x = 1
        y = 1
        for i in range(self.rows_size):
            x += self.square_side
            y += self.square_side
            pygame.draw.line(self.screen, (0, 200, 200), (self.screen_offset, y + self.screen_offset),
                             (self.screen_side + self.screen_offset, y + self.screen_offset), (1))

            pygame.draw.line(self.screen, (0, 200, 200), (x + self.screen_offset, self.screen_offset),
                             (x + self.screen_offset, self.screen_offset + self.screen_side), (1))

    
    def draw_cell(self, color, row, column):
        pygame.draw.circle(self.screen, color, ((2*column + 1)*self.square_side/2 + self.screen_offset,
                           (2*row + 1)*self.square_side/2 + self.screen_offset), 10)

        pygame.display.update()
        pygame.time.wait(10)

