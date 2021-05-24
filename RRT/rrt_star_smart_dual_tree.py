#!/usr/bin/env python

import pygame
import sys

from constants import GREEN, RED, BLACK, WHITE, GRAY
from tree import Tree
from datetime import datetime

from obstacles import Obstacles


class RRTStarSmartDualTree:
	""" Class for RRT*-Smart Dual Tree Path Planning. """
	def __init__(self, start_point, goal_point,
                 max_num_nodes, min_num_nodes,
                 goal_tolerance, epsilon_min, epsilon_max, screen,
                 obstacles, obs_resolution,
				 biasing_ratio, max_path_cost):
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
								goal_tolerance=goal_tolerance,
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
								goal_tolerance=goal_tolerance,
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

		self.max_path_cost = max_path_cost

		self.start_time = datetime.now()
		self.end_time = 0.0
		print ''

	def planning(self):
		""" ."""
		j = 1
		first_path_computed = False
		path = []
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
					self.tree = tree_obj
					print 'Tree size when goal found: ' + str(self.tree.get_tree_size())
					self.goal_found = True

					# Set n
					it = self.it
					self.n = it

					# Block Other Tree
					other_tree_obj.block_tree()

					n_nearest_ext = other_tree_obj.get_n_nearest_external()
					
					# Get nodes path from OTHER Tree
					external_nodes = other_tree_obj.get_external_nodes(n_nearest_ext)
					
					#  Add nodes path to Tree
					tree_obj.add_nodes_to_tree(external_nodes, new_node)

					path = self.tree.compute_path()

	def keep_searching(self):
		""" ."""
		tree_size = max(self.start_tree.get_tree_size(), self.goal_tree.get_tree_size() )

		self.end_time = datetime.now()
		duration = self.end_time - self.start_time

		if tree_size < self.max_num_nodes:
			if not self.goal_found:
				return True
			else:
				if tree_size > self.min_num_nodes and self.tree.get_path_cost() <= self.max_path_cost:
					self.print_final_info(tree_size, duration, self.tree.get_path_cost())
					return False
				else:
					return True
		else:
			self.print_final_info(tree_size, duration, self.tree.get_path_cost())
			return False

	def print_final_info(self, tree_size, duration, path_cost=None):
		if path_cost == None:
			print 'Path NOT found.'
		else:
			print 'Path cost: ' + str(self.tree.get_path_cost())

		print 'Algorithm duration: ' + str(duration.total_seconds())
		print 'Number of nodes: ' + str(tree_size)
		


def main():
	XDIM = 500
	YDIM = 500
	WINSIZE = [XDIM, YDIM]
	MAX_NUM_NODES = 5000
	MIN_NUM_NODES = 0
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
	goal_tolerance = 10

	bias_ratio = 100
	max_path_cost = 565
	
	rrt_star_smart_dual = RRTStarSmartDualTree(start_point, goal_point,
								MAX_NUM_NODES, MIN_NUM_NODES, goal_tolerance, 0, 30, 
								screen, obs, obs_resolution,
								bias_ratio, max_path_cost)

	path = rrt_star_smart_dual.planning()

	print "Final Path: "
	print path

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False


if __name__ == '__main__':
    main()