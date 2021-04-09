#!/usr/bin/env python

import math
import numpy as np

import sys
from datetime import datetime
import time

RADIUS = 50.0

from constants import GREEN, WHITE, RED, BLACK, BLUE, YELLOW, PURPLE, DARK_GREEN
import pygame

from tree import Tree
from node import Node
from helper_functions import *

# TODO
# if attempt to connect two tree return true stop and plot


class RRT_Star:
    """ Class for RRT* Path Planning. """
    def __init__(self, start_point, goal_point,
                 max_num_nodes, min_num_nodes,
                 goal_tolerance, epsilon_min, epsilon_max, screen):
        
        

        self.screen = screen

        self.start_point = start_point[:]
        self.goal_point = goal_point[:]

        self.max_num_nodes = max_num_nodes
        self.min_num_nodes = min_num_nodes
        self.epsilon_min = epsilon_min
        self.epsilon_max = epsilon_max

        # self.start_time = datetime.now()
        # self.time = 0.0

        self.goal_tolerance = goal_tolerance

        self.start_tree = Tree(start_point, vertex_color=GREEN, edge_color=GREEN, epsilon_min=epsilon_min, epsilon_max=epsilon_max, screen=screen)
        self.goal_tree = Tree(goal_point, vertex_color=RED, edge_color=RED, epsilon_min=epsilon_min, epsilon_max=epsilon_max, screen=screen)

        # self.path = list()
        self.path_old = list()

        self.goal_found = False

        # Draw start and goal

        # START SQUARE
        width = 20
        height = width
        left = self.start_point[0] - width/2
        top = self.start_point[1] - height/2
        self.start_square = pygame.Rect(left, top, width, height)

        self.constant_draw()
        pygame.display.update()
        time.sleep(2)


    def constant_draw(self):
        # START POINT --> YELLOW SQUARE
        # pygame.draw.rect(self.screen, YELLOW, self.start_square, 0)
        # pygame.draw.rect(self.screen, BLACK, self.start_square, 2)
        pygame.draw.circle(self.screen, GREEN, self.start_point, 8)

        # GOAL POINT --> GRAY CIRCLE
        # pygame.draw.circle(self.screen, PURPLE, self.goal_point, self.goal_tolerance)
        pygame.draw.circle(self.screen, RED, self.goal_point, 8)


    def planning(self):
        """ ."""
        count = 0
        start_time = True
        while self.start_tree.get_nodes_length() < self.max_num_nodes or self.goal_tree.get_nodes_length() < self.max_num_nodes:
            if start_time:
                # Start Tree grows
                self.start_tree.grow_tree()

                # Start Tree new node
                st_new_node = self.start_tree.get_new_node()
                # print "new node: " + str(st_new_node.point)
                # print ""


                if (self.goal_found is not True and self.goal_tree.attempt_connect(st_new_node)):
                    self.goal_found = True
                    gt_x_nearest_ext = self.goal_tree.get_x_nearest_external()

                    print "nearest ext node: " + str(gt_x_nearest_ext.point)
                    
                    # Get nodes path from GOAL Tree
                    external_nodes = self.goal_tree.get_external_nodes(gt_x_nearest_ext)
                    
                    #  Add nodes path to START Tree
                    self.start_tree.add_nodes_to_tree(external_nodes, st_new_node)
                
                if self.goal_found:
                    count = count + 1
                    if count > 2:
                        return

                if not self.goal_found:
                    # 
                    start_time = False
            else:
                # Goal Tree grows
                self.goal_tree.grow_tree()

                # Goal Tree new node
                gt_new_node = self.goal_tree.get_new_node()
                # print "new node: " + str(gt_new_node.point)
                # print ""

                if (self.goal_found is not True and self.start_tree.attempt_connect(gt_new_node)):
                    self.goal_found = True
                    st_x_nearest_ext = self.start_tree.get_x_nearest_external()
                    print "nearest ext node: " + str(st_x_nearest_ext.point)
                    
                    # Get nodes path from START Tree
                    external_nodes = self.start_tree.get_external_nodes(st_x_nearest_ext)

                    # Add nodes path to GOAL Tree
                    self.goal_tree.add_nodes_to_tree(external_nodes, gt_new_node)
                
                if self.goal_found:
                    count = count + 1
                    if count > 2:
                        return

                if not self.goal_found:
                    start_time = True 

            # path = list()
            # path = self.compute_path()
            
            # if len(self.nodes) > self.min_num_nodes:
            #     return path
        
        return [], []
    
    def compute_path(self):
        """ ."""
        path = list()
        current_node = self.goal_node
        while current_node.parent != None:
            path.insert(0, current_node.point)
            current_node = current_node.parent

        # Add the start point
        path.insert(0, current_node.point)
        
        # print "Nodes Amount: " + str(len(nodes))

        self.draw_final_path(path)
        return path

    def draw_final_path(self, path):
        """ ."""
        pass

    def is_goal_reached(self, p1, p2, tolerance):
        """ ."""
        distance = self.dist(p1,p2)
        if (distance <= tolerance):
            return True
        return False
