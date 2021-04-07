#!/usr/bin/env python
import random
from helper_functions import *
from node import Node
import pygame
from constants import GREEN, WHITE, RED, BLACK, BLUE, YELLOW, PURPLE, DARK_GREEN

class Tree:
	def __init__(self, start_point, vertex_color, edge_color, epsilon_min, epsilon_max, screen):
		""" ."""
		self.nodes = list()
		self.new_node = None

		self.screen = screen

		self.start_point = start_point

		self.k = 20.0
		self.radius = 1.0

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

	def get_nodes_length(self):
		""" ."""
		return len(self.nodes)

	def choose_parent(self, parent):
		""" ."""
		for node in self.nodes:
			if dist(node.point, self.new_node.point) < self.radius:
				node_cost = node.cost + dist(node.point, self.new_node.point)
				parent_cost = parent.cost + dist(parent.point, self.new_node.point)
				if node_cost < parent_cost:
					parent = node

		self.new_node.cost = parent.cost + dist(parent.point, self.new_node.point)
		self.new_node.parent = parent

	def rewire(self):
		""" ."""
		for node in self.nodes:
			# pygame.draw.circle(self.screen, GREEN, node.point, 4)
			self.draw_vertex(node.point)

			if node != self.new_node.parent and dist(node.point, self.new_node.point) < self.radius:
				if self.new_node.cost + dist(node.point, self.new_node.point) < node.cost:
					# Delete, paint white
					# pygame.draw.line(self.screen, WHITE, node.point, node.parent.point, 2) 
					# self.draw_edge(node.point, self.new_node.point, WHITE)
					self.erase_edge(node.point, self.new_node.point)

					# Now the node parent is the new node
					node.parent = self.new_node
					node.cost = self.new_node.cost + dist(node.point, self.new_node.point)
					# Draw
					# pygame.draw.line(self.screen, sel, node.point, self.new_node.point, 2)
					self.draw_edge(node.point, self.new_node.point)
				
			else:
				if node.parent != None:
					# pygame.draw.line(self.screen, BLUE, node.point, node.parent.point, 2)
					self.draw_edge(node.point, node.parent.point)

		self.constant_draw()
		pygame.display.update()

	def constant_draw(self):
		# START POINT --> YELLOW SQUARE
		pygame.draw.rect(self.screen, YELLOW, self.start_square, 0)
		pygame.draw.rect(self.screen, BLACK, self.start_square, 2)

		# GOAL POINT --> GRAY CIRCLE
		# pygame.draw.circle(self.screen, PURPLE, self.goal_point, self.goal_tolerance)

	def grow_tree(self):
		""" ."""
		found_next = False
		while found_next == False:
			x_rand = self.sample_free()
			x_nearest = self.get_nearest(x_rand)
			x_new = self.steer(x_nearest.point, x_rand)
			if self.obstacle_free(x_nearest, x_new):
				parent_node = x_nearest
				self.new_node = Node(x_new, parent_node)
				self.choose_parent(parent_node)
				self.nodes.append(Node(self.new_node.point, self.new_node.parent))
				self.rewire()            
				found_next = True

				# Draw the new edge
				self.draw_edge(self.new_node.point, parent_node.point)

				# Draw new vertex
				self.draw_vertex(self.new_node.point)

				pygame.display.update()
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
		return self.new_node

	def attempt_connect(self, external_node):
		""" ."""
		x_nearest = self.get_nearest(external_node.point)

		if dist(x_nearest.point, external_node.point) < self.goal_tolerance:
			# check collision
			if self.obstacle_free(x_nearest, external_node):
				self.x_nearest_ext = x_nearest
				return True
		return False

	def update_radius(self):
		nodes_size = self.nodes.shape[1] + 1
		self.radius = self.k*math.sqrt((math.log(nodes_size) / nodes_size))

	def draw_edge(self, point1, point2):
		pygame.draw.line(self.screen, self.e_color, point1, point2, 2)

	def erase_edge(self, point1, point2):
		pygame.draw.line(self.screen, WHITE, point1, point2, 2)

	def draw_vertex(self, point):
		pygame.draw.circle(self.screen, self.v_color, point, 4)

	def obstacle_free(self, n1, n2):
		return False

	def get_path(self):
        path = list()
        current_node = self.new_node
        while current_node.parent != None:
            path.append(current_node)
            current_node = current_node.parent

        # Add the first tree node
        path.append(current_node)
        
        return path

	def get_x_nearest_external(self):
		return self.x_nearest_ext

	def add_nodes_to_tree(self, nodes, parent_node):
		current_parent = parent_node
		for node in nodes:
			node.parent = current_parent
			node.cost = current_parent.cost + dist(node.point, parent_node.point)
			current_parent = node.parent

		