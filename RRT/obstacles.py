#!/usr/bin/env python

from helper_functions import dist
import pygame

class Circle:
	def __init__(self, x_c, y_c, radius, color, screen):
		self.x_c = x_c
		self.y_c = y_c
		self.radius = radius
		self.color = color
		self.screen = screen
	
	def check_collision(self, x, y):
		distance = dist((x, y), (self.x_c, self.y_c))
		if distance < self.radius:
			return True
		
		return False

	def draw(self):
		pygame.draw.circle(self.screen, self.color, (self.x_c, self.y_c), self.radius)


class Rectangle:
	def __init__(self, left, top, width, height, color, screen):
		self.left = left
		self.top = top
		self.width = width
		self.height = height
		self.color = color
		self.screen = screen

	def check_collision(self, x, y):
		if x > self.left and x < self.left + self.width and \
		   y > self.top and y < self.top + self.height:
			return True
		
		return False

	def draw(self):
		rect = pygame.Rect(self.left, self.top, self.width, self.height)
		pygame.draw.rect(self.screen, self.color, rect)


class Obstacles:
	def __init__(self, screen, color):
		self.obstacles = list()
		self.screen = screen
		self.color = color

	def make_circle(self, x_c, y_c, radius):
		circle = Circle(x_c, y_c, radius, self.color, self.screen)
		self.obstacles.append(circle)

	def make_rect(self, left, top, width, height):
		rect = Rectangle(left, top, width, height, self.color, self.screen)
		self.obstacles.append(rect)

	def check_collision(self, x, y):
		for obs in self.obstacles:
			if obs.check_collision(x, y):
				return True
		
		return False

	def draw(self):
		for obs in self.obstacles:
			obs.draw()