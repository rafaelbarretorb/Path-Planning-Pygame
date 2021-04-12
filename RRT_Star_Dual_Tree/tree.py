#!/usr/bin/env python
import random
from helper_functions import *
from node import Node
import pygame
from constants import WHITE
import time

import sys

RADIUS = 50.0

class Tree:
	def __init__(self):
		self.nodes = list()

	def __init__(self,
	             name,
				 start_point,
				 node_color,
				 connection_color,
				 goal_node_color,
				 path_color,
				 goal_tolerance,
				 epsilon_min,
				 epsilon_max,
				 screen):
		""" ."""
		self.tree_name = name
		self.nodes = list()
		self.new_node = None

		self.screen = screen

		self.k = 20.0
		self.radius = 100.0

		self.node_color = node_color
		self.connection_color = connection_color
		self.goal_node_color = goal_node_color
		self.path_color = path_color

		self.nodes.append(Node(start_point, None))

		self.max_num_nodes = 5000
		self.min_num_nodes = 200

		self.epsilon_max = epsilon_max
		self.epsilon_min = epsilon_min

		self.goal_tolerance = goal_tolerance

		self.n_nearest_ext = None

		self.goal = None

		self.tree_blocked = False
		self.path_old = list()

		# Draw Tree Start Node
		self.draw_node(start_point, radius=8)

	def get_nodes_length(self):
		""" ."""
		return len(self.nodes)

	def choose_parent(self, new_node, parent):
		""" ."""
		for node in self.nodes:
			# distance node to new_node
			d = dist(node.point, new_node.point)

			# connection cost node to new_node
			cost_n_2_new_n = node.cost + dist(node.point, new_node.point)

			# connection cost node to parent
			cost_p_2_new_n = parent.cost + dist(parent.point, new_node.point)

			if d < RADIUS and cost_n_2_new_n < cost_p_2_new_n:
				parent = node

		new_node.cost = parent.cost + dist(parent.point, new_node.point)
		new_node.parent = parent
		return new_node

	def rewire(self, new_node):
		""" ."""
		for node in self.nodes:
			# Draw node node TODO ???
			self.draw_node(node.point)

			# new_node parent
			new_n_p = new_node.parent

			# distance node to new_node
			d = dist(node.point, new_node.point)

			# connection cost node to new_node
			cost_new_n_2_n = new_node.cost + dist(node.point, new_node.point)

			if node != new_n_p and d < RADIUS and cost_new_n_2_n < node.cost:
				# Delete, paint white
				self.erase_connection(node.point, node.parent.point)

				# Now the node parent is the new node
				node.parent = new_node
				node.cost = new_node.cost + dist(node.point, new_node.point)
				
				# Draw
				self.draw_connection(node.point, new_node.point)
					
			else:
				if node.parent != None:
					self.draw_connection(node.point, node.parent.point)

		pygame.display.update()


	def grow_tree(self):
		""" ."""
		if self.tree_blocked:
			print "TREE BLOCKED"
			return
		else:
			found_next = False
			while found_next == False:
				p_rand = self.sample_free()
				n_nearest = self.get_nearest(p_rand)
				n_new = self.steer(n_nearest.point, p_rand)
				if self.obstacle_free(n_nearest, n_new):
					found_next = True
					self.insert_node(n_new, n_nearest)
	
	def insert_node(self, x_new, x_nearest):
		""" ."""
		parent_node = x_nearest
		new_node = Node(x_new, parent_node)
		new_node = self.choose_parent(new_node, parent_node)
		self.nodes.append(new_node)
		self.rewire(new_node)            
		self.new_node = self.nodes[-1]

		# Draw the new connection
		self.draw_connection(self.new_node.point, self.new_node.parent.point)

		# Draw new node
		self.draw_node(self.new_node.point)

		pygame.display.update()

		# uncomment to make animation slow
		# time.sleep(0.05)

	def sample_free(self):
		"""  Get a random point located in a free area
		random.random() returns a random number between 0 and 1
		x_rand = RANDOM_NUMBER * XDIM, RANDOM_NUMBER * YDIM
		"""
		# TODO no collision yet
		for i in range(1000):
			return int((random.random())*500), int((random.random())*500)

		sys.exit("ERROR MESSAGE: Samples in free space fail after 1000 attempts!!!")

	def steer(self, p1, p2):
		""" ."""
		distance = dist(p1,p2)
		if distance < self.epsilon_max and distance > self.epsilon_min:
			return p2
		else:
			theta = math.atan2(p2[1]-p1[1],p2[0]-p1[0])
			return int(p1[0] + self.epsilon_max*math.cos(theta)), int(p1[1] + self.epsilon_max*math.sin(theta))

	def get_nearest(self, x_rand):
		""" ."""
		nn = self.nodes[0]
		for node in self.nodes:
			if dist(node.point, x_rand) < dist(nn.point, x_rand):
				nn = node

		return nn

	def get_new_node(self):
		""" ."""
		# TODO woring hete
		return self.new_node

	def attempt_connect(self, external_node):
		""" ."""
		n_nearest = self.get_nearest(external_node.point)

		if dist(n_nearest.point, external_node.point) < self.goal_tolerance:
			# check collision
			if self.obstacle_free(n_nearest, external_node):
				self.n_nearest_ext = n_nearest
				return True
		return False

	def update_radius(self):
		# TODO node list has not shape
		nodes_size = len(self.nodes) + 1
		self.radius = self.k*math.sqrt((math.log(nodes_size) / nodes_size))

	def obstacle_free(self, n1, n2):
		return True

	def get_external_nodes(self, n_nearest_ext):
		""" ."""
		external_nodes = list()
		current_node = n_nearest_ext
		while current_node.parent != None:
			external_nodes.append(current_node)
			current_node = current_node.parent

		# Add the first tree node
		external_nodes.append(current_node)

		return external_nodes

	def get_n_nearest_external(self):
		""" ."""
		return self.n_nearest_ext

	def add_nodes_to_tree(self, external_nodes, parent_node):
		current_parent = parent_node

		nodes_index = len(self.nodes)
		for node in external_nodes:
			node.parent = current_parent
			node.cost = current_parent.cost + dist(node.point, current_parent.point)
			
			current_parent = node

			# add to the nodes list
			self.nodes.append(node)

		self.goal = self.nodes[len(self.nodes) - 1]
	
	def block_tree(self):
		""" This tree does not grow anymore."""
		self.tree_blocked = True

	def compute_path(self):
		""" ."""
		path = list()
		current_node = self.goal

		while current_node.parent != None:
			path.insert(0, current_node.point)
			current_node = current_node.parent

		# Add the start point
		path.insert(0, current_node.point)
		
		# Draw path
		self.draw_final_path(path)
		return path

	def draw_final_path(self, path):
		""" ."""
		# ERASE old path
		for i in range(len(self.path_old) - 1):
			self.erase_path(self.path_old[i], self.path_old[i + 1])
		
		pygame.display.update()
		
		self.path_old = []

		pygame.display.update()

		# Draw new path
		for i in range(len(path) - 1):
			self.draw_path(path[i], path[i + 1])
		
		# Draw Goal Node of the Tree
		self.draw_node(self.goal.point, radius=8, color=self.goal_node_color)
		
		pygame.display.update()
		
	def draw_connection(self, point1, point2, width=2):
		""" ."""
		pygame.draw.line(self.screen, self.connection_color, point1, point2, width)

	def erase_connection(self, point1, point2):
		""" ."""
		pygame.draw.line(self.screen, WHITE, point1, point2, 2)

	def draw_path(self, point1, point2):
		""" ."""
		pygame.draw.line(self.screen, self.path_color, point1, point2, 8)

	def erase_path(self, point1, point2):
		""" ."""
		pygame.draw.line(self.screen, WHITE, point1, point2, 8)

	def draw_node(self, point, radius=4, color=None):
		""" ."""
		if color is None:
			color = self.node_color

		pygame.draw.circle(self.screen, color, point, radius)

	def is_tree_blocked(self):
		""" ."""
		return self.tree_blocked