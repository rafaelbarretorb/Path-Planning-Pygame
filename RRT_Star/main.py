

from rrt_star import RRT_Star
import pygame
from pygame.locals import *
import sys
from constants import WHITE, GREEN, RED

XDIM = 640
YDIM = 480
WINSIZE = [XDIM, YDIM]
EPSILON = 7.0
NUMNODES = 2000

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('RRT* Path Planning')
    screen.fill(WHITE)

    start_point = [200, 200]
    goal_point = [400, 400]
    rrt_star = RRT_Star(start_point, goal_point, NUMNODES, 0.1, 0.4, screen)

    while True:
        # path_x, path_y = rrt_star.path_planning()
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                sys.exit("Leaving because you requested it.")
        pygame.display.update()

if __name__ == '__main__':
    main()