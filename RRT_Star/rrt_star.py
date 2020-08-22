#!/usr/bin/env python
import random
import math
import numpy as np

import sys
from datetime import datetime
import time

RADIUS = 10.0

from constants import GREEN, WHITE, RED, BLACK
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

        # Draw start and goal
        pygame.draw.circle(self.screen, BLACK, (self.start_point[0], self.start_point[1]), self.goal_tolerance)
        pygame.draw.circle(self.screen, BLACK, (self.goal_point[0], self.goal_point[1]), self.goal_tolerance)


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


    def choose_parent(self,nn,new_node,nodes):
        for node in nodes:
            if self.dist(node.point,new_node.point) < RADIUS and node.cost + self.dist(node.point, new_node.point) < nn.cost + self.dist(nn.point,new_node.point):
                nn = node
        new_node.cost = nn.cost + self.dist(nn.point,new_node.point)
        new_node.parent = nn

        return new_node

    def rewire(self, nodes, new_node):
        for i in range(len(nodes)):
            node = nodes[i]
            if node != new_node.parent and self.dist(node.point,new_node.point) < RADIUS and new_node.cost + self.dist(node.point,new_node.point) < node.cost:
                # Delete, paint white
                pygame.draw.line(self.screen, WHITE, [node.point[0], node.point[1]], [node.parent.point[0], node.parent.point[0]], 2) 
                node.parent = new_node
                node.cost = new_node.cost + self.dist(node.point,new_node.point)
                # Draw
                pygame.draw.line(self.screen, GREEN, [node.point[0], node.point[1]], [new_node.point[0], new_node.point[1]], 2)
                pygame.display.update()

        return nodes

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

        while len(self.nodes) < self.max_num_nodes: # and (datetime.now() - self.start_time).total_seconds() < 30 and not ((datetime.now() - self.start_time).total_seconds() > 5 and len(nodes) < 20):

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
                    new_node = self.choose_parent(parent_node, new_node, self.nodes)
                    self.nodes.append(new_node)
                    self.nodes = self.rewire(self.nodes, new_node)            
                    found_next = True

                    # Draw the new twig
                    pygame.draw.line(self.screen, GREEN, new_node.point, parent_node.point, 2)
                    pygame.display.update()
                    time.sleep(0.05)

                if not self.goal_found:
                    # check if the distance between the goal node and the new node is less than the goal tolerance
                    if self.is_goal_reached(x_new, self.goal_point, self.goal_tolerance):
                        new_goal_node = self.nodes[len(self.nodes)-1]
                        self.goal_found = True
                else:
                    # Final path
                    current_node = new_goal_node
                    while current_node.parent != None:
                        self.path.insert(0, current_node.point)
                        current_node = current_node.parent

                    # Add the start point
                    self.path.insert(0, current_node.point)
                    
                    # print "Nodes Amount: " + str(len(nodes))

                    self.draw_final_path(path)

                    if len(self.nodes) > self.min_num_nodes:
                        time.sleep(10)
                        return self.path
        
        print "Nodes Amount: " + str(len(self.nodes))
        return [], []
    
    def compute_final_path(self):
        # Final path
        current_node = new_goal_node
        while current_node.parent != None:
            self.path.insert(0, current_node.point)
            current_node = current_node.parent

        # Add the start point
        self.path.insert(0, current_node.point)
        
        # print "Nodes Amount: " + str(len(nodes))

        self.draw_final_path(path)

        if len(self.nodes) > self.min_num_nodes:
            time.sleep(10)
            return self.path

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
        self.path_old = path

    def sample_free(self):
        """  Get a random point located in a free area

        random.random() returns a random number between  0 and 1

        x_rand = (RANDOM_NUMBER - MAX_RANDOM_NUMBER/2)*XDIM, random.random()*self.YDIM

        """
        # TODO no collision yet
        for i in range(1000):
            return (random.random())*500, (random.random())*500

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
            return p1[0] + self.epsilon_max*math.cos(theta), p1[1] + self.epsilon_max*math.sin(theta)

    def get_nearest(self, nodes, x_rand):
        # seach
        nn = nodes[0]
        for node in nodes:
            if self.dist(node.point, x_rand) < self.dist(nn.point, x_rand):
                nn = node

        return nn

    def obstacle_free(self, n1, n2):
        return True
