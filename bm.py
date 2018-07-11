#!/usr/bin/python
# -----------
#


# ----------


import numpy as np
import math
import matplotlib.pyplot as plt

import sys, pygame 
from pygame.locals import * 

rows = 10
columns = 10

rows_space = 40
columns_space  = 40

# Grid specs
WIDTH = 5
ROWS = 20
COLUMNS = 20
SQUARE_SIDE = 30
EXT_GRID = SQUARE_SIDE*ROWS
GRID_THICK = 1

SCREEN_SIDE = SQUARE_SIDE*ROWS

SCREEN_OFFSET = 20
SCREEN_SIZE = (ROWS*(SQUARE_SIDE)+2*SCREEN_OFFSET, COLUMNS*(SQUARE_SIDE)+2*SCREEN_OFFSET)

# COLORS
green = 0, 255, 0
red = 255, 0, 0
blue = 0, 0, 255
white = 255,255,255

# 2 obstacles
# 0 free
# 1 free cleaned
grid =  np.zeros([ROWS, COLUMNS])

# OBSTACLES

# Fig. 5

grid[4][5] = 2
grid[4][6] = 2
grid[4][7] = 2
grid[4][8] = 2
grid[4][9] = 2
grid[4][10] = 2
grid[4][11] = 2
grid[4][12] = 2
grid[4][13] = 2
grid[4][14] = 2
grid[4][15] = 2
grid[4][16] = 2
grid[4][17] = 2
grid[4][18] = 2
grid[4][19] = 2



grid_shape = grid.shape 

print " grid shape " + str(grid.shape)

#print len(grid) # n = 5
#print len(grid[0]) # m = 6
#print grid[1][0]

# TODO: initial point, heading 
# 

initial = [0,0]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

backtracking_list = []

class Node:

	def __init__(self, column, row, cost, pind):
		self.column =column 
		self.row = row
		self.cost = cost
		self.pind = pind #  parent indice

	def __str__(self):
		return str(self.x) + "," + str(self.y) + "," + str(self.cost) + "," + str(self.pind)

#def path(grid, initial_point):

def verify(direction, row, column):

    if direction == 'north':
    	if row <= 0:
    		return False
    	elif grid[row-1][column] == 1 or grid[row-1][column] == 2:
    		return False
    	else:
    		return True

    elif direction == 'south':
    	
    	if row >= (grid.shape[0] - 1):
    		return False
    	elif grid[row+1][column] == 1 or grid[row+1][column] == 2:
    		return False
    	else:
    		return True

    elif direction == 'west':
    	
    	if column <= 0:
    		return False
    	elif grid[row][column-1] == 1 or grid[row][column-1] == 2:
    		return False
    	else:
    		return True

    elif direction == 'east':
    	
    	if column >= (grid.shape[1] - 1):
    		return False
    	elif grid[row][column+1] == 1 or grid[row][column+1] == 2:
    		return False
    	else:
    		return True

def valid_cell(grid, row, column):
	""" Verify is the cell is valid. """
	if (row < grid.shape[0] and row >= 0) and (column < grid.shape[1] and column >= 0):
		return True
	else:
		return False

def backtracking_points(grid, row, column):
	""" Fig. 4"""
	# fist: verify if is valid cell

	# (a) and (b)
	if valid_cell(grid,row,(column+1)):
		if grid[row][column+1] == 0:
			if valid_cell(grid,(row-1),(column+1)) or row == 0:
				if grid[(row-1)][(column+1)] == 2:
					backtracking_list.append((row,column))
			elif valid_cell(grid,(row+1),(column+1)) or row == (grid.shape[0] - 1):
				if grid[(row+1)][(column+1)] == 2:
					backtracking_list.append((row,column))


	# (c) and (d)  
	elif valid_cell(grid,row,(column-1)):
		if grid[row][column-1] == 0:
			if valid_cell(grid,(row-1),(column-1)) or row == 0:
				if grid[(row-1)][(column-1)] == 2:
					backtracking_list.append((row,column))
			elif valid_cell(grid,(row+1),(column-1)) or row == (grid.shape[0] - 1):
				if grid[(row+1)][(column-1)] == 2:
					backtracking_list.append((row,column))

	# (e) and (f)  
	elif valid_cell(grid,(row+1),column):
		if grid[row+1][column] == 0:
			if valid_cell(grid,row,(column-1)) or column == 0:
				if grid[row][(column-1)] == 2:
					backtracking_list.append((row,column))
			elif valid_cell(grid,row,(column+1)) or column == (grid.shape[1] - 1):
				if grid[row][(column+1)] == 2:
					backtracking_list.append((row,column))


#def boustrophedon_motion(grid, start_row, start_column):
def boustrophedon_motion(grid):
	# TODO: define priorities: 
	# if in column change thre is the possibility of up or down move, the robot must go up
	# if in row change and there is the possibility of right or left move, the robot must go left
	# count de number of cells cleaned

	row = grid.shape[0] - 1
	column = 0

	grid[row][column] = 1
	draw_point(row,column, green)

	free = True
	while free:

		if verify('north',row, column):
			row -= 1
			grid[row][column] = 1
			backtracking_points(grid, row, column)
			draw_point(row,column, green)

		elif verify('south',row, column):
			row += 1
			grid[row][column] = 1
			backtracking_points(grid, row, column)
			draw_point(row,column, green)

		elif verify('east',row, column): # right
			column += 1
			grid[row][column] = 1
			backtracking_points(grid, row, column)
			draw_point(row,column, green)

		elif verify('west',row, column): # left
			column -= 1
			grid[row][column] = 1
			backtracking_points(grid, row, column)
			draw_point(row,column, green)
		else:
			free = False 
			print "crtic point"

	print grid
	print backtracking_list

