#!/usr/bin/env python
import random
import math
import numpy as np

import sys
from datetime import datetime
import time

RADIUS = 50.0

from constants import GREEN, WHITE, RED, BLACK, BLUE, YELLOW, PURPLE, DARK_GREEN
import pygame

from tree import Tree


# TODO
# if attempt to connect two tree return true stop and plot


class Node(object):
    def __init__(self, point, parent, cost=0):
        super(Node, self).__init__() # parent is a Node too
        self.point = point # position
        self.parent = parent # parent Node
        self.cost = cost


class RRT_Star:
    """
        Class for RRT* Path Planning
    """
    def __init__(self,
                 start_point, goal_point,
                 max_num_nodes, min_num_nodes,
                 goal_tolerance, epsilon_min, epsilon_max, screen):

        
        self.start_tree = Tree()
        self.goal_tree = Tree()


    def constant_draw(self):
        pass




    def planning(self):
        """ ."""
        start_new_node = None
        goal_new_node = None
        while len(self.nodes) < self.max_num_nodes:
            if start_time:
                self.start_tree.grow_tree()
                start_new_node = self.start_tree.get_new_node()

                if (goal_new_node is not None and
                   self.start_tree.attempt_connect(goal_new_node)):
                    return path

            else:
                self.goal_tree.grow_tree()
                goal_new_node = self.goal_tree.get_new_node()
                
                if (start_new_node is not None and
                   self.start_tree.attempt_connect(start_new_node)):
                    return path           


    
    def compute_path(self):
        """ ."""
        pass

    def draw_final_path(self, path):
        """ ."""
        pass

    def is_goal_reached(self, p1, p2, tolerance):
        """ ."""
        pass
