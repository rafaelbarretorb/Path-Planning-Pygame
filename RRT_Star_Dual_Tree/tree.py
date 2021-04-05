#!/usr/bin/env python


class Tree(object):
    def __init__(self):
		self.nodes = list()
		self.new_node = None

    def choose_parent(self, new_node, parent):
		""" ."""
		pass

    def rewire(self, new_node):
        """ ."""
		pass

    def sample_free(self):
		""" ."""
    	pass

    def steer(self, p1, p2):
		""" ."""
    	pass

    def get_nearest(self, x_rand):
		""" ."""
    	pass

    def obstacle_free(self, n1, n2):
		""" ."""
        pass

	def grow_tree(self):
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

	def get_new_node(self):
		""" ."""
        return self.new_node
	
	def attempt_connect(self, external_node):
		""" ."""
		x_nearest = self.get_nearest(external_node.point)

		if distance(x_nearest, external_node.point) < goal_tolerance:
			# TODO connect all path between x_nearest and start/goal node
			return True
		return False

