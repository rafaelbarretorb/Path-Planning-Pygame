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

        self.screen = screen

        self.start_point = start_point[:]
        self.goal_point = goal_point[:]

        self.max_num_nodes = max_num_nodes
        self.min_num_nodes = min_num_nodes
        self.epsilon_min = epsilon_min
        self.epsilon_max = epsilon_max

        
        self.start_time = datetime.now()
        self.time = 0.0

        self.goal_tolerance = goal_tolerance

        # self.path = list()
        self.path_old = list()

        self.goal_found = False

        self.nodes = list()
        self.goal_node = None

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
        pygame.draw.rect(self.screen, YELLOW, self.start_square, 0)
        pygame.draw.rect(self.screen, BLACK, self.start_square, 2)

        # GOAL POINT --> GRAY CIRCLE
        pygame.draw.circle(self.screen, PURPLE, self.goal_point, self.goal_tolerance)

    def dist(self, p1,p2):    
        """ Class method for compute the distance between two points.

        Args:
            p1: Point 1 tuple.
            p2: Poinf 2 tuple.

        Returns:
            The distance between two points the in cartesian plan.

        """
        distance = math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))
        return distance


    def choose_parent(self, new_node, parent):
        """ ."""
        for node in self.nodes:
            if self.dist(node.point, new_node.point) < RADIUS and \
               node.cost + self.dist(node.point, new_node.point) < parent.cost + self.dist(parent.point, new_node.point):

                parent = node

        new_node.cost = parent.cost + self.dist(parent.point, new_node.point)
        new_node.parent = parent
        return new_node

    def rewire(self, new_node):
        """ ."""
        for node in self.nodes:
            pygame.draw.circle(self.screen, GREEN, node.point, 4)

            if node != new_node.parent and \
               self.dist(node.point, new_node.point) < RADIUS and \
               new_node.cost + self.dist(node.point, new_node.point) < node.cost:

                # Delete, paint white
                pygame.draw.line(self.screen, WHITE, node.point, node.parent.point, 2) 

                # Now the node parent is the new node
                node.parent = new_node
                node.cost = new_node.cost + self.dist(node.point, new_node.point)
                # Draw
                pygame.draw.line(self.screen, BLUE, node.point, new_node.point, 2)
                
            else:
                if node.parent != None:
                    pygame.draw.line(self.screen, BLUE, node.point, node.parent.point, 2)

        self.constant_draw()
        pygame.display.update()


    def path_planning(self):
        """ RRT* (RRT Star) Path Planning

        Args:
        param1
        param2
        p2: Poinf 2 tuple.

        Returns:
        Th

        """
        path = list()
        path_old = list()

        initialNode = Node(self.start_point, None)
        self.nodes.append(initialNode)

        while len(self.nodes) < self.max_num_nodes:
            found_next = False
            
            # search a node until get one in free space
            while_time = datetime.now()
            while found_next == False:
                x_rand = self.sample_free() # random point in the free space
                x_nearest = self.get_nearest(self.nodes, x_rand) # return the nearest node
                x_new = self.steer(x_nearest.point, x_rand)
                if self.obstacle_free(x_nearest, x_new):
                    parent_node = x_nearest
                    new_node = Node(x_new, parent_node)
                    new_node = self.choose_parent(new_node, parent_node)
                    self.nodes.append(new_node)
                    self.rewire(new_node)            
                    found_next = True

                    # Draw the new twig
                    pygame.draw.line(self.screen, BLUE, new_node.point, parent_node.point, 2)
                    pygame.draw.circle(self.screen, GREEN, new_node.point, 4)
                    pygame.display.update()
                    # time.sleep(0.05)

            path = list()
            if not self.goal_found:
                # check if the distance between the goal node and the new node is less than the goal tolerance
                if self.is_goal_reached(x_new, self.goal_point, self.goal_tolerance):
                    self.goal_found = True
                    self.goal_node = self.nodes[len(self.nodes)-1]
                    path = self.compute_path()
            else:
                path = self.compute_path()
            
            if len(self.nodes) > self.min_num_nodes:
                return path
        
        print "Nodes Amount: " + str(len(self.nodes))
        return [], []
    
    def compute_path(self):
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
        # Draw old path with WHITE
        for i in range(len(self.path_old) - 1):
            pygame.draw.line(self.screen, WHITE, self.path_old[i], self.path_old[i + 1], 4) 
            
        pygame.display.update()
        # Draw current path with RED
        for i in range(len(path) - 1):
            pygame.draw.line(self.screen, RED, path[i], path[i + 1], 4)
        
        pygame.display.update()
        self.path_old = path[:]
        # Draw start and goal
        # pygame.draw.circle(self.screen, YELLOW, (self.start_point[0], self.start_point[1]), 10)
        # pygame.draw.circle(self.screen, BLACK, (self.goal_point[0], self.goal_point[1]), self.goal_tolerance)

    def sample_free(self):
        """  Get a random point located in a free area

        random.random() returns a random number between  0 and 1

        x_rand = (RANDOM_NUMBER - MAX_RANDOM_NUMBER/2)*XDIM, random.random()*self.YDIM

        """
        # TODO no collision yet
        for i in range(1000):
            return int((random.random())*500), int((random.random())*500)

        sys.exit("ERROR MESSAGE: Samples in free space fail after 1000 attempts!!!")

    def is_goal_reached(self, p1, p2, tolerance):
        distance = self.dist(p1,p2)
        if (distance <= tolerance):
            return True
        return False

    def steer(self, p1, p2):
        distance = self.dist(p1,p2)
        if distance < self.epsilon_max and distance > self.epsilon_min:
            return p2
        else:
            theta = math.atan2(p2[1]-p1[1],p2[0]-p1[0])
            return int(p1[0] + self.epsilon_max*math.cos(theta)), int(p1[1] + self.epsilon_max*math.sin(theta))

    def get_nearest(self, nodes, x_rand):
        # seach
        nn = nodes[0]
        for node in nodes:
            if self.dist(node.point, x_rand) < self.dist(nn.point, x_rand):
                nn = node

        return nn

    def obstacle_free(self, n1, n2):
        return True
