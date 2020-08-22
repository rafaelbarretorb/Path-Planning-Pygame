

from rrt_star import RRT_Star
import pygame
from pygame.locals import *
import sys
from constants import WHITE, GREEN, RED

XDIM = 500
YDIM = 500
WINSIZE = [XDIM, YDIM]
EPSILON = 7.0
MAX_NUM_NODES = 2000
MIN_NUM_NODES = 500

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('RRT* Path Planning')
    screen.fill(WHITE)

    start_point = [200, 200]
    goal_point = [400, 400]
    goal_tolerance = 20
    rrt_star = RRT_Star(start_point, goal_point, MAX_NUM_NODES, MIN_NUM_NODES, goal_tolerance, 5, 30, screen)

    path = rrt_star.path_planning()
    for e in pygame.event.get():
        if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
            sys.exit("Leaving because you requested it.")
    pygame.display.update()

if __name__ == '__main__':
    main()