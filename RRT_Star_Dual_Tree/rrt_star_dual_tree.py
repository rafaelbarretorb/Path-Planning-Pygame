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

        self.start_tree = Tree('start',
                               start_point,
                               node_color=GREEN,
                               connection_color=GREEN,
                               goal_node_color=RED,
                               path_color=BLACK,
                               goal_tolerance=20,
                               epsilon_min=epsilon_min,
                               epsilon_max=epsilon_max,
                               screen=screen)

        self.goal_tree = Tree('goal',
                              goal_point,
                              node_color=RED,
                              connection_color=RED,
                              goal_node_color=GREEN,
                              path_color=BLACK,
                              goal_tolerance=20,
                              epsilon_min=epsilon_min,
                              epsilon_max=epsilon_max,
                              screen=screen)

        self.tree = Tree()

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
        pygame.draw.circle(self.screen, GREEN, self.start_point, 8)

        # GOAL POINT --> GRAY CIRCLE
        pygame.draw.circle(self.screen, RED, self.goal_point, 8)


    def planning(self):
        """ ."""
        start_tree_size = self.start_tree.get_nodes_length()
        goal_tree_size = self.goal_tree.get_nodes_length()
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

                    # Block Goal Tree
                    self.goal_tree.block_tree()
                    self.tree = self.start_tree

                    gt_n_nearest_ext = self.goal_tree.get_n_nearest_external()

                    #print "nearest ext node: " + str(gt_x_nearest_ext.point)
                    
                    # Get nodes path from GOAL Tree
                    external_nodes = self.goal_tree.get_external_nodes(gt_n_nearest_ext)
                    
                    #  Add nodes path to START Tree
                    self.start_tree.add_nodes_to_tree(external_nodes, st_new_node)
                

                if not self.goal_found:
                    # 
                    start_time = False
            else:
                # Goal Tree grows
                self.goal_tree.grow_tree()

                # Test EXIT
                # print "EXIT"
                # sys.exit()

                # Goal Tree new node
                gt_new_node = self.goal_tree.get_new_node()
                # print "new node: " + str(gt_new_node.point)
                # print ""

                if (self.goal_found is not True and self.start_tree.attempt_connect(gt_new_node)):
                    self.goal_found = True

                    # Block Start Tree
                    self.start_tree.block_tree()
                    self.tree = self.goal_tree

                    st_n_nearest_ext = self.start_tree.get_n_nearest_external()
                    
                    # Get nodes path from START Tree
                    external_nodes = self.start_tree.get_external_nodes(st_n_nearest_ext)

                    # Add nodes path to GOAL Tree
                    self.goal_tree.add_nodes_to_tree(external_nodes, gt_new_node)
    

                if not self.goal_found:
                    start_time = True 

            if self.goal_found:
                path = self.tree.compute_path()
                if self.tree.get_nodes_length() > self.min_num_nodes:
                    return path
        
        return [], []
    


    def draw_final_path(self, path):
        """ ."""
        pass

    def is_goal_reached(self, p1, p2, tolerance):
        """ ."""
        distance = self.dist(p1,p2)
        if (distance <= tolerance):
            return True
        return False


    def planning2(self):
        """ ."""
        while self.tree.get_nodes_length() < self.max_num_nodes:
            # Start Tree's turn
            self.run_tree(self.start_tree, self.goal_tree)

            # Goal Tree's turn
            self.run_tree(self.goal_tree, self.start_tree)

            if self.goal_found:
                path = self.tree.compute_path()
                if self.tree.get_nodes_length() > self.min_num_nodes:
                    return path
        
        return [], []
    
    def run_tree(self, tree_obj, other_tree_obj):
        if tree_obj.is_tree_blocked():
            return
        else:
            # Tree grows
            tree_obj.grow_tree()

            # Tree new node
            new_node = tree_obj.get_new_node()

            if not self.goal_found:
                if other_tree_obj.attempt_connect(new_node):
                    self.goal_found = True

                    # Block Other Tree
                    other_tree_obj.block_tree()

                    # # TODO review remove
                    self.tree = tree_obj

                    n_nearest_ext = other_tree_obj.get_n_nearest_external()
                    
                    # Get nodes path from GOAL Tree
                    external_nodes = other_tree_obj.get_external_nodes(n_nearest_ext)
                    
                    #  Add nodes path to START Tree
                    tree_obj.add_nodes_to_tree(external_nodes, new_node)

    def keep_searching(self):
        """ ."""
        if not self.goal_found:
            return True
        else:
            start_size = self.start_tree.get_nodes_length()
            goal_size = self.goal_tree.get_nodes_length()
            if start_size > self.max_num_nodes or goal_size > self.max_num_nodes:
                return False
            else:
                return True