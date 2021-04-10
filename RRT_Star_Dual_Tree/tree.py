#!/usr/bin/env python
import random
from helper_functions import *
from node import Node
import pygame
from constants import GREEN, WHITE, RED, BLACK, BLUE, YELLOW, PURPLE, DARK_GREEN
import time

RADIUS = 50.0

class Tree:
	def __init__(self, name, start_point, vertex_color, edge_color, epsilon_min, epsilon_max, screen):
		""" ."""
		self.tree_name = name
		self.nodes = list()
		self.new_node = None

		self.screen = screen

		self.start_point = start_point

		self.k = 20.0
		self.radius = 100.0

		self.v_color = vertex_color
		self.e_color = edge_color

		self.nodes.append(Node(self.start_point, None))

		self.max_num_nodes = 5000
		self.min_num_nodes = 200

		self.epsilon_max = epsilon_max
		self.epsilon_min = epsilon_min

		# START SQUARE
		width = 20
		height = width
		left = self.start_point[0] - width/2
		top = self.start_point[1] - height/2
		self.start_square = pygame.Rect(left, top, width, height)

		self.goal_tolerance = 20

		self.x_nearest_ext = None

		self.goal = None

		self.tree_blocked = False
		self.path_old = list()

	def get_nodes_length(self):
		""" ."""
		return len(self.nodes)

	# def choose_parent(self, new_node, parent):
	# 	""" ."""
	# 	self.update_radius()

	# 	for node in self.nodes:
	# 		if dist(node.point, new_node.point) < RADIUS:
	# 			node_cost = node.cost + dist(node.point, new_node.point)
	# 			parent_cost = parent.cost + dist(parent.point, new_node.point)
	# 			if node_cost < parent_cost:
	# 				parent = node

	# 	new_node.cost = parent.cost + dist(parent.point, new_node.point)
	# 	new_node.parent = parent

	# 	return new_node

	def choose_parent(self, new_node, parent):
		""" ."""
		for node in self.nodes:
			if dist(node.point, new_node.point) < RADIUS and \
				node.cost + dist(node.point, new_node.point) < parent.cost + dist(parent.point, new_node.point):
				parent = node

		new_node.cost = parent.cost + dist(parent.point, new_node.point)
		new_node.parent = parent
		return new_node

	def rewire(self, new_node):
		""" ."""
		for node in self.nodes:
			self.draw_vertex(node.point)

			if node != new_node.parent and dist(node.point, new_node.point) < RADIUS and \
				new_node.cost + dist(node.point, new_node.point) < node.cost:
				# Delete, paint white
				pygame.draw.line(self.screen, WHITE, node.point, node.parent.point, 2) 
				# self.draw_edge(node.point, self.new_node.point, WHITE)
				# self.erase_edge(node.point, self.new_node.point)

				# Now the node parent is the new node
				node.parent = new_node
				node.cost = new_node.cost + dist(node.point, new_node.point)
				# Draw
				# pygame.draw.line(self.screen, sel, node.point, self.new_node.point, 2)
				self.draw_edge(node.point, new_node.point)
					
			else:
				if node.parent != None:
					# pygame.draw.line(self.screen, BLUE, node.point, node.parent.point, 2)
					self.draw_edge(node.point, node.parent.point)

		pygame.display.update()


	def grow_tree(self):
		""" ."""
		if self.tree_blocked:
			print "TREE BLOCKED"
			return
		else:
			found_next = False
			while found_next == False:
				x_rand = self.sample_free()
				x_nearest = self.get_nearest(x_rand)
				x_new = self.steer(x_nearest.point, x_rand)
				if self.obstacle_free(x_nearest, x_new):
					parent_node = x_nearest
					new_node = Node(x_new, parent_node)
					new_node = self.choose_parent(new_node, parent_node)
					self.nodes.append(new_node)
					self.rewire(new_node)            
					found_next = True
					self.new_node = self.nodes[-1]

					# print "new node: " + str(self.new_node.point)

					# Draw the new edge
					self.draw_edge(self.new_node.point, parent_node.point)

					# Draw new vertex
					self.draw_vertex(self.new_node.point)

					pygame.display.update()
					time.sleep(0.01)

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
		node = Node(self.new_node.point, self.new_node.parent) 
		return node

	def attempt_connect(self, external_node):
		""" ."""
		x_nearest = self.get_nearest(external_node.point)

		if dist(x_nearest.point, external_node.point) < self.goal_tolerance:
			# check collision
			if self.obstacle_free(x_nearest, external_node):
				self.x_nearest_ext = x_nearest
				# print self.tree_name
				return True
		return False

	def update_radius(self):
		# TODO node list has not shape
		nodes_size = len(self.nodes) + 1
		self.radius = self.k*math.sqrt((math.log(nodes_size) / nodes_size))

	def draw_edge(self, point1, point2, width=2):
		pygame.draw.line(self.screen, self.e_color, point1, point2, width)

	def erase_edge(self, point1, point2):
		pygame.draw.line(self.screen, WHITE, point1, point2, 2)

	def draw_path(self, point1, point2):
		pygame.draw.line(self.screen, BLACK, point1, point2, 4)

	def erase_path(self, point1, point2):
		pygame.draw.line(self.screen, WHITE, point1, point2, 4)

	def draw_vertex(self, point):
		pygame.draw.circle(self.screen, self.v_color, point, 4)

	def obstacle_free(self, n1, n2):
		return True

	def get_external_nodes(self, x_nearest_ext):
		""" ."""
		external_nodes = list()
		current_node = x_nearest_ext
		while current_node.parent != None:
			external_nodes.append(current_node)
			current_node = current_node.parent

		# Add the first tree node
		external_nodes.append(current_node)

		return external_nodes

	def get_x_nearest_external(self):
		return self.x_nearest_ext

	def add_nodes_to_tree(self, external_nodes, parent_node):
		current_parent = parent_node
		self.draw_edge(external_nodes[0].point, parent_node.point, 4)
		for node in external_nodes:
			node.parent = current_parent
			node.cost = current_parent.cost + dist(node.point, current_parent.point)
			# print node.cost
			current_parent = node

			# add to the nodes list
			self.nodes.append(node)

		self.goal = self.nodes[len(self.nodes)-1]
		pygame.display.update()

	# def get_goal_node(self):
	# 	""" First node of other tree."""
	# 	return self.goal
	
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
		
		# print "Nodes Amount: " + str(len(nodes))

		self.draw_final_path(path)
		return path

	def draw_final_path(self, path):
		""" ."""
		# Draw old path with WHITE
		for i in range(len(self.path_old) - 1):
			self.erase_path(self.path_old[i], self.path_old[i + 1])
		
		self.path_old = []

		pygame.display.update()
		# Draw current path with RED
		for i in range(len(path) - 1):
			self.draw_path(path[i], path[i + 1])
		
		pygame.display.update()
		

