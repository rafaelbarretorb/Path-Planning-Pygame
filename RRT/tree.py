#!/usr/bin/env python

import random
from helper_functions import * # dist
from node import Node
import pygame
from constants import WHITE
import time
import sys

# TODO review remove
RADIUS = 50.0


class Tree:
	def __init__(self,
	             is_start_tree,
				 start_point,
				 node_color,
				 connection_color,
				 goal_node_color,
				 path_color,
				 goal_tolerance,
				 epsilon_min,
				 epsilon_max,
				 max_num_nodes,
				 screen,
				 obstacles, obs_resolution):
		""" ."""
		self.is_start_tree = is_start_tree
		self.nodes = list()
		self.new_node = None

		self.screen = screen
		self.obstacles = obstacles
		self.obs_resolution = obs_resolution

		self.k = 20.0
		self.radius = 100.0

		self.node_color = node_color
		self.connection_color = connection_color
		self.goal_node_color = goal_node_color
		self.path_color = path_color

		self.max_num_nodes = max_num_nodes

		self.epsilon_max = epsilon_max
		self.epsilon_min = epsilon_min

		self.goal_tolerance = goal_tolerance

		self.n_nearest_ext = None

		self.goal = None

		self.tree_blocked = False
		self.path_old = list()

		# Add the initial node
		self.nodes.append(Node(start_point, None))

		# Draw Tree Start Node
		self.draw_node(start_point, radius=8)

		pygame.display.update()

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
				if self.obstacle_free(node.point, new_node.point):
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
				if self.obstacle_free(node.point, new_node.point):
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
		found_next = False
		while found_next == False:
			p_rand = self.sample_free()
			n_nearest = self.get_nearest(p_rand)
			p_new = self.steer(n_nearest.point, p_rand)
			if self.obstacle_free(n_nearest.point, p_new):
				found_next = True
				self.insert_node(p_new, n_nearest)
	
	def insert_node(self, p_new, n_nearest):
		""" ."""
		parent_node = n_nearest
		new_node = Node(p_new, parent_node)
		new_node = self.choose_parent(new_node, parent_node)
		self.nodes.append(new_node)

		self.nodes[-1].id = len(self.nodes) - 1
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
		point_rand = RANDOM_NUMBER * XDIM, RANDOM_NUMBER * YDIM
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

	def get_nearest(self, p_rand):
		""" Returns the nearest node of the list."""
		n_nearest = self.nodes[0]
		for node in self.nodes:
			if dist(node.point, p_rand) < dist(n_nearest.point, p_rand):
				n_nearest = node

		return n_nearest

	def get_new_node(self):
		""" Returns the new node of the tree."""
		return self.new_node

	def attempt_connect(self, external_node):
		""" Attempt to connect an external node in this tree."""
		n_nearest = self.get_nearest(external_node.point)

		if dist(n_nearest.point, external_node.point) < self.goal_tolerance:
			# check collision
			if self.obstacle_free(n_nearest.point, external_node.point):
				self.n_nearest_ext = n_nearest
				return True
		return False

	def update_radius(self):
		""" Update the radius of the algorithm optimization area."""
		nodes_size = len(self.nodes) + 1
		self.radius = self.k*math.sqrt((math.log(nodes_size) / nodes_size))

	# TODO improve name of this method
	def get_external_nodes(self, n_nearest_ext):
		""" Get the nodes that lead to the initial node of the tree,
		    starting from the nearest node of the external node
			provided (n_nearest_ext)."""
		external_nodes = list()
		current_node = n_nearest_ext
		while current_node.parent != None:
			external_nodes.append(current_node)
			current_node = current_node.parent

		# Add the first tree node
		external_nodes.append(current_node)

		return external_nodes

	def get_n_nearest_external(self):
		""" Returns the node of this tree that is the nearest node
		    of the new node of the other tree."""
		return self.n_nearest_ext

	def add_nodes_to_tree(self, external_nodes, parent_node):
		""" Add a set of external nodes to this tree."""
		current_parent = parent_node

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
		""" Compute the current path resultant of the
		    fusion of the two trees.."""
		path = list()
		current_node = self.goal

		while current_node.parent != None:
			path.insert(0, current_node.point)
			current_node = current_node.parent

		# Add the start point
		path.insert(0, current_node.point)

		self.draw_current_path(path)

		if not self.is_start_tree_the_last():
			path.reverse()
		
		return path

	def draw_current_path(self, path):
		""" Erase the old path and draw the current path between
		    start and goal nodes.."""
		# ERASE old path
		for i in range(len(self.path_old) - 1):
			self.erase_path(self.path_old[i], self.path_old[i + 1])
		
		pygame.display.update()
		
		self.path_old = path[:]

		# Draw new path
		for i in range(len(path) - 1):
			self.draw_path(path[i], path[i + 1])
		
		# Draw Goal Node of the Tree
		self.draw_node(self.goal.point, radius=8, color=self.goal_node_color)
		
		pygame.display.update()
		
	def draw_connection(self, point1, point2, width=2):
		""" Draw the connection (edge) between two nodes."""
		pygame.draw.line(self.screen, self.connection_color, point1, point2, width)

	def erase_connection(self, point1, point2):
		""" Erase the connection (edge) between two nodes."""
		pygame.draw.line(self.screen, WHITE, point1, point2, 2)

	def draw_path(self, point1, point2):
		""" Draw a path line between two nodes with a larger width."""
		pygame.draw.line(self.screen, self.path_color, point1, point2, 6)

	def erase_path(self, point1, point2):
		""" Erase the path line between two nodes."""
		pygame.draw.line(self.screen, WHITE, point1, point2, 6)

	def draw_node(self, point, radius=4, color=None):
		""" Draw a circle representing a node."""
		if color is None:
			color = self.node_color

		pygame.draw.circle(self.screen, color, (point[0], point[1]), radius)

	def is_tree_blocked(self):
		""" Returns true if this tree is blocked, false otherwise."""
		return self.tree_blocked

	def set_goal(self, goal_node):
		""" Set goal node. Necessary for RRT* that has just one Tree growing."""
		self.goal = goal_node

	def get_goal(self):
		""" Get goal node."""
		return self.goal

	def path_otimization(self):
		""" Path Optimization.
		    Only RRT*-Smart algorithm """

		new_path = list()
		i = 0
		current_node = self.goal
		while current_node.parent.parent != None:
			# while self.obstacle_free(current_node, current_node.parent.parent):
			if self.obstacle_free(current_node.point, current_node.parent.parent.point):

				# if current_node.parent.parent == None:
				# 	break

				# Update parent node
				current_node.parent = current_node.parent.parent
				self.nodes[current_node.id].parent = current_node.parent

				# Update current node cost
				parent_cost = current_node.parent.cost
				dist_cost = dist(current_node.parent.point, current_node.point)
				self.nodes[current_node.id].cost = parent_cost + dist_cost
			
			if current_node.parent.parent == None:
				break
			current_node = current_node.parent
	
		return self.compute_path()

	def collision(self, p):
		""" Check if the point p is located inside some obstacle."""
		return self.obstacles.check_collision(p[0], p[1])

	def step_n_from_p1_to_p2(self, p1, p2, n):
		""" ."""
		theta = math.atan2(p2[1]-p1[1], p2[0]-p1[0])
		return (p1[0] + n*self.obs_resolution*math.cos(theta),
				p1[1] + n*self.obs_resolution*math.sin(theta))
	
	def obstacle_free(self, p1, p2):
		""" Check if there is an obstacle between points p1 and p2."""
		distance = dist(p1, p2)
		n = 1
		if distance < self.obs_resolution:
			if self.collision(p2):
				return False
			else:
				return True
		else:
			for i in range(int(math.floor(distance/self.obs_resolution))):
				p_i = self.step_n_from_p1_to_p2(p1, p2, i + 1)
				if self.collision(p_i):
					return False

			return True

	def is_start_tree_the_last(self):
		""" ."""
		return self.is_start_tree
