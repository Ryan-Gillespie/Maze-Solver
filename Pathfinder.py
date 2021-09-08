import math
from app import colors
import pygame
from queue import deque, PriorityQueue

def h(p1, p2):
	""" heuristic function that returns absolute distance. prefers straight lines """
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def euclidean_dist(p1, p2):
	""" heuristic function that returns euclidean distance. prefers diagonals """
	x1, y1 = p1
	x2, y2 = p2
	return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def reconstruct_path(prev_map, current, start, draw):
	""" returns a reconstructed path from the last node to the start node in linear time with the prev_map """
	while current in prev_map:
		current = prev_map[current]
		if current is start:
			return True
		current.color = colors['path']
		draw()

def depth_first(draw, grid, start, goal):
	""" Runs Depth First search from start to goal """
	stack = [start]
	prev_map = {}

	while len(stack) > 0:
		# safety net to exit the loop if need be
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		
		# get current node
		current = stack.pop()
		if current is not start and current is not goal:
			current.color = colors['open']

		# we've reached goal state
		if current == goal:
			reconstruct_path(prev_map, current, start, draw)
			goal.color = colors['goal']
			return True
		
		for neighbor in current.neighbors:
			if neighbor.color != colors['open'] and neighbor.color != colors['closed']:
				prev_map[neighbor] = current
				stack.append(neighbor)
		
		draw()

		if current != start and current != goal:
			current.color = colors['closed']

	return False

def breadth_first(draw, grid, start, goal):
	""" Runs Breadth first search algorithm on the grid """
	queue = [start]
	queue_hash = {start}
	prev_map = {}
	i = 0

	def get_heuristic(node):
		return euclidean_dist(node.get_pos(), goal.get_pos())

	while len(queue) > 0:
		# safety net to exit the loop if need be
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		
		# get current node
		current = queue.pop(0)
		if current is not start and current is not goal:
			current.color = colors['open']

		# we've reached goal state
		if current == goal:
			reconstruct_path(prev_map, current, start, draw)
			goal.color = colors['goal']
			return True

		current.neighbors.sort(key=get_heuristic)
		for neighbor in current.neighbors:
			if neighbor not in queue_hash:
				prev_map[neighbor] = current
				queue.append(neighbor)
				queue_hash.add(neighbor)
				if neighbor is not start and current is not goal:
					neighbor.color = colors['open']
		draw()

		if current != start and current != goal:
			current.color = colors['closed']
	
	# return none if no path is found
	return False

def best_first(draw, grid, start, goal):
	""" 
	Runs Greedy best-first search on the grid

	Nearly identical to DFS except we sort the successor states by their distance to the goal.
	"""

	stack = [start]
	prev_map = {}

	def get_heuristic(node):
		return euclidean_dist(node.get_pos(), goal.get_pos())

	while len(stack) > 0:
		# safety net to exit the loop if need be
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		
		# get current node
		current = stack.pop()
		if current is not start and current is not goal:
			current.color = colors['open']

		# we've reached goal state
		if current == goal:
			reconstruct_path(prev_map, current, start, draw)
			return True

		current.neighbors.sort(reverse=True, key=get_heuristic)
		for neighbor in current.neighbors:
			if neighbor.color != colors['open'] and neighbor.color != colors['closed']:
				prev_map[neighbor] = current
				stack.append(neighbor)
		
		draw()

		if current != start and current != goal:
			current.color = colors['closed']

	# return none if no path is found
	return False

def a_star(draw, grid, start, goal):
	""" Runs A* on the grid """
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	# hashmap to keep track of the node's previous node
	previous_map = {}
	# g score set
	g_score = {node: float("inf") for row in grid for node in row}
	g_score[start] = 0
	# f score set
	f_score = {node: float("inf") for row in grid for node in row}
	f_score[start] = euclidean_dist(start.get_pos(), goal.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		# safety net to exit the loop if need be
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		
		current = open_set.get()[2] # get the node with the lowest f score
		open_set_hash.remove(current)

		# if we've reached the goal
		if current == goal:
			reconstruct_path(previous_map, current, start, draw)
			goal.color = colors['goal']
			return True
		
		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				previous_map[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + euclidean_dist(neighbor.get_pos(), goal.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.color = colors['open']
		
		draw()

		if current != start and current != goal:
			current.color = colors['closed']

	# return None if no path is found
	return None