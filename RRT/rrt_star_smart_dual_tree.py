#!/usr/bin/env python

import pygame
import sys

from constants import GREEN, RED, BLACK, WHITE, GRAY
from tree import Tree

from obstacles import Obstacles


class RRTStarSmartDualTree:
	""" Class for RRT*-Smart Dual Tree Path Planning. """
	def __init__(self, start_point, goal_point,
                 max_num_nodes, min_num_nodes,
                 goal_tolerance, epsilon_min, epsilon_max, screen,
                 obstacles, obs_resolution,
				 biasing_ratio):
		self.screen = screen
		self.obstacles = obstacles
		self.obs_resolution = obs_resolution

		self.start_point = start_point
		self.goal_point = goal_point

		self.max_num_nodes = max_num_nodes
		self.min_num_nodes = min_num_nodes
		self.epsilon_min = epsilon_min
		self.epsilon_max = epsilon_max

		self.goal_tolerance = goal_tolerance

		self.start_tree = Tree(True,
								start_point,
								node_color=GREEN,
								connection_color=GREEN,
								goal_node_color=RED,
								path_color=BLACK,
								goal_tolerance=20,
								epsilon_min=epsilon_min,
								epsilon_max=epsilon_max,
								max_num_nodes=5000,
								screen=self.screen,
								obstacles=self.obstacles,
								obs_resolution=self.obs_resolution,
								biasing_radius=20.0)

		self.goal_tree = Tree(False,
								goal_point,
								node_color=RED,
								connection_color=RED,
								goal_node_color=GREEN,
								path_color=BLACK,
								goal_tolerance=20,
								epsilon_min=epsilon_min,
								epsilon_max=epsilon_max,
								max_num_nodes=5000,
								screen=self.screen,
								obstacles=self.obstacles,
								obs_resolution=self.obs_resolution,
								biasing_radius=20.0)

		self.tree = None

		self.goal_found = False

		self.n = None  # iteration where initial path found
		self.it = 0
		self.biasing_ratio = biasing_ratio

	def planning(self):
		""" ."""
		j = 1
		first_path_computed = False
		while self.keep_searching():
			if self.n != None and self.it == (self.n + j*self.biasing_ratio):
				self.tree.grow_tree(random_sample=False)
				j = j + 1
				
			else:
				# Start Tree's turn
				self.run_tree(self.start_tree, self.goal_tree)

				# Goal Tree's turn
				self.run_tree(self.goal_tree, self.start_tree)

				if self.goal_found:
					path = self.tree.path_optimization()

			# Iteration
			self.it = self.it + 1

		return path

	def run_tree(self, tree_obj, other_tree_obj):
		""" ."""
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

					# Set n
					it = self.it
					self.n = it

					# Block Other Tree
					other_tree_obj.block_tree()

					# # TODO review remove
					self.tree = tree_obj

					n_nearest_ext = other_tree_obj.get_n_nearest_external()
					
					# Get nodes path from OTHER Tree
					external_nodes = other_tree_obj.get_external_nodes(n_nearest_ext)
					
					#  Add nodes path to Tree
					tree_obj.add_nodes_to_tree(external_nodes, new_node)

					path = self.tree.compute_path()

	def keep_searching(self):
		""" ."""
		start_size = self.start_tree.get_nodes_length()
		goal_size = self.goal_tree.get_nodes_length()
		if start_size > self.max_num_nodes or goal_size > self.max_num_nodes:
			return False
		else:
			return True


def main():
	XDIM = 500
	YDIM = 500
	WINSIZE = [XDIM, YDIM]
	MAX_NUM_NODES = 800
	MIN_NUM_NODES = 400
	pygame.init()
	screen = pygame.display.set_mode(WINSIZE)
	pygame.display.set_caption('RRT*-Smart Dual Tree Path Planning')
	screen.fill(WHITE)
	running = True
	pygame.display.flip()

	# Obstacles
	obs = Obstacles(screen, GRAY)
	obs.make_circle(150, 150, 50)
	obs.make_rect(250, 100, 50, 300)
	obs.draw()

	obs_resolution = 5

	start_point = (50, 50)
	goal_point = (400, 400)
	goal_tolerance = 20

	bias_ratio = 50
	
	rrt_star_smart_dual = RRTStarSmartDualTree(start_point, goal_point,
								MAX_NUM_NODES, MIN_NUM_NODES, goal_tolerance, 0, 30, 
								screen, obs, obs_resolution,
								bias_ratio)

	path = rrt_star_smart_dual.planning()

	print "Final Path: "
	print path

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False


if __name__ == '__main__':
    main()