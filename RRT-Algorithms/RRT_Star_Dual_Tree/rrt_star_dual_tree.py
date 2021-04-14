#!/usr/bin/env python

from constants import GREEN, RED, BLACK, BLUE
from tree import Tree

import pygame


class RRTStarDualTree:
    """ Class for RRT* Path Planning. """
    def __init__(self, start_point, goal_point,
                 max_num_nodes, min_num_nodes,
                 goal_tolerance, epsilon_min, epsilon_max, screen):
        self.screen = screen
        self.start_point = start_point
        self.goal_point = goal_point

        self.max_num_nodes = max_num_nodes
        self.min_num_nodes = min_num_nodes
        self.epsilon_min = epsilon_min
        self.epsilon_max = epsilon_max

        self.goal_tolerance = goal_tolerance

        self.start_tree = Tree('start',
                               start_point,
                               node_color=GREEN,
                               connection_color=GREEN,
                               goal_node_color=BLUE,
                               path_color=RED,
                               goal_tolerance=20,
                               epsilon_min=epsilon_min,
                               epsilon_max=epsilon_max,
                               max_num_nodes=5000,
                               screen=self.screen)

        self.goal_tree = Tree('goal',
                              goal_point,
                              node_color=BLUE,
                              connection_color=BLUE,
                              goal_node_color=GREEN,
                              path_color=RED,
                              goal_tolerance=20,
                              epsilon_min=epsilon_min,
                              epsilon_max=epsilon_max,
                              max_num_nodes=5000,
                              screen=self.screen)

        self.tree = None

        self.goal_found = False

    def planning(self):
        """ ."""
        while self.keep_searching():
            pygame.display.update()
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
