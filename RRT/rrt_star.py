#!/usr/bin/env python

import pygame
import sys

from constants import GREEN, RED, BLACK, WHITE, YELLOW, PURPLE
from tree import Tree
from helper_functions import dist
from node import Node

RADIUS = 50.0


class RRTStar:
    """ Class for RRT* Path Planning."""
    def __init__(self,
                 start_point, goal_point,
                 max_num_nodes, min_num_nodes,
                 goal_tolerance, epsilon_min, epsilon_max, screen):

        self.screen = screen
        self.nodes = list()
        self.start_point = start_point
        self.goal_point = goal_point

        self.max_num_nodes = max_num_nodes
        self.min_num_nodes = min_num_nodes
        self.epsilon_min = epsilon_min
        self.epsilon_max = epsilon_max


        self.goal_tolerance = goal_tolerance
        self.goal_found = False

        self.tree = Tree('tree',
                               start_point,
                               node_color=GREEN,
                               connection_color=GREEN,
                               goal_node_color=BLACK,
                               path_color=RED,
                               goal_tolerance=20,
                               epsilon_min=epsilon_min,
                               epsilon_max=epsilon_max,
                               max_num_nodes=5000,
                               screen=self.screen)

        self.tree.set_goal(Node(goal_point, None))
        self.goal_node = self.tree.get_goal()

    def constant_draw(self):
        # GOAL POINT --> GRAY CIRCLE
        pygame.draw.circle(self.screen, PURPLE, self.goal_point, self.goal_tolerance)

    def planning(self):
        """ ."""
        while self.keep_searching():
            self.constant_draw()
            pygame.display.update()
            
            # Tree grows
            self.tree.grow_tree()

            new_node = self.tree.get_new_node()

            if not self.goal_found:
                if self.is_goal_reached(new_node, self.goal_node):

                    self.goal_found = True

                    # new node is the final goal
                    self.goal_node = self.tree.set_goal(new_node)
                    path = self.tree.compute_path()
            else:
                path = self.tree.compute_path()
            
            if len(self.nodes) > self.min_num_nodes:
                return path
        
        return [], []

    def keep_searching(self):
        """ ."""
        if not self.goal_found:
            return True
        else:
            tree_size = self.tree.get_nodes_length()
            if tree_size > self.max_num_nodes:
                return False
            else:
                return True

    def is_goal_reached(self, n1, n2):
        distance = dist(n1.point, n2.point)
        if (distance <= self.goal_tolerance):
            return True
        return False


XDIM = 500
YDIM = 500
WINSIZE = [XDIM, YDIM]
EPSILON = 7.0
MAX_NUM_NODES = 1500
MIN_NUM_NODES = 500

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('RRT* Path Planning')
    screen.fill(WHITE)

    start_point = [200, 200]
    goal_point = [400, 400]
    goal_tolerance = 20
    rrt_star = RRTStar(start_point, goal_point, MAX_NUM_NODES, MIN_NUM_NODES, goal_tolerance, 0, 30, screen)

    path = rrt_star.planning()
    pause = True
    # for e in pygame.event.get():
    #     if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
    #         sys.exit("Leaving because you requested it.")
    # pygame.display.update()

    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

if __name__ == '__main__':
    main()