clock = pygame.time.Clock()

def draw_point(row, column, color):
	pygame.draw.circle(screen, color, ((2*column + 1)*SQUARE_SIDE/2 + SCREEN_OFFSET, (2*row + 1)*SQUARE_SIDE/2 + SCREEN_OFFSET), 10)
	pygame.display.update()
	pygame.time.wait(10)

def init_grid():
    global screen 
    screen = pygame.display.set_mode(SCREEN_SIZE)
    #  _1_
    # |4 2|
    #  _3_
    pygame.draw.line(screen, (0, 200, 200), (SCREEN_OFFSET , SCREEN_OFFSET ), (SCREEN_OFFSET , EXT_GRID+SCREEN_OFFSET), (GRID_THICK )) # 4
    pygame.draw.line(screen, (0, 200, 200), (SCREEN_OFFSET , SCREEN_OFFSET ), (SCREEN_OFFSET + EXT_GRID, SCREEN_OFFSET ), (GRID_THICK )) # 1
    pygame.draw.line(screen, (0, 200, 200), (SCREEN_OFFSET , EXT_GRID + SCREEN_OFFSET), (SCREEN_OFFSET + EXT_GRID, SCREEN_OFFSET + EXT_GRID), (GRID_THICK))
    pygame.draw.line(screen, (0, 200, 200), (SCREEN_OFFSET + EXT_GRID, SCREEN_OFFSET), (SCREEN_OFFSET + EXT_GRID, SCREEN_OFFSET + EXT_GRID), (GRID_THICK)) # 3

    x = 1
    y = 1
    for i in range(ROWS):
        x += SQUARE_SIDE
        y += SQUARE_SIDE
        pygame.draw.line(screen, (0, 200, 200), (SCREEN_OFFSET, y + SCREEN_OFFSET), (SCREEN_SIDE + SCREEN_OFFSET, y + SCREEN_OFFSET), (1))
        pygame.draw.line(screen, (0, 200, 200), (x + SCREEN_OFFSET, SCREEN_OFFSET), (x+SCREEN_OFFSET, SCREEN_OFFSET + SCREEN_SIDE), (1))


def calc_final_path(ngoal, closedset):
    # generate final course
    rx, ry = [ngoal.x ], [ngoal.y]
    pind = ngoal.pind
    while pind != -1:
		n = closedset[pind]
		rx.append(n.x)
		ry.append(n.y)
		pind = n.pind

		pygame.draw.circle(screen, white, ((2*n.x + 1)*SQUARE_SIDE/2 + SCREEN_OFFSET, (2*n.y + 1)*SQUARE_SIDE/2 + SCREEN_OFFSET), 5)
		pygame.display.update()
		pygame.time.wait(100)

    return rx, ry



def verify_node(node, obmap):

    if node.x < 0:
        return False
    elif node.y < 0:
        return False
    elif node.x >= grid_shape[1]:
        return False
    elif node.y >= grid_shape[0]:
        return False

    for i in range(len(obmap)):
    	if obmap[i] == (node.y,node.x):
    		return False

    return True



def build_obs(obs):

	for i in range(len(obs)):
		pygame.draw.circle(screen, blue, ((2*obs[i][1] + 1)*SQUARE_SIDE/2 + SCREEN_OFFSET, (2*obs[i][0] + 1)*SQUARE_SIDE/2 + SCREEN_OFFSET), 5)

	pygame.display.update()

def calc_obstacle_map(ox, oy, reso, vr):

    obmap = [[False for i in range(xwidth)] for i in range(ywidth)]
    for ix in range(xwidth):
        x = ix + minx
        for iy in range(ywidth):
            y = iy + miny
            #  print(x, y)
            for iox, ioy in zip(ox, oy):
                d = math.sqrt((iox - x)**2 + (ioy - y)**2)
                if d <= vr / reso:
                    obmap[ix][iy] = True
                    break

	return obmap


def reset():
    global count
    #screen.fill(white)
    init_grid()
    count = 0

def main():
	#
	reset()

	# start and goal position
	sx = 0  
	sy = 0
	gx = 9
	gy = 9
	grid_size = 1.0  # [m]
	robot_size = 1.0  # [m]

	obs = []
	for i in range(grid.shape[0]):
		for j in range(grid.shape[1]):
			if grid[i][j] == 2:
				obs.append((i,j))


	# Build obstacles
	build_obs(obs)

	currentState = 'init'

	while True:
		# Finite State Machine
		if currentState == 'init':
			clock.tick(60)
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					sys.exit()

			column = 0 # x
			row = 0 # y

			boustrophedon_motion(grid)
			#rx ,ry = a_star_planning(sx, sy, gx, gy, obs)
			currentState = 'goalFound'

		elif currentState == 'goalFound':
		    #print ("Goal Reached")
		    pass


if __name__ == '__main__':
	main()